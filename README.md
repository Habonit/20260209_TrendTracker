# 바이브코딩과 데이터 분석

> 2026년 2월 9일 전주대학교 교육 컨텐츠

AI 바이브코딩을 활용한 파이썬 프로그래밍과 데이터 분석 실습 자료입니다.

## 학습 순서

| 순서 | 폴더 | 주제 | 설명 |
|:---:|------|------|------|
| 1 | `uv_python_dotenv` | 환경 설정 기초 | uv 패키지 매니저와 환경변수(.env) 사용법 |
| 2 | `use_google_api_key` | API 연동 기초 | Google Gemini API 호출 실습 |
| 3 | `initial_version` | 메인 프로젝트 | 뉴스 검색 + AI 요약 Streamlit 앱 |
| 4 | `solve_test` | 응용 프로젝트 | 수능 국어 문제 AI 풀이 및 분석 |
| 5 | `learn_python_trpg` | 복습 게임 | 파이썬 개념 복습 TRPG 퀴즈 게임 |

## 프로젝트 상세

### 1. uv_python_dotenv - 환경 설정 기초

Python 프로젝트의 기본이 되는 환경 설정을 학습합니다.

- **uv**: 빠른 Python 패키지 매니저
- **python-dotenv**: `.env` 파일로 환경변수 관리
- **학습 목표**: `uv sync`, `uv run`, `.env` 파일 사용법 익히기

```bash
cd uv_python_dotenv
uv sync
uv run python main.py
```

### 2. use_google_api_key - API 연동 기초

Google Gemini API를 호출하는 기본 패턴을 학습합니다.

- `.env`에서 API 키 로드
- `google-genai` 라이브러리 사용
- 프롬프트 파일 읽기 → API 호출 → 응답 출력

```bash
cd use_google_api_key
uv sync
# .env 파일에 GOOGLE_API_KEY 설정 후
uv run python main.py
```

### 3. initial_version - 뉴스 검색 AI 요약 앱

실제 서비스 수준의 Streamlit 웹 애플리케이션을 구현합니다.

- **Tavily API**: 최신 뉴스 검색
- **Google Gemini**: AI 핵심 요약
- **Streamlit**: 웹 UI 구현
- **학습 주제**: 클린 아키텍처, 모듈 분리, 데이터 영속화

```bash
cd initial_version
uv sync
uv run streamlit run app.py
```

### 4. solve_test - 수능 국어 AI 풀이

AI가 수능 국어 문제를 풀고 결과를 분석합니다.

- 45문제 자동 풀이
- 정답률/점수/등급 계산
- pandas, matplotlib으로 시각화
- **학습 주제**: 프롬프트 엔지니어링, 데이터 분석, Jupyter Notebook

```bash
cd solve_test
uv sync
uv run python main.py
```

### 5. learn_python_trpg - 파이썬 던전 탈출

TrendTracker 프로젝트에서 배운 개념을 TRPG 형식으로 복습합니다.

- 7개 관문, 각 관문 10문제
- 환경설정, 클래스, API, 파일I/O, UI 등 주제별 퀴즈
- 통과 시 인증서 발급

```bash
cd learn_python_trpg
python main.py
```

## 사전 준비

### 1. uv 설치

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. API 키 발급

| API | 용도 | 발급처 |
|-----|------|--------|
| Google Gemini | AI 텍스트 생성 | [Google AI Studio](https://aistudio.google.com/) |
| Tavily | 뉴스 검색 | [Tavily](https://tavily.com/) |

## 기술 스택

- **Python 3.11+**
- **uv** - 패키지 관리
- **Streamlit** - 웹 UI
- **Google Gemini API** - AI 모델
- **Tavily API** - 웹 검색
- **pandas** - 데이터 처리
- **matplotlib** - 시각화