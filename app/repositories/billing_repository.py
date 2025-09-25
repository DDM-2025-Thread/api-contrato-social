from sqlalchemy.orm import Session
from app.models.model import Billing
from typing import Optional, List

class BillingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, billing_data: dict) -> Billing:
        billing = Billing(**billing_data)
        self.db.add(billing)
        self.db.commit()
        self.db.refresh(billing)
        return billing

    def find_by_id(self, billing_id: int) -> Optional[Billing]:
        return self.db.query(Billing).filter(Billing.id == billing_id).first()

    def find_by_user_id(self, user_id: int) -> List[Billing]:
        return self.db.query(Billing).filter(Billing.user_id == user_id).all()

    def find_all(self) -> List[Billing]:
        return self.db.query(Billing).all()

    def update(self, billing_id: int, billing_data: dict) -> Optional[Billing]:
        billing = self.find_by_id(billing_id)
        if billing:
            for key, value in billing_data.items():
                setattr(billing, key, value)
            self.db.commit()
            self.db.refresh(billing)
        return billing

    def delete(self, billing_id: int) -> bool:
        billing = self.find_by_id(billing_id)
        if billing:
            self.db.delete(billing)
            self.db.commit()
            return True
        return False
