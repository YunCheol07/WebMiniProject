from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging

from config import get_settings
from services.korea_investment import ki_service
from routers import auth_router, stock_router, watchlist_router, market_router

# 설정
settings = get_settings()

# 로깅
logging.basicConfig(level=logging.INFO if settings.DEBUG else logging.WARNING)
logger = logging.getLogger(__name__)


# Lifespan 이벤트
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        logger.info("✅ 서버 시작")
        token = ki_service.get_access_token()
        if token:
            logger.info("✅ 한국투자증권 API 토큰 발급 완료")
        else:
            logger.warning("⚠️ 토큰 발급 실패")
    except Exception as e:
        logger.error(f"❌ 서버 시작 중 오류: {e}")
    
    yield
    
    logger.info("👋 서버 종료 중...")


# FastAPI 앱
app = FastAPI(
    title="주식 정보 API",
    description="한국투자증권 OpenAPI를 활용한 주식 정보 제공 API",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth_router)
app.include_router(stock_router)
app.include_router(watchlist_router)
app.include_router(market_router)


# 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "message": "주식 정보 API 서버",
        "docs": "/docs",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "token_exists": ki_service.access_token is not None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )


# uvicorn app:app --reload --host 127.0.0.1 --port 8000