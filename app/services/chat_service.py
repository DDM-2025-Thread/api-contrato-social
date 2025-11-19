from fastapi import BackgroundTasks, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.services.gemini_service import GeminiService
from app.models.enum import TicketStatus
import uuid
import os
from typing import List

from app.repositories.chat_repository import ChatRepository
from app.repositories.user_repository import UserRepository
from app.repositories.api_cost_repository import ApiCostRepository
from app.repositories.usage_log_repository import UsageLogRepository

API_KEY = os.getenv("GEMINI_API_KEY") or ""


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.chat_repository = ChatRepository(db)
        self.user_repository = UserRepository(db)
        self.cost_repository = ApiCostRepository(db)
        self.usage_log_repository = UsageLogRepository(db)
        if not API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY environment variable is not set")

        self.gemini_service = GeminiService(api_key=API_KEY)

    def create_ticket(self) -> str:
        return str(uuid.uuid4())

    async def start_upload_process(self, pdf_file: UploadFile, user_email: str, background_tasks: BackgroundTasks) -> str:
        user = self.user_repository.find_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Usuário do token não encontrado.")
        user_id = user.id

        pdf_file_bytes = await pdf_file.read()
        ticket = self.create_ticket()
        self.chat_repository.save_initial_ticket(
            ticket, TicketStatus.PROCESSING, user_id)
        background_tasks.add_task(
            self.process_gemini_response,
            ticket=ticket,
            pdf_file_bytes=pdf_file_bytes,
            user_id=user_id
        )
        return ticket

    async def process_gemini_response(self, ticket: str, pdf_file_bytes: bytes, user_id: int):
        uploaded_file = None
        try:
            uploaded_file = self.gemini_service.upload_pdf_for_processing(
                pdf_file_bytes)
            gemini_response_dict = self.gemini_service.get_contract_data(
                uploaded_file)
            self.chat_repository.save_final_response(
                ticket, gemini_response_dict)
            self.chat_repository.update_status(ticket, TicketStatus.COMPLETED)

            try:
                cost_setting = self.cost_repository.get()
                current_cost = cost_setting.cost_per_request if cost_setting else 0.01

                self.usage_log_repository.create({
                    "user_id": user_id,
                    "endpoint": "/chat/upload",
                    "cost": current_cost
                })
            except Exception as billing_e:
                print(
                    f"ERRO DE BILLING (não fatal) para ticket {ticket} (user {user_id}): {billing_e}")

        except Exception as e:
            print(f"Erro no processamento Gemini para o ticket {ticket}: {e}")
            self.chat_repository.update_status(
                ticket, TicketStatus.FAILED, error_message=str(e))
        finally:
            if uploaded_file:
                file_name = getattr(uploaded_file, "name", None)
                if file_name:
                    self.gemini_service.client.files.delete(
                        name=file_name)

    def get_chat_response_by_ticket(self, ticket: str):
        return self.chat_repository.get_response_by_ticket(ticket)

    def find_by_user(self, user_email: str) -> List[dict]:
        user = self.user_repository.find_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Usuário do token não encontrado.")
        chat_responses = self.chat_repository.find_chat_responses_by_user_id(
            user.id)
        return [{"id": chat_res.id, "ticket_uuid": chat_res.ticket_uuid, "status": chat_res.status, "created_at": chat_res.created_at, "user_id": chat_res.user_id} for chat_res in chat_responses]
