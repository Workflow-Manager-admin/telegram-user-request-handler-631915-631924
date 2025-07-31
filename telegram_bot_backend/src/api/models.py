from pydantic import BaseModel
from typing import Optional

class TelegramMessage(BaseModel):
    message_id: int
    text: Optional[str] = None
    chat: dict
    from_user: Optional[dict] = None
    date: int

class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[TelegramMessage] = None
