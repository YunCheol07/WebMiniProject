🎨 주식 대시보드 Frontend
Vue 3 + Vite 기반의 실시간 주식 정보 대시보드 웹 애플리케이션

🌟 주요 기능
1️⃣ 인증 & 사용자 관리
🔐 회원가입 / 로그인

👤 사용자 프로필 관리

🔑 JWT 토큰 기반 인증

🚪 자동 로그아웃 기능

2️⃣ 주식 검색 & 관심 종목
🔍 실시간 자동완성 검색

⚡ 300ms 디바운싱으로 빠른 응답

📊 종목명/코드 통합 검색

⭐ 관심 종목 패널 - 즐겨찾는 종목 빠른 조회

❤️ 원클릭 하트 버튼으로 관심 종목 추가/삭제

3️⃣ 코스피 시가총액 TOP 20
📈 실시간 시가총액 상위 20개 종목 표시

💹 현재가, 등락률, 거래량, 시가총액 한눈에 확인

🔄 스크롤 가능한 종목 리스트 (헤더 고정)

❤️ 각 종목별 관심 종목 추가 기능

🎯 클릭 시 해당 종목 상세 정보로 이동

4️⃣ 주식 상세 정보
💹 실시간 현재가 조회

📈 차트 데이터 시각화 (Chart.js)

📰 코스피 최신 뉴스 피드 (우측 하단)

📊 상세 투자지표 (PER, PBR, EPS, BPS)

5️⃣ 포트폴리오 관리
💼 보유 주식 등록 및 관리

💰 실시간 평가손익 자동 계산

📊 수익률 분석 (종목별/전체)

📈 총 매입금액/평가금액/평가손익 요약

🔍 종목 자동완성 검색 기능 (포트폴리오 추가 시)

🛠 기술 스택
Core
Vue 3 (Composition API) - 프로그레시브 프레임워크

Vite 5 - 초고속 빌드 도구

Vue Router - SPA 라우팅

UI/UX
Chart.js - 차트 시각화

Axios - HTTP 클라이언트

CSS3 - 커스텀 다크 테마 스타일링

Grid Layout - 반응형 대시보드 레이아웃

상태 관리
Pinia - Vue 3 공식 상태 관리

LocalStorage - 토큰 저장

📁 프로젝트 구조
text
frontend/
├── public/
│   └── favicon.ico
│
├── src/
│   ├── assets/                # 정적 리소스
│   │
│   ├── components/            # Vue 컴포넌트
│   │   ├── StockSearch.vue    # 주식 검색 (자동완성)
│   │   ├── StockInfo.vue      # 주식 상세 정보
│   │   ├── StockChart.vue     # 차트 컴포넌트
│   │   ├── StockNews.vue      # 코스피 뉴스 컴포넌트
│   │   ├── TopStocks.vue      # 시가총액 TOP 20
│   │   ├── WatchlistPanel.vue # 관심 종목 패널
│   │   └── PortfolioPanel.vue # 포트폴리오 패널
│   │
│   ├── views/                 # 페이지 컴포넌트
│   │   ├── Login.vue          # 로그인 페이지
│   │   ├── Register.vue       # 회원가입 페이지
│   │   └── StockDashboard.vue # 메인 대시보드
│   │
│   ├── stores/                # Pinia 스토어
│   │   └── auth.js            # 인증 상태 관리
│   │
│   ├── router/                # 라우터 설정
│   │   └── index.js           # 라우팅 및 가드
│   │
│   ├── App.vue                # 루트 컴포넌트
│   └── main.js                # 앱 진입점
│
├── index.html
├── vite.config.js             # Vite 설정
├── package.json
└── README.md
🚀 설치 및 실행
1. 사전 요구사항
Node.js 18 이상

npm 또는 yarn

2. 설치
bash
# 프로젝트 클론
git clone <repository-url>
cd frontend

# 의존성 설치
npm install
3. 환경 설정
프로젝트는 기본적으로 http://localhost:8000의 백엔드 API를 사용합니다.

백엔드 URL을 변경하려면 각 컴포넌트의 API_BASE 상수를 수정하세요:

javascript
// src/stores/auth.js, src/components/*.vue
const API_BASE = 'http://localhost:8000/api' // 백엔드 URL
4. 개발 서버 실행
bash
# 개발 모드 (Hot Module Replacement)
npm run dev
브라우저에서 http://localhost:5173 접속

5. 프로덕션 빌드
bash
# 빌드
npm run build

# 빌드 결과 미리보기
npm run preview
빌드된 파일은 dist/ 폴더에 생성됩니다.

🎨 주요 화면
1. 로그인 / 회원가입
깔끔한 다크 테마 UI

실시간 입력 검증

에러 메시지 표시

