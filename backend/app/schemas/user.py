"""사용자 스키마 - 네임카드 + 역할 시스템 포함"""
from pydantic import BaseModel
from typing import Optional


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str
    company: str = ""
    country: str = ""
    phone: str = ""
    preferred_language: str = "en"


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    company: str
    country: str
    phone: str
    preferred_language: str
    is_active: bool
    is_admin: bool
    # 역할 시스템
    role: str = "customer"
    vessel_id: Optional[str] = None
    # 네임카드 필드
    namecard_title: str = ""
    namecard_department: str = ""
    namecard_mobile: str = ""
    namecard_fax: str = ""
    namecard_address: str = ""
    namecard_website: str = ""
    namecard_custom_html: str = ""

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    company: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    preferred_language: Optional[str] = None
    # 네임카드 필드
    namecard_title: Optional[str] = None
    namecard_department: Optional[str] = None
    namecard_mobile: Optional[str] = None
    namecard_fax: Optional[str] = None
    namecard_address: Optional[str] = None
    namecard_website: Optional[str] = None
    namecard_custom_html: Optional[str] = None


class UserRoleUpdate(BaseModel):
    """관리자용 역할 변경 스키마"""
    role: str  # admin, captain, chief_engineer, shore_manager, engineer, customer
    admin_password: Optional[str] = None  # admin 역할 변경 시 필수


class AdminToggleRequest(BaseModel):
    """관리자 권한 토글 스키마 - 비밀번호 확인 필수"""
    admin_password: str


class UserVesselUpdate(BaseModel):
    """관리자용 선박 배정 스키마"""
    vessel_id: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
