"""Activity Log 모델 - 사용자 로그인/로그아웃 기록"""
import uuid
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    user_email = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    action = Column(String, nullable=False, index=True)  # "login", "logout", "login_failed"
    ip_address = Column(String, default="")
    user_agent = Column(Text, default="")
    details = Column(Text, default="")  # 추가 상세 (예: 실패 사유)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
