"""운전시간(Running Hours) 모델 - 일일 기록 + 누적 추적"""
import uuid
from datetime import datetime, date
from sqlalchemy import String, DateTime, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class RunningHours(Base):
    __tablename__ = "running_hours"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    equipment_id: Mapped[str] = mapped_column(String(36), ForeignKey("equipment.id"), index=True)
    recorded_date: Mapped[date] = mapped_column(Date, index=True)
    daily_hours: Mapped[float] = mapped_column(Float, default=0.0)  # 해당일 운전 시간 (0~24)
    total_hours: Mapped[float] = mapped_column(Float, default=0.0)  # 해당일 기준 누적 시간
    recorded_by: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    note: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    equipment = relationship("Equipment")

    __table_args__ = (
        UniqueConstraint("equipment_id", "recorded_date", name="uq_equipment_date"),
    )
