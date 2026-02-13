"""선박(Vessel) 모델 - Smart Vessel Management"""
import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Vessel(Base):
    __tablename__ = "vessels"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(200), index=True)
    imo_number: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    vessel_type: Mapped[str] = mapped_column(String(100))  # Container Ship, Bulk Carrier, Tanker, etc.
    flag: Mapped[str | None] = mapped_column(String(100), nullable=True)
    class_society: Mapped[str | None] = mapped_column(String(100), nullable=True)  # KR, DNV, LR, BV, etc.
    gross_tonnage: Mapped[float | None] = mapped_column(Float, nullable=True)
    build_year: Mapped[int | None] = mapped_column(nullable=True)
    owner_company: Mapped[str | None] = mapped_column(String(200), nullable=True)
    manager_company: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    equipment = relationship("Equipment", back_populates="vessel", cascade="all, delete-orphan")
