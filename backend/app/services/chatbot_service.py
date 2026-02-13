"""
YJT AI 챗봇 서비스
- API 모드: Claude API + RAG (할루시네이션 방지)
- 폴백 모드: 스마트 키워드 매칭 + DB 조회
"""
import re
import logging
import anthropic

logger = logging.getLogger(__name__)
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.config import get_settings
from app.models.part import Part
from app.models.inventory import Inventory
from app.models.service_order import ServiceOrder
from app.models.customer import Customer
from app.models.vessel import Vessel
from app.models.equipment import Equipment
from app.models.work_order import WorkOrder

settings = get_settings()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 할루시네이션 방지 시스템 프롬프트
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYSTEM_PROMPT = """당신은 용진터보(YONGJIN TURBO CO., LTD.)의 AI 기술 어시스턴트입니다.

## ⚠️ 핵심 규칙 (반드시 준수)

1. **[시스템 참고 데이터]에 있는 정보만 사실로 답변하세요.**
   - DB 조회 결과(부품 재고, 가격, 수량)는 정확히 그대로 전달
   - 데이터에 없는 수치, 가격, 수량은 절대 추측하지 마세요

2. **모르면 솔직히 모른다고 하세요.**
   - "해당 정보는 현재 시스템에 등록되어 있지 않습니다."
   - "정확한 답변을 위해 yjt@yjturbo.com으로 문의해주세요."

3. **답변 범위: 선박 관리 및 터보차저 관련 질문**
   - 터보차저, 부품, 오버홀, 서비스, 견적 → 답변 OK
   - 선박 관리, 장비 상태, 정비 계획, 작업지시서 → 답변 OK
   - 그 외(날씨, 주식, 일반 상식 등) → "죄송합니다, 선박 정비 관련 문의만 도와드릴 수 있습니다."

4. **출처를 명시하세요.**
   - DB 데이터 기반: "[재고 DB 조회] NR29/S 베어링: 40개 보유"
   - 회사 정보 기반: "[YJT 정보] 48시간 내 글로벌 엔지니어 파견"
   - 일반 기술 지식: "[일반 참고] 정확한 사항은 담당 엔지니어 확인 필요"

## 회사 정보 (이 정보는 사실입니다)
- 부산시 사하구 신산로 78번지 소재 터보차저 전문 기업
- 전 세계 31개국 네트워크, 48시간 내 엔지니어 파견 가능
- 연간 약 1,990건 오버홀 수행
- $17M 규모 부품 재고 보유 (세계 최대 MAN NR Type 재고)
- 24시간 7일 서비스 가능
- 연락처: yjt@yjturbo.com / +82-51-271-7823

## 지원 브랜드
MAN, MHI (Mitsubishi), KBB, ABB, Napier

## 서비스 범위
1. 터보차저 오버홀 (Standard Overhaul, Cartridge Overhaul)
2. 특수 세척 (Special Cleaning - G.O.C, G.I.C)
3. 동적 균형 조정 (Dynamic Balancing)
4. 부품 공급 (세계 최대 MAN NR29/S, NR34/S 정품부품 재고)
5. 기술 지원 서비스
6. Exchange Basis 서비스

## 주요 터보차저 모델
- MAN: NR12/R, NR15/R, NR20/R, NR24/R, NR26/R, NR29/S, NR34/S, NA34/S, NA40/S, NA48/S, NA57/S, NA70/S, TCA series
- MHI: MET series (MET18, MET26, MET33, MET42, MET53, MET66, MET83, MET90)
- KBB: HPR3000, HPR4000, HPR5000, ST18, ST23, ST27
- ABB: VTR series, A100, A200, TPL series
- Napier: NA series

## 주요 부품 카테고리
Nozzle Ring, Bearing (Journal/Thrust), Turbine Blade, Compressor Wheel, Shaft, Seal, Gasket, Casing, Cartridge, Filter

## 오버홀 작업 흐름
1. 터보차저 입고 및 외관 검사
2. 분해 (Disassembly)
3. 세척 (Cleaning)
4. 정밀 검사 및 측정 (Inspection & Measurement)
5. 부품 교체 판정
6. 재조립 (Reassembly)
7. 동적 균형 (Dynamic Balancing)
8. 성능 테스트
9. 출하

## 응답 언어
- 반드시 사용자가 지정한 언어로 답변하세요.
- 사용자가 다른 언어로 질문하더라도, 지정된 응답 언어로 답변하세요.
- 항상 친절하고 전문적으로 응답
- 기술 용어(부품명, 모델명)는 영어 원문 유지
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DB 조회 함수들
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def _extract_keywords(query: str) -> list[str]:
    """사용자 질문에서 검색 키워드 추출"""
    # 터보 모델명 패턴 (NR29/S, MET42, HPR3000, VTR254 등)
    model_patterns = re.findall(r'[A-Za-z]{2,4}[\-]?\d{2,5}[/]?[A-Za-z]?', query)

    # 브랜드명
    brands = ["MAN", "MHI", "KBB", "ABB", "Napier"]
    found_brands = [b for b in brands if b.lower() in query.lower()]

    # 부품 카테고리
    categories = {
        "nozzle": "Nozzle Ring", "노즐": "Nozzle Ring",
        "bearing": "Bearing", "베어링": "Bearing",
        "blade": "Turbine Blade", "블레이드": "Turbine Blade",
        "compressor": "Compressor Wheel", "컴프레서": "Compressor Wheel",
        "shaft": "Shaft", "샤프트": "Shaft",
        "seal": "Seal", "씰": "Seal",
        "gasket": "Gasket", "가스켓": "Gasket",
        "casing": "Casing", "케이싱": "Casing",
        "cartridge": "Cartridge", "카트리지": "Cartridge",
        "filter": "Filter", "필터": "Filter",
    }
    found_categories = [v for k, v in categories.items() if k in query.lower()]

    keywords = model_patterns + found_brands + found_categories

    # 일반 단어도 추가 (2글자 이상)
    for word in query.split():
        cleaned = re.sub(r'[^\w/]', '', word)
        if len(cleaned) >= 2 and cleaned not in keywords:
            keywords.append(cleaned)

    return keywords if keywords else [query]


def get_inventory_context(db: Session, query: str) -> str:
    """사용자 질문에서 관련 재고 정보를 검색하여 컨텍스트 생성"""
    keywords = _extract_keywords(query)
    context_parts = []

    # 키워드별로 OR 검색
    filters = []
    for kw in keywords:
        filters.extend([
            Part.name.ilike(f"%{kw}%"),
            Part.part_number.ilike(f"%{kw}%"),
            Part.turbo_model.ilike(f"%{kw}%"),
            Part.brand.ilike(f"%{kw}%"),
            Part.category.ilike(f"%{kw}%"),
        ])

    parts = (
        db.query(Part)
        .join(Inventory, Part.id == Inventory.part_id, isouter=True)
        .filter(or_(*filters))
        .limit(15)
        .all()
    )

    if parts:
        context_parts.append("## 📦 관련 부품 재고 정보 (DB 실시간 조회 결과)")
        for part in parts:
            qty = part.inventory.quantity if part.inventory else 0
            min_qty = part.inventory.min_quantity if part.inventory else 0
            warehouse = part.inventory.warehouse if part.inventory else "N/A"
            status = "⚠️ 재고부족" if part.inventory and part.inventory.is_low_stock else "✅ 정상"
            context_parts.append(
                f"- **{part.name}** ({part.part_number})\n"
                f"  브랜드: {part.brand} | 모델: {part.turbo_model} | 분류: {part.category}\n"
                f"  재고: {qty}개 (안전재고: {min_qty}개) | 창고: {warehouse} | 상태: {status}\n"
                f"  단가: ${part.unit_price:,.2f}"
            )

    # 주문 통계
    total_orders = db.query(ServiceOrder).count()
    pending_orders = db.query(ServiceOrder).filter(ServiceOrder.status == "Pending").count()
    in_progress = db.query(ServiceOrder).filter(ServiceOrder.status == "In Progress").count()

    if total_orders > 0:
        context_parts.append(
            f"\n## 📋 서비스 주문 현황\n"
            f"- 전체: {total_orders}건 | 대기: {pending_orders}건 | 진행중: {in_progress}건"
        )

    return "\n".join(context_parts) if context_parts else "검색 결과 없음 - 해당 키워드와 일치하는 부품이 DB에 없습니다."


def get_vessel_pms_context(db: Session, query: str) -> str:
    """선박/장비/PMS 관련 컨텍스트"""
    context_parts = []

    # 선박 관련 키워드 감지
    vessel_keywords = ["vessel", "ship", "선박", "선박", "pms", "정비", "maintenance",
                       "work order", "작업", "overdue", "초과", "장비", "equipment"]
    has_vessel_query = any(kw in query.lower() for kw in vessel_keywords)

    if has_vessel_query:
        # 선박 현황
        vessels = db.query(Vessel).filter(Vessel.is_active == True).all()
        if vessels:
            context_parts.append("## 🚢 선박 현황 (DB 조회)")
            for v in vessels:
                eq_count = db.query(Equipment).filter(
                    Equipment.vessel_id == v.id, Equipment.is_active == True
                ).count()
                context_parts.append(f"- {v.name} ({v.vessel_type}) - 장비 {eq_count}개")

        # 초과 작업지시서
        from datetime import datetime
        now = datetime.utcnow()
        overdue = (
            db.query(WorkOrder)
            .filter(
                WorkOrder.status.in_(["Planned", "InProgress"]),
                WorkOrder.due_date < now,
            )
            .limit(10)
            .all()
        )
        if overdue:
            context_parts.append(f"\n## ⚠️ 초과 작업지시서 ({len(overdue)}건)")
            for wo in overdue:
                eq = db.query(Equipment).filter(Equipment.id == wo.equipment_id).first()
                v = db.query(Vessel).filter(Vessel.id == wo.vessel_id).first()
                context_parts.append(
                    f"- [{wo.priority}] {wo.title} | {v.name if v else 'N/A'} | "
                    f"{eq.name if eq else 'N/A'} | 기한: {wo.due_date.strftime('%Y-%m-%d') if wo.due_date else 'N/A'}"
                )

        # PMS 통계
        total_wo = db.query(WorkOrder).count()
        completed_wo = db.query(WorkOrder).filter(WorkOrder.status == "Completed").count()
        if total_wo > 0:
            rate = round(completed_wo / total_wo * 100, 1)
            context_parts.append(
                f"\n## 📊 PMS 통계\n"
                f"- 전체 작업지시서: {total_wo}건 | 완료: {completed_wo}건 | 완료율: {rate}%"
            )

    return "\n".join(context_parts) if context_parts else ""



    """주문 관련 컨텍스트"""
    orders = (
        db.query(ServiceOrder)
        .filter(
            or_(
                ServiceOrder.vessel_name.ilike(f"%{query}%"),
                ServiceOrder.turbo_model.ilike(f"%{query}%"),
                ServiceOrder.turbo_brand.ilike(f"%{query}%"),
                ServiceOrder.description.ilike(f"%{query}%"),
            )
        )
        .limit(5)
        .all()
    )
    if not orders:
        return ""

    lines = ["## 📋 관련 서비스 주문 (DB 조회 결과)"]
    for o in orders:
        lines.append(
            f"- [{o.status}] {o.order_type} | {o.turbo_brand} {o.turbo_model}"
            f"{' | 선박: ' + o.vessel_name if o.vessel_name else ''}"
            f"\n  내용: {o.description or 'N/A'}"
        )
    return "\n".join(lines)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 메인 챗봇 함수
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LANGUAGE_NAMES = {
    "ko": "한국어(Korean)", "en": "English", "zh": "中文(Chinese)",
    "ja": "日本語(Japanese)", "ar": "العربية(Arabic)", "es": "Español(Spanish)",
    "hi": "हिन्दी(Hindi)", "fr": "Français(French)",
}


def chat_with_ai(message: str, history: list[dict], db: Session, language: str = "ko") -> str:
    """
    챗봇 메인 함수
    - API 키 있으면: Claude API + RAG (할루시네이션 방지)
    - API 키 없으면: 스마트 폴백
    """
    if not settings.anthropic_api_key:
        return _smart_fallback(message, db)

    return _claude_rag_response(message, history, db, language)


def _claude_rag_response(message: str, history: list[dict], db: Session, language: str = "ko") -> str:
    """Claude API + RAG 기반 응답 (할루시네이션 방지 + 다국어)"""

    # 1) DB에서 관련 데이터 수집
    inventory_context = get_inventory_context(db, message)
    order_context = get_order_context(db, message)
    vessel_pms_context = get_vessel_pms_context(db, message)

    # 2) 대화 히스토리 구성 (최근 10개)
    messages = []
    for h in history[-10:]:
        messages.append({"role": h["role"], "content": h["content"]})

    # 3) 응답 언어 지정
    lang_name = LANGUAGE_NAMES.get(language, "English")

    # 4) 사용자 메시지 + DB 데이터 주입
    data_block = f"""
