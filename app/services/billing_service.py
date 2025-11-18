from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.billing_repository import BillingRepository
from app.repositories.user_repository import UserRepository
from app.repositories.api_cost_repository import ApiCostRepository
from app.repositories.usage_log_repository import UsageLogRepository
from app.models.enum import BillingStatus
from decimal import Decimal
from typing import List
import datetime

class BillingService:
    def __init__(self, db: Session):
        self.db = db
        self.billing_repo = BillingRepository(db)
        self.user_repo = UserRepository(db)
        self.api_cost_repository = ApiCostRepository(db)
        self.usage_log_repo = UsageLogRepository(db)

    def get_my_billing_history(self, user_email: str) -> List[dict]:
        user = self.user_repo.find_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
        
        bills = self.billing_repo.find_by_user_id(user.id)
        return [{"id": bill.id, "period": bill.period, "total_cost_cents": bill.total_cost, "status": bill.status} for bill in bills]

    def get_my_billing_details(self, user_email: str, billing_id: int):
        user = self.user_repo.find_by_email(user_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

        bill = self.billing_repo.find_by_id(billing_id)
        if not bill or bill.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fatura não encontrada ou não pertence a este usuário.")
        
        return bill

    def get_current_cost(self):
        cost_setting = self.api_cost_repository.get()
        if not cost_setting:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Configuração de custo não encontrada. Rode o seed.py.")
        return {"cost_per_request": cost_setting.cost_per_request}

    def update_cost(self, new_cost: Decimal, admin_user_email: str):
        admin_user = self.user_repo.find_by_email(admin_user_email)
        if not admin_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário admin não encontrado.")

        updated_cost = self.api_cost_repository.update(new_cost, admin_user.id)
        return {"message": "Custo atualizado com sucesso", "new_cost_cents": updated_cost.cost_per_request}

    def get_user_billing_history(self, user_id: int):
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
        
        return self.billing_repo.find_by_user_id(user.id)

    def generate_monthly_bills(self, year: int, month: int):
        period_str = f"{year}-{month:02d}"
        
        try:
            start_date = datetime.datetime(year, month, 1)
            next_month = month + 1
            next_year = year
            if next_month > 12:
                next_month = 1
                next_year += 1
            end_date = datetime.datetime(next_year, next_month, 1)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data inválida.")

        logs = self.usage_log_repo.find_by_period(start_date, end_date)
        if not logs:
            return {"message": f"Nenhum log de uso encontrado para o período {period_str}."}

        logs_by_user = {}
        for log in logs:
            if log.user_id not in logs_by_user:
                logs_by_user[log.user_id] = {'total_cost': 0, 'total_requests': 0}
            
            logs_by_user[log.user_id]['total_cost'] += log.cost
            logs_by_user[log.user_id]['total_requests'] += 1

        created_count = 0
        for user_id, data in logs_by_user.items():
            existing_bill = self.billing_repo.find_by_user_and_period(user_id, period_str)
            if existing_bill:
                continue

            self.billing_repo.create({
                "user_id": user_id,
                "period": period_str,
                "total_requests": data['total_requests'],
                "total_cost": data['total_cost'],
                "status": BillingStatus.PENDING
            })
            created_count += 1
        
        return {"message": f"Geração de faturas concluída para {period_str}. {created_count} novas faturas criadas."}