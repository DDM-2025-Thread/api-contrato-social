from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.jwt import get_current_user
from app.services.user_service import UserService
from app.schemas.user_schema import UserResponse, UserUpdateRequest
from app.schemas.generic_schema import GenericResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def find_one(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService(db).find_one(user["username"])

@router.patch("/me", response_model=GenericResponse)
def update(user_update: UserUpdateRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    print(user_update)
    return UserService(db).update(user["username"], user_update)

@router.delete("/me", response_model=GenericResponse)
def delete(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService(db).soft_delete(user["username"])

# ==============================================================
# === Endpoints de Admin (Temporariamente sem proteção de role) ===
# ==============================================================

@router.delete("/{user_id}", response_model=GenericResponse)
def hard_delete(user_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return UserService(db).hard_delete(user_id)