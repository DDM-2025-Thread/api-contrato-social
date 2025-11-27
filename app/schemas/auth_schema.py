from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class RegisterResponse(BaseModel):
    message: str
    name: str
    email: EmailStr
    role: str
    token: str
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    name: str
    role: str
    token: str

    class Config:
        from_attributes = True