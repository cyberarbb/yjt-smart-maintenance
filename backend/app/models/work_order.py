"""작업 지시서(Work Order) 모델"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class WorkOrderStatus(str, enum.Enum):
    PLANNED = "Planned"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    OVERDUE = "Overdue"
    POSTPONED = "Postponed"
    CANCELLED = "Cancelled"


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    maintenance_plan_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("maintenance_plans.id"), nullable=True)
    equipment_id: Mapped[str] = mapped_column(String(36), ForeignKey("equipment.id"), index=True)
    vessel_id: Mapped[str] = mapped_column(String(36), ForeignKey("vessels.id"), index=True)

    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Planned", index=True)
    priority: Mapped[str] = mapped_column(String(20), default="Medium")

    planned_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    started_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    assigned_to: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    completed_by: Mapped[str | None] = mapped_column(String(36), nullable=True)
    actual_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    running_hours_at_completion: Mapped[float | None] = mapped_column(Float, nullable=True)

    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_class_related: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    maintenance_plan = relationship("MaintenancePlan", back_populates="work_orders")
    equipment = relationship("Equipment")
    vessel = relationship("Vessel")
