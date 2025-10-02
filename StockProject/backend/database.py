# pip install sqlalchemy psycopg2-binary alembic
# python database.py 실행
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from datetime import datetime, timezone
import uuid
from config import get_settings

# 설정 로드
settings = get_settings()

# 환경변수에서 DATABASE_URL 가져오기
DATABASE_URL = settings.database_url

engine = create_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy 2.0 스타일
class Base(DeclarativeBase):
    pass

# UTC 시간 헬퍼 함수
def utc_now():
    """timezone-aware UTC 현재 시간"""
    return datetime.now(timezone.utc)

# 모델 정의
class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    username = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    watchlist = relationship("Watchlist", back_populates="user", cascade="all, delete-orphan")
    search_history = relationship("SearchHistory", back_populates="user", cascade="all, delete-orphan")
    portfolio = relationship("Portfolio", back_populates="user", cascade="all, delete-orphan")

class Watchlist(Base):
    __tablename__ = "watchlist"
    
    watchlist_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"))
    stock_code = Column(String(10), nullable=False)
    stock_name = Column(String(100), nullable=False)
    added_at = Column(DateTime, default=utc_now)
    alert_enabled = Column(Boolean, default=False)
    target_price = Column(Integer, nullable=True)
    
    user = relationship("User", back_populates="watchlist")

class SearchHistory(Base):
    __tablename__ = "search_history"
    
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=True)
    stock_code = Column(String(10), nullable=False)
    stock_name = Column(String(100), nullable=False)
    searched_at = Column(DateTime, default=utc_now)
    
    user = relationship("User", back_populates="search_history")

class Portfolio(Base):
    __tablename__ = "portfolio"
    
    portfolio_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.user_id", ondelete="CASCADE"))
    stock_code = Column(String(10), nullable=False)
    stock_name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    avg_price = Column(Integer, nullable=False)
    purchase_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=utc_now)
    
    user = relationship("User", back_populates="portfolio")

class StockCache(Base):
    __tablename__ = "stock_cache"
    
    cache_id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(10), nullable=False)
    data = Column(JSON, nullable=False)
    cache_type = Column(String(50), nullable=False)
    cached_at = Column(DateTime, default=utc_now)
    expires_at = Column(DateTime, nullable=False)

class NewsCache(Base):
    __tablename__ = "news_cache"
    
    news_id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(10), nullable=False)
    title = Column(Text, nullable=False)
    link = Column(Text, nullable=False)
    source = Column(String(100))
    published_at = Column(DateTime)
    cached_at = Column(DateTime, default=utc_now)

# 데이터베이스 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 테이블 생성
def init_db():
    Base.metadata.create_all(bind=engine)

# 테이블 삭제 (개발용)
def drop_db():
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ 데이터베이스 테이블 생성 완료")
