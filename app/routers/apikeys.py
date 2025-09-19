from fastapi import APIRouter

router = APIRouter(prefix="/apikeys", tags=["apikeys"])

@router.post("/generate")
def generate():
    return {"message": "API Key gerada (placeholder)"}

@router.get("/{user_id}")
def list_all(user_id: int):
    return {"message": f"Lista de API Keys do usuário {user_id} (placeholder)"}