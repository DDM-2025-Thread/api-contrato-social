from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.jwt import get_current_user
from app.services.user_service import UserService
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
def find_one(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return UserService(db).find_one(user["username"])