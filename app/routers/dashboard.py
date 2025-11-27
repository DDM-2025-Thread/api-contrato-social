from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.jwt import get_current_user
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_stats(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return DashboardService(db).get_dashboard_stats(current_user_email=user['sub'])