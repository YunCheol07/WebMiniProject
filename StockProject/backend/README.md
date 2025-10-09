# 📈 주식 대시보드 Backend API

한국투자증권 OpenAPI를 활용한 실시간 주식 정보 제공 및 포트폴리오 관리 시스템

## 🌟 주요 기능

### 1️⃣ 인증 시스템
- JWT 기반 사용자 인증
- 회원가입 / 로그인
- 비밀번호 해싱 (bcrypt)
- 토큰 기반 세션 관리

### 2️⃣ 주식 검색
- 종목명 / 종목코드 검색
- 자동완성 기능
- 우선순위 기반 정렬
- 전체 종목 목록 조회

### 3️⃣ 실시간 주식 데이터
- 현재가 조회
- 차트 데이터 (일봉/주봉/월봉/연봉)
- 주식 관련 뉴스 (Google News RSS)
- **코스피 시장 뉴스 조회** ✨
- **시가총액 상위 종목 조회** ✨
- 한국투자증권 API 연동

### 4️⃣ 관심 종목
- 관심 종목 추가/삭제
- 관심 종목 목록 조회
- 사용자별 관리

### 5️⃣ 포트폴리오
- 보유 주식 등록
- 실시간 평가손익 계산
- 수익률 분석
- 포트폴리오 요약 정보

***

## 🛠 기술 스택

### Backend Framework
- **FastAPI** 0.115.0 - 고성능 비동기 웹 프레임워크
- **Python** 3.11+

### Database
- **PostgreSQL** - 메인 데이터베이스
- **SQLAlchemy** 2.0 - ORM
- **Alembic** - 데이터베이스 마이그레이션

### 인증
- **JWT (PyJWT)** - 토큰 기반 인증
- **Bcrypt** - 비밀번호 해싱

### 외부 API
- **한국투자증권 OpenAPI** - 실시간 주식 데이터
- **Google News RSS** - 주식 뉴스

### 기타
- **Pydantic** - 데이터 검증
- **python-dotenv** - 환경변수 관리
- **uvicorn** - ASGI 서버
- **feedparser** - RSS 뉴스 파싱

***

## 📁 프로젝트 구조

```
backend/
├── app.py                      # FastAPI 메인 앱
├── config.py                   # 환경설정
├── database.py                 # DB 모델 및 연결
├── auth.py                     # 인증 유틸리티
│
├── routers/                    # API 라우터
│   ├── __init__.py
│   ├── auth_router.py          # 인증 API
│   ├── stock_router.py         # 주식 검색 API
│   ├── watchlist_router.py     # 관심 종목 API
│   ├── portfolio_router.py     # 포트폴리오 API
│   └── market_router.py        # 실시간 주식 데이터 API
│
├── services/                   # 비즈니스 로직
│   ├── __init__.py
│   └── korea_investment.py     # 한국투자증권 API 서비스
│
├── schemas/                    # Pydantic 스키마
│   ├── __init__.py
│   ├── user.py
│   └── stock.py
│
├── .env                        # 환경변수 (gitignore)
├── requirements.txt            # Python 패키지
├── load_stocks.py              # 종목 데이터 로드 스크립트
└── README.md
```

***

## 🚀 설치 및 실행

### 1. 사전 요구사항

- Python 3.11 이상
- PostgreSQL 14 이상
- 한국투자증권 API 키 (앱키, 앱시크릿)

### 2. 환경 설정

**가상환경 생성 및 활성화**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**패키지 설치**
```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

`.env` 파일 생성:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/stock_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# 한국투자증권 API
REAL_APP_KEY=your-app-key
REAL_APP_SECRET=your-app-secret
REAL_URL=https://openapi.koreainvestment.com:9443
REAL_CANO=your-account-number
REAL_ACNT_PRDT_CD=01

# CORS
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# Debug
DEBUG=True
```

### 4. 데이터베이스 설정

**PostgreSQL 데이터베이스 생성**
```bash
createdb stock_db
```

**테이블 생성**
```bash
python database.py
```

**주식 종목 데이터 로드 (Excel 파일 필요)**
```bash
python load_stocks.py kospi_code_name.xlsx
```

### 5. 서버 실행

**개발 모드 (hot reload)**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**프로덕션 모드**
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

서버 실행 후: `http://localhost:8000/docs` 에서 API 문서 확인 가능

***

## 📊 데이터베이스 스키마

### Users (사용자)
```
users
├── user_id (PK, UUID)
├── email (UNIQUE)
├── password (Hashed)
├── username
├── created_at
└── updated_at
```

