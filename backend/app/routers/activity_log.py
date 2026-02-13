"""Activity Log 라우터 - Developer 전용 접속 로그 조회"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth_service import get_developer_user
from app.services.activity_log_service import get_activity_logs, get_online_users

router = APIRouter()


@router.get("/logs")
def list_activity_logs(
    action: str | None = Query(None, description="Filter by action: login, logout, login_failed"),
    user_id: str | None = Query(None, description="Filter by user_id"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    dev: User = Depends(get_developer_user),
    db: Session = Depends(get_db),
):
    """개발자: 활동 로그 목록 (최신순)"""
    result = get_activity_logs(db, action=action, user_id=user_id, limit=limit, offset=offset)
    logs = result["logs"]
    return {
        "total": result["total"],
        "logs": [
            {
                "id": log.id,
                "user_id": log.user_id,
                "user_email": log.user_email,
                "user_name": log.user_name,
                "action": log.action,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "details": log.details,
                "created_at": log.created_at.isoformat() if log.created_at else None,
            }
            for log in logs
        ],
    }


@router.get("/online")
def list_online_users(
    dev: User = Depends(get_developer_user),
    db: Session = Depends(get_db),
):
    """개발자: 현재 온라인 사용자 목록"""
    return get_online_users(db)
