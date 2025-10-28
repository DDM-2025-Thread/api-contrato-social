from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import JSON
from app.database import Base
from app.models.enum import ApiKeyStatus, BillingStatus, UserStatus, TicketStatus, Roles


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True, index=True)
    name = mapped_column(String(150))
    email = Column(String(150), unique=True, index=True)
    password_hash = Column(String(255))
    status = mapped_column(
        Enum(UserStatus), 
        nullable=False, 
        default=UserStatus.ACTIVE
    )
    role = mapped_column(
        Enum(Roles), 
        default=Roles.USER,
        nullable=False
    )
    api_keys = relationship("ApiKey", back_populates="user")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="api_keys")
    name = Column(String(100))
    key = Column(String(255), unique=True)
    key_prefix = Column(String(8), unique=True)
    status = Column(Enum(ApiKeyStatus), default=ApiKeyStatus.ACTIVE)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    endpoint = Column(String(255))
    timestamp = Column(DateTime, default=func.now())
    cost = Column(Integer)


class Billing(Base):
    __tablename__ = "billings"

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(ForeignKey("users.id"), nullable=False)
    period = Column(String(50))
    total_requests = Column(Integer)
    total_cost = Column(Integer)
    status = Column(Enum(BillingStatus), default=BillingStatus.PENDING)


class ChatTicket(Base):
    __tablename__ = "chat_ticket"

    id = mapped_column(Integer, primary_key=True, index=True)
    ticket_uuid = Column(String(36), unique=True, nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.PROCESSING, nullable=False)
    response_json = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
