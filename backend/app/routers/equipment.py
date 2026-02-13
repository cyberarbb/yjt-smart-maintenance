"""장비(Equipment) 라우터 - CRUD + 트리 구조"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.equipment import Equipment
from app.models.vessel import Vessel
from app.models.user import User
from app.schemas.equipment import (
    EquipmentCreate, EquipmentUpdate, EquipmentResponse,
    EquipmentTreeNode, EquipmentBrief,
)
from app.services.auth_service import get_current_user, get_admin_user

router = APIRouter()


def _build_tree(equipment_list: list[Equipment], parent_id: str | None = None) -> list[dict]:
    """장비 목록을 재귀 트리로 변환"""
    nodes = []
    for eq in sorted(equipment_list, key=lambda e: (e.sort_order, e.name)):
        if eq.parent_id == parent_id:
            children = _build_tree(equipment_list, eq.id)
            nodes.append({
                "id": eq.id,
                "vessel_id": eq.vessel_id,
                "parent_id": eq.parent_id,
                "equipment_code": eq.equipment_code,
                "name": eq.name,
                "category": eq.category,
                "maker": eq.maker,
                "model": eq.model,
                "status": eq.status,
                "current_running_hours": eq.current_running_hours,
                "overhaul_interval_hours": eq.overhaul_interval_hours,
                "sort_order": eq.sort_order,
                "children": children,
            })
    return nodes


@router.get("/vessels/{vessel_id}/equipment-tree", response_model=list[EquipmentTreeNode])
def get_equipment_tree(
    vessel_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """선박의 장비 트리 구조 반환"""
    vessel = db.query(Vessel).filter(Vessel.id == vessel_id).first()
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")

    all_equipment = db.query(Equipment).filter(
        Equipment.vessel_id == vessel_id,
        Equipment.is_active == True,
    ).all()

    return _build_tree(all_equipment, parent_id=None)


@router.get("/vessels/{vessel_id}/equipment", response_model=list[EquipmentResponse])
def list_vessel_equipment(
    vessel_id: str,
    category: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """선박의 장비 목록 (플랫)"""
    query = db.query(Equipment).filter(Equipment.vessel_id == vessel_id)
    if category:
        query = query.filter(Equipment.category == category)
    return query.order_by(Equipment.sort_order, Equipment.name).all()


@router.get("/equipment/categories")
def get_equipment_categories(db: Session = Depends(get_db)):
    """장비 카테고리 목록"""
    cats = db.query(Equipment.category).distinct().all()
    return [c[0] for c in cats if c[0]]


@router.get("/equipment/brief", response_model=list[EquipmentBrief])
def list_equipment_brief(
    vessel_id: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """장비 경량 목록 (드롭다운용)"""
    query = db.query(Equipment).filter(Equipment.is_active == True)
    if vessel_id:
        query = query.filter(Equipment.vessel_id == vessel_id)
    return query.order_by(Equipment.name).all()


@router.get("/equipment/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(
    equipment_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """장비 상세 조회"""
    eq = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return eq


@router.post("/equipment", response_model=EquipmentResponse, status_code=201)
def create_equipment(
    data: EquipmentCreate,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """장비 등록 (관리자 전용)"""
    # 선박 존재 확인
    vessel = db.query(Vessel).filter(Vessel.id == data.vessel_id).first()
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")

    # parent_id 존재 확인
    if data.parent_id:
        parent = db.query(Equipment).filter(Equipment.id == data.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent equipment not found")

    # equipment_code 중복 체크 (같은 선박 내)
    existing = db.query(Equipment).filter(
        Equipment.vessel_id == data.vessel_id,
        Equipment.equipment_code == data.equipment_code,
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Equipment code '{data.equipment_code}' already exists in this vessel")

    eq = Equipment(**data.model_dump())
    db.add(eq)
    db.commit()
    db.refresh(eq)
    return eq


@router.put("/equipment/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: str,
    data: EquipmentUpdate,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """장비 수정 (관리자 전용)"""
    eq = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")

    update_data = data.model_dump(exclude_unset=True)

    # equipment_code 변경 시 중복 체크
    if "equipment_code" in update_data:
        existing = db.query(Equipment).filter(
            Equipment.vessel_id == eq.vessel_id,
            Equipment.equipment_code == update_data["equipment_code"],
            Equipment.id != equipment_id,
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"Equipment code already exists in this vessel")

    for key, value in update_data.items():
        setattr(eq, key, value)

    db.commit()
    db.refresh(eq)
    return eq


@router.delete("/equipment/{equipment_id}")
def delete_equipment(
    equipment_id: str,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """장비 삭제 (관리자 전용) - 하위 장비도 함께 삭제"""
    eq = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Equipment not found")

    db.delete(eq)
    db.commit()
    return {"message": f"Equipment '{eq.name}' and its children deleted"}
