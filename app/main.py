from fastapi import FastAPI
from app.router import router
from app.config import Config
from app.utils.logger import logger

app = FastAPI(
    title="TradingView AI Bot",
    description="AI-driven trading pipeline with risk management and Alpaca execution.",
    version="1.0.0"
)

# Register routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 TradingView AI Bot starting up...")
    logger.info(f"Loaded TradingView Secret: {Config.TRADINGVIEW_WEBHOOK_SECRET}")
    logger.info(f"Loaded OpenRouter Model: {Config.MODEL_NAME}")
    logger.info("Startup complete.")

@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "TradingView AI Bot is online."
    }
