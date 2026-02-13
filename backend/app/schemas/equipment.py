"""장비(Equipment) 스키마 - 계층 구조 포함"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EquipmentCreate(BaseModel):
    vessel_id: str
    parent_id: Optional[str] = None
    equipment_code: str
    name: str
    category: str
    maker: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    rated_power: Optional[str] = None
    rated_rpm: Optional[str] = None
    initial_running_hours: float = 0.0
    current_running_hours: float = 0.0
    overhaul_interval_hours: Optional[float] = None
    install_date: Optional[datetime] = None
    description: Optional[str] = None
    sort_order: int = 0


class EquipmentUpdate(BaseModel):
    parent_id: Optional[str] = None
    equipment_code: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    maker: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    rated_power: Optional[str] = None
    rated_rpm: Optional[str] = None
    initial_running_hours: Optional[float] = None
    current_running_hours: Optional[float] = None
    overhaul_interval_hours: Optional[float] = None
    install_date: Optional[datetime] = None
    last_overhaul_date: Optional[datetime] = None
    status: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class EquipmentResponse(BaseModel):
    id: str
    vessel_id: str
    parent_id: Optional[str] = None
    equipment_code: str
    name: str
    category: str
    maker: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    rated_power: Optional[str] = None
    rated_rpm: Optional[str] = None
    initial_running_hours: float = 0.0
    current_running_hours: float = 0.0
    overhaul_interval_hours: Optional[float] = None
    install_date: Optional[datetime] = None
    last_overhaul_date: Optional[datetime] = None
    status: str = "Normal"
    description: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class EquipmentTreeNode(BaseModel):
    """재귀 트리 노드 (프론트엔드 트리 렌더링용)"""
    id: str
    vessel_id: str
    parent_id: Optional[str] = None
    equipment_code: str
    name: str
    category: str
    maker: Optional[str] = None
    model: Optional[str] = None
    status: str = "Normal"
    current_running_hours: float = 0.0
    overhaul_interval_hours: Optional[float] = None
    sort_order: int = 0
    children: list["EquipmentTreeNode"] = []

    model_config = {"from_attributes": True}


class EquipmentBrief(BaseModel):
    """장비 경량 스키마 (드롭다운 등)"""
    id: str
    equipment_code: str
    name: str
    category: str
    vessel_id: str

    model_config = {"from_attributes": True}
