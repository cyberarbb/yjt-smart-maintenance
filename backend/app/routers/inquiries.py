import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.inquiry import Inquiry
from app.models.user import User
from app.schemas.inquiry import InquiryCreate, InquiryUpdate, InquiryResponse
from app.services.auth_service import get_current_user, get_admin_user
from app.services.notification_service import notify_customer_by_email, notify_admins
from app.services.email_service import send_inquiry_response_email

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("", response_model=list[InquiryResponse])
def get_inquiries(
    skip: int = 0,
    limit: int = 50,
    resolved: bool | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Inquiry)
    if resolved is not None:
        query = query.filter(Inquiry.is_resolved == resolved)
    return query.order_by(Inquiry.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/my-inquiries", response_model=list[InquiryResponse])
def get_my_inquiries(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """고객: 자신의 문의만 조회 (이메일 기반 매칭)"""
    return (
        db.query(Inquiry)
        .filter(Inquiry.contact_email == user.email)
        .order_by(Inquiry.created_at.desc())
        .all()
    )


@router.post("", response_model=InquiryResponse, status_code=201)
def create_inquiry(data: InquiryCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    inquiry = Inquiry(**data.model_dump())
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)

    # 새 문의 시 관리자에게 알림
    notify_admins(
        db,
        title="New Inquiry Received",
        message=f"New inquiry from {inquiry.contact_email}: {inquiry.subject}",
        type="inquiry",
        reference_id=inquiry.id,
        reference_type="inquiry",
    )

    return inquiry


# ── AI 답변 초안 생성 (/{inquiry_id} 보다 먼저 등록!) ──
class DraftRequest(BaseModel):
    inquiry_id: str


class DraftResponse(BaseModel):
    draft: str
    detected_language: str


@router.post("/generate-draft", response_model=DraftResponse)
def generate_inquiry_draft(
    data: DraftRequest,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    """문의 내용의 언어를 감지하고 AI로 답변 초안을 자동 생성"""
    inquiry = db.query(Inquiry).filter(Inquiry.id == data.inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    detected_lang = _detect_language(inquiry.message)
    draft = _generate_ai_draft(inquiry.subject, inquiry.message, detected_lang)

    return DraftResponse(draft=draft, detected_language=detected_lang)


@router.get("/{inquiry_id}", response_model=InquiryResponse)
def get_inquiry(inquiry_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry


class InquiryUpdateWithEmail(BaseModel):
    """문의 답변 업데이트 + 이메일 발송 옵션"""
    is_resolved: bool | None = None
    response: str | None = None
    send_email: bool = False     # True면 고객에게 이메일도 발송


@router.put("/{inquiry_id}", response_model=InquiryResponse)
def update_inquiry(
    inquiry_id: str,
    data: InquiryUpdateWithEmail,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db),
):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    # 업데이트 (send_email 필드 제외)
    update_data = data.model_dump(exclude_unset=True, exclude={"send_email"})
    for key, value in update_data.items():
        setattr(inquiry, key, value)
    db.commit()
    db.refresh(inquiry)

    # 응답 시 인앱 알림
    if inquiry.contact_email:
        notify_customer_by_email(
            db,
            email=inquiry.contact_email,
            title="Inquiry Response Received",
            message=f"Your inquiry '{inquiry.subject}' has received a response.",
            type="inquiry",
            reference_id=inquiry.id,
            reference_type="inquiry",
        )

    # 이메일 발송 옵션
    if data.send_email and inquiry.contact_email and inquiry.response:
        # 문의 언어 감지해서 해당 언어로 이메일 발송
        detected_lang = _detect_language(inquiry.message)
        try:
            email_result = send_inquiry_response_email(
                to_email=inquiry.contact_email,
                subject=inquiry.subject,
                original_message=inquiry.message,
                response_text=inquiry.response,
                sender_user=admin,
                language=detected_lang,
            )
            logger.info(f"[INQUIRY-EMAIL] {email_result}")
        except Exception as e:
            logger.error(f"[INQUIRY-EMAIL] Failed: {e}")

    return inquiry


# ── 언어 감지 ──────────────────────────────────────────
def _detect_language(text: str) -> str:
    """텍스트 언어 자동 감지 (간단한 문자 범위 기반)"""
    if not text:
        return "en"

    # 문자 범위로 언어 감지
    korean_count = sum(1 for c in text if '\uac00' <= c <= '\ud7a3' or '\u3131' <= c <= '\u3163')
    japanese_count = sum(1 for c in text if '\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff')
    chinese_count = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    arabic_count = sum(1 for c in text if '\u0600' <= c <= '\u06ff')
    hindi_count = sum(1 for c in text if '\u0900' <= c <= '\u097f')

    total = len(text)
    if total == 0:
        return "en"

    scores = {
        "ko": korean_count,
        "ja": japanese_count,
        "zh": chinese_count,
        "ar": arabic_count,
        "hi": hindi_count,
    }

    # 스페인어/프랑스어 감지 (특수 문자 기반)
    spanish_markers = ["ñ", "¿", "¡", "á", "é", "ú", "ó"]
    french_markers = ["ç", "œ", "è", "ê", "ë", "î", "ï", "û", "ù", "à", "â"]

    if any(m in text.lower() for m in spanish_markers):
        scores["es"] = 5
    if any(m in text.lower() for m in french_markers):
        scores["fr"] = 5

    best_lang = max(scores, key=scores.get)
    if scores[best_lang] > 0:
        return best_lang

    return "en"


# ── AI 초안 생성 ──────────────────────────────────────
LANGUAGE_NAMES = {
    "ko": "한국어", "en": "English", "zh": "中文",
    "ja": "日本語", "ar": "العربية", "es": "Español",
    "hi": "हिन्दी", "fr": "Français",
}


def _generate_ai_draft(subject: str, message: str, language: str) -> str:
    """Claude API로 문의 답변 초안 생성"""
    from app.config import get_settings
    settings = get_settings()

    lang_name = LANGUAGE_NAMES.get(language, "English")

    if not settings.anthropic_api_key:
        return _fallback_draft(subject, message, language)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

        system_prompt = f"""You are a professional customer service representative for YONGJIN TURBO CO., LTD. (용진터보), a turbocharger maintenance company based in Busan, South Korea.

Generate a professional and helpful response draft for the customer inquiry below.

Rules:
- Respond in {lang_name}
- Be professional, courteous, and helpful
- If the inquiry is about parts/pricing, mention that the sales team will provide a detailed quote
- If technical, provide general guidance and offer to connect with an engineer
- Keep technical terms (part numbers, model names) in English
- Reference company contact: yjt@yjturbo.com / +82-51-271-7823
- Keep the response concise (3-5 paragraphs)
- Do NOT include greeting/closing - just the body content (the system will add signature automatically)"""

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"Subject: {subject}\n\nCustomer Message:\n{message}"
            }],
        )
        return response.content[0].text

    except Exception as e:
        logger.error(f"[AI-DRAFT] Claude API error: {e}")
        return _fallback_draft(subject, message, language)


def _fallback_draft(subject: str, message: str, language: str) -> str:
    """AI 사용 불가 시 템플릿 기반 초안"""
    templates = {
        "ko": f"문의해 주셔서 감사합니다.\n\n\"{subject}\" 관련하여 확인 후 상세 답변 드리겠습니다.\n\n추가 문의사항이 있으시면 yjt@yjturbo.com 또는 +82-51-271-7823으로 연락해 주세요.",
        "en": f"Thank you for your inquiry.\n\nRegarding \"{subject}\", we will review and provide a detailed response shortly.\n\nFor any additional questions, please contact us at yjt@yjturbo.com or +82-51-271-7823.",
        "zh": f"感谢您的咨询。\n\n关于\"{subject}\"，我们将核实后为您提供详细回复。\n\n如有其他问题，请联系 yjt@yjturbo.com 或 +82-51-271-7823。",
        "ja": f"お問い合わせいただきありがとうございます。\n\n「{subject}」について、確認の上、詳細なご回答を差し上げます。\n\nご不明な点がございましたら、yjt@yjturbo.com または +82-51-271-7823 までご連絡ください。",
        "ar": f"شكرًا لاستفسارك.\n\nبخصوص \"{subject}\"، سنقوم بالمراجعة وتقديم رد مفصل قريبًا.\n\nلأي أسئلة إضافية، يرجى الاتصال بنا على yjt@yjturbo.com أو 7823-271-51-82+.",
        "es": f"Gracias por su consulta.\n\nCon respecto a \"{subject}\", revisaremos y proporcionaremos una respuesta detallada en breve.\n\nPara cualquier pregunta adicional, contáctenos en yjt@yjturbo.com o +82-51-271-7823.",
        "hi": f"आपकी पूछताछ के लिए धन्यवाद।\n\n\"{subject}\" के संबंध में, हम समीक्षा करके शीघ्र ही विस्तृत उत्तर प्रदान करेंगे।\n\nकिसी भी अतिरिक्त प्रश्न के लिए, कृपया yjt@yjturbo.com या +82-51-271-7823 पर संपर्क करें।",
        "fr": f"Merci pour votre demande.\n\nConcernant \"{subject}\", nous examinerons et fournirons une réponse détaillée sous peu.\n\nPour toute question supplémentaire, veuillez nous contacter à yjt@yjturbo.com ou +82-51-271-7823.",
    }
    return templates.get(language, templates["en"])
