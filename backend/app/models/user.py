"""사용자 모델 - 회원가입/로그인 + 네임카드 + 역할 시스템"""
import enum
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import uuid


class UserRole(str, enum.Enum):
    """사용자 역할"""
    DEVELOPER = "developer"            # 개발자 (최상위 권한)
    ADMIN = "admin"                    # 시스템 관리자 (YJT)
    CAPTAIN = "captain"                # 선장
    CHIEF_ENGINEER = "chief_engineer"  # 기관장
    SHORE_MANAGER = "shore_manager"    # 육상관리자 (해운사)
    ENGINEER = "engineer"              # 정비 엔지니어
    CUSTOMER = "customer"              # 일반 고객


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    company = Column(String, default="")
    country = Column(String, default="")
    phone = Column(String, default="")
    preferred_language = Column(String, default="en")  # en, ko, zh, ja, ar, es, hi
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # 역할 시스템 (Phase 3)
    role = Column(String, default="customer")  # UserRole enum 값
    vessel_id = Column(String, ForeignKey("vessels.id"), nullable=True)  # 배정 선박

    # 네임카드 (이메일 서명) 필드
    namecard_title = Column(String, default="")        # 직책 (e.g. "Sales Manager")
    namecard_department = Column(String, default="")    # 부서 (e.g. "Sales Department")
    namecard_mobile = Column(String, default="")        # 모바일 (e.g. "+82-10-1234-5678")
    namecard_fax = Column(String, default="")           # 팩스
    namecard_address = Column(String, default="")       # 주소
    namecard_website = Column(String, default="")       # 웹사이트
    namecard_custom_html = Column(Text, default="")     # 커스텀 HTML 서명 (고급)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
