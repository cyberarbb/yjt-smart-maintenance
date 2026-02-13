"""장비(Equipment) 모델 - 선박별 장비 계층 구조"""
import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class EquipmentCategory(str, enum.Enum):
    MAIN_ENGINE = "Main Engine"
    GENERATOR = "Generator"
    BOILER = "Boiler"
    TURBOCHARGER = "Turbocharger"
    PUMP = "Pump"
    COMPRESSOR = "Compressor"
    STEERING_GEAR = "Steering Gear"
    EMERGENCY_GENERATOR = "Emergency Generator"
    PURIFIER = "Purifier"
    HEAT_EXCHANGER = "Heat Exchanger"
    CRANE = "Crane"
    FUEL_SYSTEM = "Fuel System"
    EXHAUST_SYSTEM = "Exhaust System"
    OTHER = "Other"


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vessel_id: Mapped[str] = mapped_column(String(36), ForeignKey("vessels.id"), index=True)
    parent_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("equipment.id"), nullable=True, index=True)

    equipment_code: Mapped[str] = mapped_column(String(50), index=True)  # e.g. "ME-001", "TC-001"
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(100))  # EquipmentCategory values
    maker: Mapped[str | None] = mapped_column(String(200), nullable=True)
    model: Mapped[str | None] = mapped_column(String(200), nullable=True)
    serial_number: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # 기술 사양
    rated_power: Mapped[str | None] = mapped_column(String(100), nullable=True)  # e.g. "68,640 kW"
    rated_rpm: Mapped[str | None] = mapped_column(String(50), nullable=True)  # e.g. "80 RPM"

    # 운전시간 관리
    initial_running_hours: Mapped[float] = mapped_column(Float, default=0.0)
    current_running_hours: Mapped[float] = mapped_column(Float, default=0.0)
    overhaul_interval_hours: Mapped[float | None] = mapped_column(Float, nullable=True)  # e.g. 24000

    # 설치/상태
    install_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_overhaul_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="Normal")  # Normal, Warning, Critical, Inactive

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)  # 트리 정렬 순서
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    vessel = relationship("Vessel", back_populates="equipment")
    children = relationship("Equipment", back_populates="parent", cascade="all, delete-orphan")
    parent = relationship("Equipment", remote_side=[id], back_populates="children")
