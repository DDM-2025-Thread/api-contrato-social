from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.enum import TicketStatus


class ChatResponseSchema(BaseModel):
    id: int
    name: str
    ticket_uuid: str
    status: TicketStatus
    created_at: datetime
    user_id: int
    response_json: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True
