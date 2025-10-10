# 웹 서비스 미니 프로젝트

# 📈 주식 대시보드 - Stock Dashboard

<div align="center">

![Vue.js](https://img.shields.io/badge/Vue.js-3.5.12-4FC08D?style=flat-square&logo=vue.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?style=flat-square&logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

**한국투자증권 OpenAPI를 활용한 실시간 주식 정보 제공 및 포트폴리오 관리 시스템**

[📖 문서](#-문서) • [🚀 시작하기](#-빠른-시작) • [✨ 기능](#-주요-기능) • [🛠 기술](#️-기술-스택)

</div>

---

## 📑 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [기술 스택](#️-기술-스택)
- [시스템 아키텍처](#-시스템-아키텍처)
- [빠른 시작](#-빠른-시작)
- [프로젝트 구조](#-프로젝트-구조)
- [주요 화면](#-주요-화면)
- [API 문서](#-api-문서)
- [데이터베이스](#-데이터베이스)
- [개발 가이드](#-개발-가이드)
- [문제 해결](#-문제-해결)
- [라이선스](#-라이선스)

---

## 🎯 프로젝트 소개

**주식 대시보드**는 개인 투자자를 위한 실시간 주식 정보 제공 및 포트폴리오 관리 웹 애플리케이션입니다.

### 개발 배경

- 복잡한 증권 앱 대신 **간편한 웹 기반 대시보드** 필요
- 여러 종목의 **수익률을 한눈에** 확인하고 싶은 요구
- **실시간 시가총액 순위** 모니터링 기능 부재
- 무료로 사용 가능한 **포트폴리오 관리 도구** 제공

### 핵심 가치

✅ **실시간성**: 한국투자증권 API를 통한 실시간 시세 제공  
✅ **직관성**: 다크 테마 기반 깔끔한 UI/UX  
✅ **편리성**: 원클릭 관심 종목 등록 및 포트폴리오 관리  
✅ **정확성**: 자동 계산되는 평가손익 및 수익률  

---

## 🌟 주요 기능

### 1. 사용자 인증 및 관리

- 🔐 **JWT 토큰 기반 인증**
  - 회원가입 / 로그인
  - 비밀번호 해싱 (bcrypt)
  - 자동 로그아웃 기능
- 👤 **개인화된 대시보드**
  - 사용자별 관심 종목
  - 사용자별 포트폴리오

### 2. 주식 검색 및 조회

- 🔍 **실시간 자동완성 검색**
  - 300ms 디바운싱으로 빠른 응답
  - 종목명/코드 통합 검색
  - 키보드 네비게이션 지원 (↑↓ Enter ESC)
- 📊 **종목 상세 정보**
  - 실시간 현재가
  - 차트 데이터 (일봉/주봉/월봉/연봉)
  - 투자지표 (PER, PBR, EPS, BPS)

### 3. 코스피 시가총액 TOP 20

- 📈 **실시간 시가총액 상위 20개 종목**
- 💹 **현재가, 등락률, 거래량, 시가총액** 한눈에 확인
- 🔄 **스크롤 가능한 종목 리스트** (헤더 고정)
- ❤️ **원클릭 관심 종목 추가**
- 🎯 **클릭 시 상세 정보로 이동**

### 4. 관심 종목 관리

- ⭐ **관심 종목 패널**
  - 즐겨찾는 종목 빠른 조회
  - 실시간 등락률 색상 구분
  - 하트 버튼으로 추가/삭제
- 📱 **반응형 레이아웃**

### 5. 포트폴리오 관리

- 💼 **보유 주식 등록 및 관리**
- 💰 **실시간 평가손익 자동 계산**
  - 평가손익 = (현재가 - 평균매입가) × 수량
  - 수익률 = ((현재가 - 평균매입가) / 평균매입가) × 100
- 📊 **수익률 분석**
  - 종목별 손익
  - 전체 포트폴리오 요약
- 🔍 **종목 자동완성 검색** (포트폴리오 추가 시)

### 6. 뉴스 피드

- 📰 **코스피 최신 뉴스** (Google News RSS)
- 📱 **우측 하단 뉴스 패널**
- 🔗 **클릭 시 원문 링크로 이동**

---

## 🛠️ 기술 스택

### Frontend

| 분류 | 기술 | 버전 | 용도 |
|------|------|------|------|
| **Framework** | Vue 3 | 3.5.12 | Composition API 기반 프론트엔드 |
| **Build Tool** | Vite | 5.4.9 | 초고속 빌드 및 HMR |
| **Routing** | Vue Router | 4.4.5 | SPA 라우팅 및 가드 |
| **State** | Pinia | 2.2.4 | 상태 관리 |
| **HTTP** | Axios | 1.7.7 | API 통신 |
| **Charts** | Chart.js | 4.4.6 | 차트 시각화 |
| **Styling** | CSS3 | - | 커스텀 다크 테마 |

### Backend

| 분류 | 기술 | 버전 | 용도 |
|------|------|------|------|
| **Framework** | FastAPI | 0.115.0 | 고성능 비동기 웹 프레임워크 |
| **Server** | Uvicorn | 0.32.0 | ASGI 서버 |
| **Database** | PostgreSQL | 14+ | 메인 데이터베이스 |
| **ORM** | SQLAlchemy | 2.0.35 | 데이터베이스 ORM |
| **Auth** | PyJWT | 3.3.0 | JWT 토큰 인증 |
| **Password** | Bcrypt | 1.7.4 | 비밀번호 해싱 |
| **Validation** | Pydantic | 2.9.2 | 데이터 검증 |
| **External API** | 한국투자증권 OpenAPI | - | 실시간 주식 데이터 |

### DevOps & Tools

- **Version Control**: Git, GitHub
- **API Documentation**: OpenAPI 3.0, Swagger UI
- **Database Tool**: pgAdmin, DBeaver
- **Testing**: Postman, curl
- **Package Manager**: npm, pip

---

## 🏗 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                         Client                              │
│                    (Vue 3 + Vite)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Dashboard   │  │  Portfolio   │  │  Watchlist   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/REST API (JWT Auth)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend Server                           │
│                   (FastAPI + Python)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Auth Router  │  │ Stock Router │  │Market Router │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────┬───────────────────┬──────────────────┬────────────┘
         │                   │                  │
         ▼                   ▼                  ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   PostgreSQL    │  │ Korea Investment│  │  Google News    │
│    Database     │  │      API        │  │      RSS        │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### 데이터 흐름

1. **사용자 인증**: 클라이언트 → FastAPI → PostgreSQL (사용자 검증)
2. **주식 조회**: 클라이언트 → FastAPI → 한국투자증권 API → 클라이언트
3. **포트폴리오**: 클라이언트 → FastAPI → PostgreSQL + 한국투자증권 API
4. **뉴스 조회**: 클라이언트 → FastAPI → Google News RSS → 클라이언트

---

## 🚀 빠른 시작

### 사전 요구사항

- Node.js 18 이상
- Python 3.11 이상
- PostgreSQL 14 이상
- 한국투자증권 API 키 ([발급 방법](https://www.koreainvestment.com))

### 1. 저장소 클론

```
git clone https://github.com/YunCheol07/WebMiniProject.git
cd WebMiniProject/StockProject
```

### 2. Backend 설정

```
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정 (.env 파일 생성)
cp .env.example .env
# .env 파일을 열어 다음 정보 입력:
# - DATABASE_URL
# - SECRET_KEY
# - REAL_APP_KEY
# - REAL_APP_SECRET

# 데이터베이스 생성 및 테이블 생성
createdb stock_db
python database.py

# 주식 종목 데이터 로드
python load_stocks.py kospi_code_name.xlsx

# 서버 실행
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**백엔드 실행 확인**: http://localhost:8000/docs

### 3. Frontend 설정

```
cd ../frontend

# 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```

**프론트엔드 실행 확인**: http://localhost:5173

### 4. 전체 시스템 실행

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API 문서: http://localhost:8000/docs

---

## 📁 프로젝트 구조

```
StockProject/
├── frontend/                    # Vue 3 프론트엔드
│   ├── src/
│   │   ├── assets/             # 정적 리소스
│   │   ├── components/         # Vue 컴포넌트
│   │   │   ├── StockSearch.vue        # 주식 검색
│   │   │   ├── StockInfo.vue          # 주식 상세 정보
│   │   │   ├── StockChart.vue         # 차트
│   │   │   ├── StockNews.vue          # 뉴스
│   │   │   ├── TopStocks.vue          # 시가총액 TOP 20
│   │   │   ├── WatchlistPanel.vue     # 관심 종목 패널
│   │   │   └── PortfolioPanel.vue     # 포트폴리오 패널
│   │   ├── views/              # 페이지 컴포넌트
│   │   │   ├── Login.vue              # 로그인
│   │   │   ├── Register.vue           # 회원가입
│   │   │   └── StockDashboard.vue     # 메인 대시보드
│   │   ├── stores/             # Pinia 스토어
│   │   │   └── auth.js                # 인증 상태
│   │   ├── router/             # 라우터
│   │   │   └── index.js               # 라우팅 설정
│   │   ├── App.vue             # 루트 컴포넌트
│   │   └── main.js             # 진입점
│   ├── package.json
│   └── vite.config.js
│
├── backend/                     # FastAPI 백엔드
│   ├── routers/                # API 라우터
│   │   ├── auth_router.py             # 인증 API
│   │   ├── stock_router.py            # 주식 검색 API
│   │   ├── market_router.py           # 실시간 데이터 API
│   │   ├── watchlist_router.py        # 관심 종목 API
│   │   └── portfolio_router.py        # 포트폴리오 API
│   ├── services/               # 비즈니스 로직
│   │   └── korea_investment.py        # 한국투자증권 API
│   ├── schemas/                # Pydantic 스키마
│   ├── app.py                  # FastAPI 메인 앱
│   ├── database.py             # DB 모델 및 연결
│   ├── auth.py                 # 인증 유틸리티
│   ├── config.py               # 환경설정
│   ├── requirements.txt        # Python 패키지
│   └── .env                    # 환경변수 (gitignore)
│
├── docs/                        # 문서
│   ├── API.md                  # API 명세서
│   ├── ERD.dbml                # 데이터베이스 ERD
│   └── openapi.yaml            # OpenAPI 명세
│
└── README.md                    # 프로젝트 README
```

---

## 📸 주요 화면

### 1. 로그인 / 회원가입

<table>
  <tr>
    <td width="50%">
      <img src="https://via.placeholder.com/600x400?text=Login+Page" alt="로그인" />
      <p align="center"><b>로그인 페이지</b></p>
    </td>
    <td width="50%">
      <img src="https://via.placeholder.com/600x400?text=Register+Page" alt="회원가입" />
      <p align="center"><b>회원가입 페이지</b></p>
    </td>
  </tr>
</table>

- 깔끔한 다크 테마 UI
- 실시간 입력 검증
- 에러 메시지 표시

### 2. 메인 대시보드

```
┌─────────────────────────────────────────────────────────────┐
│  🏠 주식 대시보드       [사용자명] 환영합니다! [로그아웃]     │
├─────────────────────────────────────────────────────────────┤
│  📈 주식 검색              ⭐ 관심 종목                      │
│  ┌──────────────────┐    ┌──────────────────────────────┐  │
│  │ [삼성전자_____🔍]│    │ -  삼성전자        +2.94%     │  │
│  │                  │    │ -  SK하이닉스      -0.18%     │  │
│  │ 선택: 삼성전자    │    │ -  카카오          +0%        │  │
│  └──────────────────┘    │ -  신한지주        +3.49%     │  │
│                          └──────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  📊 코스피 시가총액 TOP 20         │  💼 내 주식 현황        │
│  ┌─────────────────────────────┐  │  ┌──────────────────┐  │
│  │ 순위 종목명   현재가  등락률   │  │  총 매입: 316,000원│  │
│  │ ❤️ 1 삼성전자 89,000 +3.49%  │  │  총 평가: 475,200원│  │
│  │ 🤍 2 SK하이닉스 395,500 +9.86%│  │  평가손익: +159,200│  │
│  │ 🤍 3 LG에너지솔루션 399,000   │  │  (+50.38%)        │  │
│  │ ❤️ 4 삼성바이오 1,009,000    │  │                    │  │
│  │  ⋮  (스크롤 가능)            │  │  [+ 종목 추가]     │  │
│  └─────────────────────────────┘  └──────────────────────┘  │
│                                    📰 코스피 최신 뉴스       │
│                                    ┌──────────────────────┐ │
│                                    │ -  뉴스 제목 1...     │ │
│                                    └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 3. 코스피 시가총액 TOP 20

- **고정 헤더**: 제목과 컬럼명 항상 상단 고정
- **스크롤 영역**: 종목 리스트만 독립적으로 스크롤
- **실시간 업데이트**: 현재가, 등락률 실시간 반영
- **관심 종목 연동**: 하트 버튼 클릭으로 관심 종목 추가

### 4. 포트폴리오 관리

```
┌─────────────────────────────────────────────┐
│ 💼 내 주식 현황                [+ 종목 추가] │
├─────────────────────────────────────────────┤
│ 총 매입금액      총 평가금액     평가손익     │
│ 316,000원       475,200원      +159,200원    │
│                                (+50.38%)     │
├─────────────────────────────────────────────┤
│ 종목명   보유수량  평균매입가  현재가  손익   │
│ 카카오   2주     42,000원   59,600원  +35,200│
│ 삼성전자 4주     58,000원   89,000원  +124,000│
└─────────────────────────────────────────────┘
```

---

## 📚 API 문서

### 인증 API

| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| POST | `/api/auth/register` | 회원가입 | ❌ |
| POST | `/api/auth/login` | 로그인 | ❌ |
| GET | `/api/auth/me` | 현재 사용자 정보 | ✅ |
| POST | `/api/auth/logout` | 로그아웃 | ✅ |

### 주식 검색 API

| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| GET | `/api/stocks/search?q={query}` | 종목 검색 (자동완성) | ❌ |
| GET | `/api/stocks/{stock_code}` | 특정 종목 정보 | ❌ |
| GET | `/api/stocks/list?page=1&limit=20` | 전체 종목 목록 | ❌ |

### 실시간 데이터 API

| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| GET | `/api/stock/current/{stock_code}` | 현재가 조회 | ❌ |
| GET | `/api/stock/chart/{stock_code}?period=D` | 차트 데이터 | ❌ |
| GET | `/api/stock/news/{stock_code}` | 종목별 뉴스 | ❌ |
| GET | `/api/stock/market-news?limit=10` | 코스피 시장 뉴스 | ❌ |
| GET | `/api/stock/top-stocks?limit=20` | **시가총액 상위 종목** | ❌ |

### 관심 종목 API

| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| GET | `/api/watchlist` | 관심 종목 목록 | ✅ |
| POST | `/api/watchlist/{stock_code}` | 관심 종목 추가 | ✅ |
| DELETE | `/api/watchlist/{stock_code}` | 관심 종목 삭제 | ✅ |
| GET | `/api/watchlist/check/{stock_code}` | 포함 여부 확인 | ✅ |

### 포트폴리오 API

| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| GET | `/api/portfolio` | 포트폴리오 조회 (실시간 손익) | ✅ |
| POST | `/api/portfolio` | 보유 종목 추가 | ✅ |
| PUT | `/api/portfolio/{portfolio_id}` | 보유 종목 수정 | ✅ |
| DELETE | `/api/portfolio/{portfolio_id}` | 보유 종목 삭제 | ✅ |

**상세 API 문서**: http://localhost:8000/docs (Swagger UI)

---

## 🗄 데이터베이스

### ERD (Entity Relationship Diagram)

```
┌─────────────────┐       ┌─────────────────┐
│     users       │       │     stocks      │
├─────────────────┤       ├─────────────────┤
│ user_id (PK)    │       │ stock_id (PK)   │
│ email (UNIQUE)  │       │ stock_code      │
│ password        │       │ stock_name      │
│ username        │       └─────────────────┘
│ created_at      │                │
│ updated_at      │                │
└────────┬────────┘                │
         │                         │
         │ 1                       │ 1
         │                         │
         │ N                       │ N
         ▼                         ▼
┌─────────────────┐       ┌─────────────────┐
│   watchlist     │       │   portfolio     │
├─────────────────┤       ├─────────────────┤
│ watchlist_id(PK)│       │ portfolio_id(PK)│
│ user_id (FK)    │       │ user_id (FK)    │
│ stock_id (FK)   │       │ stock_id (FK)   │
│ added_at        │       │ quantity        │
└─────────────────┘       │ avg_price       │
                          │ purchase_date   │
                          │ created_at      │
                          └─────────────────┘
```

### 테이블 설명

#### users (사용자)
- **PK**: `user_id` (UUID)
- **Unique**: `email`
- **용도**: 사용자 계정 정보 저장

#### stocks (주식 종목)
- **PK**: `stock_id`
- **Unique**: `stock_code` (6자리 종목코드)
- **용도**: 주식 종목 마스터 데이터

#### watchlist (관심 종목)
- **PK**: `watchlist_id`
- **FK**: `user_id`, `stock_id`
- **Unique**: `(user_id, stock_id)` 조합
- **용도**: 사용자별 관심 종목 저장

#### portfolio (포트폴리오)
- **PK**: `portfolio_id`
- **FK**: `user_id`, `stock_id`
- **용도**: 보유 주식 정보 및 매입가 저장

---

## 👨‍💻 개발 가이드

### Frontend 개발

#### 새 컴포넌트 추가

```
# src/components/에 컴포넌트 생성
touch src/components/NewComponent.vue
```

```
<script setup>
import { ref } from 'vue'

const data = ref(null)
</script>

<template>
  <div class="new-component">
    <!-- 컴포넌트 내용 -->
  </div>
</template>

<style scoped>
.new-component {
  /* 스타일 */
}
</style>
```

#### API 호출

```
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

// GET 요청
const data = await axios.get(`${API_BASE}/stocks/search?q=삼성`)

// POST 요청 (인증 필요)
const token = localStorage.getItem('token')
await axios.post(`${API_BASE}/watchlist/005930`, null, {
  headers: { Authorization: `Bearer ${token}` }
})
```

### Backend 개발

#### 새 라우터 추가

```
# routers/new_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/api/new", tags=["새 기능"])

@router.get("/")
async def get_data(db: Session = Depends(get_db)):
    return {"message": "Hello"}
```

```
# app.py에 등록
from routers import new_router

app.include_router(new_router.router)
```

#### 데이터베이스 모델 추가

```
# database.py
class NewTable(Base):
    __tablename__ = "new_table"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=utc_now)
```

### 환경변수 관리

**Backend (.env)**
```
DATABASE_URL=postgresql://user:password@localhost:5432/stock_db
SECRET_KEY=your-secret-key-here
REAL_APP_KEY=your-korea-investment-app-key
REAL_APP_SECRET=your-korea-investment-app-secret
```

**Frontend (src/components/에서)**
```
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
```

---

## 🐛 문제 해결

### 1. CORS 에러

**증상**: 프론트엔드에서 백엔드 API 호출 시 CORS 오류

**해결**:
```
# backend/app.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. 데이터베이스 연결 실패

**증상**: `Connection refused` 오류

**해결**:
```
# PostgreSQL 실행 확인
sudo systemctl status postgresql  # Linux
brew services list | grep postgresql  # Mac
Get-Service postgresql*  # Windows

# 데이터베이스 생성 확인
psql -U postgres -c "\l" | grep stock_db
```

### 3. 한국투자증권 API 토큰 오류

**증상**: `401 Unauthorized` 또는 토큰 발급 실패

**해결**:
1. `.env` 파일에서 `REAL_APP_KEY`, `REAL_APP_SECRET` 확인
2. 한국투자증권 홈페이지에서 API 사용 권한 확인
3. 로그 확인: `logger.info("🔑 토큰 발급 시도")`

### 4. 가상환경 경로 오류 (Windows)

**증상**: `Unable to create process using` 오류

**해결**:
```
# 가상환경 재생성
deactivate
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 5. 포트 충돌

**증상**: `Address already in use` 오류

**해결**:
```
# 포트 사용 프로세스 확인 및 종료
# Linux/Mac
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 🚀 배포

### Frontend 배포 (Vercel)

```
cd frontend

# 빌드
npm run build

# Vercel 배포
npm install -g vercel
vercel --prod
```

### Backend 배포 (Heroku)

```
cd backend

# Procfile 생성
echo "web: uvicorn app:app --host 0.0.0.0 --port \$PORT" > Procfile

# Heroku 배포
heroku create stock-dashboard-api
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

### 환경변수 설정

**Vercel (Frontend)**
```
VITE_API_URL=https://stock-dashboard-api.herokuapp.com/api
```

**Heroku (Backend)**
```
heroku config:set SECRET_KEY=your-secret-key
heroku config:set REAL_APP_KEY=your-app-key
heroku config:set REAL_APP_SECRET=your-app-secret
```

---

## 📊 성능 최적화

### Frontend

✅ **구현된 최적화**
- 300ms 디바운싱 (검색)
- Lazy Loading (라우트 코드 스플리팅)
- 컴포넌트 분리 (재사용성)
- LocalStorage 토큰 저장

### Backend

✅ **구현된 최적화**
- 비동기 처리 (FastAPI)
- 데이터베이스 인덱스 (stock_code, email)
- Connection Pool (PostgreSQL)
- API 타임아웃 설정 (10초)

### 향후 개선 방안

- [ ] Redis 캐싱 (TOP 20 종목)
- [ ] WebSocket 실시간 데이터 스트리밍
- [ ] CDN 적용
- [ ] 이미지 최적화 (WebP)

---

## 📄 라이선스

MIT License

Copyright (c) 2025 곽윤철

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

---

## 👨‍💻 개발자

**곽윤철 (Kwak Yun Cheol)**

- 📧 Email: kyc4061@daum.net
- 🐙 GitHub: [@YunCheol07](https://github.com/YunCheol07)
- 📂 Repository: [WebMiniProject](https://github.com/YunCheol07/WebMiniProject)

---

## 🙏 감사의 말

이 프로젝트는 다음 오픈소스 및 서비스 덕분에 가능했습니다:

- [한국투자증권](https://www.koreainvestment.com) - OpenAPI 제공
- [FastAPI](https://fastapi.tiangolo.com) - 뛰어난 웹 프레임워크
- [Vue.js](https://vuejs.org) - 직관적인 프론트엔드 프레임워크
- [Chart.js](https://www.chartjs.org) - 강력한 차트 라이브러리
- [Google News](https://news.google.com) - RSS 뉴스 피드

---

## 📈 개발 로드맵

### ✅ 완료된 기능 (v1.1.0)

- [x] 사용자 인증 시스템
- [x] 주식 검색 및 자동완성
- [x] 실시간 주식 데이터 조회
- [x] 관심 종목 관리
- [x] 포트폴리오 관리
- [x] 시가총액 TOP 20 조회
- [x] 코스피 시장 뉴스 피드
- [x] 차트 시각화

### 🔜 향후 계획 (v1.2.0)

- [ ] 다크/라이트 테마 토글
- [ ] 모바일 반응형 최적화
- [ ] PWA 지원
- [ ] 실시간 알림 (WebSocket)
- [ ] 여러 종목 차트 비교
- [ ] 포트폴리오 엑셀 내보내기
- [ ] 종목별 메모 기능
- [ ] 거래 내역 관리
- [ ] 배당금 추적
- [ ] 백테스팅 기능

---

## 🎯 기여 가이드

이슈 제보 및 Pull Request는 언제나 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

<div align="center">

**⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요! ⭐**

Made with ❤️ by [곽윤철](https://github.com/YunCheol07)

</div>


