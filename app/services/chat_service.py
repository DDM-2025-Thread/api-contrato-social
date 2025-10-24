from fastapi import BackgroundTasks, UploadFile
from sqlalchemy.orm import Session
from app.repositories.chat_repository import ChatRepository
from app.services.gemini_service import GeminiService
from app.models.enum import TicketStatus
import uuid
import os

API_KEY = os.getenv("GEMINI_API_KEY")


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.chat_repo = ChatRepository(db)
        self.gemini_service = GeminiService(api_key=API_KEY)

    def create_ticket(self) -> str:
        return str(uuid.uuid4())

    async def start_upload_process(self, pdf_file: UploadFile, background_tasks: BackgroundTasks) -> str:
        pdf_file_bytes = await pdf_file.read()
        ticket = self.create_ticket()
        self.chat_repo.save_initial_ticket(ticket, TicketStatus.PROCESSING)
        background_tasks.add_task(
            self.process_gemini_response,
            ticket=ticket,
            pdf_file_bytes=pdf_file_bytes
        )
        return ticket

    async def process_gemini_response(self, ticket: str, pdf_file_bytes: bytes):
        uploaded_file = None
        try:
            uploaded_file = self.gemini_service.upload_pdf_for_processing(
                pdf_file_bytes)
            gemini_response_dict = self.gemini_service.get_contract_data(
                uploaded_file)
            self.chat_repo.save_final_response(ticket, gemini_response_dict)
            self.chat_repo.update_status(ticket, TicketStatus.COMPLETED)
        except Exception as e:
            print(f"Erro no processamento Gemini para o ticket {ticket}: {e}")
            self.chat_repo.update_status(
                ticket, TicketStatus.FAILED, error_message=str(e))
        finally:
            if uploaded_file:
                self.gemini_service.client.files.delete(
                    name=uploaded_file.name)

    def get_chat_response_by_ticket(self, ticket: str):
        return self.chat_repo.get_response_by_ticket(ticket)
