"""정비 계획(Maintenance Plan) 모델"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class IntervalType(str, enum.Enum):
    CALENDAR = "Calendar"           # 캘린더 기반 (예: 6개월마다)
    RUNNING_HOURS = "RunningHours"  # 운전시간 기반 (예: 12000시간마다)
    CONDITION = "Condition"         # 상태 기반


class Priority(str, enum.Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class MaintenancePlan(Base):
    __tablename__ = "maintenance_plans"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    equipment_id: Mapped[str] = mapped_column(String(36), ForeignKey("equipment.id"), index=True)
    vessel_id: Mapped[str] = mapped_column(String(36), ForeignKey("vessels.id"), index=True)

    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    interval_type: Mapped[str] = mapped_column(String(50), default="Calendar")  # IntervalType values
    interval_value: Mapped[float | None] = mapped_column(Float, nullable=True)  # 주기 값 (월 or 시간)
    interval_unit: Mapped[str] = mapped_column(String(20), default="months")    # months, hours

    priority: Mapped[str] = mapped_column(String(20), default="Medium")  # Priority values
    is_class_related: Mapped[bool] = mapped_column(default=False)  # 선급 관련 여부
    estimated_hours: Mapped[float | None] = mapped_column(Float, nullable=True)  # 예상 작업 시간
    spare_parts: Mapped[str | None] = mapped_column(Text, nullable=True)  # 필요 부품 JSON

    last_done_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_done_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    next_due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    next_due_hours: Mapped[float | None] = mapped_column(Float, nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    equipment = relationship("Equipment")
    vessel = relationship("Vessel")
    work_orders = relationship("WorkOrder", back_populates="maintenance_plan")
