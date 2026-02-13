"""선박 서비스 - 접근 제어 + 요약 통계"""
from sqlalchemy.orm import Session
from app.models.vessel import Vessel
from app.models.user import User


def get_accessible_vessels(db: Session, user: User) -> list[Vessel]:
    """사용자 역할에 따라 접근 가능한 선박 목록 반환"""
    query = db.query(Vessel)

    role = getattr(user, "role", None) or "admin"

    # admin / shore_manager → 전체 선박
    if role in ("admin", "shore_manager") or user.is_admin:
        return query.order_by(Vessel.name).all()

    # captain / chief_engineer / engineer → 본인 배정 선박만
    vessel_id = getattr(user, "vessel_id", None)
    if vessel_id:
        return query.filter(Vessel.id == vessel_id).all()

    # customer → 활성 선박만 (보기 전용)
    return query.filter(Vessel.is_active == True).order_by(Vessel.name).all()


def get_vessel_summary(db: Session, vessel: Vessel) -> dict:
    """선박 요약 정보 (장비 수 포함)"""
    equipment_count = 0
    try:
        if hasattr(vessel, "equipment") and vessel.equipment:
            equipment_count = len(vessel.equipment)
    except Exception:
        pass

    return {
        "id": vessel.id,
        "name": vessel.name,
        "vessel_type": vessel.vessel_type,
        "flag": vessel.flag,
        "owner_company": vessel.owner_company,
        "is_active": vessel.is_active,
        "equipment_count": equipment_count,
    }