[시스템 참고 데이터 - 아래 데이터는 DB에서 실시간 조회한 결과입니다. 이 데이터만 사실로 답변하세요.]

{inventory_context}
{order_context if order_context else ""}
{vessel_pms_context if vessel_pms_context else ""}

[규칙 리마인더]
- 위 데이터에 있는 수치(재고, 가격)만 정확히 전달하세요.
- 데이터에 없는 정보는 "시스템에 등록되지 않은 정보"라고 안내하세요.
- 터보차저 관련 일반 기술 지식은 [일반 참고]로 표시하되, 정확한 확인은 담당자를 안내하세요.

[⚠️ 필수: 응답 언어]
- 반드시 {lang_name} 로 답변하세요. 부품명/모델명 등 기술 용어는 영어 원문을 유지하세요.
""".strip()

    user_content = f"{message}\n\n{data_block}"
    messages.append({"role": "user", "content": user_content})

    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        return response.content[0].text
    except anthropic.AuthenticationError:
        return "⚠️ API 키가 유효하지 않습니다. .env 파일의 ANTHROPIC_API_KEY를 확인해주세요."
    except anthropic.RateLimitError:
        return "⚠️ API 호출 한도에 도달했습니다. 잠시 후 다시 시도해주세요.\n\n긴급 문의: yjt@yjturbo.com"
    except Exception as e:
        # API 오류 시 폴백으로 전환
        logger.error(f"Claude API 오류 → 폴백 전환: {type(e).__name__}: {e}")
        return _smart_fallback(message, db)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 스마트 폴백 (API 없이 동작)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def _smart_fallback(message: str, db: Session) -> str:
    """API 키 없이도 동작하는 스마트 응답 시스템"""
    msg = message.lower().strip()
    keywords = _extract_keywords(message)

    # ── 1. 인사/환영 ──
    greetings = ["안녕", "hello", "hi", "헬로", "처음", "시작"]
    if any(g in msg for g in greetings) and len(msg) < 20:
        return (
            "안녕하세요! 용진터보(YJT) AI 어시스턴트입니다. 🚢\n\n"
            "아래 질문들을 도와드릴 수 있습니다:\n\n"
            "📦 **부품/재고 조회**\n"
            "   예: \"MAN NR29/S 베어링 재고\", \"KBB 부품 목록\"\n\n"
            "🔧 **오버홀 서비스**\n"
            "   예: \"오버홀 절차\", \"카트리지 오버홀이란?\"\n\n"
            "💰 **견적/가격 문의**\n"
            "   예: \"NR34/S 노즐링 가격\", \"견적 요청\"\n\n"
            "📞 **연락처/위치**\n"
            "   예: \"연락처\", \"위치\"\n\n"
            "🏢 **회사 소개**\n"
            "   예: \"용진터보 소개\", \"지원 브랜드\"\n\n"
            "질문을 입력해주세요!"
        )

    # ── 2. 부품/재고 조회 ──
    inventory_kw = ["재고", "stock", "inventory", "부품", "part", "가격", "price", "견적", "quote", "얼마"]
    brand_kw = ["man", "mhi", "kbb", "abb", "napier"]
    part_kw = ["nozzle", "노즐", "bearing", "베어링", "blade", "블레이드", "seal", "씰",
               "gasket", "가스켓", "shaft", "샤프트", "cartridge", "카트리지", "casing", "케이싱",
               "compressor", "컴프레서", "filter", "필터", "wheel", "휠"]
    model_match = re.search(r'[A-Za-z]{2,4}[\-]?\d{2,5}[/]?[A-Za-z]?', msg)

    if any(kw in msg for kw in inventory_kw) or any(kw in msg for kw in brand_kw) or \
       any(kw in msg for kw in part_kw) or model_match:

        context = get_inventory_context(db, message)

        if "검색 결과 없음" not in context:
            # 가격 관련 질문이면 견적 안내 추가
            price_note = ""
            if any(kw in msg for kw in ["가격", "price", "견적", "quote", "얼마", "cost"]):
                price_note = (
                    "\n\n💰 **견적 안내**\n"
                    "위 단가는 참고 가격이며, 실제 견적은 수량·납기·운송 조건에 따라 달라질 수 있습니다.\n"
                    "정확한 견적: 📧 yjt@yjturbo.com / 📞 +82-51-271-7823"
                )
            return f"[재고 DB 조회 결과]\n\n{context}{price_note}"
        else:
            return (
                f"검색하신 '{message}'와 일치하는 부품을 찾지 못했습니다.\n\n"
                "💡 **검색 팁:**\n"
                "- 모델명으로 검색: `NR29/S`, `MET42`, `HPR3000`\n"
                "- 브랜드로 검색: `MAN`, `KBB`, `ABB`\n"
                "- 부품 종류로 검색: `베어링`, `노즐링`, `가스켓`\n\n"
                "또는 📧 yjt@yjturbo.com으로 문의해주세요."
            )

    # ── 3. 오버홀 서비스 ──
    if any(kw in msg for kw in ["오버홀", "overhaul", "정비", "수리", "maintenance"]):
        if any(kw in msg for kw in ["절차", "과정", "순서", "flow", "process", "어떻게"]):
            return (
                "🔧 **터보차저 오버홀 작업 절차**\n\n"
                "1️⃣ **입고 및 외관 검사** - 터보차저 수령 후 외관 상태 확인\n"
                "2️⃣ **분해 (Disassembly)** - 완전 분해 및 부품별 분리\n"
                "3️⃣ **세척 (Cleaning)** - Special Cleaning (G.O.C, G.I.C)\n"
                "4️⃣ **정밀 검사 및 측정** - 각 부품 치수, 마모도, 크랙 검사\n"
                "5️⃣ **부품 교체 판정** - 교체 필요 부품 식별 및 고객 협의\n"
                "6️⃣ **재조립 (Reassembly)** - 신품/수리 부품으로 재조립\n"
                "7️⃣ **동적 균형 (Dynamic Balancing)** - 로터 밸런싱\n"
                "8️⃣ **성능 테스트** - 최종 성능 확인\n"
                "9️⃣ **출하** - 포장 및 배송\n\n"
                "⏱️ **소요 기간**: 일반적으로 7~14일\n"
                "✅ **보증**: 1년 보증 제공\n"
                "🌍 **현장 서비스**: 48시간 내 전세계 엔지니어 파견 가능\n\n"
                "견적 요청: 📧 yjt@yjturbo.com / 📞 +82-51-271-7823"
            )
        elif any(kw in msg for kw in ["종류", "타입", "type", "카트리지", "cartridge"]):
            return (
                "🔧 **오버홀 서비스 종류**\n\n"
                "**1. Standard Overhaul (표준 오버홀)**\n"
                "   - 전체 분해, 세척, 검사, 재조립\n"
                "   - 마모/손상 부품 교체\n"
                "   - 동적 균형 조정 + 성능 테스트\n\n"
                "**2. Cartridge Overhaul (카트리지 오버홀)**\n"
                "   - 카트리지(회전체) 단위 오버홀\n"
                "   - 현장에서 빠른 교체 가능\n"
                "   - Exchange Basis 서비스 지원\n\n"
                "**3. Special Cleaning (특수 세척)**\n"
                "   - G.O.C (Gas Outlet Casing) 세척\n"
                "   - G.I.C (Gas Inlet Casing) 세척\n"
                "   - 성능 저하 방지용 정기 세척\n\n"
                "지원 브랜드: MAN, MHI, KBB, ABB, Napier\n"
                "문의: 📧 yjt@yjturbo.com / 📞 +82-51-271-7823"
            )
        else:
            # 관련 주문도 함께 표시
            order_info = get_order_context(db, message)
            order_section = f"\n\n{order_info}" if order_info else ""
            return (
                "🔧 **오버홀 서비스 안내**\n\n"
                "용진터보는 전 세계 터보차저 오버홀 전문 기업입니다.\n\n"
                "**서비스 종류:**\n"
                "- Standard Overhaul (표준 오버홀)\n"
                "- Cartridge Overhaul (카트리지 오버홀)\n"
                "- Special Cleaning (특수 세척)\n"
                "- Dynamic Balancing (동적 균형 조정)\n\n"
                "**지원 브랜드:** MAN, MHI, KBB, ABB, Napier\n"
                "**실적:** 연간 약 1,990건 오버홀 수행\n"
                "**보증:** 1년 보증 제공\n"
                "**대응:** 48시간 내 전세계 엔지니어 파견\n\n"
                "더 자세한 안내를 원하시면:\n"
                "- \"오버홀 절차\" → 작업 단계별 안내\n"
                "- \"오버홀 종류\" → 서비스 유형별 안내\n\n"
                f"견적 요청: 📧 yjt@yjturbo.com / 📞 +82-51-271-7823{order_section}"
            )

    # ── 4. 회사 정보 ──
    if any(kw in msg for kw in ["회사", "소개", "about", "company", "용진", "yjt", "yongjin"]):
        return (
            "🏢 **용진터보 (YONGJIN TURBO CO., LTD.)** 소개\n\n"
            "대한민국 부산 소재 **터보차저 전문 기업**입니다.\n\n"
            "**📊 주요 실적:**\n"
            "- 연간 약 1,990건 오버홀 수행\n"
            "- $17,000,000 규모 부품 재고 보유\n"
            "- 세계 최대 MAN NR Type 부품 재고\n\n"
            "**🌍 글로벌 네트워크:**\n"
            "- 31개국+ 서비스 (아시아 15, 유럽 8, 아메리카 5, 오세아니아 2, 아프리카 1)\n"
            "- 48시간 내 전세계 엔지니어 파견\n"
            "- 24시간 7일 상담 가능\n\n"
            "**🔧 지원 브랜드:** MAN, MHI, KBB, ABB, Napier\n\n"
            "**📍 위치:** 부산시 사하구 신산로 78번지\n"
            "**📧 이메일:** yjt@yjturbo.com\n"
            "**📞 전화:** +82-51-271-7823"
        )

    # ── 5. 연락처 ──
    if any(kw in msg for kw in ["연락", "contact", "문의", "전화", "이메일", "email", "phone", "위치", "주소", "address", "location"]):
        return (
            "📞 **용진터보 연락처**\n\n"
            "📧 **이메일:** yjt@yjturbo.com\n"
            "📞 **전화:** +82-51-271-7823\n"
            "📍 **주소:** 부산시 사하구 신산로 78번지 (우: 49434)\n\n"
            "⏰ **운영:** 24시간 7일 상담 가능\n"
            "🌍 **글로벌 서비스:** 48시간 내 전세계 엔지니어 파견"
        )

    # ── 6. 브랜드 정보 ──
    if any(kw in msg for kw in ["브랜드", "brand", "지원", "취급"]):
        # 브랜드별 재고 통계
        brand_stats = (
            db.query(Part.brand, func.count(Part.id))
            .group_by(Part.brand)
            .all()
        )
        stats_text = "\n".join([f"  - {b}: {c}종" for b, c in brand_stats])
        return (
            "🏭 **지원 터보차저 브랜드**\n\n"
            "**MAN** (HD Hyundai Marine Engine)\n"
            "  모델: NR12/R, NR15/R, NR20/R, NR24/R, NR26/R, NR29/S, NR34/S, NA40/S, TCA series\n\n"
            "**MHI** (Mitsubishi Heavy Industries)\n"
            "  모델: MET18, MET26, MET33, MET42, MET53, MET66, MET83, MET90\n\n"
            "**KBB**\n"
            "  모델: HPR3000, HPR4000, HPR5000, ST18, ST23, ST27\n\n"
            "**ABB**\n"
            "  모델: VTR series, A100, A200, TPL series\n\n"
            "**Napier**\n"
            "  모델: NA series\n\n"
            f"📦 **현재 보유 부품:**\n{stats_text}\n\n"
            "특정 모델의 부품을 조회하시려면 모델명을 입력해주세요.\n"
            "예: \"NR29/S 부품\", \"MET42 재고\""
        )

    # ── 7. 주문/서비스 상태 ──
    if any(kw in msg for kw in ["주문", "order", "상태", "status", "서비스"]):
        order_context = get_order_context(db, message)
        if order_context:
            return f"[주문 DB 조회 결과]\n\n{order_context}\n\n상세 문의: 📧 yjt@yjturbo.com"

        total = db.query(ServiceOrder).count()
        pending = db.query(ServiceOrder).filter(ServiceOrder.status == "Pending").count()
        in_prog = db.query(ServiceOrder).filter(ServiceOrder.status == "In Progress").count()
        done = db.query(ServiceOrder).filter(ServiceOrder.status == "Completed").count()
        return (
            "📋 **서비스 주문 현황**\n\n"
            f"- 전체: {total}건\n"
            f"- ⏳ 대기중: {pending}건\n"
            f"- 🔄 진행중: {in_prog}건\n"
            f"- ✅ 완료: {done}건\n\n"
            "특정 주문 조회는 선박명이나 모델명으로 검색해주세요.\n"
            "예: \"Maersk 주문 상태\", \"NR29/S 서비스\""
        )

    # ── 8. 도움말 / 기본 응답 ──
    return (
        "안녕하세요! 용진터보 AI 어시스턴트입니다. 🚢\n\n"
        "아래 키워드로 질문해주세요:\n\n"
        "📦 **부품/재고**: \"MAN NR29/S 베어링\", \"KBB 부품 재고\"\n"
        "🔧 **오버홀**: \"오버홀 절차\", \"오버홀 종류\"\n"
        "💰 **가격/견적**: \"NR34/S 노즐링 가격\"\n"
        "🏢 **회사 소개**: \"용진터보 소개\"\n"
        "📞 **연락처**: \"연락처\", \"위치\"\n"
        "🏭 **브랜드**: \"지원 브랜드\"\n"
        "📋 **주문 현황**: \"주문 상태\"\n\n"
        "자세한 기술 문의는 📧 yjt@yjturbo.com으로 연락해주세요."
    )
