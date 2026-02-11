"""
Uvicorn 서버 실행 스크립트
- keep-alive timeout 설정으로 CLOSE_WAIT 방지
- graceful shutdown으로 커넥션 정리
"""
import uvicorn
from app.config import get_settings

settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.uvicorn_host,
        port=settings.uvicorn_port,
        reload=settings.app_debug,
        # ── CLOSE_WAIT 방지 핵심 설정 ──
        timeout_keep_alive=settings.uvicorn_keep_alive,   # 유휴 keep-alive 커넥션 30초 후 종료
        timeout_graceful_shutdown=settings.uvicorn_timeout_notify,  # graceful shutdown 대기
        # ── 기타 ──
        log_level="info",
        access_log=True,
    )
