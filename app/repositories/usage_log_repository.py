from sqlalchemy.orm import Session
from app.models.model import UsageLog
from typing import Optional, List
import datetime

class UsageLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, usage_log_data: dict) -> UsageLog:
        usage_log = UsageLog(**usage_log_data)
        self.db.add(usage_log)
        self.db.commit()
        self.db.refresh(usage_log)
        return usage_log

    def find_by_id(self, usage_log_id: int) -> Optional[UsageLog]:
        return self.db.query(UsageLog).filter(UsageLog.id == usage_log_id).first()

    def find_by_user_id(self, user_id: int) -> List[UsageLog]:
        return self.db.query(UsageLog).filter(UsageLog.user_id == user_id).all()

    def find_all(self) -> List[UsageLog]:
        return self.db.query(UsageLog).all()

    def find_by_period(self, start_date: datetime.datetime, end_date: datetime.datetime) -> List[UsageLog]:
        return self.db.query(UsageLog).filter(
            UsageLog.timestamp >= start_date,
            UsageLog.timestamp < end_date
        ).all()

    def update(self, usage_log_id: int, usage_log_data: dict) -> Optional[UsageLog]:
        usage_log = self.find_by_id(usage_log_id)
        if usage_log:
            for key, value in usage_log_data.items():
                setattr(usage_log, key, value)
            self.db.commit()
            self.db.refresh(usage_log)
        return usage_log

    def delete(self, usage_log_id: int) -> bool:
        usage_log = self.find_by_id(usage_log_id)
        if usage_log:
            self.db.delete(usage_log)
            self.db.commit()
            return True
        return False