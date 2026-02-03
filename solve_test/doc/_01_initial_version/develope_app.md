# 수능 국어 문제 풀이 AI - 개발 명세서

> 이 문서를 따라 단계별로 개발하면 완성된 프로젝트를 만들 수 있습니다.

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [개발 환경 설정](#2-개발-환경-설정)
3. [프로젝트 구조](#3-프로젝트-구조)
4. [Step 1: 도메인 모델 정의](#step-1-도메인-모델-정의)
5. [Step 2: 에러 처리 모듈](#step-2-에러-처리-모듈)
6. [Step 3: 프롬프트 모듈](#step-3-프롬프트-모듈)
7. [Step 4: Gemini AI 클라이언트](#step-4-gemini-ai-클라이언트)
8. [Step 5: 레포지토리 (데이터 저장/조회)](#step-5-레포지토리-데이터-저장조회)
9. [Step 6: 서비스 (비즈니스 로직)](#step-6-서비스-비즈니스-로직)
10. [Step 7: 메인 진입점](#step-7-메인-진입점)
11. [Step 8: 분석 노트북](#step-8-분석-노트북)
12. [실행 및 테스트](#실행-및-테스트)
13. [응답 형식 강제 (3단계 모드)](#응답-형식-강제-3단계-모드)
14. [프롬프트 실험 가이드](#프롬프트-실험-가이드)

---

## 1. 프로젝트 개요

### 목표
2023년 11월 수능 국어 문제를 Google Gemini AI로 풀이하고 결과를 분석하는 프로그램 개발

### 주요 기능
- 45개 수능 국어 문제 자동 풀이
- AI 응답 형식 강제 (3단계 모드 학습)
- 중간 저장으로 안정적인 실행
- 점수 계산 및 분석

### 기술 스택

| 항목 | 기술 |
|------|------|
| 언어 | Python 3.11 |
| AI API | Google Gemini (`gemini-2.0-flash-lite`) |
| SDK | `google-genai` (공식 Python SDK) |
| 패키지 관리 | uv |
| 데이터 처리 | pandas |
| 시각화 | matplotlib |

### 데이터 구조

```
수능 국어 시험
├── 총 45문제
├── 2점 문제: 35개 (70점)
├── 3점 문제: 10개 (30점)
└── 총점: 100점
```

---

## 2. 개발 환경 설정

### 2.1 프로젝트 디렉토리 생성

```bash
mkdir -p solve_test
cd solve_test
```

### 2.2 uv 프로젝트 초기화

```bash
# Python 3.11로 프로젝트 초기화
uv init --python 3.11
```

### 2.3 의존성 설치

```bash
# 필수 패키지 설치
uv add google-genai python-dotenv typing-extensions pandas matplotlib scikit-learn
```

### 2.4 환경변수 설정

`.env.example` 파일 생성:

```bash
# .env.example

# Gemini API Key (필수)
GEMINI_API_KEY=your_api_key_here

# Response Mode (1, 2, 3)
# Mode 1: 프롬프트만
# Mode 2: Mode 1 + MIME type (application/json)
# Mode 3: Mode 2 + Schema 정의
RESPONSE_MODE=3

# Model
MODEL=gemini-2.0-flash-lite

# Max Output Tokens
MAX_OUTPUT_TOKENS=2048
```

실제 사용 시 `.env` 파일로 복사 후 API 키 입력:

```bash
cp .env.example .env
# .env 파일을 열어 GEMINI_API_KEY 값 입력
```

#### 환경변수 목록

| 변수명 | 필수 | 기본값 | 설명 |
|--------|------|--------|------|
| `GEMINI_API_KEY` | O | - | Gemini API 키 |
| `RESPONSE_MODE` | X | `3` | 응답 형식 모드 (1, 2, 3) |
| `MODEL` | X | `gemini-2.0-flash-lite` | 사용할 Gemini 모델 |
| `MAX_OUTPUT_TOKENS` | X | `2048` | 최대 출력 토큰 수 |

### 2.5 디렉토리 구조 생성

```bash
mkdir -p domain repository service ai utils prompts data output
touch domain/__init__.py repository/__init__.py service/__init__.py ai/__init__.py utils/__init__.py prompts/__init__.py
```

---

## 3. 프로젝트 구조

최종 프로젝트 구조입니다. 각 파일을 순서대로 작성합니다.

```
solve_test/
├── ai/
│   ├── __init__.py
│   └── gemini_client.py      # Gemini API 클라이언트
├── data/
│   ├── 2023_11_KICE_flat.json # 문제 데이터
│   └── source.json            # 원본 데이터
├── doc/
│   └── 개발_명세서.md          # 이 문서
├── domain/
│   ├── __init__.py
│   └── problem.py             # 데이터 클래스
├── output/
│   └── results.csv            # 풀이 결과 (자동 생성)
├── prompts/
│   ├── __init__.py
│   └── prompt.py              # 프롬프트 정의
├── repository/
│   ├── __init__.py
│   └── problem_repository.py  # 데이터 저장/조회
├── service/
│   ├── __init__.py
│   └── solver_service.py      # 비즈니스 로직
├── utils/
│   ├── __init__.py
│   └── exceptions.py          # 에러 처리
├── main.py                    # 진입점
├── analyze.ipynb              # 분석 노트북
├── pyproject.toml             # 의존성 정의
├── .env                       # 환경변수 (gitignore)
└── .env.example               # 환경변수 예시
```

---

## Step 1: 도메인 모델 정의

> 데이터 구조를 정의하는 dataclass를 작성합니다.

### 파일: `domain/problem.py`

```python
from dataclasses import dataclass
from typing import List


@dataclass
class Problem:
    """수능 국어 문제"""

    id: int
    paragraph: str  # 지문
    question: str  # 문제
    question_plus: str  # 보기 (없으면 "[없음]")
    choices: List[str]  # 선택지 5개
    answer: int  # 정답 (1~5)
    score: int  # 배점 (2 또는 3)


@dataclass
class Answer:
    """AI 풀이 결과"""

    problem_id: int
    predicted: int  # AI가 예측한 답
    actual: int  # 실제 정답
    is_correct: bool  # 정답 여부
    reasoning: str  # AI의 추론 과정
    score: int  # 해당 문제 배점
```

### 파일: `domain/__init__.py`

```python
from .problem import Problem, Answer

__all__ = ["Problem", "Answer"]
```

### 학습 포인트
- `@dataclass`: 데이터 클래스 데코레이터
- 타입 힌트 (`int`, `str`, `List[str]`, `bool`)
- 데이터 모델링의 중요성

---

## Step 2: 에러 처리 모듈

> 앱 전용 에러 클래스와 에러 메시지를 정의합니다.

### 파일: `utils/exceptions.py`

```python
class AppError(Exception):
    """앱 전용 에러 클래스"""

    def __init__(self, error_type: str):
        self.error_type = error_type
        super().__init__(error_type)


ERROR_MESSAGES = {
    "api_key_invalid": "API 키가 유효하지 않습니다. .env 파일을 확인해주세요.",
    "rate_limit": "요청 한도 초과. 60초 후 재시도합니다.",
    "network_error": "네트워크 연결을 확인해주세요.",
    "parse_error": "AI 응답 파싱 실패. 재시도합니다.",
    "file_not_found": "데이터 파일을 찾을 수 없습니다.",
}


def handle_error(error_type: str) -> str:
    """에러 타입에 맞는 메시지 반환"""
    return ERROR_MESSAGES.get(error_type, "알 수 없는 오류가 발생했습니다.")
```

### 파일: `utils/__init__.py`

```python
from .exceptions import AppError, handle_error, ERROR_MESSAGES

__all__ = ["AppError", "handle_error", "ERROR_MESSAGES"]
```

### 학습 포인트
- 커스텀 Exception 클래스
- 딕셔너리를 활용한 에러 메시지 관리
- `.get()` 메서드의 기본값 활용

---

## Step 3: 프롬프트 모듈

> AI에게 보낼 프롬프트를 별도 모듈로 분리합니다. 프롬프트 실험이 용이해집니다.

### 파일: `prompts/prompt.py`

```python
"""
프롬프트 정의 파일

이 파일을 수정하여 다양한 프롬프트 실험을 할 수 있습니다.
- SYSTEM_PROMPT: AI의 역할 정의
- USER_PROMPT_TEMPLATE: 문제 형식 템플릿
- MAX_OUTPUT_TOKENS: 출력 토큰 제한 (환경변수로 설정 가능)
"""

import os

# 출력 토큰 제한 (reasoning 길이 조절)
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "2048"))

# 시스템 프롬프트 (AI 역할 정의)
SYSTEM_PROMPT = """당신은 수능 국어 문제를 푸는 전문가입니다.
주어진 지문을 꼼꼼히 읽고, 문제의 의도를 정확히 파악하여 답을 선택하세요.
반드시 선택한 답의 이유를 구체적으로 설명해야 합니다.
"""

# 유저 프롬프트 템플릿 (문제 형식)
USER_PROMPT_TEMPLATE = """다음 수능 국어 문제를 풀어주세요.

[지문]
{paragraph}

[문제]
{question}

[보기]
{question_plus}

[선택지]
1. {choice_1}
2. {choice_2}
3. {choice_3}
4. {choice_4}
5. {choice_5}

다음 JSON 형식으로 답변하세요:
{{
  "choice": 정답번호(1-5),
  "reasoning": "왜 이 답을 선택했는지 구체적인 근거를 설명하세요. 지문의 어떤 부분이 근거가 되는지, 다른 선택지가 왜 틀렸는지 포함해주세요."
}}
"""


def build_user_prompt(problem) -> str:
    """Problem 객체로 유저 프롬프트 생성"""
    return USER_PROMPT_TEMPLATE.format(
        paragraph=problem.paragraph,
        question=problem.question,
        question_plus=problem.question_plus,
        choice_1=problem.choices[0],
        choice_2=problem.choices[1],
        choice_3=problem.choices[2],
        choice_4=problem.choices[3],
        choice_5=problem.choices[4],
    )
```

### 파일: `prompts/__init__.py`

```python
from .prompt import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    MAX_OUTPUT_TOKENS,
    build_user_prompt,
)

__all__ = [
    "SYSTEM_PROMPT",
    "USER_PROMPT_TEMPLATE",
    "MAX_OUTPUT_TOKENS",
    "build_user_prompt",
]
```

### 학습 포인트
- 프롬프트 엔지니어링
- 템플릿 문자열 (`{변수}`, `{{리터럴 중괄호}}`)
- 상수와 함수의 분리
- 환경변수로 설정값 외부화 (`os.getenv`)

---

## Step 4: Gemini AI 클라이언트

> Gemini API를 호출하는 클라이언트입니다. 3단계 모드를 지원합니다.

### 파일: `ai/gemini_client.py`

```python
import os
import re
import json
import typing_extensions as typing
from google import genai
from google.genai import types

from domain.problem import Problem, Answer
from utils.exceptions import AppError
from prompts.prompt import SYSTEM_PROMPT, MAX_OUTPUT_TOKENS, build_user_prompt


class SolverResponse(typing.TypedDict):
    """Mode 3용 응답 스키마"""

    choice: int
    reasoning: str


class GeminiClient:
    """Gemini API 클라이언트 (3단계 모드 지원)"""

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.mode = int(os.getenv("RESPONSE_MODE", "3"))
        self.model_name = os.getenv("MODEL", "gemini-2.0-flash-lite")
        print(f"[GeminiClient] Model: {self.model_name}")
        print(f"[GeminiClient] Mode: {self.mode}")
        print(f"[GeminiClient] Max Output Tokens: {MAX_OUTPUT_TOKENS}")

    def _get_generation_config(self) -> types.GenerateContentConfig | None:
        """모드에 따른 generation_config 반환"""
        if self.mode == 1:
            # Mode 1: 프롬프트만 (기본 설정 + 토큰 제한)
            return types.GenerateContentConfig(
                max_output_tokens=MAX_OUTPUT_TOKENS,
            )
        elif self.mode == 2:
            # Mode 2: MIME type 추가
            return types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=MAX_OUTPUT_TOKENS,
            )
        else:
            # Mode 3: Schema 추가
            return types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SolverResponse,
                max_output_tokens=MAX_OUTPUT_TOKENS,
            )

    def _build_prompt(self, problem: Problem) -> str:
        """시스템 프롬프트 + 유저 프롬프트 결합"""
        user_prompt = build_user_prompt(problem)
        return SYSTEM_PROMPT + "\n\n" + user_prompt

    def solve_problem(self, problem: Problem) -> Answer:
        """문제 풀이 (모드에 따라 다른 설정 적용)"""
        prompt = self._build_prompt(problem)
        config = self._get_generation_config()

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config,
            )
            return self._parse_response(response.text, problem)
        except Exception as e:
            error_msg = str(e).lower()
            if "rate" in error_msg or "quota" in error_msg:
                raise AppError("rate_limit")
            elif "api" in error_msg or "key" in error_msg:
                raise AppError("api_key_invalid")
            else:
                raise AppError("network_error")

    def _parse_response(self, response_text: str, problem: Problem) -> Answer:
        """응답 파싱"""
        try:
            data = json.loads(response_text)
            predicted = data.get("choice", 0)
            reasoning = data.get("reasoning", "")
        except json.JSONDecodeError:
            # Mode 1에서 JSON 파싱 실패 시 텍스트 파싱 시도
            predicted = self._extract_answer_from_text(response_text)
            reasoning = response_text

        return Answer(
            problem_id=problem.id,
            predicted=predicted,
            actual=problem.answer,
            is_correct=(predicted == problem.answer),
            reasoning=reasoning,
            score=problem.score,
        )

    def _extract_answer_from_text(self, text: str) -> int:
        """텍스트에서 정답 번호 추출 (Mode 1 fallback)"""
        patterns = [
            r"정답[:\s]*(\d)",
            r'"choice"[:\s]*(\d)',
            r"답[:\s]*(\d)",
            r"(\d)번",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return int(match.group(1))
        return 0
```

### 파일: `ai/__init__.py`

```python
from .gemini_client import GeminiClient

__all__ = ["GeminiClient"]
```

### 학습 포인트
- API 클라이언트 패턴
- 환경변수 활용 (`os.getenv`)
- TypedDict를 활용한 스키마 정의
- JSON 파싱과 예외 처리
- 정규표현식 (`re.search`)

---

## Step 5: 레포지토리 (데이터 저장/조회)

> 데이터 저장과 조회를 담당합니다. pandas를 사용하여 CSV를 처리합니다.

### 파일: `repository/problem_repository.py`

```python
import json
from typing import List, Set
from pathlib import Path

import pandas as pd

from domain.problem import Problem, Answer


class ProblemRepository:
    """문제 데이터 저장/조회 담당"""

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def load_problems(self) -> List[Problem]:
        """JSON 파일에서 문제 로드"""
        with open(self.data_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)

        problems = []
        for _, item in data.items():
            problem = Problem(
                id=item["id"],
                paragraph=item["paragraph"],
                question=item["question"],
                question_plus=item["question_plus"],
                choices=item["choices"],
                answer=item["answer"],
                score=item.get("score", 2),
            )
            problems.append(problem)

        return sorted(problems, key=lambda p: p.id)

    def init_output(self, output_path: str):
        """출력 파일 초기화 (헤더만 있는 빈 DataFrame 저장)"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(columns=[
            "problem_id", "score", "predicted", "actual",
            "is_correct", "earned_score", "reasoning"
        ])
        df.to_csv(path, index=False, encoding="utf-8-sig")

    def append_result(self, answer: Answer, output_path: str):
        """결과 한 줄 추가 (기존 파일에 append)"""
        earned = answer.score if answer.is_correct else 0
        new_row = pd.DataFrame([{
            "problem_id": answer.problem_id,
            "score": answer.score,
            "predicted": answer.predicted,
            "actual": answer.actual,
            "is_correct": answer.is_correct,
            "earned_score": earned,
            "reasoning": answer.reasoning,
        }])
        new_row.to_csv(output_path, mode="a", header=False, index=False, encoding="utf-8-sig")

    def get_solved_ids(self, output_path: str) -> Set[int]:
        """이미 풀이된 문제 ID 조회 (재시작 시 사용)"""
        path = Path(output_path)
        if not path.exists():
            return set()

        df = pd.read_csv(path, encoding="utf-8-sig")
        if df.empty:
            return set()

        return set(df["problem_id"].tolist())
```

### 파일: `repository/__init__.py`

```python
from .problem_repository import ProblemRepository

__all__ = ["ProblemRepository"]
```

### 학습 포인트
- Repository 패턴 (데이터 접근 추상화)
- pandas DataFrame 활용
- CSV 파일 읽기/쓰기 (append 모드)
- `utf-8-sig` 인코딩 (Excel 호환)
- `pathlib.Path` 활용

---

## Step 6: 서비스 (비즈니스 로직)

> 문제 풀이의 핵심 비즈니스 로직입니다. Rate Limit 처리와 재시도 로직을 포함합니다.

### 파일: `service/solver_service.py`

```python
import time
from typing import List
from pathlib import Path

import pandas as pd

from domain.problem import Problem, Answer
from ai.gemini_client import GeminiClient
from repository.problem_repository import ProblemRepository
from utils.exceptions import AppError, handle_error


class SolverService:
    """문제 풀이 비즈니스 로직 (Rate Limit 처리 포함)"""

    def __init__(self, client: GeminiClient, repository: ProblemRepository):
        self.client = client
        self.repository = repository

    def solve_all(self, problems: List[Problem], output_path: str) -> List[Answer]:
        """모든 문제 풀이 (중간 저장)"""
        # 이미 풀이된 문제 제외
        solved_ids = self.repository.get_solved_ids(output_path)
        remaining = [p for p in problems if p.id not in solved_ids]

        if solved_ids:
            print(f"이전 풀이 {len(solved_ids)}개 발견, {len(remaining)}개 남음")
        else:
            # 새 파일 초기화
            self.repository.init_output(output_path)

        if not remaining:
            print("모든 문제가 이미 풀이되었습니다.")
            return []

        results = []
        for i, problem in enumerate(remaining):
            # 문제 풀이
            answer = self._solve_with_retry(problem)
            results.append(answer)

            # 즉시 저장
            self.repository.append_result(answer, output_path)

            # 진행 상황 출력
            status = "O" if answer.is_correct else "X"
            earned = answer.score if answer.is_correct else 0
            print(f"[{i+1}/{len(remaining)}] 문제 {problem.id} ({problem.score}점): {status} (+{earned}점)")

            # Rate Limit 처리 (마지막 문제 제외)
            if i < len(remaining) - 1:
                if (i + 1) % 5 == 0:
                    print(">>> 60초 대기 (Rate Limit)...")
                    time.sleep(60)
                else:
                    time.sleep(10)

        return results

    def _solve_with_retry(self, problem: Problem, max_retries: int = 3) -> Answer:
        """재시도 로직 포함 문제 풀이"""
        for attempt in range(max_retries):
            try:
                return self.client.solve_problem(problem)
            except AppError as e:
                print(f"  [재시도 {attempt+1}/{max_retries}] {handle_error(e.error_type)}")
                if e.error_type == "rate_limit":
                    time.sleep(60)
                elif e.error_type == "parse_error":
                    time.sleep(5)
                else:
                    time.sleep(10)
            except Exception as e:
                print(f"  [재시도 {attempt+1}/{max_retries}] 예상치 못한 오류: {e}")
                time.sleep(10)

        # 모든 재시도 실패 시 빈 Answer 반환
        return Answer(
            problem_id=problem.id,
            predicted=0,
            actual=problem.answer,
            is_correct=False,
            reasoning="[풀이 실패]",
            score=problem.score,
        )

    def calculate_score(self, output_path: str) -> tuple[int, int, int, int]:
        """결과 파일에서 점수 계산

        Returns:
            (총 문제 수, 정답 수, 획득 점수, 총점)
        """
        path = Path(output_path)
        if not path.exists():
            return 0, 0, 0, 0

        df = pd.read_csv(path, encoding="utf-8-sig")
        if df.empty:
            return 0, 0, 0, 0

        total_count = len(df)
        correct_count = int(df["is_correct"].sum())
        earned_score = int(df["earned_score"].sum())
        total_score = int(df["score"].sum())

        return total_count, correct_count, earned_score, total_score
```

### 파일: `service/__init__.py`

```python
from .solver_service import SolverService

__all__ = ["SolverService"]
```

### 학습 포인트
- Service 패턴 (비즈니스 로직 분리)
- Rate Limit 처리 전략
- 재시도 로직 (Retry Pattern)
- 중간 저장으로 안정성 확보

### Rate Limit 전략

Gemini 무료 버전은 분당 요청 수 제한이 있습니다.

```
문제 1 → 10초 대기
문제 2 → 10초 대기
문제 3 → 10초 대기
문제 4 → 10초 대기
문제 5 → 60초 대기 (5문제마다 1분 대기)
문제 6 → 10초 대기
...
```

---

## Step 7: 메인 진입점

> 프로그램의 진입점입니다. argparse로 CLI 인자를 처리합니다.

### 파일: `main.py`

```python
import os
import sys
import argparse
from dotenv import load_dotenv

from domain.problem import Problem, Answer
from repository.problem_repository import ProblemRepository
from service.solver_service import SolverService
from ai.gemini_client import GeminiClient


def parse_args():
    """CLI 인자 파싱"""
    parser = argparse.ArgumentParser(description="수능 국어 문제 풀이 AI")
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="./data/2023_11_KICE_flat.json",
        help="입력 데이터 경로 (JSON)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="./output/results.csv",
        help="출력 결과 경로 (CSV)"
    )
    return parser.parse_args()


def main():
    # 0. CLI 인자 파싱
    args = parse_args()

    # 1. 환경변수 로드
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    mode = os.getenv("RESPONSE_MODE", "3")

    if not api_key:
        print("GEMINI_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 확인하거나 환경변수를 설정해주세요.")
        sys.exit(1)

    print("=== 수능 국어 문제 풀이 AI ===")
    print(f"Response Mode: {mode}")
    print(f"입력: {args.input}")
    print(f"출력: {args.output}")
    print()

    # 2. 의존성 초기화
    repository = ProblemRepository(args.input)
    client = GeminiClient(api_key)
    service = SolverService(client, repository)

    # 3. 문제 로드
    try:
        problems = repository.load_problems()
        total_score = sum(p.score for p in problems)
        print(f"총 {len(problems)}개 문제 로드 완료 (만점: {total_score}점)")
        print()
    except FileNotFoundError:
        print("데이터 파일을 찾을 수 없습니다.")
        print(f"{args.input} 경로를 확인해주세요.")
        sys.exit(1)

    # 4. 문제 풀이 실행 (중간 저장)
    try:
        results = service.solve_all(problems, args.output)
    except KeyboardInterrupt:
        print("\n중단됨 (진행 상황은 저장되었습니다)")
        sys.exit(0)

    print()
    print(f"결과가 {args.output}에 저장되었습니다.")

    # 5. 점수 계산 및 출력
    total_count, correct_count, earned, total = service.calculate_score(args.output)
    accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
    score_rate = (earned / total * 100) if total > 0 else 0

    print()
    print("=" * 40)
    print("결과")
    print("=" * 40)
    print(f"총 문제: {total_count}개")
    print(f"정답: {correct_count}개 / 오답: {total_count - correct_count}개")
    print(f"정답률: {accuracy:.1f}%")
    print()
    print(f"획득 점수: {earned}점 / {total}점")
    print(f"점수 백분율: {score_rate:.1f}%")
    print("=" * 40)


if __name__ == "__main__":
    main()
```

### 학습 포인트
- argparse를 활용한 CLI 인자 처리
- python-dotenv로 환경변수 관리
- 의존성 주입 (Dependency Injection)
- 프로그램 실행 흐름 설계

---

## Step 8: 분석 노트북

> 풀이 결과를 분석하는 Jupyter Notebook입니다.

### 파일: `analyze.ipynb`

주요 셀 구성:

#### 셀 1: 데이터 로드 및 점수 계산

```python
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 결과 파일 로드
results = pd.read_csv("./output/results.csv", encoding="utf-8-sig")

# 점수 계산
total_count = len(results)
correct_count = results['is_correct'].sum()
total_score = results['score'].sum()
earned_score = results['earned_score'].sum()
accuracy = correct_count / total_count * 100
score_rate = earned_score / total_score * 100

print(f"총 문제: {total_count}개")
print(f"정답: {correct_count}개 / 오답: {total_count - correct_count}개")
print(f"정답률: {accuracy:.1f}%")
print(f"획득 점수: {earned_score}점 / {total_score}점")
print(f"점수 백분율: {score_rate:.1f}%")
```

#### 셀 2: 오답 문제 분석 (reasoning 확인)

```python
wrong_df = results[results['is_correct'] == False]
print(f"오답 문제: {len(wrong_df)}개")

for _, row in wrong_df.iterrows():
    print("=" * 60)
    print(f"문제 {int(row['problem_id'])} ({int(row['score'])}점)")
    print(f"  AI 예측: {int(row['predicted'])}번")
    print(f"  정답: {int(row['actual'])}번")
    print(f"  AI 근거: {row['reasoning'][:200]}...")
```

#### 셀 3: 혼동 행렬

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(results["actual"], results["predicted"], labels=[1,2,3,4,5])
disp = ConfusionMatrixDisplay(cm, display_labels=[1,2,3,4,5])
disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.show()
```

---

## 실행 및 테스트

### 기본 실행

```bash
# .env 파일 설정 후
uv run python main.py
```

### 경로 지정 실행

```bash
uv run python main.py -i ./data/2023_11_KICE_flat.json -o ./output/results.csv
```

### 모드 변경 실행

```bash
# Mode 1: 프롬프트만
RESPONSE_MODE=1 uv run python main.py

# Mode 2: 프롬프트 + MIME type
RESPONSE_MODE=2 uv run python main.py

# Mode 3: 프롬프트 + MIME type + Schema (기본값)
RESPONSE_MODE=3 uv run python main.py
```

### 모델/토큰 변경 실행

```bash
# 다른 모델 사용
MODEL=gemini-2.0-flash uv run python main.py

# 토큰 수 변경
MAX_OUTPUT_TOKENS=4096 uv run python main.py

# 여러 환경변수 동시 변경
MODEL=gemini-2.0-flash MAX_OUTPUT_TOKENS=4096 RESPONSE_MODE=2 uv run python main.py
```

### 중단 후 재실행

프로그램 중단 후 재실행하면 이전 풀이를 건너뛰고 이어서 진행합니다.

```bash
# Ctrl+C로 중단 후
uv run python main.py  # 자동으로 이어서 풀이
```

### 분석 실행

```bash
jupyter notebook analyze.ipynb
```

---

## 응답 형식 강제 (3단계 모드)

> AI 응답을 원하는 형태로 고정하기 위한 3단계 모드입니다.

### Mode 비교

| Mode | 방법 | 강제 수준 | 결과 |
|------|------|----------|------|
| 1 | 프롬프트만 | 약함 | JSON 파싱 실패 가능 |
| 2 | Mode 1 + `response_mime_type` | 중간 | JSON 구조 보장 |
| 3 | Mode 2 + `response_schema` | 강함 | 필드까지 보장 |

### 교육 포인트

```
Mode 1 실행 → JSON 파싱 실패 경험 → "프롬프트만으론 부족하구나"
    ↓
Mode 2 실행 → JSON은 오지만 필드가 다름 → "구조는 맞는데..."
    ↓
Mode 3 실행 → 완벽한 응답 → "스키마로 완벽하게 통제!"
```

학생들이 직접 모드를 바꿔가며 실행해보면서 **왜 점점 더 엄격한 방법이 필요한지** 체감할 수 있습니다.

---

## 프롬프트 실험 가이드

`prompts/prompt.py` 파일을 수정하여 다양한 실험을 할 수 있습니다.

### 실험 1: 더 상세한 풀이

```python
MAX_OUTPUT_TOKENS = 2048

SYSTEM_PROMPT = """당신은 수능 국어 문제를 푸는 전문가입니다.
단계별로 사고하며 문제를 풀어주세요:
1. 지문의 핵심 내용 파악
2. 문제가 묻는 것 정확히 이해
3. 각 선택지 하나씩 검토
4. 소거법으로 오답 제거
5. 최종 답 선택
"""
```

### 실험 2: 간결한 응답

```python
MAX_OUTPUT_TOKENS = 512

SYSTEM_PROMPT = """수능 국어 전문가입니다. 정답과 핵심 이유만 간결히 답하세요."""
```

### 실험 3: Chain-of-Thought

```python
USER_PROMPT_TEMPLATE = """...
다음 형식으로 단계별로 답변하세요:
{{
  "choice": 정답번호,
  "reasoning": {{
    "passage_summary": "지문 핵심 내용",
    "question_intent": "문제의 의도",
    "choice_analysis": "각 선택지 분석",
    "final_reason": "최종 선택 이유"
  }}
}}
"""
```

---

## 부록: 예상 출력 예시

### CLI 출력

```
=== 수능 국어 문제 풀이 AI ===
Response Mode: 3
입력: ./data/2023_11_KICE_flat.json
출력: ./output/results.csv

[GeminiClient] Model: gemini-2.0-flash-lite
[GeminiClient] Mode: 3
[GeminiClient] Max Output Tokens: 2048
총 45개 문제 로드 완료 (만점: 100점)

[1/45] 문제 1 (2점): O (+2점)
[2/45] 문제 2 (3점): O (+3점)
[3/45] 문제 3 (2점): X (+0점)
[4/45] 문제 4 (2점): O (+2점)
[5/45] 문제 5 (2점): O (+2점)
>>> 60초 대기 (Rate Limit)...
[6/45] 문제 6 (2점): O (+2점)
...

결과가 ./output/results.csv에 저장되었습니다.

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

### 결과 CSV 구조

| problem_id | score | predicted | actual | is_correct | earned_score | reasoning |
|------------|-------|-----------|--------|------------|--------------|-----------|
| 1 | 2 | 4 | 4 | True | 2 | 지문에서 "독자의 배경지식, 관점"은... |
| 2 | 3 | 5 | 5 | True | 3 | ⓓ에서 "내가 진정으로 좋아하는..."  |
| 3 | 2 | 2 | 1 | False | 0 | 스스로 독서 계획을 세우는 것은... |

---

## 체크리스트

개발 완료 후 확인해주세요:

- [ ] `.env` 파일에 `GEMINI_API_KEY` 설정
- [ ] `data/2023_11_KICE_flat.json` 파일 존재 확인
- [ ] `uv run python main.py` 실행 테스트
- [ ] Mode 1, 2, 3 변경 실행 테스트
- [ ] 모델/토큰 환경변수 변경 테스트
- [ ] 중단 후 재실행 테스트
- [ ] `analyze.ipynb`에서 결과 분석
