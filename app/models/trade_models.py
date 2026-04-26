from pydantic import BaseModel

class TradeSignal(BaseModel):
    symbol: str
    action: str
    confidence: float
    timestamp: str
