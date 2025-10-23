from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.enum import UserStatus

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: str

    class Config:
        orm_mode = True

class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    status: Optional[UserStatus] = None