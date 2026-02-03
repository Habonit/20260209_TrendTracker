# KICE Solver - 수능 국어 문제 풀이 AI

Google Gemini API를 활용하여 수능 국어 문제를 자동으로 풀이하고 결과를 분석하는 프로젝트입니다.

## 소개

이 프로젝트는 AI가 수능 국어 시험을 얼마나 잘 풀 수 있는지 실험하고, 그 결과를 분석하는 도구입니다.

- **자동 풀이**: 45개 수능 국어 문제를 Gemini AI가 자동으로 풀이
- **점수 계산**: 정답률, 획득 점수, 예상 등급 계산
- **오답 분석**: AI가 왜 틀렸는지 reasoning 확인
- **시각화**: 다양한 그래프로 결과 분석

## 데이터 출처

문제 데이터는 [NomaDamas/KICE_slayer_AI_Korean](https://github.com/NomaDamas/KICE_slayer_AI_Korean) 저장소에서 가져왔습니다.

- **원본 데이터**: 2023년 11월 수능 국어 영역
- **총 45문제**: 2점 35개 (70점) + 3점 10개 (30점) = 100점 만점

## 설치

### 1. 저장소 클론

```bash
git clone <repository-url>
cd solve_test
```

### 2. 의존성 설치

[uv](https://github.com/astral-sh/uv)를 사용합니다.

```bash
uv sync
```

### 3. 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열어 Gemini API 키를 입력합니다:

```bash
GEMINI_API_KEY=your_api_key_here
```

API 키는 [Google AI Studio](https://aistudio.google.com/apikey)에서 발급받을 수 있습니다.

## 사용법

### 문제 풀이 실행

```bash
uv run python main.py
```

#### 옵션

```bash
# 입출력 경로 지정
# arparse 참조
uv run python main.py -i ./data/2023_11_KICE_flat.json -o ./output/results.csv

# Response Mode 변경 (1, 2, 3)
RESPONSE_MODE=1 uv run python main.py

# 모델 변경
MODEL=gemini-2.0-pro uv run python main.py

# 출력 토큰 수 변경
MAX_OUTPUT_TOKENS=4096 uv run python main.py
```

#### Response Mode 설명

| Mode | 설정 | 설명 |
|------|------|------|
| 1 | 프롬프트만 | JSON 파싱 실패 가능성 있음 |
| 2 | + MIME type | `application/json` 응답 보장 |
| 3 (기본) | + Schema | 필드 구조까지 강제 |

### 결과 분석

결과 파일이 생성되면 `analyze.ipynb` 노트북으로 분석할 수 있습니다.

```bash
jupyter notebook analyze.ipynb
```

또는 VS Code에서 직접 노트북을 실행합니다.

## 프로젝트 구조

```
solve_test/
├── ai/
│   └── gemini_client.py      # Gemini API 클라이언트
├── data/
│   └── 2023_11_KICE_flat.json # 문제 데이터
├── doc/
│   ├── develop_app.md        # 앱 개발 명세서
│   └── develope_notebook.md  # 노트북 개발 명세서
├── domain/
│   └── problem.py            # 데이터 모델 (Problem, Answer)
├── output/
│   └── results.csv           # 풀이 결과 (자동 생성)
├── prompts/
│   └── prompt.py             # 프롬프트 정의
├── repository/
│   └── problem_repository.py # 데이터 저장/조회
├── service/
│   └── solver_service.py     # 비즈니스 로직
├── utils/
│   └── exceptions.py         # 에러 처리
├── main.py                   # 진입점
├── analyze.ipynb             # 결과 분석 노트북
├── .env                      # 환경변수 (gitignore)
└── .env.example              # 환경변수 예시
```

## 환경변수

| 변수명 | 필수 | 기본값 | 설명 |
|--------|------|--------|------|
| `GEMINI_API_KEY` | O | - | Gemini API 키 |
| `RESPONSE_MODE` | X | `3` | 응답 형식 모드 (1, 2, 3) |
| `MODEL` | X | `gemini-2.0-flash-lite` | 사용할 Gemini 모델 |
| `MAX_OUTPUT_TOKENS` | X | `2048` | 최대 출력 토큰 수 |

## 출력 예시

### CLI 출력

```
=== 수능 국어 문제 풀이 AI ===
Response Mode: 3
입력: ./data/2023_11_KICE_flat.json
출력: ./output/results.csv

[GeminiClient] Model: gemini-2.0-flash-lite
[GeminiClient] Mode: 3
총 45개 문제 로드 완료 (만점: 100점)

[1/45] 문제 1 (2점): O (+2점)
[2/45] 문제 2 (3점): O (+3점)
[3/45] 문제 3 (2점): X (+0점)
...

========================================
결과
========================================
총 문제: 45개
정답: 38개 / 오답: 7개
정답률: 84.4%

획득 점수: 82점 / 100점
점수 백분율: 82.0%
========================================
```

### 결과 CSV

| problem_id | score | predicted | actual | is_correct | earned_score | reasoning |
|------------|-------|-----------|--------|------------|--------------|-----------|
| 1 | 2 | 4 | 4 | True | 2 | {"choice": 4, "reasoning": "..."} |
| 2 | 3 | 5 | 5 | True | 3 | {"choice": 5, "reasoning": "..."} |
| 3 | 2 | 2 | 1 | False | 0 | {"choice": 2, "reasoning": "..."} |

## 주요 기능

### 중간 저장

프로그램 중단 후 재실행하면 이전 풀이를 건너뛰고 이어서 진행합니다.

```bash
# Ctrl+C로 중단 후
uv run python main.py  # 자동으로 이어서 풀이
```

### Rate Limit 처리

Gemini 무료 버전의 요청 제한을 자동으로 처리합니다.

- 문제당 10초 대기
- 5문제마다 60초 대기
- 요청 실패 시 자동 재시도

## 기술 스택

- **Python 3.11**
- **Google Gemini API** (`google-genai`)
- **pandas** - 데이터 처리
- **matplotlib** - 시각화
- **scikit-learn** - 혼동 행렬

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

문제 데이터의 저작권은 한국교육과정평가원(KICE)에 있습니다.
