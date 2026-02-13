"""운전시간(Running Hours) 라우터"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.equipment import Equipment
from app.models.running_hours import RunningHours
from app.schemas.running_hours import (
    RunningHoursRecord,
    RunningHoursBulkRecord,
    RunningHoursResponse,
    RunningHoursLatest,
    RunningHoursChartData,
)
from app.services.auth_service import get_current_user, get_engineer_or_above
from app.services.running_hours_service import (
    record_daily_hours,
    get_equipment_history,
    get_chart_data,
    get_latest_hours,
)

router = APIRouter()


@router.post("/record", response_model=RunningHoursResponse)
def record_hours(
    data: RunningHoursRecord,
    user: User = Depends(get_engineer_or_above),
    db: Session = Depends(get_db),
):
    """단건 운전시간 기록"""
    if data.daily_hours < 0 or data.daily_hours > 24:
        raise HTTPException(status_code=400, detail="Daily hours must be between 0 and 24")

    try:
        record = record_daily_hours(
            db=db,
            equipment_id=data.equipment_id,
            recorded_date=data.recorded_date,
            daily_hours=data.daily_hours,
            user_id=user.id,
            note=data.note,
        )
        db.commit()
        db.refresh(record)

        # equipment 정보 추가
        eq = db.query(Equipment).filter(Equipment.id == record.equipment_id).first()
        result = {
            "id": record.id,
            "equipment_id": record.equipment_id,
            "recorded_date": record.recorded_date,
            "daily_hours": record.daily_hours,
            "total_hours": record.total_hours,
            "recorded_by": record.recorded_by,
            "note": record.note,
            "created_at": record.created_at,
            "equipment_name": eq.name if eq else None,
            "equipment_code": eq.equipment_code if eq else None,
        }
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/record/bulk")
def record_hours_bulk(
    data: RunningHoursBulkRecord,
    user: User = Depends(get_engineer_or_above),
    db: Session = Depends(get_db),
):
    """벌크 운전시간 기록 (여러 장비 한번에)"""
    results = []
    errors = []

    for rec in data.records:
        if rec.daily_hours < 0 or rec.daily_hours > 24:
            errors.append(f"{rec.equipment_id}: hours must be 0-24")
            continue
        try:
            record = record_daily_hours(
                db=db,
                equipment_id=rec.equipment_id,
                recorded_date=data.recorded_date,
                daily_hours=rec.daily_hours,
                user_id=user.id,
                note=rec.note,
            )
            results.append(rec.equipment_id)
        except Exception as e:
            errors.append(f"{rec.equipment_id}: {str(e)}")

    db.commit()
    return {
        "recorded": len(results),
        "errors": errors,
        "date": data.recorded_date.isoformat(),
    }


@router.get("/vessel/{vessel_id}/latest", response_model=list[RunningHoursLatest])
def get_vessel_latest_hours(
    vessel_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """선박 장비별 최신 운전시간"""
    return get_latest_hours(db, vessel_id)


@router.get("/equipment/{equipment_id}/history")
def get_hours_history(
    equipment_id: str,
    days: int = 30,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """장비 운전시간 히스토리"""
    records = get_equipment_history(db, equipment_id, days)
    eq = db.query(Equipment).filter(Equipment.id == equipment_id).first()

    return [
        {
            "id": r.id,
            "equipment_id": r.equipment_id,
            "recorded_date": r.recorded_date.isoformat(),
            "daily_hours": r.daily_hours,
            "total_hours": r.total_hours,
            "note": r.note,
            "equipment_name": eq.name if eq else None,
            "equipment_code": eq.equipment_code if eq else None,
        }
        for r in records
    ]


@router.get("/equipment/{equipment_id}/chart", response_model=list[RunningHoursChartData])
def get_hours_chart(
    equipment_id: str,
    days: int = 30,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """차트용 운전시간 데이터"""
    return get_chart_data(db, equipment_id, days)
