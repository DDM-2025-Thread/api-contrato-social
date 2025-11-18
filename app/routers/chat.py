from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.jwt import get_current_user
from app.services.chat_service import ChatService
from typing import Annotated

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/upload")
async def upload(
    pdf_file: Annotated[UploadFile, File()],
    background_tasks: BackgroundTasks,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)

    user_email = user["sub"]

    ticket = await chat_service.start_upload_process(
        pdf_file=pdf_file,
        user_email=user_email,
        background_tasks=background_tasks
    )
    return ticket


@router.get("/getChatResponse/{ticket}")
async def get_result(
    ticket: str,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_user),
):
    chat_service = ChatService(db)
    response_data = chat_service.get_chat_response_by_ticket(ticket=ticket)
    return response_data
