from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.jwt import get_current_user
from app.services.apikeys_service import ApiKeysService
from app.schemas.generic_schema import GenericResponse

router = APIRouter(prefix="/apikeys", tags=["apikeys"])

@router.post("/generate", response_model=GenericResponse, status_code=status.HTTP_201_CREATED)
def generate(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return ApiKeysService(db).create_api_key(user["username"])

@router.get("/{user_id}")
def list_all(user_id: int):
    return {"message": f"Lista de API Keys do usuário {user_id} (placeholder)"}