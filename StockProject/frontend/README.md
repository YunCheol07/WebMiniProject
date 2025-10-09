# 🎨 실시간 주식 대시보드 (Vue 3 + Vite)
<p align="center">
<img src="https://img.shields.io/badge/Vue.js-3.4.29-4FC08D?style=for-the-badge&logo=vue.js" alt="Vue.js">
<img src="https://img.shields.io/badge/Vite-5.3.1-646CFF?style=for-the-badge&logo=vite" alt="Vite">
<img src="https://img.shields.io/badge/Pinia-2.1.7-FFD83A?style=for-the-badge&logo=pinia" alt="Pinia">
<img src="https://img.shields.io/badge/Chart.js-4.4.3-FF6384?style=for-the-badge&logo=chart.js" alt="Chart.js">
<img src="https://img.shields.io/badge/Axios-1.7.2-5A29E4?style=for-the-badge&logo=axios" alt="Axios">
<img src="https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge" alt="License">
</p>

Vue 3와 Vite를 기반으로 구축된 실시간 주식 정보 대시보드 웹 애플리케이션입니다.  
JWT 인증, 실시간 주식 검색, 포트폴리오 관리 등 다양한 기능을 제공하며 다크 테마 기반의 사용자 친화적인 UI를 자랑합니다.  

목차
주요 기능

메인 화면

기술 스택

프로젝트 구조

시작하기

API 엔드포인트

아키텍처 및 스타일 가이드

향후 개발 계획

라이선스

기여하기

🌟 주요 기능
1️⃣ 인증 & 사용자 관리
🔐 회원가입 / 로그인: JWT 토큰 기반의 안전한 인증 시스템

👤 프로필 관리: 사용자 정보 관리 기능

🚪 자동 로그아웃: 토큰 만료 시 자동 로그아웃 및 로그인 페이지로 리디렉션

2️⃣ 주식 검색 & 관심 종목
🔍 실시간 자동완성 검색: 종목명/코드로 즉시 검색 (300ms 디바운싱 적용)

❤️ 원클릭 관심 종목: 하트 버튼으로 손쉽게 관심 종목 추가/삭제

⭐ 관심 종목 패널: 즐겨찾는 종목의 등락률을 한눈에 모아보기

3️⃣ 시가총액 TOP 20
📈 실시간 순위: 코스피 시가총액 상위 20개 종목을 실시간 데이터로 제공

🔄 고정 헤더 & 스크롤: 스크롤 시에도 컬럼 헤더가 고정되어 가독성 향상

🎯 상세 정보 연동: 종목 클릭 시 해당 종목의 상세 정보 페이지로 이동

4️⃣ 포트폴리오 관리
💼 보유 주식 관리: 보유 주식의 수량, 평균 매입가 등록 및 관리

💰 실시간 평가손익: 현재가와 연동하여 실시간 평가손익 및 수익률 자동 계산

📊 자산 요약: 총 매입금액, 총 평가금액, 전체 평가손익 요약 정보 제공

🖼️ 메인 화면
👉 Tip: 이 영역을 실제 프로젝트의 스크린샷이나 GIF 이미지로 교체하면 훨씬 좋습니다.

Plaintext

┌─────────────────────────────────────────────────────────────┐
│ 🏠 주식 대시보드           [사용자명] 환영합니다! [로그아웃]     │
├─────────────────────────────────────────────────────────────┤
│ 📈 주식 검색               ⭐ 관심 종목                      │
│ ┌──────────────────┐     ┌──────────────────────────────┐ │
│ │ [삼성전자_____🔍]│     │ • 삼성전자          +2.94%     │ │
│ │                  │     │ • SK하이닉스        -0.18%     │ │
│ │ 선택: 삼성전자   │     │ • 카카오            +0%        │ │
│ └──────────────────┘     └──────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ 📊 코스피 시가총액 TOP 20      │ 💼 내 주식 현황              │
│ ┌───────────────────────────┐  │ ┌──────────────────┐   │
│ │ 순위 종목명   현재가  등락률│  │  총 매입: 316,000원  │   │
│ │ ❤️ 1 삼성전자 89,000 +3.49%│  │  총 평가: 475,200원  │   │
│ │ 🤍 2 SK하이닉스 395,500 +9.86%││  평가손익: +159,200  │   │
│ │  ⋮  (스크롤 가능)          │  │  (+50.38%)           │   │
│ └───────────────────────────┘  └──────────────────────┘   │
│                                  📰 코스피 최신 뉴스          │
│                                  ┌──────────────────────┐  │
│                                  │ • 뉴스 제목 1...     │  │
│                                  │ • 뉴스 제목 2...     │  │
│                                  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
🛠 기술 스택
구분	기술	설명
Core	Vue 3 (Composition API), Vite 5	프로그레시브 프레임워크와 초고속 빌드 도구
Routing	Vue Router	SPA를 위한 공식 라우터
State Management	Pinia	Vue 3를 위한 공식 상태 관리 라이브러리
UI/UX	Chart.js, CSS3 Grid Layout	데이터 시각화 및 반응형 레이아웃
HTTP Client	Axios	Promise 기반의 HTTP 클라이언트 (인터셉터 활용)
Persistence	LocalStorage	JWT 토큰 등 클라이언트 측 데이터 저장

📁 프로젝트 구조
컴포넌트 기반의 직관적인 구조를 따릅니다.

