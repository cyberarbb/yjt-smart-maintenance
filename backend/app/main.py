import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine, Base, dispose_engine
from app.routers import parts, inventory, customers, service_orders, inquiries, chatbot, auth, i18n

logger = logging.getLogger("uvicorn.error")
settings = get_settings()


# ── Lifespan: startup + shutdown 관리 ─────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ▶ Startup
    Base.metadata.create_all(bind=engine)
    from app.seed.seed_data import seed_database
    seed_database()
    logger.info("✅ Application started - DB ready")
    yield
    # ▶ Shutdown: 모든 DB 커넥션 정리 (CLOSE_WAIT 방지 핵심)
    dispose_engine()
    logger.info("🛑 Application shutdown - all connections disposed")


app = FastAPI(
    title=settings.app_name,
    description="용진터보 AI 기반 스마트 정비 플랫폼 API",
    version="1.0.0",
    lifespan=lifespan,
)


# ── CORS ──────────────────────────────────────────────────────
# 프로덕션(Render) + 로컬 개발 모두 지원
_origins = [
    settings.frontend_url,
    "http://localhost:3000",
]
# Render 등 *.onrender.com 도메인도 허용
import os
_extra = os.environ.get("EXTRA_CORS_ORIGINS", "")
if _extra:
    _origins.extend([o.strip() for o in _extra.split(",") if o.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Connection 헤더 미들웨어 (keep-alive 타임아웃 명시) ────────
@app.middleware("http")
async def add_connection_headers(request: Request, call_next):
    response: Response = await call_next(request)
    # keep-alive 타임아웃을 명시하여 클라이언트가 적절히 커넥션을 재활용/종료
    response.headers["Connection"] = "keep-alive"
    response.headers["Keep-Alive"] = "timeout=30, max=100"
    return response


# ── Routers ───────────────────────────────────────────────────
app.include_router(parts.router, prefix="/api/parts", tags=["Parts"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])
app.include_router(service_orders.router, prefix="/api/orders", tags=["Service Orders"])
app.include_router(inquiries.router, prefix="/api/inquiries", tags=["Inquiries"])
app.include_router(chatbot.router, prefix="/api/chat", tags=["AI Chatbot"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(i18n.router, prefix="/api/i18n", tags=["i18n"])


@app.get("/")
def root():
    return {"message": "YJT Smart Maintenance Platform API", "version": "1.0.0"}


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