### Stocks (주식 종목)
```
stocks
├── stock_id (PK)
├── stock_code (UNIQUE)
├── stock_name
├── created_at
└── updated_at
```

### Watchlist (관심 종목)
```
watchlist
├── watchlist_id (PK)
├── user_id (FK → users)
├── stock_id (FK → stocks)
├── added_at
├── alert_enabled
└── target_price
```

### Portfolio (포트폴리오)
```
portfolio
├── portfolio_id (PK)
├── user_id (FK → users)
├── stock_id (FK → stocks)
├── quantity
├── avg_price
├── purchase_date
└── created_at
```

***

## 🔌 API 엔드포인트

### 인증 API (`/api/auth`)

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/register` | 회원가입 |
| POST | `/login` | 로그인 |
| GET | `/me` | 현재 사용자 정보 |
| POST | `/logout` | 로그아웃 |

### 주식 검색 API (`/api/stocks`)

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/search?q={query}` | 종목 검색 (자동완성) |
| GET | `/{stock_code}` | 특정 종목 정보 |
| GET | `/list?page=1&limit=20` | 전체 종목 목록 |

### 실시간 데이터 API (`/api/stock`)

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/current/{stock_code}` | 현재가 조회 |
| GET | `/chart/{stock_code}?period=D` | 차트 데이터 (D/W/M/Y) |
| GET | `/news/{stock_code}` | 종목별 뉴스 조회 |
| GET | `/market-news?limit=10` | **코스피 시장 뉴스** ✨ |
| GET | `/top-stocks?limit=20` | **시가총액 상위 종목** ✨ |

### 관심 종목 API (`/api/watchlist`)

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/` | 관심 종목 목록 |
| POST | `/{stock_code}` | 관심 종목 추가 |
| DELETE | `/{stock_code}` | 관심 종목 삭제 |
| GET | `/check/{stock_code}` | 포함 여부 확인 |

### 포트폴리오 API (`/api/portfolio`)

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/` | 포트폴리오 조회 (실시간 손익 포함) |
| POST | `/` | 보유 종목 추가 |
| PUT | `/{portfolio_id}` | 보유 종목 수정 |
| DELETE | `/{portfolio_id}` | 보유 종목 삭제 |

***

## ✨ 신규 API 상세 설명

### 1. 코스피 시장 뉴스 조회

```http
GET /api/stock/market-news?limit=10
```

**설명**: Google News RSS를 통해 코스피 시장 전체 뉴스를 조회합니다.[1]

**Parameters**:
- `limit` (optional): 조회할 뉴스 개수 (기본값: 10, 최대: 30)

**Response**:
```json
{
  "success": true,
  "count": 10,
  "news": [
    {
      "title": "코스피, 외국인 매수세에 상승 마감",
      "link": "https://news.google.com/...",
      "published": "2025-10-09T14:30:00Z",
      "source": "매일경제"
    }
  ]
}
```

### 2. 시가총액 상위 종목 조회

```http
GET /api/stock/top-stocks?limit=20
```

**설명**: 2025년 10월 기준 코스피 시가총액 상위 종목을 실시간으로 조회합니다.[2]

**주요 특징**:
- 🏆 **정확한 순위**: 2025년 10월 기준 코스피 시가총액 TOP 30 하드코딩
- 💹 **실시간 데이터**: 한국투자증권 API로 현재가, 등락률 실시간 조회
- 📊 **시가총액 계산**: 현재가 × 상장주식수로 정확한 시가총액 계산
- 🔢 **동적 정렬**: API 응답 후 실제 시가총액 기준 재정렬
- 📝 **포맷팅**: "조원", "억원" 단위로 읽기 쉽게 표시

**Parameters**:
- `limit` (optional): 조회할 종목 개수 (기본값: 20, 최대: 50)

**Response**:
```json
{
  "success": true,
  "count": 20,
  "stocks": [
    {
      "rank": 1,
      "stock_code": "005930",
      "stock_name": "삼성전자",
      "current_price": 89000,
      "change": 3000,
      "change_rate": 3.49,
      "volume": 15234567,
      "market_cap": 532000000000000,
      "market_cap_formatted": "532.0조원"
    }
  ]
}
```

**포함된 TOP 30 종목** (2025년 10월 기준):
1. 삼성전자 (005930)
2. SK하이닉스 (000660)
3. LG에너지솔루션 (373220)
4. 삼성바이오로직스 (207940)
5. 삼성전자우 (005935)
6. 한화에어로스페이스 (012450)
7. HD현대중공업 (329180)
8. 현대차 (005380)
9. KB금융 (105560)
10. 두산에너빌리티 (034020)
11. 기아 (000270)
12. 셀트리온 (068270)
13. NAVER (035420)
14. 신한지주 (055550)
15. 한화오션 (042660)
16. 삼성물산 (028260)
17. 삼성생명 (032830)
18. SK스퀘어 (402340)
19. HD한국조선해양 (009540)
20. 현대모비스 (012330)
21. 카카오 (035720)
22. 하나금융지주 (086790)
23. 한국전력공사 (015760)
24. POSCO홀딩스 (005490)
25. LG화학 (051910)
26. HD현대일렉트릭 (267260)
27. HMM (011200)
28. 메리츠금융지주 (287410)
29. LG전자 (066570)
30. SK이노베이션 (096770)

***

## 🔧 Korea Investment Service 업데이트

### 신규 메서드: `get_stock_info()`

**기능**: 종목 기본 정보 + 시가총액 계산

```python
def get_stock_info(self, stock_code: str) -> Dict[str, Any]:
    """
    종목 기본 정보 조회 (시가총액 포함)
    
    Returns:
        - stock_code: 종목코드
        - current_price: 현재가
        - change: 전일대비
        - change_rate: 등락률 (%)
        - volume: 거래량
        - market_cap: 시가총액 (원)
        - listed_shares: 상장주식수
        - per: PER
        - pbr: PBR
    """