frontend/
├── public/
├── src/
│   ├── assets/              # 정적 리소스 (CSS, 이미지)
│   ├── components/          # 재사용 가능한 Vue 컴포넌트
│   ├── views/               # 페이지 단위 컴포넌트
│   ├── stores/              # Pinia 상태 관리 모듈
│   ├── router/              # Vue Router 설정 및 네비게이션 가드
│   ├── App.vue              # 루트 컴포넌트
│   └── main.js              # 애플리케이션 진입점
├── index.html
├── vite.config.js           # Vite 설정 파일
├── package.json
└── README.md

🚀 시작하기
1. 사전 요구사항
Node.js (18.x 이상)

npm 또는 yarn

2. 설치
Bash

# 1. 프로젝트를 클론합니다.
git clone <repository-url>

# 2. 프로젝트 디렉토리로 이동합니다.
cd frontend

# 3. 의존성 패키지를 설치합니다.
npm install

3. 환경 설정
API 서버의 주소를 설정해야 합니다. 프로젝트는 기본적으로 http://localhost:8000/api를 바라봅니다.

URL을 변경하려면 각 컴포넌트 또는 서비스 파일에 정의된 API_BASE 상수를 수정하세요. (추후 .env 파일로 관리 예정)

JavaScript

// 예: src/stores/auth.js, src/components/*.vue
const API_BASE = 'http://localhost:8000/api'; // 백엔드 URL

4. 개발 서버 실행

# HMR(Hot Module Replacement)이 적용된 개발 서버를 실행합니다.
npm run dev
서버가 실행되면 브라우저에서 http://localhost:5173으로 접속하세요.

5. 프로덕션 빌드

# 프로덕션용으로 프로젝트를 빌드합니다.
npm run build

# 빌드 결과물을 미리 봅니다.
npm run preview
빌드된 정적 파일은 dist/ 폴더에 생성됩니다.

🔌 API 엔드포인트
Method	Endpoint	설명
POST	/api/auth/register	회원가입
POST	/api/auth/login	로그인 (JWT 토큰 발급)
GET	/api/auth/me	현재 로그인된 사용자 정보 조회
GET	/api/stocks/search	주식 검색 (자동완성)
GET	/api/stock/detail	주식 상세 정보 조회
GET	/api/stock/top-stocks	시가총액 상위 20개 종목 조회
GET	/api/watchlist	관심 종목 목록 조회
POST	/api/watchlist/:code	관심 종목 추가
DELETE	/api/watchlist/:code	관심 종목 삭제
GET	/api/portfolio	포트폴리오 목록 조회
POST	/api/portfolio	포트폴리오에 종목 추가
DELETE	/api/portfolio/:id	포트폴리오에서 종목 삭제
GET	/api/news/kospi	코스피 최신 뉴스 조회

Sheets로 내보내기
🎨 아키텍처 및 스타일 가이드
Axios 인터셉터
요청 인터셉터: 모든 API 요청에 자동으로 Authorization: Bearer <token> 헤더를 추가합니다.

응답 인터셉터: 401 Unauthorized 에러 발생 시 토큰을 삭제하고 로그인 페이지로 리디렉션하여 토큰 만료에 대응합니다.

라우터 가드 (router/index.js)
meta: { requiresAuth: true }: 해당 라우트는 인증된 사용자만 접근 가능합니다.

meta: { requiresGuest: true }: 해당 라우트는 로그인하지 않은 사용자만 접근 가능합니다. (예: 로그인, 회원가입 페이지)

스타일 가이드
다크 테마: 눈의 피로를 줄이고 집중도를 높이는 다크 테마를 기본으로 합니다.

Scoped CSS: 컴포넌트별 스타일 충돌을 방지하기 위해 <style scoped> 사용을 원칙으로 합니다.

CSS Variables: 색상, 폰트 등 디자인 시스템을 변수로 관리하여 일관성을 유지합니다.

주요 색상 팔레트:

--primary-green: #4CAF50; (상승, 긍정)

--primary-red: #f44336; (하락, 부정)

--bg-dark: #1e1e1e; (메인 배경)

--bg-card: #2d2d2d; (카드 배경)

--text-primary: #ffffff; (기본 텍스트)

📈 향후 개발 계획
[ ] 다크/라이트 테마 전환 토글 기능

[ ] 차트 인터랙션 개선 (확대/축소, 기간 설정)

[ ] 모바일 환경을 위한 반응형 UI 최적화

[ ] WebSocket을 이용한 실시간 데이터 업데이트 고도화

[ ] 여러 종목의 차트를 한 번에 비교하는 기능

[ ] 포트폴리오 데이터를 Excel 파일로 내보내는 기능

[ ] PWA(Progressive Web App) 지원으로 네이티브 앱처럼 사용

[ ] 종목별 개인 메모 기능 추가

📄 라이선스
이 프로젝트는 MIT License를 따릅니다. 자세한 내용은 LICENSE 파일을 참고하세요.

🙏 기여하기
이슈 제보 및 Pull Request는 언제나 환영합니다! 기여를 원하시면 아래 절차를 따라주세요.

프로젝트를 Fork 하세요.

새로운 기능 브랜치를 생성하세요. (git checkout -b feature/AmazingFeature)

변경 사항을 커밋하세요. (git commit -m 'Add some AmazingFeature')

브랜치에 Push 하세요. (git push origin feature/AmazingFeature)

Pull Request를 열어주세요.