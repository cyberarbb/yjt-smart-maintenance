import logging
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chatbot_service import chat_with_ai

logger = logging.getLogger(__name__)
router = APIRouter()


class ChatMessage(BaseModel):
    message: str
    history: list[dict] = []
    language: str = "ko"  # 사용자 선택 언어


class ChatResponse(BaseModel):
    response: str
    source: str = "ai"


@router.post("", response_model=ChatResponse)
def chat(data: ChatMessage, db: Session = Depends(get_db)):
    try:
        response = chat_with_ai(data.message, data.history, db, data.language)
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Chatbot error: {e}", exc_info=True)
        return ChatResponse(response=f"⚠️ 오류가 발생했습니다: {str(e)}", source="error")
