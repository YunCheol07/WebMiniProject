# 📈 주식 대시보드 Backend API

한국투자증권 OpenAPI를 활용한 실시간 주식 정보 제공 및 포트폴리오 관리 시스템입니다. FastAPI로 구축되었으며, JWT 기반 인증, 주식 데이터 조회, 관심 종목 및 포트폴리오 관리 기능을 제공합니다.

## 🌟 주요 기능

### 1️⃣ 인증 시스템
- **JWT 기반** 사용자 인증 (회원가입, 로그인, 로그아웃)
- **bcrypt**를 사용한 안전한 비밀번호 해싱
- 토큰 기반의 stateless 세션 관리

### 2️⃣ 주식 검색
- 종목명 또는 종목코드로 주식 검색
- 검색어 자동완성 기능 (우선순위 정렬)
- 전체 주식 목록 페이징 조회

### 3️⃣ 실시간 주식 데이터
- **현재가, 등락률, 거래량** 등 실시간 시세 조회
- **일/주/월/년** 기준 차트 데이터 조회
- 종목별 최신 뉴스 (Google News RSS)
- **코스피 시장 전체 뉴스** 조회 기능
- **시가총액 상위 종목** 실시간 조회 (TOP 50)

### 4️⃣ 관심 종목 (Watchlist)
- 사용자의 관심 종목 추가, 삭제, 목록 조회
- 특정 종목이 관심 목록에 포함되어 있는지 확인

### 5️⃣ 포트폴리오 관리
- 보유 주식 등록 (종목, 수량, 평균 매입가)
- **실시간 평가손익 및 수익률** 자동 계산
- 포트폴리오 전체 요약 정보 제공 (총 매입, 총 평가, 총 손익)
- 보유 종목 수정 및 삭제

---

## 🛠 기술 스택

- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL, SQLAlchemy (ORM)
- **Authentication**: JWT (python-jose), bcrypt (passlib)
- **API**: 한국투자증권 OpenAPI, Google News RSS (feedparser)
- **Data Validation**: Pydantic
- **Server**: Uvicorn (ASGI)
- **Others**: python-dotenv, pandas, openpyxl

---

## 📁 프로젝트 구조

```
backend/
├── app.py                      # FastAPI 메인 앱, 라우터 등록
├── config.py                   # 환경설정 (Pydantic Settings)
├── database.py                 # DB 모델(SQLAlchemy) 및 세션 관리
├── auth.py                     # 인증 유틸리티 (JWT, 해싱)
│
├── routers/                    # API 엔드포인트 (라우터)
│   ├── auth_router.py          # 인증 API (회원가입, 로그인)
│   ├── stock_router.py         # 주식 검색 및 정보 조회 API
│   ├── market_router.py        # 실시간 시세, 뉴스, TOP 종목 API
│   ├── watchlist_router.py     # 관심 종목 API
│   └── portfolio_router.py     # 포트폴리오 API
│
├── services/                   # 비즈니스 로직
│   └── korea_investment.py     # 한국투자증권 API 서비스 로직
│
├── schemas/                    # 데이터 검증 (Pydantic 스키마)
│   ├── user.py                 # 사용자 관련 스키마
│   └── stock.py                # 주식 관련 스키마
│
├── .env                        # 환경변수 파일 (보안)
├── requirements.txt            # Python 패키지 목록
├── load_stocks.py              # DB에 주식 종목 데이터 로드 스크립트
└── README.md                   # 프로젝트 문서
```

---

## 🚀 설치 및 실행

### 1. 사전 요구사항
- Python 3.11 이상
- PostgreSQL 14 이상
- 한국투자증권 API 키 (앱키, 앱시크릿, 계좌번호)

### 2. 환경 설정
```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 패키지 설치
pip install -r requirements.txt
```

### 3. 환경변수 설정
`.env` 파일을 생성하고 아래 내용을 채워주세요.

