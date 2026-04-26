from app.utils.logger import logger

class ExecutionEngine:
    """
    Converts strategy output into executable broker instructions.
    This engine does NOT place trades — it prepares the order object.
    """

    @staticmethod
    def build_order(strategy_result: dict):
        """
        Takes normalized strategy output and builds a broker-ready order.
        """

        if not strategy_result.get("success"):
            logger.error(f"Strategy engine failed: {strategy_result}")
            return {
                "success": False,
                "error": "Strategy engine failed",
                "details": strategy_result
            }

        symbol = strategy_result.get("symbol")
        price = strategy_result.get("price")
        action = strategy_result.get("action")
        confidence = strategy_result.get("confidence")
        reason = strategy_result.get("reason")

        if not symbol:
            return {
                "success": False,
                "error": "Missing symbol in strategy result"
            }

        # Convert action → broker side
        side = "buy" if action == "buy" else "sell" if action == "sell" else "hold"

        logger.info(f"Execution engine building order: {symbol} {side} @ {price}")

        # HOLD → no order
        if side == "hold":
            return {
                "success": True,
                "order_required": False,
                "symbol": symbol,
                "side": "hold",
                "reason": reason,
                "confidence": confidence
            }

        # BUY or SELL → build order object
        order = {
            "symbol": symbol,
            "side": side,
            "type": "market",
            "qty": 1,  # Position sizing engine will override this later
            "time_in_force": "gtc",
            "confidence": confidence,
            "reason": reason
        }

        return {
            "success": True,
            "order_required": True,
            "order": order
        }


# Singleton instance
execution_engine = ExecutionEngine()
