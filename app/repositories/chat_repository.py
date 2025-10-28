from sqlalchemy import select, update
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.models.model import ChatTicket
from app.models.enum import TicketStatus


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_initial_ticket(self, ticket: str, status: str) -> ChatTicket:
        chat_ticket = ChatTicket(
            ticket_uuid=ticket,
            status=status,
        )
        self.db.add(chat_ticket)
        self.db.commit()
        self.db.refresh(chat_ticket)
        return chat_ticket

    def update_status(self, ticket: str, status: TicketStatus, error_message: Optional[str] = None) -> None:
        stmt = update(ChatTicket).where(ChatTicket.ticket_uuid == ticket).values(
            status=status.value,
            error_message=error_message
        )
        self.db.execute(stmt)
        self.db.commit()

    def save_final_response(self, ticket: str, response_data: Dict[str, Any]) -> None:
        stmt = update(ChatTicket).where(ChatTicket.ticket_uuid == ticket).values(
            response_json=response_data,
        )
        self.db.execute(stmt)
        self.db.commit()

    def get_response_by_ticket(self, ticket: str) -> Optional[Dict[str, Any]]:
        stmt = select(ChatTicket).where(ChatTicket.ticket_uuid == ticket)
        result = self.db.execute(stmt)
        chat_ticket = result.scalar_one_or_none()
        if chat_ticket is None:
            return None
        return {
            "ticket": chat_ticket.ticket_uuid,
            "status": chat_ticket.status,
            "response": chat_ticket.response_json,
            "error_message": chat_ticket.error_message
        }
