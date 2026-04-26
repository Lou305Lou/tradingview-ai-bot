from app.utils.logger import logger

class StrategyEngine:
    """
    Converts AI decisions into executable trading instructions.
    Ensures safety, normalization, and deterministic behavior.
    """

    VALID_ACTIONS = ["buy", "sell", "hold"]

    @staticmethod
    def normalize_action(action: str) -> str:
        """
        Normalize AI action into one of: buy, sell, hold.
        """
        if not action:
            return "hold"

        action = action.lower().strip()

        if action not in StrategyEngine.VALID_ACTIONS:
            return "hold"

        return action

    @staticmethod
    def process_ai_decision(ai_result: dict, symbol: str, price: float | None):
        """
        Takes AI output and converts it into a safe, executable instruction.
        """

        if not ai_result.get("success"):
            logger.error(f"AI decision failed: {ai_result}")
            return {
                "success": False,
                "error": "AI decision failed",
                "details": ai_result
            }

        decision = ai_result.get("decision", {})

        action = StrategyEngine.normalize_action(decision.get("action"))
        confidence = decision.get("confidence", 0.0)
        reason = decision.get("reason", "No reason provided")

        logger.info(f"Strategy normalized action: {action}, confidence: {confidence}")

        return {
            "success": True,
            "symbol": symbol,
            "price": price,
            "action": action,
            "confidence": confidence,
            "reason": reason
        }


# Singleton instance
strategy_engine = StrategyEngine()
