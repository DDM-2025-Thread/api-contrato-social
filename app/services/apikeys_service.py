from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.api_keys_repository import ApiKeysRepository
from app.repositories.user_repository import UserRepository
from app.core.security import generate_api_key, hash_api_key
from app.models.enum import ApiKeyStatus

MAX_API_KEYS = 3

class ApiKeysService:
    def __init__(self, db: Session):
        self.repository = ApiKeysRepository(db)
        self.user_repository = UserRepository(db)

    def create_api_key(self, apikey_data, user_email: str):
        user = self.user_repository.find_by_email(user_email)
        if not user:
            raise Exception("Usuário não encontrado.")

        existing_keys = self.repository.find_by_user_id(user.id)
        if len(existing_keys) >= MAX_API_KEYS:
            raise Exception("Limite de chaves API atingido.")
        
        new_key = generate_api_key()
        hashed_key = hash_api_key(new_key)
        key_prefix = new_key[:8]

        self.repository.create({
            "user_id": user.id,
            "name": apikey_data.name,
            "key": hashed_key,
            "key_prefix": key_prefix
        })
        
        return {
            "message": "API Key gerada com sucesso. Guarde-a em um local seguro, pois ela não será exibida novamente.",
            "data": {
                "api_key": new_key
            }
        }

    def list_api_keys(self, user_email: str):
        user = self.user_repository.find_by_email(user_email)
        if not user:
            raise Exception("Usuário não encontrado.")

        keys = self.repository.find_by_user_id(user.id)
        return {
            "message": "Lista de API Keys.",
            "data": {
                "api_keys": [
                    {
                        "id": key.id,
                        "name": key.name,
                        "created_at": key.created_at
                    }
                    for key in keys
                    ]
            }
        }
    
    def revoke_key(self, user_email: str, key_id: int):
        user = self.user_repository.find_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

        key = self.repository.find_by_id_and_user_id(key_id, user.id)

        if not key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chave de API não encontrada ou não pertence a este usuário."
            )

        self.repository.update(key.id, {"status": ApiKeyStatus.REVOKED})

        return {"message": "Chave de API revogada com sucesso."}