"""분석 라우터 - 차트/리포트 데이터 API"""
from collections import defaultdict
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func
from app.database import get_db
from app.models.part import Part
from app.models.inventory import Inventory
from app.models.service_order import ServiceOrder
from app.models.user import User
from app.models.vessel import Vessel
from app.models.equipment import Equipment
from app.models.work_order import WorkOrder
from app.models.maintenance_plan import MaintenancePlan
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("/inventory-by-brand")
def inventory_by_brand(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """브랜드별 재고 수량"""
    results = (
        db.query(Part.brand, sql_func.sum(Inventory.quantity).label("total"))
        .join(Inventory, Part.id == Inventory.part_id)
        .group_by(Part.brand)
        .order_by(sql_func.sum(Inventory.quantity).desc())
        .all()
    )
    return [{"brand": r[0], "quantity": r[1] or 0} for r in results]


@router.get("/order-status-distribution")
def order_status_distribution(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """주문 상태 분포"""
    results = (
        db.query(ServiceOrder.status, sql_func.count().label("count"))
        .group_by(ServiceOrder.status)
        .all()
    )
    return [{"status": r[0], "count": r[1]} for r in results]


@router.get("/monthly-orders")
def monthly_orders(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """월별 주문 추이 (최근 6개월) - DB 호환 (SQLite + PostgreSQL)"""
    orders = db.query(ServiceOrder.created_at).all()
    monthly: dict[str, int] = defaultdict(int)
    for (created_at,) in orders:
        if created_at:
            key = created_at.strftime("%Y-%m")
            monthly[key] += 1
    data = [{"month": k, "count": v} for k, v in sorted(monthly.items(), reverse=True)[:6]]
    data.reverse()
    return data


@router.get("/inventory-value-by-brand")
def inventory_value_by_brand(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """브랜드별 재고 가치"""
    results = (
        db.query(
            Part.brand,
            sql_func.sum(Part.unit_price * Inventory.quantity).label("value"),
        )
        .join(Inventory, Part.id == Inventory.part_id)
        .group_by(Part.brand)
        .order_by(sql_func.sum(Part.unit_price * Inventory.quantity).desc())
        .all()
    )
    return [{"brand": r[0], "value": round(r[1] or 0, 2)} for r in results]


@router.get("/low-stock-summary")
def low_stock_summary(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """저재고 요약"""
    results = (
        db.query(Part, Inventory)
        .join(Inventory, Part.id == Inventory.part_id)
        .filter(Inventory.quantity <= Inventory.min_quantity)
        .all()
    )
    return [
        {
            "part_number": p.part_number,
            "name": p.name,
            "brand": p.brand,
            "quantity": inv.quantity,
            "min_quantity": inv.min_quantity,
        }
        for p, inv in results
    ]


# ── PMS Analytics (Phase 3 Batch 5) ─────────────────────────

@router.get("/pms-completion-rate")
def pms_completion_rate(
    vessel_id: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """선박별 PMS 완료율"""
    query = db.query(Vessel)
    if vessel_id:
        query = query.filter(Vessel.id == vessel_id)
    vessels = query.all()

    results = []
    for v in vessels:
        total = db.query(WorkOrder).filter(WorkOrder.vessel_id == v.id).count()
        completed = db.query(WorkOrder).filter(
            WorkOrder.vessel_id == v.id, WorkOrder.status == "Completed"
        ).count()
        rate = round((completed / total * 100), 1) if total > 0 else 0
        results.append({
            "vessel_id": v.id,
            "vessel_name": v.name,
            "total": total,
            "completed": completed,
            "completion_rate": rate,
        })
    return results


@router.get("/work-order-distribution")
def work_order_distribution(
    vessel_id: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """작업지시서 상태 분포"""
    query = db.query(WorkOrder.status, sql_func.count().label("count"))
    if vessel_id:
        query = query.filter(WorkOrder.vessel_id == vessel_id)
    results = query.group_by(WorkOrder.status).all()
    return [{"status": r[0], "count": r[1]} for r in results]


@router.get("/equipment-reliability")
def equipment_reliability(
    vessel_id: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """장비 신뢰도 (정비 완료율 기반)"""
    eq_query = db.query(Equipment)
    if vessel_id:
        eq_query = eq_query.filter(Equipment.vessel_id == vessel_id)
    equipment_list = eq_query.filter(Equipment.is_active == True).all()

    results = []
    for eq in equipment_list:
        total_wo = db.query(WorkOrder).filter(WorkOrder.equipment_id == eq.id).count()
        completed_wo = db.query(WorkOrder).filter(
            WorkOrder.equipment_id == eq.id, WorkOrder.status == "Completed"
        ).count()
        overdue_wo = db.query(WorkOrder).filter(
            WorkOrder.equipment_id == eq.id,
            WorkOrder.status.in_(["Planned", "InProgress"]),
            WorkOrder.due_date < datetime.utcnow(),
        ).count()

        if total_wo > 0:
            results.append({
                "equipment_id": eq.id,
                "equipment_name": eq.name,
                "equipment_code": eq.equipment_code,
                "category": eq.category,
                "total_wo": total_wo,
                "completed_wo": completed_wo,
                "overdue_wo": overdue_wo,
                "reliability": round(completed_wo / total_wo * 100, 1),
            })
    return sorted(results, key=lambda x: x["reliability"])


@router.get("/vessel-summary")
def vessel_summary_analytics(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """전체 선박 요약"""
    vessels = db.query(Vessel).filter(Vessel.is_active == True).all()
    now = datetime.utcnow()
    results = []
    for v in vessels:
        eq_count = db.query(Equipment).filter(Equipment.vessel_id == v.id, Equipment.is_active == True).count()
        total_wo = db.query(WorkOrder).filter(WorkOrder.vessel_id == v.id).count()
        overdue_wo = db.query(WorkOrder).filter(
            WorkOrder.vessel_id == v.id,
            WorkOrder.status.in_(["Planned", "InProgress"]),
            WorkOrder.due_date < now,
        ).count()
        completed_wo = db.query(WorkOrder).filter(
            WorkOrder.vessel_id == v.id, WorkOrder.status == "Completed"
        ).count()

        results.append({
            "vessel_id": v.id,
            "vessel_name": v.name,
            "vessel_type": v.vessel_type,
            "equipment_count": eq_count,
            "total_work_orders": total_wo,
            "overdue_work_orders": overdue_wo,
            "completed_work_orders": completed_wo,
            "completion_rate": round(completed_wo / total_wo * 100, 1) if total_wo > 0 else 0,
        })
    return results
