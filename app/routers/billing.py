from fastapi import APIRouter

router = APIRouter(prefix="/billing", tags=["billing"])

@router.get("/{user_id}")
def get(user_id: int):
    return {"message": f"Faturas do usuário {user_id} (placeholder)"}