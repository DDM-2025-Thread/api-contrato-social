from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth_schema import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterResponse)
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService(db).register(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )

@router.post("/login", response_model=LoginResponse)
def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService(db).login(
        email=user_data.email,
        password=user_data.password
    )