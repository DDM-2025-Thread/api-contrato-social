from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.core.security import hash_password, generate_api_key
from app.repositories.user_repository import UserRepository
from app.repositories.api_keys_repository import ApiKeysRepository

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    exists = UserRepository(db).find_by_email(user_data.email)
    if exists:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    new_user = UserRepository(db).create({
        "name": user_data.name,
        "email": user_data.email,
        "password_hash": hash_password(user_data.password)
    })

    if not new_user:
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")

    api_key = ApiKeysRepository(db).create({
        "user_id": new_user.id,
        "key": generate_api_key()
    })

    return {
        "message": "Usuário registrado com sucesso",
        "name": new_user.name,
        "email": new_user.email,
        "api_key": api_key.key
    }

@router.post("/login")
def login():
    return {"message": "Login realizado com sucesso (placeholder)"}
