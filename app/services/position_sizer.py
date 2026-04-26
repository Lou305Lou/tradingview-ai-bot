from app.utils.logger import logger

class PositionSizer:
    """
    Determines the number of shares to trade based on confidence and risk rules.
    This module is deterministic, safe, and never returns invalid quantities.
    """

    MIN_QTY = 1
    MAX_QTY = 10  # Hard cap for safety

    @staticmethod
    def calculate_size(confidence: float) -> int:
        """
        Converts AI confidence (0–1) into a position size.
        """

        if confidence is None:
            return PositionSizer.MIN_QTY

        # Clamp confidence
        confidence = max(0.0, min(1.0, confidence))

        # Scale quantity
        qty = int(PositionSizer.MIN_QTY + (confidence * (PositionSizer.MAX_QTY - 1)))

        # Safety clamp
        qty = max(PositionSizer.MIN_QTY, min(PositionSizer.MAX_QTY, qty))

        return qty

    @staticmethod
    def apply_sizing(order: dict):
        """
        Takes a broker-ready order and applies position sizing.
        """

        if not order.get("success"):
            return order

        if not order.get("order_required"):
            return order

        order_obj = order.get("order")
        confidence = order_obj.get("confidence", 0.0)

        qty = PositionSizer.calculate_size(confidence)

        logger.info(f"PositionSizer: confidence={confidence}, qty={qty}")

        order_obj["qty"] = qty

        return {
            "success": True,
            "order_required": True,
            "order": order_obj
        }


# Singleton instance
position_sizer = PositionSizer()
