import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import TelegramUpdate
from .services.telegram_service import TelegramBotService

app = FastAPI(
    title="Telegram Bot Backend",
    description="Backend service for processing Telegram bot commands and interactions",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_telegram_service():
    return TelegramBotService()

@app.get("/")
def health_check():
    """
    PUBLIC_INTERFACE
    Health check endpoint to verify service status
    """
    return {"message": "Healthy"}

@app.post("/webhook")
async def telegram_webhook(
    update: TelegramUpdate,
    telegram_service: TelegramBotService = Depends(get_telegram_service)
):
    """
    PUBLIC_INTERFACE
    Webhook endpoint for receiving updates from Telegram
    
    This endpoint receives updates from Telegram when new messages or interactions
    occur with the bot. It processes these updates and generates appropriate responses.
    
    Args:
        update: The update object received from Telegram
        telegram_service: Injectable TelegramBotService instance
    
    Returns:
        dict: A confirmation of the update being processed
    """
    try:
        await telegram_service.process_update(update.dict())
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup():
    """Verify environment variables on startup"""
    if not os.getenv("TELEGRAM_BOT_TOKEN"):
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable must be set")
