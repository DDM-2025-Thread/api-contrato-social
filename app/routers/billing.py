from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.jwt import get_current_user, get_current_admin, get_current_super_admin
from app.services.billing_service import BillingService
from app.schemas.api_cost_schema import ApiCostResponse, ApiCostUpdateRequest, BillingResponse, GenerateBillsRequest
from typing import List

router = APIRouter(prefix="/billing", tags=["billing"])

# ==============================================================
# === Endpoints de Usuário
# ==============================================================

@router.get("/me", response_model=List[BillingResponse])
def get_my_billing(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return BillingService(db).get_my_billing_history(user["sub"])

@router.get("/me/{billing_id}", response_model=BillingResponse)
def get_my_billing_details(billing_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return BillingService(db).get_my_billing_details(user["sub"], billing_id)

# ==============================================================
# === Endpoints de Admin
# ==============================================================

@router.get("/admin/config", response_model=ApiCostResponse)
def get_api_cost(_: None=Depends(get_current_admin), db: Session = Depends(get_db)):
    return BillingService(db).get_current_cost()

@router.put("/admin/config")
def update_api_cost(cost_update: ApiCostUpdateRequest, user=Depends(get_current_admin), db: Session = Depends(get_db)):
    print(user)
    return BillingService(db).update_cost(cost_update.new_cost, user["sub"])

@router.get("/admin/user/{user_id}", response_model=List[BillingResponse])
def get_user_billing(user_id: int, user=Depends(get_current_admin), db: Session = Depends(get_db)):
    return BillingService(db).get_user_billing_history(user_id)

# ==============================================================
# === Endpoints de Super Admin
# ==============================================================

@router.post("/admin/generate-bills")
def generate_bills(request: GenerateBillsRequest, user=Depends(get_current_super_admin), db: Session = Depends(get_db)):
    return BillingService(db).generate_monthly_bills(request.year, request.month)