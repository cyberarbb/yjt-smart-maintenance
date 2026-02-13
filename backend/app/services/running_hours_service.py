"""운전시간 서비스 - 누적 계산, 차트 데이터, 정비 트리거 체크"""
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.models.running_hours import RunningHours
from app.models.equipment import Equipment


def record_daily_hours(
    db: Session,
    equipment_id: str,
    recorded_date: date,
    daily_hours: float,
    user_id: str | None = None,
    note: str | None = None,
) -> RunningHours:
    """일일 운전시간 기록 및 누적 계산"""
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise ValueError("Equipment not found")

    # 직전 기록에서 누적 시간 가져오기
    prev = (
        db.query(RunningHours)
        .filter(
            RunningHours.equipment_id == equipment_id,
            RunningHours.recorded_date < recorded_date,
        )
        .order_by(desc(RunningHours.recorded_date))
        .first()
    )
    prev_total = prev.total_hours if prev else equipment.current_running_hours

    new_total = prev_total + daily_hours

    # 기존 기록이 있으면 업데이트
    existing = (
        db.query(RunningHours)
        .filter(
            RunningHours.equipment_id == equipment_id,
            RunningHours.recorded_date == recorded_date,
        )
        .first()
    )

    if existing:
        old_daily = existing.daily_hours
        existing.daily_hours = daily_hours
        existing.total_hours = new_total
        existing.recorded_by = user_id
        existing.note = note
        record = existing
    else:
        record = RunningHours(
            equipment_id=equipment_id,
            recorded_date=recorded_date,
            daily_hours=daily_hours,
            total_hours=new_total,
            recorded_by=user_id,
            note=note,
        )
        db.add(record)

    # Equipment의 current_running_hours 업데이트
    equipment.current_running_hours = new_total

    # 상태 자동 업데이트 (오버홀 기준)
    if equipment.overhaul_interval_hours:
        ratio = new_total / equipment.overhaul_interval_hours
        if ratio >= 1.0:
            equipment.status = "Critical"
        elif ratio >= 0.85:
            equipment.status = "Warning"
        else:
            equipment.status = "Normal"

    return record


def get_equipment_history(
    db: Session,
    equipment_id: str,
    days: int = 30,
) -> list[RunningHours]:
    """장비 운전시간 히스토리"""
    cutoff = date.today() - timedelta(days=days)
    return (
        db.query(RunningHours)
        .filter(
            RunningHours.equipment_id == equipment_id,
            RunningHours.recorded_date >= cutoff,
        )
        .order_by(RunningHours.recorded_date)
        .all()
    )


def get_chart_data(
    db: Session,
    equipment_id: str,
    days: int = 30,
) -> list[dict]:
    """차트용 데이터"""
    records = get_equipment_history(db, equipment_id, days)
    return [
        {
            "date": r.recorded_date.isoformat(),
            "hours": r.daily_hours,
            "total": r.total_hours,
        }
        for r in records
    ]


def get_latest_hours(
    db: Session,
    vessel_id: str,
) -> list[dict]:
    """선박 장비별 최신 운전시간"""
    equipment_list = (
        db.query(Equipment)
        .filter(Equipment.vessel_id == vessel_id, Equipment.is_active == True)
        .order_by(Equipment.sort_order, Equipment.name)
        .all()
    )

    results = []
    for eq in equipment_list:
        latest = (
            db.query(RunningHours)
            .filter(RunningHours.equipment_id == eq.id)
            .order_by(desc(RunningHours.recorded_date))
            .first()
        )

        results.append({
            "equipment_id": eq.id,
            "equipment_code": eq.equipment_code,
            "equipment_name": eq.name,
            "category": eq.category,
            "current_hours": eq.current_running_hours,
            "overhaul_interval": eq.overhaul_interval_hours,
            "last_recorded_date": latest.recorded_date if latest else None,
            "daily_hours": latest.daily_hours if latest else 0.0,
        })

    return results