2. 메인 대시보드 레이아웃
text
┌─────────────────────────────────────────────────────────────┐
│  🏠 주식 대시보드       [사용자명] 환영합니다! [로그아웃]     │
├─────────────────────────────────────────────────────────────┤
│  📈 주식 검색              ⭐ 관심 종목                      │
│  ┌──────────────────┐    ┌──────────────────────────────┐  │
│  │ [삼성전자_____🔍]│    │ • 삼성전자        +2.94%     │  │
│  │                  │    │ • SK하이닉스      -0.18%     │  │
│  │ 선택: 삼성전자    │    │ • 카카오          +0%        │  │
│  └──────────────────┘    │ • 신한지주        +3.49%     │  │
│                          └──────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  📊 코스피 시가총액 TOP 20         │  💼 내 주식 현황        │
│  ┌─────────────────────────────┐  │  ┌──────────────────┐  │
│  │ 순위 종목명   현재가  등락률   │  │  총 매입: 316,000원│  │
│  │ ❤️ 1 삼성전자 89,000 +3.49%  │  │  총 평가: 475,200원│  │
│  │ 🤍 2 SK하이닉스 395,500 +9.86%│  │  평가손익: +159,200│  │
│  │ 🤍 3 LG에너지솔루션 399,000   │  │  (+50.38%)        │  │
│  │ ❤️ 4 삼성바이오 1,009,000    │  │                    │  │
│  │ ❤️ 5 삼성전자우 70,000       │  │  [+ 종목 추가]     │  │
│  │  ⋮  (스크롤 가능)            │  │                    │  │
│  └─────────────────────────────┘  └──────────────────────┘  │
│                                    📰 코스피 최신 뉴스       │
│                                    ┌──────────────────────┐ │
│                                    │ • 뉴스 제목 1...     │ │
│                                    │ • 뉴스 제목 2...     │ │
│                                    └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
3. 코스피 시가총액 TOP 20
고정 헤더: 제목과 컬럼명 항상 상단 고정

스크롤 영역: 종목 리스트만 독립적으로 스크롤

실시간 업데이트: 현재가, 등락률 실시간 반영

관심 종목 연동: 하트 버튼 클릭으로 관심 종목 추가

순위 표시: 1~20위 순위 번호 표시

4. 관심 종목 패널
등록된 관심 종목 목록 표시

클릭 시 해당 종목 상세 조회

하트 버튼으로 삭제 가능

등락률 색상 구분 (빨강: 상승, 파랑: 하락)

5. 포트폴리오 관리
text
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
6. 코스피 최신 뉴스
우측 하단에 뉴스 피드 표시

실시간 코스피 관련 뉴스 업데이트

클릭 시 원문 링크로 이동

스크롤 가능한 뉴스 목록

🎮 사용 방법
기본 조작
주식 검색

검색창에 종목명 또는 코드 입력

자동완성 목록에서 선택 또는 Enter

선택한 종목의 상세 정보 표시

관심 종목 추가

하트(❤️) 버튼 클릭

관심 종목 패널에 자동 추가

다시 클릭 시 삭제

TOP 20 종목 조회

좌측 패널에서 시가총액 상위 종목 확인

종목 클릭 시 상세 정보 조회

스크롤하여 전체 20개 종목 확인

포트폴리오 관리

[+ 종목 추가] 버튼 클릭

종목 검색 (자동완성)

보유 수량, 평균 매입가, 매입 날짜 입력

실시간 평가손익 자동 계산

키보드 단축키
키	동작
Enter	검색 실행 또는 종목 선택
↓	자동완성 목록 아래로 이동
↑	자동완성 목록 위로 이동
ESC	자동완성 목록 닫기
🎨 스타일 가이드
컬러 팔레트
css
/* Primary Colors */
--primary-green: #4CAF50;  /* 메인 색상, 상승 */
--primary-red: #f44336;    /* 수익 */
--primary-blue: #2196F3;   /* 손실 */

/* Background */
--bg-dark: #1e1e1e;        /* 메인 배경 */
--bg-card: #2d2d2d;        /* 카드 배경 */
--bg-hover: #353535;       /* 호버 배경 */

/* Text */
--text-primary: #ffffff;   /* 기본 텍스트 */
--text-secondary: #aaa;    /* 보조 텍스트 */
--text-disabled: #666;     /* 비활성화 */

/* Border */
--border-default: #444;    /* 기본 테두리 */
--border-active: #4CAF50;  /* 활성 테두리 */
레이아웃 특징
다크 테마: 눈의 피로 감소

카드 기반: 정보 계층 구조화

Fixed Header: TOP 20 패널 헤더 고정

Grid Layout: 반응형 2열 레이아웃

호버 효과: 인터랙티브 피드백

부드러운 전환: 모든 애니메이션 0.3s

커스텀 스크롤바: 녹색 스크롤바 (Webkit)

폰트 크기 가이드
css
/* 제목 */
h3: 24px (코스피 TOP 20)
h3: 18px (섹션 제목)

/* 테이블 헤더 */
th: 16px (컬럼명)

/* 테이블 데이터 */
td: 16px (기본값)
.stock-name: 17px (종목명)
.value.price: 17px (현재가)

