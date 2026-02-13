# YJT Smart Maintenance Platform

용진터보(YJT) - 터보차저 전문 기업 스마트 정비 플랫폼 (Phase 1 MVP)

## 기술 스택

- **Backend**: Python FastAPI + SQLAlchemy ORM
- **Frontend**: Next.js (TypeScript) + Tailwind CSS
- **Database**: PostgreSQL (개발: SQLite 호환)
- **AI/LLM**: Claude API (Anthropic) + LangChain (RAG)
- **Vector DB**: ChromaDB (로컬)
- **Migration**: Alembic

## 프로젝트 구조

```
yjt-smart-maintenance/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI 엔트리포인트
│       ├── config.py            # 환경변수, 설정
│       ├── database.py          # DB 연결, 세션
│       ├── models/              # SQLAlchemy 모델 (Part, Inventory, Customer, ServiceOrder, Inquiry)
│       ├── schemas/             # Pydantic 스키마
│       ├── routers/             # API 라우터 (parts, inventory, customers, service_orders, inquiries, chatbot)
│       ├── services/            # 비즈니스 로직 (inventory_service, chatbot_service, search_service)
│       └── seed/                # 시드 데이터
├── frontend/
│   └── src/
│       ├── app/                 # Next.js 페이지 (dashboard, inventory, chatbot, orders, inquiries)
│       ├── components/          # React 컴포넌트 (layout, inventory, chatbot, dashboard, ui)
│       └── lib/                 # API 클라이언트, 유틸
└── README.md
```

## 핵심 데이터 모델

- **Part**: part_number, name, brand(Enum: MAN/MHI/KBB/ABB/Napier), turbo_model, category, unit_price(USD)
- **Inventory**: part_id(FK→Part), quantity, min_quantity(안전재고), warehouse
- **Customer**: company_name, contact_name, email, phone, country, vessel_type
- **ServiceOrder**: customer_id(FK→Customer), order_type(Enum: Overhaul/PartSupply/TechnicalService), turbo_brand, turbo_model, vessel_name, status(Enum: Pending/InProgress/Completed/Cancelled)
- **Inquiry**: 고객 문의 모델
- 모든 PK는 UUID 사용

## 현재 진행 상태

- [ ] Step 1: 프로젝트 초기 설정 (디렉토리, FastAPI, Next.js, .env)
- [ ] Step 2: DB 모델 & API 기본 구조 (SQLAlchemy, Alembic, Pydantic, CRUD)
- [ ] Step 3: 부품 재고 관리 시스템 (CRUD, 입출고, 재고 알림, 시드 데이터)
- [ ] Step 4: AI 챗봇 RAG (Claude API, ChromaDB, 기술문서 임베딩, 재고 연동)
- [ ] Step 5: 프론트엔드 레이아웃 & 대시보드
- [ ] Step 6: 프론트엔드 재고관리 & 챗봇 UI
- [ ] Step 7: 통합 테스트 & 시드 데이터

## 코딩 규칙

- Backend: Python 3.11+, 타입 힌트 필수, async/await 사용
- Frontend: TypeScript strict mode, 함수형 컴포넌트
- API 응답: JSON, snake_case (백엔드) / camelCase (프론트엔드)
- 커밋 메시지: 한글 허용, conventional commits 형식

## 실행 방법

```bash
# Backend
cd backend && uvicorn app.main:app --reload  # → http://localhost:8000/docs

# Frontend
cd frontend && npm run dev  # → http://localhost:3000
```
