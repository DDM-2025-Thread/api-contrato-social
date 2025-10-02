from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.repositories.api_keys_repository import ApiKeysRepository
from app.core.security import hash_password, verify_password, generate_api_key

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.api_key_repo = ApiKeysRepository(db)

    def register(self, name: str, email: str, password: str):
        if self.user_repo.find_by_email(email):
            raise HTTPException(status_code=400, detail="Usuário já existe")

        new_user = self.user_repo.create({
            "name": name,
            "email": email,
            "password_hash": hash_password(password)
        })

        if not new_user:
            raise HTTPException(status_code=500, detail="Erro ao criar usuário")

        api_key = self.api_key_repo.create({
            "user_id": new_user.id,
            "key": generate_api_key()
        })

        return {
            "message": "Usuário registrado com sucesso",
            "name": new_user.name,
            "email": new_user.email,
            "api_key": api_key.key
        }

    def login(self, email: str, password: str):
        user = self.user_repo.find_by_email(email)
        if not user:
            raise HTTPException(status_code=400, detail="Usuário não encontrado")

        if not verify_password(password, str(user.password_hash)):
            raise HTTPException(status_code=400, detail="Senha incorreta")

        return {"message": "Login realizado com sucesso"}