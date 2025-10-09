# 🎨 주식 대시보드 Frontend

Vue 3 + Vite 기반의 실시간 주식 정보 대시보드 웹 애플리케이션

![Vue.js](https://img.shields.io/badge/Vue.js-3.5-4FC08D?style=flat&logo=vue.js&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?style=flat&logo=vite&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-1.7-5A29E4?style=flat&logo=axios&logoColor=white)

---

## 🌟 주요 기능

### 1️⃣ 인증 & 사용자 관리
- 🔐 회원가입 / 로그인
- 👤 사용자 프로필 관리
- 🔑 JWT 토큰 기반 인증
- 🚪 자동 로그아웃 기능

### 2️⃣ 주식 검색
- 🔍 실시간 자동완성 검색
- ⌨️ 키보드 네비게이션 (↑↓ Enter)
- 📊 종목명/코드 통합 검색
- ⚡ 300ms 디바운싱으로 빠른 응답

### 3️⃣ 주식 정보
- 💹 실시간 현재가 조회
- 📈 차트 데이터 시각화 (Chart.js)
- 📰 관련 뉴스 표시
- 📊 상세 투자지표 (PER, PBR, EPS, BPS)

### 4️⃣ 관심 종목
- ⭐ 원클릭 관심 종목 추가/삭제
- ❤️ 하트 버튼으로 시각적 피드백
- 📋 관심 종목 목록 관리
- 🔄 실시간 동기화

### 5️⃣ 포트폴리오 관리
- 💼 보유 주식 등록
- 💰 실시간 평가손익 계산
- 📊 수익률 분석
- 📈 총 자산 현황 요약

---

## 🛠 기술 스택

### Core
- **Vue 3** (Composition API) - 프로그레시브 프레임워크
- **Vite 5** - 초고속 빌드 도구
- **Vue Router** - SPA 라우팅

### UI/UX
- **Chart.js** - 차트 시각화
- **Axios** - HTTP 클라이언트
- **CSS3** - 커스텀 스타일링 (다크 테마)

### 상태 관리
- **Pinia** - Vue 3 공식 상태 관리
- **LocalStorage** - 토큰 저장

---

## 📁 프로젝트 구조

frontend/  
├── public/  
│ └── favicon.ico  
│  
├── src/  
│ ├── assets/ # 정적 리소스  
│ │  
│ ├── components/ # Vue 컴포넌트  
│ │ ├── StockSearch.vue # 주식 검색 (자동완성)  
│ │ ├── StockInfo.vue # 주식 상세 정보  
│ │ ├── StockChart.vue # 차트 컴포넌트  
│ │ ├── StockNews.vue # 뉴스 컴포넌트  
│ │ ├── WatchlistPanel.vue # 관심 종목 패널  
│ │ └── PortfolioPanel.vue # 포트폴리오 패널  
│ │  
│ ├── views/ # 페이지 컴포넌트  
│ │ ├── Login.vue # 로그인 페이지  
│ │ ├── Register.vue # 회원가입 페이지  
│ │ └── StockDashboard.vue # 메인 대시보드  
│ │  
│ ├── stores/ # Pinia 스토어  
│ │ └── auth.js # 인증 상태 관리  
│ │  
│ ├── router/ # 라우터 설정  
│ │ └── index.js # 라우팅 및 가드  
│ │  
│ ├── App.vue # 루트 컴포넌트  
│ └── main.js # 앱 진입점  
│  
├── index.html  
├── vite.config.js # Vite 설정  
├── package.json  
└── README.md  

---

## 🚀 설치 및 실행

### 1. 사전 요구사항

- Node.js 18 이상
- npm 또는 yarn

### 2. 설치

프로젝트 클론
git clone <repository-url>
cd frontend

의존성 설치
npm install

### 3. 환경 설정

프로젝트는 기본적으로 `http://localhost:8000`의 백엔드 API를 사용합니다.

백엔드 URL을 변경하려면 각 컴포넌트의 `API_BASE` 상수를 수정하세요:

// src/stores/auth.js, src/components/*.vue
const API_BASE = 'http://localhost:8000/api' // 백엔드 URL

### 4. 개발 서버 실행

개발 모드 (Hot Module Replacement)
npm run dev

브라우저에서 http://localhost:5173 접속
text

### 5. 프로덕션 빌드

빌드
npm run build

빌드 결과 미리보기
npm run preview

text

빌드된 파일은 `dist/` 폴더에 생성됩니다.

---

## 🎨 주요 화면

### 1. 로그인 / 회원가입
- 깔끔한 다크 테마 UI
- 실시간 입력 검증
- 에러 메시지 표시

### 2. 주식 검색
┌─────────────────────────────────────┐  
│ 📈 주식 검색 │  
├─────────────────────────────────────┤  
│ [삼성전자____________] [🔍 조회] │  
│ ┌─────────────────────────────┐ │  
│ │ 삼성전자 005930 │ │  
│ │ 삼성SDI 006400 │ │  
│ │ 삼성바이오로직스 207940 │ │  
│ └─────────────────────────────┘ │  
│ │  
│ 선택된 종목: 삼성전자 (005930) │  
└─────────────────────────────────────┘  

### 3. 주식 정보
- 현재가, 전일대비, 시가, 거래량
- 52주 최고가/최저가
- 투자지표 (PER, PBR, EPS, BPS)
- ❤️ 관심 종목 추가 버튼

### 4. 포트폴리오
┌─────────────────────────────────────────────┐  
│ 💼 내 주식 현황                              │  
├─────────────────────────────────────────────┤  
│ 총 매입금액    총 평가금액     평가손익          │  
│ 10,000,000원 11,500,000원 +1,500,000원       │  
│ (+15.0%)                                    │  
├─────────────────────────────────────────────┤  
│  종목명  수량 매입가  현재가  수익률             │  
│ 삼성전자 10주 70,000 75,000 +7.14%            │  
│ 카카오   5주  50,000 48,000 -4.00%            │  
└─────────────────────────────────────────────┘  

---

## 🎮 사용 방법

### 키보드 단축키

| 키 | 동작 |
|---|------|
| **Enter** | 선택된 종목 조회 (또는 첫 번째 검색 결과) |
| **↓** | 다음 검색 결과로 이동 |
| **↑** | 이전 검색 결과로 이동 |
| **ESC** | 검색 결과 닫기 |

### 검색 팁

1. **종목명으로 검색**
   - "삼성" 입력 → 삼성전자, 삼성SDI 등 표시

2. **종목코드로 검색**
   - "005930" 입력 → 삼성전자 표시

3. **빠른 조회**
   - 검색어 입력 후 바로 Enter 키

---

## 🎨 스타일 가이드

### 컬러 팔레트

/* Primary Colors /  
--primary-green: #4CAF50; / 메인 색상 /  
--primary-red: #f44336; / 상승 (수익) /  
--primary-blue: #2196F3; / 하락 (손실) */  

/* Background /  
--bg-dark: #1e1e1e; / 메인 배경 /  
--bg-card: #2d2d2d; / 카드 배경 /  
--bg-hover: #353535; / 호버 배경 */  

/* Text /  
--text-primary: #ffffff; / 기본 텍스트 /  
--text-secondary: #aaa; / 보조 텍스트 /  
--text-disabled: #666; / 비활성화 */  

/* Border /  
--border-default: #444; / 기본 테두리 /  
--border-active: #4CAF50; / 활성 테두리 */  

### 컴포넌트 스타일

- **다크 테마**: 눈의 피로 감소
- **카드 레이아웃**: 정보 구조화
- **호버 효과**: 인터랙티브 피드백
- **부드러운 전환**: 모든 애니메이션 0.3s

---

## 🔌 API 통신

### Axios 인터셉터

// 요청 시 자동으로 토큰 추가  
axios.interceptors.request.use(config => {  
const token = localStorage.getItem('token')  
if (token) {  
config.headers.Authorization = Bearer ${token}  
}  
return config  
})  

### 에러 처리

try {  
const response = await axios.get('/api/stocks/search', { params: { q: query } })  
// 성공 처리  
} catch (error) {  
console.error('API 에러:', error)  
alert('오류가 발생했습니다')  
}  

---

## 🛡️ 라우터 가드

### 인증 보호

// 로그인 필요한 페이지  
{  
path: '/',  
component: StockDashboard,  
meta: { requiresAuth: true }  
}  

// 로그인 시 접근 불가 (로그인/회원가입)  
{  
path: '/login',  
component: Login,  
meta: { requiresGuest: true }  
}  

### 자동 리다이렉트

- 미인증 사용자 → `/login` 이동
- 인증된 사용자가 로그인 페이지 접근 → `/` 이동

---

## 📦 주요 패키지

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

---

## 🔧 개발 도구

### VS Code 추천 확장

- **Volar** - Vue 3 언어 지원
- **ESLint** - 코드 린팅
- **Prettier** - 코드 포맷팅

### 브라우저 확장

- **Vue Devtools** - Vue 디버깅 도구

---

## 🚨 문제 해결

### 1. CORS 에러

// backend app.py에서 CORS 설정 확인  
app.add_middleware(  
CORSMiddleware,  
allow_origins=["http://localhost:5173"],  
allow_credentials=True,  
allow_methods=[""],  
allow_headers=[""],  
)  

### 2. 토큰 만료

// 401 에러 발생 시 자동 로그아웃  
if (error.response?.status === 401) {  
logout()  
router.push('/login')  
}  

### 3. 개발 서버 포트 변경

// vite.config.js  
export default defineConfig({   
server: {  
port: 3000 // 기본 5173에서 변경  
}  
})  

---

## 📝 개발 가이드

### 새 컴포넌트 추가

1. `src/components/` 에 `.vue` 파일 생성
2. Composition API 사용 권장
3. props와 emits 명확히 정의

<script setup> import { ref, defineProps, defineEmits } from 'vue' const props = defineProps({ title: String, data: Object }) const emit = defineEmits(['update', 'close']) </script>

### 새 페이지 추가

1. `src/views/` 에 컴포넌트 생성
2. `router/index.js`에 라우트 추가

{  
path: '/new-page',  
name: 'NewPage',  
component: () => import('../views/NewPage.vue'),  
meta: { requiresAuth: true }  
}  

---

## 🎯 성능 최적화

### 구현된 최적화

✅ **디바운싱**: 검색 API 호출 300ms 딜레이
✅ **Lazy Loading**: 라우트 기반 코드 스플리팅
✅ **컴포넌트 분리**: 재사용성 및 유지보수성 향상
✅ **로컬 스토어**: 토큰 로컬 저장으로 서버 부하 감소

---

## 📈 향후 개발 계획

### 🔜 예정 기능

- [ ] 다크/라이트 테마 토글
- [ ] 차트 인터랙션 개선
- [ ] 모바일 반응형 최적화
- [ ] PWA 지원
- [ ] 실시간 알림 (WebSocket)
- [ ] 차트 비교 기능
- [ ] 엑셀 내보내기

---

## 👨‍💻 개발자

**곽윤철**
- Email: kyc4061@daum.net
- GitHub: [@YunCheol07](https://github.com/YunCheol07/WebMiniProject)

---

## 📄 라이선스

MIT License

---

## 🙏 기여

이슈 제보 및 Pull Request는 언제나 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---