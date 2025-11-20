from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.enum import TicketStatus

class ChatResponseSchema(BaseModel):
    id: int
    ticket_uuid: str
    status: TicketStatus
    response_json: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True