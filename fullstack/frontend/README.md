# 가온북스 도서 검색 - React 프론트엔드

## 개요
가온북스 도서 검색 시스템의 React 기반 프론트엔드입니다.

## 기능
- 도서명으로 도서 검색
- 검색 결과를 카드 형태로 표시
- 품절/재고 상태 표시
- 반응형 디자인
- 실시간 검색 결과 업데이트

## 기술 스택
- React 19
- Vite
- CSS3 (반응형 디자인)

## 개발 환경 설정

### 1. 의존성 설치
```bash
npm install
```

### 2. 개발 서버 실행
```bash
npm run dev
```

### 3. 빌드
```bash
npm run build
```

### 4. 미리보기
```bash
npm run preview
```

## 프로젝트 구조
```
src/
├── components/
│   └── BookCard.jsx      # 도서 카드 컴포넌트
├── App.jsx               # 메인 앱 컴포넌트
├── App.css               # 메인 스타일
└── main.jsx              # 앱 진입점
```

## API 연동
- 백엔드 API: `/api/find/{도서명}/`
- 프록시 설정: `vite.config.js`에서 백엔드 서버로 요청 전달

## 환경 요구사항
- Node.js 18+
- npm 9+
- 백엔드 서버 (FastAPI) 실행 필요

## 개발 가이드
1. 백엔드 서버를 먼저 실행 (포트 8000)
2. React 개발 서버 실행 (포트 5173)
3. 브라우저에서 `http://localhost:5173` 접속
4. 도서명으로 검색 테스트
