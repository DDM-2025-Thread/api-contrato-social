from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, mapped_column
from datetime import datetime
from app.database import Base
from app.models.enum import ApiKeyStatus, BillingStatus

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(150))
    email = Column(String(150), unique=True, index=True)
    password_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    api_key = relationship("ApiKey", back_populates="User")

class ApiKey(Base):
    __tablename__ = "api_keys"

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    User = relationship("User", back_populates="api_keys")
    key = Column(String(150), unique=True)
    status = Column(Enum(ApiKeyStatus), default=ApiKeyStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    endpoint = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)
    cost = Column(Integer)

class Billing(Base):
    __tablename__ = "billings"

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    period = Column(String(50))
    total_requests = Column(Integer)
    total_cost = Column(Integer)
    status = Column(Enum(BillingStatus), default=BillingStatus.PENDING)