"""운전시간(Running Hours) 스키마"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class RunningHoursRecord(BaseModel):
    """단건 운전시간 기록"""
    equipment_id: str
    recorded_date: date
    daily_hours: float  # 0~24
    note: Optional[str] = None


class RunningHoursBulkRecord(BaseModel):
    """벌크 운전시간 기록 (여러 장비 한번에)"""
    vessel_id: str
    recorded_date: date
    records: list[RunningHoursRecord]


class RunningHoursResponse(BaseModel):
    id: str
    equipment_id: str
    recorded_date: date
    daily_hours: float
    total_hours: float
    recorded_by: Optional[str] = None
    note: Optional[str] = None
    created_at: Optional[datetime] = None

    # 편의 필드 (join으로 채워짐)
    equipment_name: Optional[str] = None
    equipment_code: Optional[str] = None

    model_config = {"from_attributes": True}


class RunningHoursLatest(BaseModel):
    """장비별 최신 운전시간"""
    equipment_id: str
    equipment_code: str
    equipment_name: str
    category: str
    current_hours: float
    overhaul_interval: Optional[float] = None
    last_recorded_date: Optional[date] = None
    daily_hours: float = 0.0


class RunningHoursChartData(BaseModel):
    """차트용 데이터"""
    date: str
    hours: float
    total: float
