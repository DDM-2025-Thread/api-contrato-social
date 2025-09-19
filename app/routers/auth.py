from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register():
    return {"message": "Usuário registrado com sucesso (placeholder)"}

@router.post("/login")
def login():
    return {"message": "Login realizado com sucesso (placeholder)"}
