from app.utils.logger import logger

class RiskEngine:
    """
    Enforces safety rules before an order is allowed to execute.
    This engine NEVER crashes and ALWAYS returns a deterministic result.
    """

    MAX_POSITION_SIZE = 10          # Hard cap
    MIN_CONFIDENCE = 0.15           # Below this → HOLD
    BLOCKED_SYMBOLS = ["OTC", "PINK"]  # Example restricted markets

    @staticmethod
    def validate_order(order_result: dict):
        """
        Takes a sized order and applies risk checks.
        """

        if not order_result.get("success"):
            return order_result

        if not order_result.get("order_required"):
            return order_result

        order = order_result.get("order")
        symbol = order.get("symbol")
        qty = order.get("qty")
        confidence = order.get("confidence", 0.0)

        # 1. Block restricted symbols
        if any(blocked in symbol.upper() for blocked in RiskEngine.BLOCKED_SYMBOLS):
            logger.warning(f"RiskEngine: Blocked symbol {symbol}")
            return {
                "success": False,
                "error": "Symbol is restricted by risk rules",
                "symbol": symbol
            }

        # 2. Confidence threshold
        if confidence < RiskEngine.MIN_CONFIDENCE:
            logger.info(f"RiskEngine: Low confidence {confidence}, forcing HOLD")
            return {
                "success": True,
                "order_required": False,
                "symbol": symbol,
                "side": "hold",
                "reason": "Confidence too low",
                "confidence": confidence
            }

        # 3. Max position size
        if qty > RiskEngine.MAX_POSITION_SIZE:
            logger.warning(f"RiskEngine: qty {qty} exceeds max {RiskEngine.MAX_POSITION_SIZE}")
            order["qty"] = RiskEngine.MAX_POSITION_SIZE

        logger.info(f"RiskEngine: Order approved {order}")

        return {
            "success": True,
            "order_required": True,
            "order": order
        }


# Singleton instance
risk_engine = RiskEngine()
