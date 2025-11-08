# 🎨 주식 대시보드 Frontend (Vue 3 + Vite)

FastAPI 백엔드와 연동되는 실시간 주식 정보 대시보드 웹 애플리케이션입니다. Vue 3 (Composition API)와 Vite를 기반으로 구축되었으며, Pinia를 사용한 상태 관리, Vue Router를 통한 SPA 라우팅, Chart.js를 이용한 데이터 시각화 기능을 갖추고 있습니다.

## 🌟 주요 기능

### 1️⃣ 인증 및 라우팅
- **JWT 기반 인증**: 로그인, 회원가입 및 토큰 기반 세션 관리.
- **라우터 가드**: 인증 상태에 따라 특정 페이지 접근을 제어 (`/login`, `/` 등).
- **자동 리다이렉트**: 인증되지 않은 사용자는 로그인 페이지로, 이미 로그인한 사용자는 대시보드로 안내.

### 2️⃣ 핵심 대시보드
- **통합 검색**: 종목명/코드로 주식을 검색하고 자동완성 목록 제공. (Debouncing 적용)
- **시가총액 TOP 20**: 실시간 시가총액 상위 종목을 조회하고, 클릭 시 상세 정보 확인.
- **포트폴리오 관리**: 보유 주식을 추가/삭제하고, 실시간 평가손익 및 수익률 자동 계산.
- **관심 종목**: 자주 보는 종목을 등록하고 빠르게 조회.
- **코스피 뉴스**: 실시간 시장 뉴스를 확인.

### 3️⃣ 주식 상세 정보 (모달)
- **실시간 시세**: 현재가, 등락률, 거래량 등 상세 정보 표시.
- **주가 차트**: Chart.js를 활용하여 기간별(1개월/3개월/1년/3년) 주가 차트 시각화.
- **관련 뉴스**: 선택된 종목과 관련된 최신 뉴스 목록 제공.
- **투자지표**: PER, PBR 등 주요 투자지표 확인.

### 4️⃣ UI/UX
- **다크 테마**: 사용자의 눈 피로도를 줄이는 일관된 다크 모드 UI.
- **반응형 레이아웃**: Grid와 Flexbox를 사용해 다양한 화면 크기에 대응.
- **컴포넌트 기반 설계**: 재사용 가능하고 관리하기 쉬운 컴포넌트로 구성.

---

## 🛠 기술 스택

- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **State Management**: Pinia (via `useAuth` composable)
- **Routing**: Vue Router
- **HTTP Client**: Axios
- **Charting**: Chart.js
- **Styling**: CSS3 (Scoped Styles)

---

## 📁 프로젝트 구조

```
frontend/
├── src/
│   ├── assets/               # CSS, 이미지 등 정적 파일
│   ├── components/           # 재사용 가능한 Vue 컴포넌트
│   │   ├── StockSearch.vue   # 주식 검색 (헤더)
│   │   ├── TopStocks.vue     # 시가총액 TOP 20 (좌측 패널)
│   │   ├── PortfolioPanel.vue# 포트폴리오 (우측 패널)
│   │   ├── WatchlistPanel.vue# 관심 종목 (검색창 하단)
│   │   ├── MarketNews.vue    # 시장 뉴스 (우측 패널)
│   │   ├── StockInfo.vue     # 종목 상세 정보 (모달)
│   │   └── StockChart.vue    # 주가 차트 (모달)
│   │
│   ├── views/                # 페이지 단위 컴포넌트
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   └── StockDashboard.vue
│   │
│   ├── stores/               # 상태 관리 (Pinia)
│   │   └── auth.js           # (useAuth 훅으로 구현됨)
│   │
│   ├── router/               # 라우팅 설정
│   │   └── index.js
│   │
│   ├── App.vue               # 애플리케이션 루트 컴포넌트
│   └── main.js               # 앱 진입점 (Vue 인스턴스 생성)
│
├── .gitignore
├── index.html
├── package.json
└── vite.config.js
```

---

## 🚀 설치 및 실행

### 1. 사전 요구사항
- Node.js 18+
- npm 또는 yarn
- 백엔드 서버 실행 (기본 `http://localhost:8000`)

### 2. 설치
```bash
# 의존성 패키지 설치
npm install
```

### 3. 개발 서버 실행
```bash
npm run dev
```
이제 브라우저에서 `http://localhost:5173`으로 접속할 수 있습니다.

### 4. 프로덕션 빌드
```bash
npm run build
```
빌드 결과물은 `dist` 폴더에 생성됩니다.

---

## 🔌 API 연동

- 모든 API 요청은 `axios`를 통해 이루어집니다.
- `stores/auth.js`에서 로그인 성공 시 `axios`의 기본 헤더에 `Authorization: Bearer {token}`을 설정하여, 이후 모든 요청에 인증 토큰이 자동으로 포함됩니다.
- API 기본 URL은 각 컴포넌트 내의 `API_BASE` 상수에 정의되어 있습니다 (`http://localhost:8000/api`).

---

## 🔐 상태 관리 및 인증

- **`stores/auth.js`**: `useAuth`라는 Composable 함수 형태로 인증 로직을 구현했습니다.
  - `user`, `token` 상태를 `ref`로 관리합니다.
  - `login`, `register`, `logout`, `fetchUser` 등의 함수를 제공합니다.
  - `localStorage`에 토큰을 저장하여 로그인 상태를 유지합니다.
- **`router/index.js`**: `beforeEach` 가드를 사용하여 라우트 이동 시 인증 상태를 체크합니다.
  - `meta: { requiresAuth: true }`: 로그인이 필요한 페이지
  - `meta: { requiresGuest: true }`: 로그인하지 않은 상태에서만 접근 가능한 페이지

---

## 🎨 스타일링

- 전체적으로 **다크 테마**를 적용하여 통일성을 유지했습니다.
- 각 컴포넌트의 `<style>` 태그에 `scoped` 속성을 사용하여 CSS가 해당 컴포넌트에만 적용되도록 캡슐화했습니다.
- 주 색상은 녹색(`--primary-green`)으로, 상승/수익은 붉은색, 하락/손실은 파란색으로 표현하여 시각적 직관성을 높였습니다.
