from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.usage_log_repository import UsageLogRepository
from app.repositories.user_repository import UserRepository
from app.repositories.api_cost_repository import ApiCostRepository

class DashboardService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.usage_log_repository = UsageLogRepository(db)
        self.api_cost_repository = ApiCostRepository(db)

    def get_dashboard_stats(self, current_user_email: str):
        current_user = self.user_repository.find_by_email(current_user_email)
        
        if not current_user:
            raise Exception("Usuário atual não encontrado.")
        
        users = self.user_repository.find_all()
        
        users = [
            user for user in users
            if user.id != current_user.id and user.role != "super_admin"
        ]
        
        total_users = len(users)
        
        usage = self.usage_log_repository.find_all()
        
        total_requests = len(usage)
        total_revenue = sum(log.cost for log in usage if log.cost is not None)
        
        print(f"Total Users: {total_users}, Total Requests: {total_requests}, Total Revenue: {total_revenue}")

        return {
            "total_users": total_users,
            "total_requests": total_requests,
            "total_revenue": total_revenue
        }