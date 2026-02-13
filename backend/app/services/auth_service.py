"""인증 서비스 - JWT + Password Hashing + 역할 기반 접근 제어"""
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.config import get_settings

settings = get_settings()

# ── JWT 설정 ──
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24 * 7  # 7일

# ── Bearer 토큰 인증 ──
security = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """bcrypt로 비밀번호 해싱"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """bcrypt로 비밀번호 검증"""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str | None:
    """토큰에서 user_id 추출. 실패 시 None 반환."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """현재 인증된 사용자를 반환하는 의존성"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    user_id = decode_token(credentials.credentials)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or deactivated",
        )

    return user


def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User | None:
    """선택적 인증 - 로그인하지 않아도 접근 가능한 엔드포인트용"""
    if not credentials:
        return None
    user_id = decode_token(credentials.credentials)
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id, User.is_active == True).first()


def get_admin_user(
    user: User = Depends(get_current_user),
) -> User:
    """관리자 전용 의존성 - is_admin=True 또는 developer 역할"""
    if not user.is_admin and getattr(user, "role", None) != "developer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return user


def get_developer_user(
    user: User = Depends(get_current_user),
) -> User:
    """개발자 전용 의존성 - role=developer 필수"""
    if getattr(user, "role", None) != "developer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Developer privileges required",
        )
    return user


# ── 역할 기반 의존성 (Phase 3) ──────────────────────────

def _get_user_role(user: User) -> str:
    """사용자의 역할 반환 (하위 호환성)"""
    role = getattr(user, "role", None)
    if not role:
        return "admin" if user.is_admin else "customer"
    return role


def require_role(*allowed_roles: str):
    """특정 역할만 허용하는 의존성 팩토리

    Usage:
        @router.get("/captain-only")
        def captain_only(user: User = Depends(require_role("admin", "captain"))):
            ...
    """
    def dependency(user: User = Depends(get_current_user)) -> User:
        role = _get_user_role(user)
        # developer와 admin은 항상 허용
        if role in ("developer", "admin") or user.is_admin:
            return user
        if role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{role}' not authorized. Required: {', '.join(allowed_roles)}",
            )
        return user
    return dependency


def get_engineer_or_above(
    user: User = Depends(get_current_user),
) -> User:
    """엔지니어 이상 역할 (engineer, chief_engineer, captain, shore_manager, admin, developer)"""
    allowed = {"developer", "admin", "captain", "chief_engineer", "shore_manager", "engineer"}
    role = _get_user_role(user)
    if role not in allowed and not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Engineer or above role required",
        )
    return user


def get_manager_or_above(
    user: User = Depends(get_current_user),
) -> User:
    """관리자급 이상 역할 (captain, chief_engineer, shore_manager, admin, developer)"""
    allowed = {"developer", "admin", "captain", "chief_engineer", "shore_manager"}
    role = _get_user_role(user)
    if role not in allowed and not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager or above role required",
        )
    return user
