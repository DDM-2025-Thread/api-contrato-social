from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.model import User
from app.models.enum import UserStatus

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_data: dict) -> User:
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def find_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def find_all(self) -> List[User]:
        return self.db.query(User).all()
    
    def update(self, user_id: int, user_data: dict) -> Optional[User]:
        user = self.find_by_id(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        user = self.find_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def soft_delete(self, user_id: int) -> bool:
        user = self.find_by_id(user_id)
        if user:
            user.status = UserStatus.INACTIVE
            self.db.commit()
            self.db.refresh(user)
            return True
        return False