```

**기존 메서드와 차이점**:

| 메서드 | 용도 | 반환 데이터 |
|--------|------|------------|
| `get_current_price()` | 현재가만 간단히 조회 | API 원본 응답 전체 |
| `get_stock_info()` | 시가총액 계산 포함 상세 정보 | 정제된 핵심 데이터 + 계산값 |

***

## 🔐 인증 방식

### JWT 토큰 기반 인증

1. **로그인** → Access Token 발급
2. **API 요청** 시 Header에 토큰 포함
```
Authorization: Bearer {access_token}
```
3. **토큰 만료** 시 재로그인 필요

### 보호된 엔드포인트

- 관심 종목 API (전체)
- 포트폴리오 API (전체)
- `/api/auth/me`

### 공개 엔드포인트

- `/api/stock/current/{stock_code}` ✅
- `/api/stock/chart/{stock_code}` ✅
- `/api/stock/news/{stock_code}` ✅
- `/api/stock/market-news` ✅
- `/api/stock/top-stocks` ✅

***

## 📦 주요 라이브러리

```
fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.35
psycopg2-binary==2.9.10
pydantic==2.9.2
pydantic-settings==2.6.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.1
pandas==2.2.3
openpyxl==3.1.5
feedparser==6.0.11
requests==2.32.3
```

***

## 🧪 테스트

### API 문서로 테스트
```
http://localhost:8000/docs
```

### cURL 예시

**회원가입**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "username": "홍길동"
  }'
```

**종목 검색**
```bash
curl "http://localhost:8000/api/stocks/search?q=삼성"
```

**현재가 조회 (토큰 불필요)**
```bash
curl "http://localhost:8000/api/stock/current/005930"
```

**시가총액 TOP 20 조회** ✨
```bash
curl "http://localhost:8000/api/stock/top-stocks?limit=20"
```

**코스피 시장 뉴스** ✨
```bash
curl "http://localhost:8000/api/stock/market-news?limit=10"
```

**포트폴리오 조회 (토큰 필요)**
```bash
curl -X GET "http://localhost:8000/api/portfolio" \
  -H "Authorization: Bearer {your_token}"
```

***

## 🛡️ 보안

### 구현된 보안 기능

✅ 비밀번호 해싱 (bcrypt)  
✅ JWT 토큰 인증  
✅ CORS 설정  
✅ SQL Injection 방지 (SQLAlchemy ORM)  
✅ 입력 데이터 검증 (Pydantic)  
✅ 환경변수로 민감 정보 관리  
✅ API 타임아웃 설정 (10초)  
✅ 로깅을 통한 에러 추적  

### 권장 사항

- `.env` 파일을 절대 커밋하지 마세요
- 프로덕션에서는 `DEBUG=False` 설정
- HTTPS 사용 필수
- 강력한 `SECRET_KEY` 생성
- 한국투자증권 API 키 보안 유지

***

