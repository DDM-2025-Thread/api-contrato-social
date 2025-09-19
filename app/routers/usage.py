from fastapi import APIRouter

router = APIRouter(prefix="/usage", tags=["usage"])

@router.get("/{user_id}")
def get(user_id: int):
    return {"message": f"Histórico de uso do usuário {user_id} (placeholder)"}