from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chat_service import ChatService
from typing import Annotated

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/upload")
async def upload(
    pdf_file: Annotated[UploadFile, File()],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    ticket = await chat_service.start_upload_process(
        pdf_file=pdf_file,
        background_tasks=background_tasks
    )
    return ticket


@router.get("/getChatResponse/{ticket}")
async def get_result(
    ticket: str,
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    response_data = chat_service.get_chat_response_by_ticket(ticket=ticket)
    return response_data
