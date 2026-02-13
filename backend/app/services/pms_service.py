"""PMS 서비스 - 작업지시서 자동 생성, 초과 감지, 통계"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.maintenance_plan import MaintenancePlan
from app.models.work_order import WorkOrder
from app.models.equipment import Equipment


def get_overdue_work_orders(db: Session, vessel_id: str | None = None) -> list[WorkOrder]:
    """초과(Overdue) 작업지시서 목록"""
    query = db.query(WorkOrder).filter(
        WorkOrder.status.in_(["Planned", "InProgress"]),
        WorkOrder.due_date < datetime.utcnow(),
    )
    if vessel_id:
        query = query.filter(WorkOrder.vessel_id == vessel_id)
    return query.order_by(WorkOrder.due_date).all()


def get_upcoming_work_orders(db: Session, vessel_id: str | None = None, days: int = 30) -> list[WorkOrder]:
    """예정 작업지시서 (향후 N일)"""
    cutoff = datetime.utcnow() + timedelta(days=days)
    query = db.query(WorkOrder).filter(
        WorkOrder.status == "Planned",
        WorkOrder.planned_date <= cutoff,
        WorkOrder.planned_date >= datetime.utcnow(),
    )
    if vessel_id:
        query = query.filter(WorkOrder.vessel_id == vessel_id)
    return query.order_by(WorkOrder.planned_date).all()


def get_pms_stats(db: Session, vessel_id: str | None = None) -> dict:
    """PMS 통계"""
    base = db.query(WorkOrder)
    if vessel_id:
        base = base.filter(WorkOrder.vessel_id == vessel_id)

    total = base.count()
    completed = base.filter(WorkOrder.status == "Completed").count()
    overdue = base.filter(
        WorkOrder.status.in_(["Planned", "InProgress"]),
        WorkOrder.due_date < datetime.utcnow(),
    ).count()
    in_progress = base.filter(WorkOrder.status == "InProgress").count()
    planned = base.filter(WorkOrder.status == "Planned").count()

    completion_rate = round((completed / total * 100), 1) if total > 0 else 0

    return {
        "total": total,
        "completed": completed,
        "overdue": overdue,
        "in_progress": in_progress,
        "planned": planned,
        "completion_rate": completion_rate,
    }


def get_calendar_data(db: Session, vessel_id: str, year: int, month: int) -> list[dict]:
    """캘린더용 월별 작업지시서 데이터"""
    from calendar import monthrange
    _, last_day = monthrange(year, month)
    start = datetime(year, month, 1)
    end = datetime(year, month, last_day, 23, 59, 59)

    work_orders = (
        db.query(WorkOrder)
        .filter(
            WorkOrder.vessel_id == vessel_id,
            WorkOrder.planned_date >= start,
            WorkOrder.planned_date <= end,
        )
        .order_by(WorkOrder.planned_date)
        .all()
    )

    results = []
    for wo in work_orders:
        is_overdue = wo.status in ("Planned", "InProgress") and wo.due_date and wo.due_date < datetime.utcnow()
        results.append({
            "id": wo.id,
            "title": wo.title,
            "date": wo.planned_date.strftime("%Y-%m-%d") if wo.planned_date else None,
            "status": "Overdue" if is_overdue else wo.status,
            "priority": wo.priority,
            "is_class_related": wo.is_class_related,
            "equipment_id": wo.equipment_id,
        })

    return results
