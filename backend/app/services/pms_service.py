"""PMS 서비스 - 작업지시서 자동 생성, 초과 감지, 통계"""
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.maintenance_plan import MaintenancePlan
from app.models.work_order import WorkOrder
from app.models.equipment import Equipment
from app.models.vessel import Vessel

# 다이제스트 표시용 한국 표준시 (DB 시각은 UTC로 저장됨)
KST = timezone(timedelta(hours=9))


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


# ── Due Digest (외부 알림 채널용 텍스트 요약) ─────────────

def _fmt_kst(dt: datetime | None, with_time: bool = False) -> str:
    """UTC 저장 시각을 KST 문자열로. 표시 전용."""
    if not dt:
        return "-"
    kst = dt.replace(tzinfo=timezone.utc).astimezone(KST)
    return kst.strftime("%Y-%m-%d %H:%M") if with_time else kst.strftime("%m-%d")


def _name_maps(db: Session, work_orders: list[WorkOrder]) -> tuple[dict, dict]:
    """선박·장비 이름을 한 번에 조회 (N+1 방지)."""
    vessel_ids = {wo.vessel_id for wo in work_orders if wo.vessel_id}
    equipment_ids = {wo.equipment_id for wo in work_orders if wo.equipment_id}

    vessels = (
        db.query(Vessel.id, Vessel.name).filter(Vessel.id.in_(vessel_ids)).all()
        if vessel_ids else []
    )
    equipment = (
        db.query(Equipment.id, Equipment.equipment_code, Equipment.name)
        .filter(Equipment.id.in_(equipment_ids))
        .all()
        if equipment_ids else []
    )
    return (
        {v_id: v_name for v_id, v_name in vessels},
        {e_id: f"{e_code} {e_name}" for e_id, e_code, e_name in equipment},
    )


def _digest_line(wo: WorkOrder, vessel_names: dict, equipment_names: dict, now: datetime) -> str:
    vessel = vessel_names.get(wo.vessel_id, "미지정 선박")
    equipment = equipment_names.get(wo.equipment_id, "미지정 장비")
    flag = " [선급]" if wo.is_class_related else ""

    if wo.due_date and wo.due_date < now:
        overdue_days = (now - wo.due_date).days
        when = f"{overdue_days}일 초과 (기한 {_fmt_kst(wo.due_date)})"
    else:
        when = f"예정 {_fmt_kst(wo.planned_date)} / 기한 {_fmt_kst(wo.due_date)}"

    return f"· [{vessel}] {equipment} — {wo.title} / {when}{flag}"


def build_due_digest(
    db: Session,
    vessel_id: str | None = None,
    days: int = 7,
    limit: int = 10,
) -> str:
    """정비 만기 다이제스트를 사람이 읽는 텍스트로 만든다.

    Buzz 워크플로(daily-pms-digest)가 이 문자열을 그대로 채널에 게시하므로,
    JSON 이 아니라 줄바꿈이 있는 평문을 반환한다. `limit` 은 각 섹션에
    나열할 최대 건수이며, 넘치면 "외 N건" 으로 접는다.
    """
    now = datetime.utcnow()
    overdue = get_overdue_work_orders(db, vessel_id)
    upcoming = get_upcoming_work_orders(db, vessel_id, days)
    stats = get_pms_stats(db, vessel_id)

    vessel_names, equipment_names = _name_maps(db, overdue + upcoming)

    lines: list[str] = [f"기준 시각: {_fmt_kst(now, with_time=True)} (KST)"]

    lines.append("")
    if overdue:
        lines.append(f"■ 기한 초과 {len(overdue)}건")
        for wo in overdue[:limit]:
            lines.append(_digest_line(wo, vessel_names, equipment_names, now))
        if len(overdue) > limit:
            lines.append(f"  외 {len(overdue) - limit}건")
    else:
        lines.append("■ 기한 초과 없음")

    lines.append("")
    if upcoming:
        lines.append(f"■ 향후 {days}일 예정 {len(upcoming)}건")
        for wo in upcoming[:limit]:
            lines.append(_digest_line(wo, vessel_names, equipment_names, now))
        if len(upcoming) > limit:
            lines.append(f"  외 {len(upcoming) - limit}건")
    else:
        lines.append(f"■ 향후 {days}일 예정 없음")

    lines.append("")
    lines.append(
        f"■ 현황: 총 {stats['total']}건 / 완료 {stats['completed']}건 "
        f"({stats['completion_rate']}%) / 진행 {stats['in_progress']}건 / 초과 {stats['overdue']}건"
    )

    return "\n".join(lines)