## 🚨 문제 해결

### 1. DB 연결 실패
```bash
# PostgreSQL 실행 확인
sudo systemctl status postgresql

# 연결 테스트
psql -U postgres
```

### 2. 한국투자증권 API 토큰 오류
- 앱키/앱시크릿 확인
- API 사용 권한 확인
- 계좌번호 형식 확인
- 로그 확인: `logger.info("🔑 토큰 발급 시도")`

### 3. 종목 데이터 없음
```bash
# 종목 데이터 재로드
python load_stocks.py kospi_code_name.xlsx
```

### 4. TOP 20 조회 시 일부 종목 누락
- DB에 해당 종목 코드가 등록되어 있는지 확인
- 로그에서 `logger.warning("DB에 없는 종목")` 메시지 확인
- API 호출 실패 종목은 자동으로 건너뜀

### 5. 시가총액 계산 오류
- 상장주식수(`lstn_stcn`) 필드가 0인 경우 시가총액도 0으로 표시
- 한국투자증권 API 응답 확인 필요

***

## 📝 개발 로드맵

### ✅ 완료된 기능
- [x] 사용자 인증 시스템
- [x] 주식 검색 및 자동완성
- [x] 실시간 주식 데이터 조회
- [x] 관심 종목 관리
- [x] 포트폴리오 관리
- [x] 손익 계산 기능
- [x] **시가총액 상위 종목 조회** ✨
- [x] **코스피 시장 뉴스 피드** ✨
- [x] **종목별 상세 정보 (시가총액, PER, PBR)** ✨

### 🔜 향후 계획
- [ ] 주식 알림 기능
- [ ] 차트 분석 기능 (기술적 지표)
- [ ] 거래 내역 관리
- [ ] 배당금 추적
- [ ] 백테스팅 기능
- [ ] Redis 캐싱 (TOP 20 캐싱)
- [ ] WebSocket 실시간 데이터 스트리밍
- [ ] 시가총액 순위 변동 히스토리
- [ ] 업종별 상위 종목 조회
- [ ] 거래대금 상위 종목

***

## 🎯 성능 최적화 팁

### TOP 20 조회 최적화

**현재 방식**:
- 30개 종목 조회 → 시가총액 기준 정렬 → 상위 20개 선택
- 일부 종목 API 실패 대비 여유분 확보

**향후 개선 방안**:
```python
# Redis 캐싱 (5분 TTL)
@router.get("/top-stocks")
@cache(expire=300)
async def get_top_stocks():
    ...
```

### 뉴스 조회 최적화
- RSS 파싱 결과 캐싱 (10분)
- 비동기 처리로 응답 속도 개선

---

## 👨‍💻 개발자

**곽윤철**
- Email: kyc4061@daum.net
- GitHub: [@YunCheol07](https://github.com/YunCheol07/WebMiniProject)

***

## 📄 라이선스

MIT License

***

## 🙏 감사의 말

- [한국투자증권](https://www.koreainvestment.com) - OpenAPI 제공
- [FastAPI](https://fastapi.tiangolo.com) - 뛰어난 프레임워크
- [SQLAlchemy](https://www.sqlalchemy.org) - 강력한 ORM
- [Google News](https://news.google.com) - RSS 뉴스 피드 제공

***

## 📋 변경 이력

### v1.1.0 (2025-10-09)
- ✨ **시가총액 상위 종목 조회 API 추가** (`/api/stock/top-stocks`)
- ✨ **코스피 시장 뉴스 API 추가** (`/api/stock/market-news`)
- ✨ **종목 상세 정보 조회 메서드 추가** (`get_stock_info()`)
- 🔧 시가총액 자동 계산 기능 (현재가 × 상장주식수)
- 📊 시가총액 포맷팅 기능 (조원/억원 단위)
- 🏆 2025년 10월 기준 코스피 TOP 30 종목 반영

### v1.0.0 (Initial Release)
- 기본 인증 시스템
- 주식 검색 및 조회
- 관심 종목 관리
- 포트폴리오 관리

***

<div align="center">

**⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요! ⭐**

</div>

[1](https://www.promleeblog.com/blog/post/313-1-setting-up-vue-3)
[2](https://trytoso.tistory.com/entry/Vue-Vite-%EB%A9%80%ED%8B%B0-%EB%AA%A8%EB%93%88-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EA%B5%AC%EC%A1%B0-%EC%99%84%EB%B2%BD-%EA%B0%80%EC%9D%B4%EB%93%9C)