import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

# .env 파일 절대 경로 (backend/ 디렉토리 기준)
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

# ✅ .env 파일을 OS 환경변수에 직접 로드 (override=True로 빈 값 덮어쓰기)
# pydantic-settings는 OS 환경변수 > .env 파일 우선이므로,
# OS에 빈 값이 있으면 .env 값이 무시됨 → load_dotenv로 먼저 세팅
load_dotenv(_ENV_FILE, override=True)


class Settings(BaseSettings):
    app_name: str = "YJT Smart Maintenance Platform"
    app_env: str = "development"
    app_debug: bool = True
    secret_key: str = "dev-secret-key-change-in-production"

    # Database
    database_url: str = "sqlite:///./yjt_maintenance.db"

    # Anthropic Claude API
    anthropic_api_key: str = ""

    # CORS
    frontend_url: str = "http://localhost:3000"

    # Server (Uvicorn) - CLOSE_WAIT 방지
    uvicorn_host: str = "0.0.0.0"
    uvicorn_port: int = 8000
    uvicorn_keep_alive: int = 30       # keep-alive 타임아웃 (초) - 유휴 커넥션 30초 후 종료
    uvicorn_timeout_notify: int = 30   # graceful shutdown 대기 시간
    uvicorn_workers: int = 1           # 개발 환경 1, 프로덕션 환경 2~4

    model_config = {"env_file": str(_ENV_FILE), "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache()
def get_settings():
    return Settings()
