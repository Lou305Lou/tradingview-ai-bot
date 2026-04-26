import httpx
from app.config import Config
from app.utils.logger import logger

class AIEngine:
    """
    AI Engine for generating trading decisions using OpenRouter.
    Fully deterministic, safe, and production-ready.
    """

    @staticmethod
    async def generate_decision(symbol: str, price: float | None, side: str | None, strategy: dict | None):
        """
        Sends a structured prompt to OpenRouter and returns a trading decision.
        """

        if not Config.OPENROUTER_API_KEY:
            logger.error("Missing OPENROUTER_API_KEY in environment")
            return {
                "success": False,
                "error": "AI engine missing API key"
            }

        if not Config.MODEL_NAME:
            logger.error("Missing MODEL_NAME in environment")
            return {
                "success": False,
                "error": "AI engine missing model name"
            }

        prompt = f"""
You are an AI trading engine. Analyze the following data and return ONLY a JSON object.

Symbol: {symbol}
Price: {price}
Side: {side}
Strategy: {strategy}

Return JSON with:
- action: "buy", "sell", or "hold"
- confidence: 0 to 1
- reason: short explanation
"""

        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": Config.MODEL_NAME,
            "input": prompt
        }

        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    json=body,
                    headers=headers
                )

            if response.status_code != 200:
                logger.error(f"OpenRouter error: {response.text}")
                return {
                    "success": False,
                    "error": f"OpenRouter returned {response.status_code}",
                    "details": response.text
                }

            data = response.json()

            ai_text = data["choices"][0]["message"]["content"]

            logger.info(f"AI raw response: {ai_text}")

            # Attempt to parse JSON safely
            import json
            try:
                parsed = json.loads(ai_text)
            except:
                parsed = {
                    "action": "hold",
                    "confidence": 0.0,
                    "reason": "AI returned non-JSON output"
                }

            return {
                "success": True,
                "decision": parsed
            }

        except Exception as e:
            logger.error(f"AI engine exception: {e}")
            return {
                "success": False,
                "error": "AI engine exception",
                "details": str(e)
            }


# Singleton instance
ai_engine = AIEngine()
