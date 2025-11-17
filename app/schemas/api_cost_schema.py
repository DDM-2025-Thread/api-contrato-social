from pydantic import BaseModel, Field
from decimal import Decimal
from app.models.enum import BillingStatus

class ApiCostResponse(BaseModel):
    cost_per_request: Decimal

class ApiCostUpdateRequest(BaseModel):
    new_cost: Decimal = Field(..., gt=0)

class BillingResponse(BaseModel):
    id: int
    user_id: int
    period: str
    total_requests: int
    total_cost: int
    status: BillingStatus

    class Config:
        from_attributes = True

class GenerateBillsRequest(BaseModel):
    year: int = Field(..., gt=2020)
    month: int = Field(..., ge=1, le=12)