from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def find_all():
    return {"message": "Lista de usuários (placeholder)"}

@router.get("/{user_id}")
def find_one(user_id: int):
    return {"message": f"Detalhes do usuário {user_id} (placeholder)"}
