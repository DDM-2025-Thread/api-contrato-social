from sqlalchemy.orm import Session
from app.models.model import ApiKey
from typing import Optional, List

class ApiKeysRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, api_key_data: dict) -> ApiKey:
        api_key = ApiKey(**api_key_data)
        self.db.add(api_key)
        self.db.commit()
        self.db.refresh(api_key)
        return api_key

    def find_by_id(self, api_key_id: int) -> Optional[ApiKey]:
        return self.db.query(ApiKey).filter(ApiKey.id == api_key_id).first()

    def find_by_user_id(self, user_id: int) -> List[ApiKey]:
        return self.db.query(ApiKey).filter(ApiKey.user_id == user_id).all()

    def find_all(self) -> List[ApiKey]:
        return self.db.query(ApiKey).all()

    def update(self, api_key_id: int, api_key_data: dict) -> Optional[ApiKey]:
        api_key = self.find_by_id(api_key_id)
        if api_key:
            for key, value in api_key_data.items():
                setattr(api_key, key, value)
            self.db.commit()
            self.db.refresh(api_key)
        return api_key

    def delete(self, api_key_id: int) -> bool:
        api_key = self.find_by_id(api_key_id)
        if api_key:
            self.db.delete(api_key)
            self.db.commit()
            return True
        return False