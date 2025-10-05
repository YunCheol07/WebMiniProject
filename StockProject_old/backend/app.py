from fastapi import FastAPI, HTTPException, Query, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import timedelta
import requests
import json
from datetime import datetime, timezone
from typing import Optional
import uvicorn
import logging
from urllib.parse import quote
import feedparser

from config import get_settings
from database import get_db, User
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# 설정 로드
settings = get_settings()

# 로깅 설정
logging.basicConfig(level=logging.INFO if settings.DEBUG else logging.WARNING)
logger = logging.getLogger(__name__)

# 전역 변수
config = None
access_token = None

# 설정 로드
def load_config():
    """환경변수에서 설정 로드"""
    return {
        'REAL_APP_KEY': settings.REAL_APP_KEY,
        'REAL_APP_SECRET': settings.REAL_APP_SECRET,
        'REAL_URL': settings.REAL_URL,
        'REAL_CANO': settings.REAL_CANO,
        'REAL_ACNT_PRDT_CD': settings.REAL_ACNT_PRDT_CD
    }

# 토큰 발급
def get_access_token_sync():
    """동기 방식 토큰 발급"""
    global access_token, config
    
    if not config:
        config = load_config()
    
    headers = {"content-type": "application/json"}
    body = {
        "grant_type": "client_credentials",
        "appkey": config['REAL_APP_KEY'],
        "appsecret": config['REAL_APP_SECRET']
    }
    
    PATH = "oauth2/tokenP"
    URL = f"{config['REAL_URL']}/{PATH}"
    
    try:
        logger.info(f"🔑 토큰 발급 시도: {URL}")
        res = requests.post(URL, headers=headers, data=json.dumps(body), timeout=10)
        
        logger.info(f"📡 응답 상태 코드: {res.status_code}")
        
        if res.status_code == 200:
            access_token = res.json()["access_token"]
            logger.info(f"✅ 토큰 발급 성공")
            return access_token
        else:
            logger.error(f"❌ 토큰 발급 실패 - 상태코드: {res.status_code}")
            return None
    
    except Exception as e:
        logger.error(f"❌ 토큰 발급 오류: {e}")
        return None

# Lifespan 이벤트 핸들러
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global config
    
    try:
        config = load_config()
        logger.info("✅ 환경변수 로드 완료")
        
        token = get_access_token_sync()
        if token:
            logger.info("✅ FastAPI 서버 시작 및 토큰 발급 완료")
        else:
            logger.warning("⚠️ 토큰 발급 실패")
    
    except Exception as e:
        logger.error(f"❌ 서버 시작 중 오류: {e}")
    
    yield
    
    logger.info("👋 서버 종료 중...")

# FastAPI 앱 생성
app = FastAPI(
    title="주식 정보 API",
    description="한국투자증권 OpenAPI를 활용한 주식 정보 제공 API",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Pydantic 모델 ====================

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: str
    email: str
    username: str
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# ==================== 인증 API ====================

@app.post("/api/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """회원가입"""
    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비밀번호는 최소 6자 이상이어야 합니다"
        )
    
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다"
        )
    
    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        password=hashed_password,
        username=user_data.username
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token_jwt = create_access_token(
        data={"sub": new_user.user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    user_response = UserResponse(
        user_id=new_user.user_id,
        email=new_user.email,
        username=new_user.username,
        created_at=new_user.created_at
    )
    
    return TokenResponse(
        access_token=access_token_jwt,
        token_type="bearer",
        user=user_response
    )

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """로그인"""
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다"
        )
    
    access_token_jwt = create_access_token(
        data={"sub": user.user_id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    user_response = UserResponse(
        user_id=user.user_id,
        email=user.email,
        username=user.username,
        created_at=user.created_at
    )
    
    return TokenResponse(
        access_token=access_token_jwt,
        token_type="bearer",
        user=user_response
    )

@app.get("/api/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """현재 로그인한 사용자 정보"""
    return UserResponse(
        user_id=current_user.user_id,
        email=current_user.email,
        username=current_user.username,
        created_at=current_user.created_at
    )

@app.post("/api/auth/logout")
async def logout():
    """로그아웃"""
    return {"message": "로그아웃 성공"}

# ==================== 기존 주식 API ====================

@app.get("/")
async def root():
    return {
        "message": "주식 정보 API 서버",
        "docs": "/docs",
        "version": "1.0.0",
        "token_status": "active" if access_token else "inactive"
    }

@app.get("/api/stock/current/{stock_code}")
async def get_current_price(stock_code: str):
    """현재가 조회"""
    global access_token, config
    
    if not access_token:
        token = get_access_token_sync()
        if not token:
            raise HTTPException(status_code=500, detail="인증 토큰 발급 실패")
    
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}",
        "appkey": config['REAL_APP_KEY'],
        "appsecret": config['REAL_APP_SECRET'],
        "tr_id": "FHKST01010100"
    }
    
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code
    }
    
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{config['REAL_URL']}/{PATH}"
    
    try:
        res = requests.get(URL, headers=headers, params=params, timeout=10)
        
        if res.status_code == 200:
            return res.json()
        else:
            raise HTTPException(status_code=res.status_code, detail="API 호출 실패")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/chart/{stock_code}")
async def get_stock_chart(stock_code: str, period: str = Query("D")):
    """차트 데이터 조회"""
    global access_token, config
    
    if not access_token:
        get_access_token_sync()
    
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}",
        "appkey": config['REAL_APP_KEY'],
        "appsecret": config['REAL_APP_SECRET'],
        "tr_id": "FHKST03010100"
    }
    
    end_date = datetime.now().strftime("%Y%m%d")
    period_days = {"D": 30, "W": 90, "M": 365, "Y": 365 * 3}
    days = period_days.get(period, 30)
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")
    
    params = {
        "fid_cond_mrkt_div_code": "J",
        "fid_input_iscd": stock_code,
        "fid_input_date_1": start_date,
        "fid_input_date_2": end_date,
        "fid_period_div_code": period,
        "fid_org_adj_prc": "0"
    }
    
    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{config['REAL_URL']}/{PATH}"
    
    try:
        res = requests.get(URL, headers=headers, params=params, timeout=10)
        if res.status_code == 200:
            return res.json()
        else:
            raise HTTPException(status_code=res.status_code, detail="차트 조회 실패")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/news/{stock_code}")
async def get_stock_news(stock_code: str):
    """뉴스 조회"""
    stock_names = {
        '005930': '삼성전자', '000660': 'SK하이닉스', '035420': 'NAVER',
        '035720': '카카오', '005380': '현대차', '051910': 'LG화학',
        '006400': '삼성SDI', '000270': '기아', '207940': '삼성바이오로직스',
        '068270': '셀트리온', '005490': 'POSCO홀딩스', '105560': 'KB금융',
        '055550': '신한지주', '012330': '현대모비스', '028260': '삼성물산'
    }
    
    stock_name = stock_names.get(stock_code, f"종목{stock_code}")
    
    try:
        search_query = quote(stock_name)
        news_url = f"https://news.google.com/rss/search?q={search_query}+주식&hl=ko&gl=KR&ceid=KR:ko"
        
        feed = feedparser.parse(news_url)
        
        news_items = []
        for entry in feed.entries[:10]:
            news_items.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', ''),
                'source': entry.get('source', {}).get('title', 'Unknown')
            })
        
        return {
            "success": True,
            "stock_name": stock_name,
            "news_count": len(news_items),
            "news": news_items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "token_exists": access_token is not None
    }

# 서버 실행
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )


# uvicorn app:app --reload --host 0.0.0.0 --port 8000