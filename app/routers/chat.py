from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.database.dependencies import get_async_session
from app.schemas.chat_schema import TicketResponse, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/upload", response_model=TicketResponse)
async def upload(
    pdf_file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_async_session)
):
    chat_service = ChatService(db)
    ticket = await chat_service.start_upload_process(
        pdf_file=pdf_file,
        background_tasks=background_tasks
    )
    return TicketResponse(ticket=ticket)


@router.get("/getChatResponse/{ticket}", response_model=ChatResponse)
async def get_result(
    ticket: str,
    db: AsyncSession = Depends(get_async_session)
):
    chat_service = ChatService(db)
    response_data = await chat_service.get_chat_response_by_ticket(ticket=ticket)
    return response_data
