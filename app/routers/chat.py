from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.jwt import get_current_user
from app.services.chat_service import ChatService
from typing import Annotated, List
from app.schemas.chat_schema import ChatResponseSchema

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/upload")
async def upload(
    pdf_file: Annotated[UploadFile, File()],
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user),
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


@router.get("/get-response/{ticket}", response_model=ChatResponseSchema)
def get_result(
    ticket: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    chat_service = ChatService(db)
    user_email = user["sub"]
    return chat_service.get_chat_response_by_ticket(ticket=ticket, user_email=user_email)


@router.get("/find-by-user", response_model=List[ChatResponseSchema])
def get_chats(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    user_email = user["sub"]
    return chat_service.find_chats_by_user_email(user_email=user_email)


@router.delete("/delete/{ticket}", status_code=status.HTTP_200_OK)
def delete(
    ticket: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    user_email = user["sub"]
    chat_service.delete_by_ticket(ticket=ticket, user_email=user_email)
    return {"message": "Chat successfully deleted"}
