from sqlalchemy.orm import Session
from app.models.model import ApiCost
from typing import Optional
from decimal import Decimal

class ApiCostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self) -> Optional[ApiCost]:
        return self.db.query(ApiCost).filter(ApiCost.id == 1).first()

    def update(self, new_cost: Decimal, admin_user_id: int) -> ApiCost:
        cost_setting = self.get()
        if not cost_setting:
            cost_setting = ApiCost(id=1, cost_per_request=new_cost, updated_by_id=admin_user_id)
            self.db.add(cost_setting)
        else:
            cost_setting.cost_per_request = new_cost
            cost_setting.updated_by_user_id = admin_user_id
        
        self.db.commit()
        self.db.refresh(cost_setting)
        return cost_setting