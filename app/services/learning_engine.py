import json
import os
from datetime import datetime
from app.utils.logger import logger

class LearningEngine:
    """
    Logs every AI decision, strategy output, and executed order
    into a structured JSONL file for future analysis.
    """

    LOG_FILE = "learning_log.jsonl"

    @staticmethod
    def _write_log(entry: dict):
        """
        Writes a single JSON entry to the learning log.
        Always safe. Never crashes.
        """
        try:
            with open(LearningEngine.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error(f"LearningEngine write error: {e}")

    @staticmethod
    def record_event(event_type: str, data: dict):
        """
        Records any event in the pipeline:
        - ai_decision
        - strategy_output
        - execution_order
        - alpaca_response
        """

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "data": data
        }

        logger.info(f"LearningEngine logged event: {event_type}")

        LearningEngine._write_log(entry)

        return {
            "success": True,
            "logged": event_type
        }


# Singleton instance
learning_engine = LearningEngine()
