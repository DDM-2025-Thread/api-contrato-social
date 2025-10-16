from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any
from app.models.model import ChatTicket


class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_initial_ticket(self, ticket: str, status: str) -> ChatTicket:
        chat_ticket = ChatTicket(
            ticket_uuid=ticket,
            status=status,
        )
        self.db.add(chat_ticket)
        await self.db.commit()
        await self.db.refresh(chat_ticket)
        return chat_ticket

    async def update_status(self, ticket: str, status: str, error_message: Optional[str] = None) -> None:
        stmt = update(ChatTicket).where(ChatTicket.ticket_uuid == ticket).values(
            status=status,
            error_message=error_message
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def save_final_response(self, ticket: str, response_data: Dict[str, Any]) -> None:
        stmt = update(ChatTicket).where(ChatTicket.ticket_uuid == ticket).values(
            response_json=response_data,
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_response_by_ticket(self, ticket: str) -> Optional[Dict[str, Any]]:
        stmt = select(ChatTicket).where(ChatTicket.ticket_uuid == ticket)
        result = await self.db.execute(stmt)
        chat_ticket = result.scalar_one_or_none()
        if chat_ticket is None:
            return None
        return {
            "ticket": chat_ticket.ticket_uuid,
            "status": chat_ticket.status,
            "response": chat_ticket.response_json,
            "error_message": chat_ticket.error_message
        }
