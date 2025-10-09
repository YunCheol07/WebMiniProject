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

---

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

---

## 📁 프로젝트 구조

backend/  
├── app.py # FastAPI 메인 앱  
├── config.py # 환경설정  
├── database.py # DB 모델 및 연결  
├── auth.py # 인증 유틸리티  
│  
├── routers/ # API 라우터  
│ ├── init.py  
│ ├── auth_router.py # 인증 API  
│ ├── stock_router.py # 주식 검색 API  
│ ├── watchlist_router.py # 관심 종목 API  
│ ├── portfolio_router.py # 포트폴리오 API  
│ └── market_router.py # 실시간 주식 데이터 API  
│  
├── services/ # 비즈니스 로직  
│ ├── init.py  
│ └── korea_investment.py # 한국투자증권 API 서비스  
│  
├── schemas/ # Pydantic 스키마  
│ ├── init.py  
│ ├── user.py  
│ └── stock.py  
│  
├── .env # 환경변수 (gitignore)  
├── requirements.txt # Python 패키지  
├── load_stocks.py # 종목 데이터 로드 스크립트  
└── README.md  

---

## 🚀 설치 및 실행

### 1. 사전 요구사항

- Python 3.11 이상
- PostgreSQL 14 이상
- 한국투자증권 API 키 (앱키, 앱시크릿)

### 2. 환경 설정

가상환경 생성 및 활성화
python -m venv venv  
source venv/bin/activate # Windows: venv\Scripts\activate  

패키지 설치
pip install -r requirements.txt

### 3. 환경변수 설정

`.env` 파일 생성:

Database  
DATABASE_URL=postgresql://username:password@localhost:5432/stock_db  

JWT  
SECRET_KEY=your-secret-key-here  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=60  

한국투자증권 API  
REAL_APP_KEY=your-app-key  
REAL_APP_SECRET=your-app-secret  
REAL_URL=https://openapi.koreainvestment.com:9443  
REAL_CANO=your-account-number  
REAL_ACNT_PRDT_CD=01  

CORS  
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]  

Debug  
DEBUG=True  

### 4. 데이터베이스 설정

PostgreSQL 데이터베이스 생성
createdb stock_db

테이블 생성
python database.py

주식 종목 데이터 로드 (Excel 파일 필요)
python load_stocks.py kospi_code_name.xlsx

text

### 5. 서버 실행

개발 모드 (hot reload)
uvicorn app:app --reload --host 0.0.0.0 --port 8000

프로덕션 모드
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

text

서버 실행 후: `http://localhost:8000/docs` 에서 API 문서 확인 가능

---

## 📊 데이터베이스 스키마

### Users (사용자)
users
├── user_id (PK, UUID)
├── email (UNIQUE)
├── password (Hashed)
├── username
├── created_at
└── updated_at

text

### Stocks (주식 종목)
stocks
├── stock_id (PK)
├── stock_code (UNIQUE)
├── stock_name
├── created_at
└── updated_at

text

### Watchlist (관심 종목)
watchlist
├── watchlist_id (PK)
├── user_id (FK → users)
├── stock_id (FK → stocks)
├── added_at
├── alert_enabled
└── target_price

text

### Portfolio (포트폴리오)
portfolio
├── portfolio_id (PK)
├── user_id (FK → users)
├── stock_id (FK → stocks)
├── quantity
├── avg_price
├── purchase_date
└── created_at

text

---

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
| GET | `/chart/{stock_code}?period=D` | 차트 데이터 |
| GET | `/news/{stock_code}` | 관련 뉴스 |

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

---

## 🔐 인증 방식

### JWT 토큰 기반 인증

1. **로그인** → Access Token 발급
2. **API 요청** 시 Header에 토큰 포함
Authorization: Bearer {access_token}

text
3. **토큰 만료** 시 재로그인 필요

### 보호된 엔드포인트

- 관심 종목 API (전체)
- 포트폴리오 API (전체)
- `/api/auth/me`

---

## 📦 주요 라이브러리

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

---

## 🧪 테스트

### API 문서로 테스트
http://localhost:8000/docs

text

### cURL 예시

회원가입
curl -X POST "http://localhost:8000/api/auth/register"
-H "Content-Type: application/json"
-d '{
"email": "user@example.com",
"password": "password123",
"username": "홍길동"
}'

종목 검색
curl "http://localhost:8000/api/stocks/search?q=삼성"

현재가 조회 (토큰 필요 없음)
curl "http://localhost:8000/api/stock/current/005930"

포트폴리오 조회 (토큰 필요)
curl -X GET "http://localhost:8000/api/portfolio"
-H "Authorization: Bearer {your_token}"

---

## 🛡️ 보안

### 구현된 보안 기능

✅ 비밀번호 해싱 (bcrypt)
✅ JWT 토큰 인증
✅ CORS 설정
✅ SQL Injection 방지 (SQLAlchemy ORM)
✅ 입력 데이터 검증 (Pydantic)
✅ 환경변수로 민감 정보 관리

### 권장 사항

- `.env` 파일을 절대 커밋하지 마세요
- 프로덕션에서는 `DEBUG=False` 설정
- HTTPS 사용 필수
- 강력한 `SECRET_KEY` 생성

---

## 🚨 문제 해결

### 1. DB 연결 실패
PostgreSQL 실행 확인
sudo systemctl status postgresql

연결 테스트
psql -U postgres

text

### 2. 한국투자증권 API 토큰 오류
- 앱키/앱시크릿 확인
- API 사용 권한 확인
- 계좌번호 형식 확인

### 3. 종목 데이터 없음
종목 데이터 재로드
python load_stocks.py kospi_code_name.xlsx

---

## 📝 개발 로드맵

### ✅ 완료된 기능
- [x] 사용자 인증 시스템
- [x] 주식 검색 및 자동완성
- [x] 실시간 주식 데이터 조회
- [x] 관심 종목 관리
- [x] 포트폴리오 관리
- [x] 손익 계산 기능

### 🔜 향후 계획
- [ ] 주식 알림 기능
- [ ] 차트 분석 기능
- [ ] 거래 내역 관리
- [ ] 배당금 추적
- [ ] 백테스팅 기능
- [ ] Redis 캐싱
- [ ] WebSocket 실시간 데이터

---

## 👨‍💻 개발자

**곽윤철**
- Email: kyc4061@daum.net
- GitHub: [@YunCheol07](https://github.com/YunCheol07/WebMiniProject)

---

## 📄 라이선스

MIT License

---

## 🙏 감사의 말

- [한국투자증권](https://www.koreainvestment.com) - OpenAPI 제공
- [FastAPI](https://fastapi.tiangolo.com) - 뛰어난 프레임워크
- [SQLAlchemy](https://www.sqlalchemy.org) - 강력한 ORM

---
