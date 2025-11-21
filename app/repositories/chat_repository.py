from sqlalchemy import select, update
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from app.models.model import ChatResponse
from app.models.enum import TicketStatus


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_initial_ticket(self, ticket: str, status: TicketStatus, user_id: int) -> ChatResponse:
        chat_response = ChatResponse(
            ticket_uuid=ticket,
            status=status.value if isinstance(
                status, TicketStatus) else status,
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

    def get_response_by_ticket(self, ticket: str) -> Optional[ChatResponse]:
        stmt = select(ChatResponse).where(ChatResponse.ticket_uuid == ticket)
        result = self.db.execute(stmt)
        chat_response = result.scalar_one_or_none()
        return chat_response

    def find_chats_by_user_id(self, user_id: int) -> List[ChatResponse]:
        stmt = select(
            ChatResponse.id,
            ChatResponse.ticket_uuid,
            ChatResponse.status,
            ChatResponse.created_at,
            ChatResponse.user_id
        ).where(ChatResponse.user_id == user_id)

        result = self.db.execute(stmt)

        return [
            {
                "id": row.id,
                "ticket_uuid": row.ticket_uuid,
                "status": row.status.value if isinstance(row.status, TicketStatus) else row.status,
                "created_at": row.created_at,
                "user_id": row.user_id,
                "response_json": None,
                "error_message": None,
            }
            for row in result.all()
        ]
