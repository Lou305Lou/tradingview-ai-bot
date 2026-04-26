import httpx
from app.config import Config
from app.utils.logger import logger

class AlpacaClient:
    """
    Handles all communication with the Alpaca trading API.
    Fully safe, async, and production-ready.
    """

    BASE_URL = "https://paper-api.alpaca.markets/v2"

    @staticmethod
    async def submit_order(order: dict):
        """
        Submits a market order to Alpaca.
        """

        if not Config.ALPACA_API_KEY or not Config.ALPACA_SECRET_KEY:
            logger.error("Missing Alpaca API credentials")
            return {
                "success": False,
                "error": "Missing Alpaca API credentials"
            }

        headers = {
            "APCA-API-KEY-ID": Config.ALPACA_API_KEY,
            "APCA-API-SECRET-KEY": Config.ALPACA_SECRET_KEY,
            "Content-Type": "application/json"
        }

        url = f"{AlpacaClient.BASE_URL}/orders"

        logger.info(f"Submitting Alpaca order: {order}")

        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.post(url, json=order, headers=headers)

            if response.status_code not in [200, 201]:
                logger.error(f"Alpaca error: {response.text}")
                return {
                    "success": False,
                    "error": f"Alpaca returned {response.status_code}",
                    "details": response.text
                }

            data = response.json()
            logger.info(f"Alpaca order accepted: {data}")

            return {
                "success": True,
                "order": data
            }

        except Exception as e:
            logger.error(f"Alpaca exception: {e}")
            return {
                "success": False,
                "error": "Alpaca exception",
                "details": str(e)
            }


# Singleton instance
alpaca_client = AlpacaClient()
