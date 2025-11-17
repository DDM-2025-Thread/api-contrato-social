from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.jwt import get_current_user, get_current_admin, get_current_super_admin
from app.services.user_service import UserService
from app.schemas.user_schema import UserResponse, UserUpdateRequest
from app.schemas.generic_schema import GenericResponse
from app.schemas.auth_schema import RegisterRequest

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def find_one(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService(db).find_one(user["sub"])

@router.patch("/me", response_model=GenericResponse)
def update(user_update: UserUpdateRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    print(user_update)
    return UserService(db).update(user["sub"], user_update)

@router.delete("/me", response_model=GenericResponse)
def delete(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService(db).soft_delete(user["sub"])

# ==============================================================
# === Endpoints de Admin
# ==============================================================

@router.delete("/{user_id}", response_model=GenericResponse)
def hard_delete(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return UserService(db).hard_delete(user_id)

@router.patch("/{user_id}/reactivate", response_model=GenericResponse)
def reactivate(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_admin)):
    return UserService(db).reactivate(user_id)

# ==============================================================
# === Endpoints de Super Admin
# ==============================================================

@router.post("/users/create-admin")
def create_admin(user_data: RegisterRequest, current_user=Depends(get_current_super_admin), db: Session = Depends(get_db)):
    return UserService(db).create_admin(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )