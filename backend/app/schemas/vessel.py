"""선박(Vessel) 스키마"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VesselCreate(BaseModel):
    name: str
    imo_number: Optional[str] = None
    vessel_type: str
    flag: Optional[str] = None
    class_society: Optional[str] = None
    gross_tonnage: Optional[float] = None
    build_year: Optional[int] = None
    owner_company: Optional[str] = None
    manager_company: Optional[str] = None
    description: Optional[str] = None


class VesselUpdate(BaseModel):
    name: Optional[str] = None
    imo_number: Optional[str] = None
    vessel_type: Optional[str] = None
    flag: Optional[str] = None
    class_society: Optional[str] = None
    gross_tonnage: Optional[float] = None
    build_year: Optional[int] = None
    owner_company: Optional[str] = None
    manager_company: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class VesselResponse(BaseModel):
    id: str
    name: str
    imo_number: Optional[str] = None
    vessel_type: str
    flag: Optional[str] = None
    class_society: Optional[str] = None
    gross_tonnage: Optional[float] = None
    build_year: Optional[int] = None
    owner_company: Optional[str] = None
    manager_company: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class VesselSummary(BaseModel):
    """선박 요약 (목록용 경량 스키마)"""
    id: str
    name: str
    vessel_type: str
    flag: Optional[str] = None
    owner_company: Optional[str] = None
    is_active: bool = True
    equipment_count: int = 0

    model_config = {"from_attributes": True}
