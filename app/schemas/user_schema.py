from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    message: str
    name: str
    email: EmailStr
    api_key: str
    
    class Config:
        orm_mode = True
