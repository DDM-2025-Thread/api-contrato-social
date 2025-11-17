from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register(self, name: str, email: str, password: str):
        if self.user_repository.find_by_email(email):
            raise HTTPException(status_code=400, detail="Usuário já existe")

        new_user = self.user_repository.create({
            "name": name,
            "email": email,
            "password_hash": hash_password(password)
        })

        if not new_user:
            raise HTTPException(status_code=500, detail="Erro ao criar usuário")

        access_token = create_access_token(data={"sub": new_user.email}, scope="user")

        return {
            "message": "Usuário registrado com sucesso",
            "name": new_user.name,
            "email": new_user.email,
            "token": access_token
        }

    def login(self, email: str, password: str):
        user = self.user_repository.find_by_email(email)
        if not user:
            raise HTTPException(status_code=400, detail="Usuário não encontrado")

        if not verify_password(password, str(user.password_hash)):
            raise HTTPException(status_code=400, detail="Senha incorreta")

        token_data = {
            "sub": user.email,
            "role": user.role.value
        }

        access_token = create_access_token(data=token_data, scope="user")
        
        return {
            "name": user.name,
            "token": access_token
        }
