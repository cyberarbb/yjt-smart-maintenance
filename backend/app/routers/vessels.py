"""선박(Vessel) 라우터 - CRUD + 역할별 필터링"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.vessel import Vessel
from app.models.user import User
from app.schemas.vessel import VesselCreate, VesselUpdate, VesselResponse, VesselSummary
from app.services.auth_service import get_current_user, get_admin_user
from app.services.vessel_service import get_accessible_vessels, get_vessel_summary

router = APIRouter()


@router.get("", response_model=list[VesselResponse])
def list_vessels(
    active_only: bool = False,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """역할에 따른 선박 목록"""
    vessels = get_accessible_vessels(db, user)
    if active_only:
        vessels = [v for v in vessels if v.is_active]
    return vessels


@router.get("/summary", response_model=list[VesselSummary])
def list_vessel_summaries(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """선박 요약 목록 (장비 수 포함)"""
    vessels = get_accessible_vessels(db, user)
    return [get_vessel_summary(db, v) for v in vessels]


@router.get("/types")
def get_vessel_types(db: Session = Depends(get_db)):
    """선박 유형 목록"""
    types = db.query(Vessel.vessel_type).distinct().all()
    return [t[0] for t in types if t[0]]


@router.get("/{vessel_id}", response_model=VesselResponse)
def get_vessel(
    vessel_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """선박 상세 조회"""
    vessel = db.query(Vessel).filter(Vessel.id == vessel_id).first()
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")
    return vessel


@router.post("", response_model=VesselResponse, status_code=201)
def create_vessel(
    data: VesselCreate,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """선박 등록 (관리자 전용)"""
    # IMO 번호 중복 체크
    if data.imo_number:
        existing = db.query(Vessel).filter(Vessel.imo_number == data.imo_number).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"IMO number {data.imo_number} already registered")

    vessel = Vessel(**data.model_dump())
    db.add(vessel)
    db.commit()
    db.refresh(vessel)
    return vessel


@router.put("/{vessel_id}", response_model=VesselResponse)
def update_vessel(
    vessel_id: str,
    data: VesselUpdate,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """선박 수정 (관리자 전용)"""
    vessel = db.query(Vessel).filter(Vessel.id == vessel_id).first()
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")

    # IMO 번호 중복 체크 (다른 선박)
    if data.imo_number:
        existing = db.query(Vessel).filter(
            Vessel.imo_number == data.imo_number,
            Vessel.id != vessel_id,
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"IMO number {data.imo_number} already registered")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vessel, key, value)

    db.commit()
    db.refresh(vessel)
    return vessel


@router.delete("/{vessel_id}")
def delete_vessel(
    vessel_id: str,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """선박 삭제 (관리자 전용)"""
    vessel = db.query(Vessel).filter(Vessel.id == vessel_id).first()
    if not vessel:
        raise HTTPException(status_code=404, detail="Vessel not found")

    db.delete(vessel)
    db.commit()
    return {"message": f"Vessel '{vessel.name}' deleted"}
