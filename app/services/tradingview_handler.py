from app.services.ai_engine import ai_engine
from app.services.strategy_engine import strategy_engine
from app.services.execution_engine import execution_engine
from app.services.position_sizer import position_sizer
from app.services.risk_engine import risk_engine
from app.services.alpaca_client import alpaca_client
from app.services.learning_engine import learning_engine
from app.utils.logger import logger


async def process_tradingview_alert(payload: dict) -> dict:
    """
    Main orchestrator for the entire TradingView → AI → Trade pipeline.
    This function NEVER crashes and ALWAYS returns a deterministic structure.
    """

    symbol = payload.get("symbol")
    price = payload.get("price")
    side = payload.get("side")
    strategy = payload.get("strategy", {})

    logger.info(f"TradingView alert received: {payload}")

    # 1. AI DECISION
    ai_result = await ai_engine.generate_decision(
        symbol=symbol,
        price=price,
        side=side,
        strategy=strategy
    )

    learning_engine.record_event("ai_decision", ai_result)

    if not ai_result.get("success"):
        return {
            "success": False,
            "stage": "ai_engine",
            "details": ai_result
        }

    # 2. STRATEGY ENGINE
    strategy_result = strategy_engine.process_ai_decision(
        ai_result=ai_result,
        symbol=symbol,
        price=price
    )

    learning_engine.record_event("strategy_output", strategy_result)

    if not strategy_result.get("success"):
        return {
            "success": False,
            "stage": "strategy_engine",
            "details": strategy_result
        }

    # 3. EXECUTION ENGINE (build order)
    execution_result = execution_engine.build_order(strategy_result)

    learning_engine.record_event("execution_order", execution_result)

    if not execution_result.get("success"):
        return {
            "success": False,
            "stage": "execution_engine",
            "details": execution_result
        }

    # HOLD → no trade
    if not execution_result.get("order_required"):
        return {
            "success": True,
            "action": "hold",
            "reason": execution_result.get("reason", "No order required"),
            "confidence": execution_result.get("confidence", 0.0)
        }

    # 4. POSITION SIZER
    sized_order = position_sizer.apply_sizing(execution_result)

    learning_engine.record_event("position_sizing", sized_order)

    if not sized_order.get("success"):
        return {
            "success": False,
            "stage": "position_sizer",
            "details": sized_order
        }

    # 5. RISK ENGINE
    risk_checked = risk_engine.validate_order(sized_order)

    learning_engine.record_event("risk_check", risk_checked)

    if not risk_checked.get("success"):
        return {
            "success": False,
            "stage": "risk_engine",
            "details": risk_checked
        }

    # HOLD after risk check
    if not risk_checked.get("order_required"):
        return {
            "success": True,
            "action": "hold",
            "reason": risk_checked.get("reason", "Risk engine forced HOLD"),
            "confidence": risk_checked.get("confidence", 0.0)
        }

    # 6. ALPACA CLIENT (submit order)
    final_order = risk_checked.get("order")
    alpaca_result = await alpaca_client.submit_order(final_order)

    learning_engine.record_event("alpaca_response", alpaca_result)

    if not alpaca_result.get("success"):
        return {
            "success": False,
            "stage": "alpaca_client",
            "details": alpaca_result
        }

    # SUCCESS
    return {
        "success": True,
        "message": "Trade executed successfully",
        "symbol": symbol,
        "order": alpaca_result.get("order")
    }
