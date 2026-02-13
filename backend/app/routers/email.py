"""이메일 발송 API - 고객에게 직접 이메일 발송 (관리자 전용)"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth_service import get_admin_user
from app.services.email_service import send_email

router = APIRouter()


class SendEmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str              # 본문 텍스트 (HTML로 변환)
    cc_email: str = ""     # 참조


@router.post("/send")
def send_email_endpoint(
    data: SendEmailRequest,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """고객에게 이메일 발송 (관리자 전용, 네임카드 서명 자동 삽입)"""
    # 본문 텍스트를 HTML로 변환 (줄바꿈 유지)
    body_html = f'<div style="font-size:14px; color:#1e293b; white-space:pre-wrap;">{data.body}</div>'

    result = send_email(
        to_email=data.to_email,
        subject=data.subject,
        body_html=body_html,
        sender_user=admin,
    )

    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])

    return result
