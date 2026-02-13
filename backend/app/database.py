from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import StaticPool, QueuePool
from app.config import get_settings

settings = get_settings()

connect_args = {}
pool_config = {}
db_url = settings.database_url

if db_url.startswith("sqlite"):
    # SQLite: 단일 커넥션, StaticPool 사용 (CLOSE_WAIT 발생 없음)
    connect_args = {"check_same_thread": False}
    pool_config = {
        "poolclass": StaticPool,
    }
else:
    # Render PostgreSQL: postgres:// → postgresql:// 변환 (SQLAlchemy 2.0+ 필수)
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    # PostgreSQL: QueuePool + 커넥션 재활용 설정 (Render 무료 플랜 최적화)
    pool_config = {
        "poolclass": QueuePool,
        "pool_size": 3,            # Render 무료 플랜: 작은 풀
        "max_overflow": 5,         # 초과 허용 커넥션 수
        "pool_pre_ping": True,     # 사용 전 커넥션 유효성 검사 (끊어진 커넥션 자동 제거)
        "pool_recycle": 300,       # 5분마다 커넥션 재생성 (Render 무료 DB 안정성)
        "pool_timeout": 30,        # 풀에서 커넥션 대기 최대 시간
    }

engine = create_engine(
    db_url,
    connect_args=connect_args,
    **pool_config,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """DB 세션 의존성 - 요청 완료 후 반드시 반환"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def dispose_engine():
    """서버 종료 시 모든 커넥션 정리 (CLOSE_WAIT 방지)"""
    engine.dispose()
