from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin
from app.schemas.generic_schema import GenericResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService(db).register(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )

@router.post("/login", response_model=GenericResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return AuthService(db).login(
        email=user_data.email,
        password=user_data.password
    )