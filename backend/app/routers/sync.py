"""동기화 라우터 - Google Sheets 데이터 내보내기"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import get_settings
from app.models.user import User
from app.services.auth_service import get_admin_user

router = APIRouter()


@router.post("/sheets")
def sync_to_google_sheets(
    user: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """DB 데이터를 Google Sheets로 동기화 (관리자 전용)"""
    settings = get_settings()

    if not settings.google_sheets_credentials_file or not settings.google_sheets_spreadsheet_id:
        raise HTTPException(
            status_code=400,
            detail="Google Sheets is not configured. Set GOOGLE_SHEETS_CREDENTIALS_FILE and GOOGLE_SHEETS_SPREADSHEET_ID in .env",
        )

    try:
        from app.services.google_sheets_service import sync_all
        result = sync_all(
            db=db,
            credentials_file=settings.google_sheets_credentials_file,
            spreadsheet_id=settings.google_sheets_spreadsheet_id,
        )
        return {"status": "success", **result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")
