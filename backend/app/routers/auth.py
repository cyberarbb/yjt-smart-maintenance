"""인증 라우터 - 회원가입/로그인/프로필/사용자관리 + 역할 + 비밀번호 찾기"""
import random
import time
import logging
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.vessel import Vessel
from app.schemas.user import (
    UserRegister, UserLogin, UserResponse, UserUpdate, TokenResponse,
    UserRoleUpdate, UserVesselUpdate, AdminToggleRequest,
)
from app.services.auth_service import (
    hash_password, verify_password, create_access_token, get_current_user, get_admin_user, get_developer_user
)
from app.services.activity_log_service import record_activity
from app.services.email_service import send_password_reset_email

logger = logging.getLogger(__name__)

router = APIRouter()

# ── 비밀번호 리셋 코드 저장소 (인메모리) ──
_reset_codes: dict[str, dict] = {}  # {email: {"code": "123456", "expires_at": float}}


class ForgotPasswordRequest(BaseModel):
    email: str
    language: str = "en"


class ResetPasswordRequest(BaseModel):
    email: str
    code: str
    new_password: str


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """회원가입"""
    try:
        # 이메일 중복 체크
        if db.query(User).filter(User.email == data.email).first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        # 비밀번호 최소 길이
        if len(data.password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters",
            )

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            company=data.company,
            country=data.country,
            phone=data.phone,
            preferred_language=data.preferred_language,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = create_access_token(user.id)
        return TokenResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Register failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, request: Request, db: Session = Depends(get_db)):
    """로그인"""
    try:
        ip_address = request.client.host if request.client else ""
        user_agent = request.headers.get("user-agent", "")

        user = db.query(User).filter(User.email == data.email).first()
        if not user or not verify_password(data.password, user.hashed_password):
            # 로그인 실패 기록
            try:
                record_activity(
                    db, user_id=user.id if user else "unknown",
                    user_email=data.email, user_name=user.full_name if user else "Unknown",
                    action="login_failed", ip_address=ip_address, user_agent=user_agent,
                    details="Invalid email or password",
                )
            except Exception:
                pass  # activity log 실패해도 로그인 로직은 계속
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated",
            )

        # 로그인 성공 기록
        try:
            record_activity(
                db, user_id=user.id, user_email=user.email, user_name=user.full_name,
                action="login", ip_address=ip_address, user_agent=user_agent,
            )
        except Exception:
            pass  # activity log 실패해도 로그인은 계속

        token = create_access_token(user.id)
        return TokenResponse(
            access_token=token,
            user=UserResponse.model_validate(user),
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Login failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/logout")
def logout(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """로그아웃 (활동 기록용)"""
    ip_address = request.client.host if request.client else ""
    user_agent = request.headers.get("user-agent", "")
    record_activity(
        db, user_id=user.id, user_email=user.email, user_name=user.full_name,
        action="logout", ip_address=ip_address, user_agent=user_agent,
    )
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    """현재 로그인한 사용자 정보"""
    return UserResponse.model_validate(user)


@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """프로필 업데이트"""
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.company is not None:
        user.company = data.company
    if data.country is not None:
        user.country = data.country
    if data.phone is not None:
        user.phone = data.phone
    if data.preferred_language is not None:
        user.preferred_language = data.preferred_language

    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """비밀번호 변경 (로그인한 사용자 본인)"""
    # 현재 비밀번호 확인
    if not verify_password(data.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # 새 비밀번호 검증
    if len(data.new_password) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters")

    if data.current_password == data.new_password:
        raise HTTPException(status_code=400, detail="New password must be different from current password")

    user.hashed_password = hash_password(data.new_password)
    db.commit()

    # Activity Log
    ip_address = request.client.host if request.client else ""
    user_agent = request.headers.get("user-agent", "")
    record_activity(
        db, user_id=user.id, user_email=user.email, user_name=user.full_name,
        action="password_changed", ip_address=ip_address, user_agent=user_agent,
        details="Password changed by user",
    )

    return {"message": "Password changed successfully"}


# ── 사용자 관리 (관리자 전용) ──

@router.get("/users", response_model=list[UserResponse])
def list_users(
    admin: User = Depends(get_developer_user),
    db: Session = Depends(get_db),
):
    """관리자: 전체 사용자 목록"""
    return [UserResponse.model_validate(u) for u in db.query(User).order_by(User.created_at.desc()).all()]


@router.put("/users/{user_id}/toggle-admin", response_model=UserResponse)
def toggle_admin(
    user_id: str,
    data: AdminToggleRequest,
    admin: User = Depends(get_developer_user),
    db: Session = Depends(get_db),
):
    """관리자: 사용자 관리자 권한 토글 (비밀번호 확인 필수)"""
    # 관리자 비밀번호 확인
    if not verify_password(data.admin_password, admin.hashed_password):
        raise HTTPException(status_code=403, detail="Admin password is incorrect")

    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    if target.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot change own admin status")
    # developer는 admin 토글 대상이 아님
    if target.role == "developer":
        raise HTTPException(status_code=400, detail="Cannot change developer's admin status")
    target.is_admin = not target.is_admin
    # is_admin과 role 동기화
    if target.is_admin:
        target.role = "admin"
    else:
        # admin 해제 시 role도 customer로 변경
        if target.role == "admin":
            target.role = "customer"
    db.commit()
    db.refresh(target)
    return UserResponse.model_validate(target)


@router.put("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: str,
    data: UserRoleUpdate,
    admin: User = Depends(get_developer_user),
    db: Session = Depends(get_db),
):
    """관리자: 사용자 역할 변경 (admin/developer 역할 부여 시 비밀번호 확인 필수)"""
    # 유효한 역할 체크
    valid_roles = {r.value for r in UserRole}
    if data.role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"Invalid role. Valid: {', '.join(valid_roles)}")

    # developer 역할은 developer만 부여 가능
    if data.role == "developer":
        if getattr(admin, "role", None) != "developer":
            raise HTTPException(status_code=403, detail="Only developer can grant developer role")
        if not data.admin_password:
            raise HTTPException(status_code=400, detail="Password required to grant developer role")
        if not verify_password(data.admin_password, admin.hashed_password):
            raise HTTPException(status_code=403, detail="Password is incorrect")

    # admin 역할로 변경 시 비밀번호 확인 필수
    elif data.role == "admin":
        if not data.admin_password:
            raise HTTPException(status_code=400, detail="Admin password required to grant admin role")
        if not verify_password(data.admin_password, admin.hashed_password):
            raise HTTPException(status_code=403, detail="Admin password is incorrect")

    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    # developer의 역할은 다른 developer만 변경 가능
    if target.role == "developer" and getattr(admin, "role", None) != "developer":
        raise HTTPException(status_code=403, detail="Only developer can change developer's role")

    target.role = data.role
    # admin/developer 역할이면 is_admin도 동기화
    if data.role in ("admin", "developer"):
        target.is_admin = True
    else:
        # admin에서 다른 역할로 변경 시 is_admin도 해제
        if target.is_admin and target.id != admin.id:
            target.is_admin = False
    db.commit()
    db.refresh(target)
    return UserResponse.model_validate(target)


@router.put("/users/{user_id}/vessel", response_model=UserResponse)
def update_user_vessel(
    user_id: str,
    data: UserVesselUpdate,
    admin: User = Depends(get_developer_user),
    db: Session = Depends(get_db),
):
    """관리자: 사용자 선박 배정"""
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    if data.vessel_id:
        vessel = db.query(Vessel).filter(Vessel.id == data.vessel_id).first()
        if not vessel:
            raise HTTPException(status_code=404, detail="Vessel not found")

    target.vessel_id = data.vessel_id
    db.commit()
    db.refresh(target)
    return UserResponse.model_validate(target)


@router.get("/roles")
def get_available_roles(user: User = Depends(get_current_user)):
    """사용 가능한 역할 목록 (developer 역할은 developer만 볼 수 있음)"""
    roles = []
    # developer 역할은 developer만 볼 수 있음
    if getattr(user, "role", None) == "developer":
        roles.append({"value": "developer", "label": "Developer", "description": "Developer (개발자 - 최상위 권한)"})
    roles.extend([
        {"value": "admin", "label": "Admin", "description": "System Administrator (YJT)"},
        {"value": "captain", "label": "Captain", "description": "Ship Captain (선장)"},
        {"value": "chief_engineer", "label": "Chief Engineer", "description": "Chief Engineer (기관장)"},
        {"value": "shore_manager", "label": "Shore Manager", "description": "Shore Manager (육상관리자)"},
        {"value": "engineer", "label": "Engineer", "description": "Maintenance Engineer (정비 엔지니어)"},
        {"value": "customer", "label": "Customer", "description": "General Customer (고객)"},
    ])
    return roles


# ── 비밀번호 찾기 / 리셋 ──

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """비밀번호 찾기 - 이메일로 6자리 인증 코드 발송"""
    # 만료된 코드 정리
    now = time.time()
    expired = [k for k, v in _reset_codes.items() if v["expires_at"] < now]
    for k in expired:
        del _reset_codes[k]

    email = data.email.strip().lower()
    user = db.query(User).filter(User.email == email).first()

    # 보안: 이메일 존재 여부와 관계없이 동일 응답
    if user:
        code = f"{random.randint(0, 999999):06d}"
        _reset_codes[email] = {
            "code": code,
            "expires_at": now + 600,  # 10분 만료
        }
        # 이메일 발송
        lang = getattr(user, "preferred_language", data.language) or data.language
        result = send_password_reset_email(email, code, lang)
        print(f"[AUTH] Password reset code for {email}: {code}")
        logger.info(f"[AUTH] Password reset code sent to {email}: {code}")

    return {"message": "If the email exists, a verification code has been sent."}


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, request: Request, db: Session = Depends(get_db)):
    """비밀번호 리셋 - 인증 코드 검증 후 비밀번호 변경"""
    email = data.email.strip().lower()
    code_data = _reset_codes.get(email)

    # 코드 검증
    if not code_data:
        raise HTTPException(status_code=400, detail="No reset code found. Please request a new code.")
    if time.time() > code_data["expires_at"]:
        del _reset_codes[email]
        raise HTTPException(status_code=400, detail="Code has expired. Please request a new code.")
    if code_data["code"] != data.code.strip():
        raise HTTPException(status_code=400, detail="Invalid verification code.")

    # 비밀번호 검증
    if len(data.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")

    # 사용자 찾기 + 비밀번호 업데이트
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.hashed_password = hash_password(data.new_password)
    db.commit()

    # 코드 삭제 (1회용)
    del _reset_codes[email]

    # Activity Log
    ip_address = request.client.host if request.client else ""
    user_agent = request.headers.get("user-agent", "")
    record_activity(
        db, user_id=user.id, user_email=user.email, user_name=user.full_name,
        action="password_reset", ip_address=ip_address, user_agent=user_agent,
        details="Password reset via email verification code",
    )

    return {"message": "Password has been reset successfully."}
