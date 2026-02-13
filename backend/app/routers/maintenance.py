"""정비 계획(Maintenance Plan) + 작업지시서(Work Order) 라우터"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.equipment import Equipment
from app.models.vessel import Vessel
from app.models.maintenance_plan import MaintenancePlan
from app.models.work_order import WorkOrder
from app.services.auth_service import get_current_user, get_admin_user, get_engineer_or_above
from app.services.pms_service import (
    get_overdue_work_orders,
    get_upcoming_work_orders,
    get_pms_stats,
    get_calendar_data,
)

router = APIRouter()


# ── Maintenance Plans ──────────────────────────────────

@router.get("/plans")
def list_maintenance_plans(
    vessel_id: str | None = None,
    equipment_id: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """정비 계획 목록"""
    query = db.query(MaintenancePlan).filter(MaintenancePlan.is_active == True)
    if vessel_id:
        query = query.filter(MaintenancePlan.vessel_id == vessel_id)
    if equipment_id:
        query = query.filter(MaintenancePlan.equipment_id == equipment_id)

    plans = query.order_by(MaintenancePlan.next_due_date).all()
    return [_plan_to_dict(p, db) for p in plans]


@router.get("/plans/{plan_id}")
def get_maintenance_plan(
    plan_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """정비 계획 상세"""
    plan = db.query(MaintenancePlan).filter(MaintenancePlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Maintenance plan not found")
    return _plan_to_dict(plan, db)


@router.post("/plans", status_code=201)
def create_maintenance_plan(
    data: dict,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """정비 계획 등록"""
    # Parse dates
    for date_field in ["last_done_date", "next_due_date"]:
        if data.get(date_field) and isinstance(data[date_field], str):
            data[date_field] = datetime.fromisoformat(data[date_field])

    plan = MaintenancePlan(**data)
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return _plan_to_dict(plan, db)


@router.put("/plans/{plan_id}")
def update_maintenance_plan(
    plan_id: str,
    data: dict,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """정비 계획 수정"""
    plan = db.query(MaintenancePlan).filter(MaintenancePlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Maintenance plan not found")

    for date_field in ["last_done_date", "next_due_date"]:
        if data.get(date_field) and isinstance(data[date_field], str):
            data[date_field] = datetime.fromisoformat(data[date_field])

    for key, value in data.items():
        if hasattr(plan, key):
            setattr(plan, key, value)

    db.commit()
    db.refresh(plan)
    return _plan_to_dict(plan, db)


# ── Work Orders ────────────────────────────────────────

@router.get("/work-orders")
def list_work_orders(
    vessel_id: str | None = None,
    status: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """작업지시서 목록"""
    query = db.query(WorkOrder)
    if vessel_id:
        query = query.filter(WorkOrder.vessel_id == vessel_id)
    if status:
        query = query.filter(WorkOrder.status == status)

    orders = query.order_by(WorkOrder.planned_date).all()

    # Overdue 상태 자동 감지
    now = datetime.utcnow()
    results = []
    for wo in orders:
        d = _wo_to_dict(wo, db)
        if wo.status in ("Planned", "InProgress") and wo.due_date and wo.due_date < now:
            d["is_overdue"] = True
        else:
            d["is_overdue"] = False
        results.append(d)

    return results


@router.get("/work-orders/stats")
def get_work_order_stats(
    vessel_id: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """PMS 통계"""
    return get_pms_stats(db, vessel_id)


@router.get("/work-orders/calendar")
def get_work_order_calendar(
    vessel_id: str,
    year: int = Query(default=None),
    month: int = Query(default=None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """캘린더 데이터"""
    now = datetime.utcnow()
    y = year or now.year
    m = month or now.month
    return get_calendar_data(db, vessel_id, y, m)


@router.get("/work-orders/overdue")
def get_overdue(
    vessel_id: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """초과 작업지시서"""
    orders = get_overdue_work_orders(db, vessel_id)
    return [_wo_to_dict(wo, db) for wo in orders]


@router.get("/work-orders/upcoming")
def get_upcoming(
    vessel_id: str | None = None,
    days: int = 30,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """예정 작업지시서"""
    orders = get_upcoming_work_orders(db, vessel_id, days)
    return [_wo_to_dict(wo, db) for wo in orders]


@router.get("/work-orders/{wo_id}")
def get_work_order(
    wo_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """작업지시서 상세"""
    wo = db.query(WorkOrder).filter(WorkOrder.id == wo_id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    return _wo_to_dict(wo, db)


@router.post("/work-orders", status_code=201)
def create_work_order(
    data: dict,
    user: User = Depends(get_engineer_or_above),
    db: Session = Depends(get_db),
):
    """작업지시서 생성"""
    for date_field in ["planned_date", "due_date", "started_date", "completed_date"]:
        if data.get(date_field) and isinstance(data[date_field], str):
            data[date_field] = datetime.fromisoformat(data[date_field])

    wo = WorkOrder(**data)
    db.add(wo)
    db.commit()
    db.refresh(wo)
    return _wo_to_dict(wo, db)


@router.put("/work-orders/{wo_id}")
def update_work_order(
    wo_id: str,
    data: dict,
    user: User = Depends(get_engineer_or_above),
    db: Session = Depends(get_db),
):
    """작업지시서 수정 (상태 변경 포함)"""
    wo = db.query(WorkOrder).filter(WorkOrder.id == wo_id).first()
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")

    for date_field in ["planned_date", "due_date", "started_date", "completed_date"]:
        if data.get(date_field) and isinstance(data[date_field], str):
            data[date_field] = datetime.fromisoformat(data[date_field])

    # 상태 변경 로직
    if "status" in data:
        new_status = data["status"]
        if new_status == "InProgress" and not wo.started_date:
            data["started_date"] = datetime.utcnow()
        elif new_status == "Completed" and not wo.completed_date:
            data["completed_date"] = datetime.utcnow()
            data["completed_by"] = user.id

    for key, value in data.items():
        if hasattr(wo, key):
            setattr(wo, key, value)

    db.commit()
    db.refresh(wo)
    return _wo_to_dict(wo, db)


# ── Helpers ─────────────────────────────────────────────

def _plan_to_dict(plan: MaintenancePlan, db: Session) -> dict:
    eq = db.query(Equipment).filter(Equipment.id == plan.equipment_id).first()
    return {
        "id": plan.id,
        "equipment_id": plan.equipment_id,
        "vessel_id": plan.vessel_id,
        "title": plan.title,
        "description": plan.description,
        "interval_type": plan.interval_type,
        "interval_value": plan.interval_value,
        "interval_unit": plan.interval_unit,
        "priority": plan.priority,
        "is_class_related": plan.is_class_related,
        "estimated_hours": plan.estimated_hours,
        "last_done_date": plan.last_done_date.isoformat() if plan.last_done_date else None,
        "next_due_date": plan.next_due_date.isoformat() if plan.next_due_date else None,
        "next_due_hours": plan.next_due_hours,
        "equipment_name": eq.name if eq else None,
        "equipment_code": eq.equipment_code if eq else None,
        "is_active": plan.is_active,
    }


def _wo_to_dict(wo: WorkOrder, db: Session) -> dict:
    eq = db.query(Equipment).filter(Equipment.id == wo.equipment_id).first()
    return {
        "id": wo.id,
        "maintenance_plan_id": wo.maintenance_plan_id,
        "equipment_id": wo.equipment_id,
        "vessel_id": wo.vessel_id,
        "title": wo.title,
        "description": wo.description,
        "status": wo.status,
        "priority": wo.priority,
        "planned_date": wo.planned_date.isoformat() if wo.planned_date else None,
        "due_date": wo.due_date.isoformat() if wo.due_date else None,
        "started_date": wo.started_date.isoformat() if wo.started_date else None,
        "completed_date": wo.completed_date.isoformat() if wo.completed_date else None,
        "assigned_to": wo.assigned_to,
        "actual_hours": wo.actual_hours,
        "remarks": wo.remarks,
        "is_class_related": wo.is_class_related,
        "equipment_name": eq.name if eq else None,
        "equipment_code": eq.equipment_code if eq else None,
        "created_at": wo.created_at.isoformat() if wo.created_at else None,
    }
