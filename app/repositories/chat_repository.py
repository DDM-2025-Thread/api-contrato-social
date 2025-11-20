from sqlalchemy import select, update
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from app.models.model import ChatResponse
from app.models.enum import TicketStatus


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_initial_ticket(self, ticket: str, status: str, user_id: int) -> ChatResponse:
        chat_response = ChatResponse(
            ticket_uuid=ticket,
            status=status,
            user_id=user_id
        )
        self.db.add(chat_response)
        self.db.commit()
        self.db.refresh(chat_response)
        return chat_response

    def update_status(self, ticket: str, status: TicketStatus, error_message: Optional[str] = None) -> None:
        stmt = update(ChatResponse).where(ChatResponse.ticket_uuid == ticket).values(
            status=status.value,
            error_message=error_message
        )
        self.db.execute(stmt)
        self.db.commit()

    def save_final_response(self, ticket: str, response_data: Dict[str, Any]) -> None:
        stmt = update(ChatResponse).where(ChatResponse.ticket_uuid == ticket).values(
            response_json=response_data,
        )
        self.db.execute(stmt)
        self.db.commit()

    def get_response_by_ticket(self, ticket: str) -> Optional[Dict[str, Any]]:
        stmt = select(ChatResponse).where(ChatResponse.ticket_uuid == ticket)
        result = self.db.execute(stmt)
        chat_response = result.scalar_one_or_none()
        return chat_response

    def find_chats_by_user_id(self, user_id: int) -> List[ChatResponse]:
        return self.db.query(ChatResponse).filter(ChatResponse.user_id == user_id).all()
