from sqlalchemy.orm import Session
from app.repositories.api_keys_repository import ApiKeysRepository
from app.repositories.user_repository import UserRepository
from app.core.security import generate_api_key

MAX_API_KEYS = 3

class ApiKeysService:
    def __init__(self, db: Session):
        self.repository = ApiKeysRepository(db)
        self.user_repository = UserRepository(db)

    def create_api_key(self, user_email: str):
        user = self.user_repository.find_by_email(user_email)
        if not user:
            raise Exception("Usuário não encontrado.")

        existing_keys = self.repository.find_by_user_id(user.id)
        if len(existing_keys) >= MAX_API_KEYS:
            raise Exception("Limite de chaves API atingido.")
        
        new_key = generate_api_key()
        self.repository.create({
            "user_id": user.id,
            "key": new_key
        })
        
        return {
            "message": "API Key gerada com sucesso.",
            "data": {
                "api_key": new_key
            }
        }