```env
# Database
DATABASE_URL="postgresql://<user>:<password>@<host>:<port>/<db_name>"

# JWT
SECRET_KEY="<your_strong_secret_key>"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

# 한국투자증권 API
REAL_APP_KEY="<your_app_key>"
REAL_APP_SECRET="<your_app_secret>"
REAL_URL="https://openapi.koreainvestment.com:9443"
REAL_CANO="<your_account_number>"
REAL_ACNT_PRDT_CD="01"

# CORS
CORS_ORIGINS='["http://localhost:5173","http://127.0.0.1:5173"]'

# Debug
DEBUG=True
```

### 4. 데이터베이스 설정
```bash
# 1. PostgreSQL에서 데이터베이스 생성
createdb stock_db

# 2. 테이블 생성
python database.py

# 3. 주식 종목 데이터 로드 (kospi_code_name.xlsx 파일 필요)
python load_stocks.py kospi_code_name.xlsx
```

### 5. 서버 실행
```bash
# 개발 모드 (hot-reload 지원)
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
서버 실행 후 `http://localhost:8000/docs`에서 API 문서를 확인할 수 있습니다.

---

## 📊 데이터베이스 스키마

### `users` (사용자)
- `user_id` (PK, UUID)
- `email` (UNIQUE)
- `password` (Hashed)
- `username`

### `stocks` (주식 종목)
- `stock_id` (PK)
- `stock_code` (UNIQUE)
- `stock_name`

### `watchlist` (관심 종목)
- `watchlist_id` (PK)
- `user_id` (FK)
- `stock_id` (FK)

### `portfolio` (포트폴리오)
- `portfolio_id` (PK)
- `user_id` (FK)
- `stock_id` (FK)
- `quantity` (보유 수량)
- `avg_price` (평균 매입가)
- `purchase_date` (매입일)

---

## 🔌 API 엔드포인트

- `[P]` = 비공개 (인증 필요)
- `[G]` = 공개

### 인증 (`/api/auth`)
- `POST /register`: 회원가입 `[G]`
- `POST /login`: 로그인 `[G]`
- `GET /me`: 현재 사용자 정보 `[P]`
- `POST /logout`: 로그아웃 `[G]`

### 주식 검색 (`/api/stocks`)
- `GET /search?q={query}`: 종목 검색 `[G]`
- `GET /list`: 전체 종목 목록 `[G]`
- `GET /{stock_code}`: 특정 종목 정보 `[G]`

### 시장 데이터 (`/api/stock`)
- `GET /current/{stock_code}`: 현재가 조회 `[G]`
- `GET /chart/{stock_code}`: 차트 데이터 조회 `[G]`
- `GET /news/{stock_code}`: 종목별 뉴스 `[G]`
- `GET /market-news`: 코스피 시장 뉴스 `[G]`
- `GET /top-stocks`: 시가총액 상위 종목 `[G]`

### 관심 종목 (`/api/watchlist`)
- `GET /`: 내 관심 종목 목록 `[P]`
- `POST /{stock_code}`: 관심 종목 추가 `[P]`
- `DELETE /{stock_code}`: 관심 종목 삭제 `[P]`
- `GET /check/{stock_code}`: 포함 여부 확인 `[P]`

### 포트폴리오 (`/api/portfolio`)
- `GET /`: 내 포트폴리오 조회 (실시간 손익 포함) `[P]`
- `POST /`: 보유 종목 추가 `[P]`
- `PUT /{portfolio_id}`: 보유 종목 수정 `[P]`
- `DELETE /{portfolio_id}`: 보유 종목 삭제 `[P]`

---

## 🔐 인증 방식

- **JWT (JSON Web Token)**를 사용합니다.
- 로그인 성공 시 `access_token`이 발급됩니다.
- 인증이 필요한 API를 호출할 때 HTTP Header에 아래와 같이 토큰을 포함해야 합니다.
  ```
  Authorization: Bearer {your_access_token}
  ```

---

## 👨‍💻 개발자

- **곽윤철**
- **Email**: kyc4061@daum.net
- **GitHub**: [https://github.com/YunCheol07](https://github.com/YunCheol07)
