"""Activity Log 서비스 - 로그 기록 및 조회"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.activity_log import ActivityLog


def record_activity(
    db: Session,
    user_id: str,
    user_email: str,
    user_name: str,
    action: str,
    ip_address: str = "",
    user_agent: str = "",
    details: str = "",
):
    """활동 로그 기록"""
    log = ActivityLog(
        user_id=user_id,
        user_email=user_email,
        user_name=user_name,
        action=action,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
    )
    db.add(log)
    db.commit()
    return log


def get_activity_logs(
    db: Session,
    action: str | None = None,
    user_id: str | None = None,
    limit: int = 100,
    offset: int = 0,
):
    """활동 로그 조회 (최신순)"""
    query = db.query(ActivityLog)
    if action:
        query = query.filter(ActivityLog.action == action)
    if user_id:
        query = query.filter(ActivityLog.user_id == user_id)
    total = query.count()
    logs = query.order_by(desc(ActivityLog.created_at)).offset(offset).limit(limit).all()
    return {"total": total, "logs": logs}


def get_online_users(db: Session):
    """현재 온라인 사용자 (마지막 로그인이 로그아웃보다 최신인 사용자)
    서브쿼리로 각 유저의 마지막 login/logout 시간 비교
    """
    from sqlalchemy import func, case, and_
    from sqlalchemy.orm import aliased

    # 각 유저의 마지막 로그인/로그아웃 시간
    subq = (
        db.query(
            ActivityLog.user_id,
            ActivityLog.user_email,
            ActivityLog.user_name,
            func.max(
                case(
                    (ActivityLog.action == "login", ActivityLog.created_at),
                    else_=None,
                )
            ).label("last_login"),
            func.max(
                case(
                    (ActivityLog.action == "logout", ActivityLog.created_at),
                    else_=None,
                )
            ).label("last_logout"),
        )
        .group_by(ActivityLog.user_id, ActivityLog.user_email, ActivityLog.user_name)
        .all()
    )

    online = []
    for row in subq:
        # 로그인 기록이 있고, 로그아웃이 없거나 로그인이 더 최신
        if row.last_login and (row.last_logout is None or row.last_login > row.last_logout):
            online.append({
                "user_id": row.user_id,
                "user_email": row.user_email,
                "user_name": row.user_name,
                "last_login": row.last_login.isoformat() if row.last_login else None,
            })
    return online
