import uuid
from datetime import datetime
from sqlalchemy import String, Text, Float, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class TurboBrand(str, enum.Enum):
    MAN = "MAN"
    MHI = "MHI"
    KBB = "KBB"
    ABB = "ABB"
    NAPIER = "Napier"
    OTHER = "Other"


class PartCategory(str, enum.Enum):
    NOZZLE_RING = "Nozzle Ring"
    BEARING = "Bearing"
    TURBINE_BLADE = "Turbine Blade"
    COMPRESSOR_WHEEL = "Compressor Wheel"
    SHAFT = "Shaft"
    SEAL = "Seal"
    GASKET = "Gasket"
    CASING = "Casing"
    CARTRIDGE = "Cartridge"
    FILTER = "Filter"
    OTHER = "Other"


class Part(Base):
    __tablename__ = "parts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    part_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    brand: Mapped[str] = mapped_column(String(20), index=True)
    turbo_model: Mapped[str] = mapped_column(String(100), index=True)
    category: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    unit_price: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    equipment_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    lead_time_days: Mapped[int | None] = mapped_column(nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    inventory = relationship("Inventory", back_populates="part", uselist=False)
