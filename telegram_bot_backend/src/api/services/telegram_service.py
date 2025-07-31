import os
from typing import Optional
from fastapi import HTTPException
import httpx

class TelegramBotService:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    async def send_message(self, chat_id: int, text: str) -> dict:
        """
        PUBLIC_INTERFACE
        Send a message to a specific chat.
        
        Args:
            chat_id: The ID of the chat to send the message to
            text: The text of the message to send
            
        Returns:
            dict: The response from Telegram's API
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/sendMessage",
                json={"chat_id": chat_id, "text": text}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Failed to send message")
            return response.json()

    async def process_update(self, update: dict) -> Optional[dict]:
        """
        PUBLIC_INTERFACE
        Process an update received from Telegram.
        
        Args:
            update: The update object received from Telegram
            
        Returns:
            Optional[dict]: The response to send back to the user, if any
        """
        if "message" not in update:
            return None
            
        message = update["message"]
        if "text" not in message:
            return None
            
        # Echo the message back for now - this will be enhanced later
        return await self.send_message(
            chat_id=message["chat"]["id"],
            text=f"Received: {message['text']}"
        )