/* 버튼 */
.add-btn: 13px
.delete-btn: 16px
🔌 API 통신
Axios 인터셉터
javascript
// 요청 시 자동으로 토큰 추가
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
주요 API 엔드포인트
javascript
// 인증
POST /api/auth/register         # 회원가입
POST /api/auth/login            # 로그인
GET  /api/auth/me               # 내 정보

// 주식
GET  /api/stocks/search         # 주식 검색
GET  /api/stock/detail          # 주식 상세 정보
GET  /api/stock/top-stocks      # 시가총액 TOP 20

// 관심 종목
GET    /api/watchlist           # 관심 종목 조회
POST   /api/watchlist/:code     # 관심 종목 추가
DELETE /api/watchlist/:code     # 관심 종목 삭제

// 포트폴리오
GET    /api/portfolio           # 포트폴리오 조회
POST   /api/portfolio           # 포트폴리오 추가
DELETE /api/portfolio/:id       # 포트폴리오 삭제

// 뉴스
GET  /api/news/kospi            # 코스피 뉴스
에러 처리
javascript
try {
  const response = await axios.get('/api/stocks/search', { 
    params: { q: query, limit: 10 } 
  })
  // 성공 처리
} catch (error) {
  if (error.response?.status === 401) {
    // 인증 만료 - 로그아웃 처리
    logout()
    router.push('/login')
  } else {
    console.error('API 에러:', error)
    alert('오류가 발생했습니다')
  }
}
🛡️ 라우터 가드
인증 보호
javascript
// 로그인 필요한 페이지
{
  path: '/',
  component: StockDashboard,
  meta: { requiresAuth: true }
}

// 로그인 시 접근 불가
{
  path: '/login',
  component: Login,
  meta: { requiresGuest: true }
}
자동 리다이렉트
미인증 사용자 → /login 이동

인증된 사용자가 로그인 페이지 접근 → / 이동

📦 주요 패키지
json
{
  "dependencies": {
    "vue": "^3.5.12",
    "vue-router": "^4.4.5",
    "pinia": "^2.2.4",
    "axios": "^1.7.7",
    "chart.js": "^4.4.6"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.1.4",
    "vite": "^5.4.9"
  }
}
🔧 개발 도구
VS Code 추천 확장
Volar - Vue 3 언어 지원

ESLint - 코드 린팅

Prettier - 코드 포맷팅

브라우저 확장
Vue Devtools - Vue 디버깅 도구

🚨 문제 해결
1. CORS 에러
python
# backend app.py에서 CORS 설정 확인
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
2. 토큰 만료
javascript
// 401 에러 발생 시 자동 로그아웃
if (error.response?.status === 401) {
  logout()
  router.push('/login')
}
3. 개발 서버 포트 변경
javascript
// vite.config.js
export default defineConfig({
  server: {
    port: 3000  // 기본 5173에서 변경
  }
})
4. TOP 20 스크롤 문제
css
/* 헤더 고정, 리스트만 스크롤 */
.top-stocks {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.stocks-list-container {
  flex: 1;
  overflow-y: auto;
}
📝 개발 가이드
새 컴포넌트 추가
src/components/ 에 .vue 파일 생성

Composition API 사용 권장

props와 emits 명확히 정의

text
<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
  title: String,
  data: Object
})

const emit = defineEmits(['update', 'close'])
</script>
새 페이지 추가
src/views/ 에 컴포넌트 생성

router/index.js에 라우트 추가

javascript
{
  path: '/new-page',
  name: 'NewPage',
  component: () => import('../views/NewPage.vue'),
  meta: { requiresAuth: true }
}
스타일 가이드
text
<style scoped>
/* 컴포넌트 스타일은 scoped 사용 */
.component {
  /* 다크 테마 유지 */
  background: #2d2d2d;
  color: white;
  
  /* 일관된 간격 */
  padding: 20px;
  margin: 10px;
  
  /* 부드러운 전환 */
  transition: all 0.3s;
}
</style>
🎯 성능 최적화
구현된 최적화
✅ 디바운싱: 검색 API 호출 300ms 딜레이
✅ Lazy Loading: 라우트 기반 코드 스플리팅
✅ 컴포넌트 분리: 재사용성 및 유지보수성 향상
✅ 로컬 스토어: 토큰 로컬 저장으로 서버 부하 감소
✅ Fixed Header: 불필요한 리렌더링 방지
✅ Flexbox Layout: 효율적인 레이아웃 렌더링

📈 향후 개발 계획
🔜 예정 기능
 다크/라이트 테마 토글

 차트 인터랙션 개선 (확대/축소)

 모바일 반응형 최적화

 PWA 지원

 실시간 알림 (WebSocket)

 여러 종목 차트 비교 기능

 포트폴리오 엑셀 내보내기

 TOP 20 → TOP 50 확장 옵션

 뉴스 키워드 필터링

 종목별 메모 기능

👨‍💻 개발자
곽윤철

Email: kyc4061@daum.net

GitHub: @YunCheol07

📄 라이선스
MIT License

🙏 기여
이슈 제보 및 Pull Request는 언제나 환영합니다!

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request