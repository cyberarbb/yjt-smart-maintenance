from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.chatbot_service import chat_with_ai

router = APIRouter()


class ChatMessage(BaseModel):
    message: str
    history: list[dict] = []
    language: str = "ko"  # 사용자 선택 언어


class ChatResponse(BaseModel):
    response: str
    source: str = "ai"


@router.post("/", response_model=ChatResponse)
def chat(data: ChatMessage, db: Session = Depends(get_db)):
    response = chat_with_ai(data.message, data.history, db, data.language)
    return ChatResponse(response=response)
