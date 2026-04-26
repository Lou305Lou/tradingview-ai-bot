from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import Config
from app.services.tradingview_handler import process_tradingview_alert

router = APIRouter()

class TradingViewPayload(BaseModel):
    secret: str
    symbol: str | None = None
    price: float | None = None
    side: str | None = None
    strategy: dict | None = None


@router.post("/webhook")
async def webhook(payload: TradingViewPayload):
    """
    TradingView webhook endpoint.
    Validates secret and forwards payload to the orchestrator.
    """

    # Validate secret
    if payload.secret != Config.TRADINGVIEW_WEBHOOK_SECRET:
        raise HTTPException(status_code=400, detail="Invalid secret")

    # Process alert
    result = await process_tradingview_alert(payload.dict())

    return {
        "success": True,
        "message": "Webhook processed",
        "result": result
    }
