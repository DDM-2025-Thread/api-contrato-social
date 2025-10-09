from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.jwt import get_current_user
from app.services.apikeys_service import ApiKeysService
from app.schemas.generic_schema import GenericResponse
from app.schemas.apikeys_schema import ApiKeyRequest

router = APIRouter(prefix="/apikeys", tags=["apikeys"])

@router.post("/generate", response_model=GenericResponse, status_code=status.HTTP_201_CREATED)
def generate(apikey_data: ApiKeyRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return ApiKeysService(db).create_api_key(apikey_data, user["username"])

@router.get("/")
def list_all(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return ApiKeysService(db).list_api_keys(user['username'])