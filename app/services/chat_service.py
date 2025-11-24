from fastapi import BackgroundTasks, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.services.gemini_service import GeminiService
from app.models.enum import TicketStatus
from app.models.model import ChatResponse
import uuid
import os
from typing import List
from app.database import get_db

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

        file_name_full = pdf_file.filename or "sem_nome"
        MAX_NAME_LENGTH = 120
        pdf_name = file_name_full[:MAX_NAME_LENGTH]

        pdf_file_bytes = await pdf_file.read()
        ticket = self.create_ticket()
        self.chat_repository.save_initial_ticket(
            ticket=ticket, name=pdf_name, status=TicketStatus.PROCESSING, user_id=user_id)
        background_tasks.add_task(
            self.process_gemini_response,
            ticket=ticket,
            pdf_file_bytes=pdf_file_bytes,
            user_id=user_id
        )
        return ticket

    def process_gemini_response(self, ticket: str, pdf_file_bytes: bytes, user_id: int):
        uploaded_file = None
        db_session = next(get_db())

        chat_repository = ChatRepository(db_session)
        cost_repository = ApiCostRepository(db_session)
        usage_log_repository = UsageLogRepository(db_session)

        try:
            uploaded_file = self.gemini_service.upload_pdf_for_processing(
                pdf_file_bytes)
            gemini_response_dict = self.gemini_service.get_contract_data(
                uploaded_file)
            chat_repository.save_final_response(
                ticket=ticket, user_id=user_id, response_data=gemini_response_dict)
            chat_repository.update_status(
                ticket=ticket, user_id=user_id, status=TicketStatus.COMPLETED)

            try:
                cost_setting = cost_repository.get()
                current_cost = cost_setting.cost_per_request if cost_setting else 0.01

                usage_log_repository.create({
                    "user_id": user_id,
                    "endpoint": "/chat/upload",
                    "cost": current_cost
                })
            except Exception as billing_e:
                print(
                    f"ERRO DE BILLING (não fatal) para ticket {ticket} (user {user_id}): {billing_e}")

        except Exception as e:
            print(f"Erro no processamento Gemini para o ticket {ticket}: {e}")
            chat_repository.update_status(
                ticket=ticket, user_id=user_id, status=TicketStatus.FAILED, error_message=str(e))
        finally:
            db_session.close()
            if uploaded_file:
                file_name = getattr(uploaded_file, "name", None)
                if file_name:
                    self.gemini_service.client.files.delete(
                        name=file_name)

    def get_chat_response_by_ticket(self, ticket: str, user_email: str):
        user = self.user_repository.find_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Usuário do token não encontrado.")
        chat_response = self.chat_repository.get_response_by_ticket(
            ticket=ticket, user_id=user.id)
        if not chat_response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Ticket não encontrado.")
        return chat_response

    def find_chats_by_user_email(self, user_email: str) -> List[ChatResponse]:
        user = self.user_repository.find_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Usuário do token não encontrado.")
        return self.chat_repository.find_chats_by_user_id(
            user.id)
