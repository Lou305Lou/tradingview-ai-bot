# TradingView AI Bot

A production‑ready FastAPI backend that receives TradingView alerts, sends them to an AI model for decision‑making, sizes positions, and executes trades via Alpaca.

----------------------------------------

## Project Structure

tradingview-ai-bot/
    app/
        main.py
        router.py
        config.py
        utils/
            logger.py
        services/
            ai_engine.py
            alpaca_client.py
            tradingview_handler.py
            position_sizer.py
    requirements.txt
    Dockerfile
    docker-compose.yml
    .env.example

----------------------------------------

## Setup

### 1. Create .env

cp .env.example .env

Fill in:
- ALPACA_API_KEY
- ALPACA_SECRET_KEY
- OPENROUTER_API_KEY
- TRADINGVIEW_WEBHOOK_SECRET

----------------------------------------

## Run Locally

pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000

----------------------------------------

## Run with Docker

docker build -t tradingview-ai-bot .

docker run -p 8000:8000 --env-file .env tradingview-ai-bot

----------------------------------------

## Run with Docker Compose

docker-compose up --build

----------------------------------------

## Endpoints

Health Check:
GET /health

TradingView Webhook:
POST /webhook

Payload example:
{
  "ticker": "AAPL",
  "price": 190.25,
  "side": "buy",
  "secret": "YOUR_SECRET"
}

----------------------------------------

## Flow

1. TradingView sends alert  
2. Webhook validates secret  
3. AI analyzes alert  
4. Position size calculated  
5. Alpaca executes trade  
6. JSON response returned  

----------------------------------------

## Deployment

Deploy using Docker on any container platform (Railway, Render, Fly.io, AWS, etc).

----------------------------------------

## Notes

- Requires valid API keys  
- AI output is JSON‑validated and hardened  
- Safe for production use  
