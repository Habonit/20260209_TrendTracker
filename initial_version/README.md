# initial_version 🚀

키워드로 최신 뉴스를 검색하고 Google Gemini AI를 통해 핵심 내용을 요약해주는 Streamlit 웹 어플리케이션입니다.

## 🌟 주요 기능

- **최신 뉴스 최우선 검색**: Tavily의 고급 검색(Advanced Search)과 발행일 기준 수동 정렬을 통해 가장 최근의 기사를 최상단에 배치합니다.
- **AI 핵심 요약**: Google Gemini(gemini-2.5-flash)가 복잡한 뉴스 내용을 한눈에 보기 좋게 요약해줍니다.
- **검색 기록 관리**: 모든 검색 결과는 로컬 CSV 파일에 자동 저장되어 언제든 다시 확인할 수 있습니다.
- **데이터 백업**: 누적된 검색 데이터를 CSV 파일로 한꺼번에 다운로드할 수 있습니다.

## 🛠 설치 및 실행 방법

### 1. uv 설치 (권장 패키지 관리자)

가장 먼저 `uv`가 설치되어 있어야 합니다. (이미 설치되어 있다면 이 단계를 건너뛰세요.)

- **macOS/Linux**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows (PowerShell)**:
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

### 2. 프로젝트 설정 및 의존성 설치

```bash
# 프로젝트 폴더로 이동 후 가상환경 및 패키지 설치
uv sync
```

### 3. 환경변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 필요한 API 키를 입력합니다.

```bash
cp .env.example .env
```

`.env` 파일 내용 예시:
```env
TAVILY_API_KEY=tvly-xxxxxxxxxxxx
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
SEARCH_DOMAINS=zdnet.co.kr,etnews.com,hani.co.kr,donga.com
CSV_PATH=data/search_history.csv
```

### 4. 앱 실행

```bash
uv run streamlit run app.py
```

## 🔑 API 키 발급 안내

### Tavily API (뉴스 검색)
1. [Tavily 공식 홈페이지](https://tavily.com/)에 가입합니다.
2. 대시보드에서 API 키를 발급받습니다 (무료 플랜 제공).

### Google Gemini API (AI 요약)
1. [Google AI Studio](https://aistudio.google.com/)에 접속합니다.
2. 'Get API key' 메뉴에서 새 API 키를 생성합니다.

## 📁 폴더 구조

```
initial_version/
├── app.py                # 메인 Streamlit 앱 진입점
├── config/               # 환경 설정 (Settings 클래스)
├── domain/               # 데이터 모델 (NewsArticle, SearchResult)
├── services/             # 비즈니스 로직 (API 연동 서비스)
├── repositories/         # 데이터 접근 계층 (CSV 저장 관리)
├── components/           # UI 컴포넌트 (사이드바, 결과 화면 등)
├── utils/                # 유틸리티 (에러 처리, 입력 전처리 등)
└── data/                 # 검색 기록 CSV 저장 폴더
```

## ⚠️ 주의사항
- 검색 기록은 `data/search_history.csv` 파일에 물리적으로 저장됩니다. 이 파일을 삭제하면 이전 기록을 불러올 수 없습니다.
- Tavily와 Gemini API는 무료 할당량이 제한되어 있으므로 대량 검색 시 유의하세요.
