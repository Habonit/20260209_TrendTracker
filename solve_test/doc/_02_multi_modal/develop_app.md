# 멀티모달 이미지 처리 기능 추가 - 개발 가이드

> 이 문서를 따라 단계별로 개발하면 기존 텍스트 기반 앱에 이미지 처리 기능을 추가할 수 있습니다.

---

## 목차

1. [개요](#1-개요)
2. [사전 준비](#2-사전-준비)
3. [Step 1: 프롬프트 모듈 추가](#step-1-프롬프트-모듈-추가)
4. [Step 2: 멀티모달 AI 클라이언트 추가](#step-2-멀티모달-ai-클라이언트-추가)
5. [Step 3: main.py 수정](#step-3-mainpy-수정)
6. [Step 4: 에러 타입 추가 (선택)](#step-4-에러-타입-추가-선택)
7. [테스트 데이터 준비](#테스트-데이터-준비)
8. [실행 및 테스트](#실행-및-테스트)
9. [학습 포인트 정리](#학습-포인트-정리)
10. [체크리스트](#체크리스트)

---

## 1. 개요

### 목표

기존 텍스트 기반 수능 문제 풀이 앱에 **이미지 문제 처리 기능**을 추가합니다.

### 설계 원칙: OCP (Open-Closed Principle)

```
"소프트웨어 개체(클래스, 모듈, 함수 등)는
 확장에는 열려 있어야 하고, 수정에는 닫혀 있어야 한다."
```

| 파일 | 변경 여부 | 설명 |
|------|----------|------|
| `domain/problem.py` | **유지** | 데이터 클래스 수정 없음 |
| `prompts/prompt.py` | **유지** | 기존 텍스트 프롬프트 유지 |
| `ai/gemini_client.py` | **유지** | 기존 클라이언트 유지 |
| `service/solver_service.py` | **유지** | 공통 서비스 그대로 사용 |
| `repository/problem_repository.py` | **유지** | 공통 저장소 그대로 사용 |
| `main.py` | **수정** | 분기 로직만 추가 |
| `prompts/prompt_multi.py` | **신규** | 이미지용 프롬프트 |
| `ai/gemini_multi_client.py` | **신규** | 멀티모달 클라이언트 |

### 변경 전후 비교

**Before (텍스트만)**
```
main.py → GeminiClient → prompt.py
```

**After (텍스트 + 이미지)**
```
main.py
  ├── type=text  → GeminiClient      → prompt.py
  └── type=multi → GeminiMultiClient → prompt_multi.py
```

---

## 2. 사전 준비

### 2.1 기존 프로젝트 확인

텍스트 버전이 정상 동작하는지 확인합니다.

```bash
# 텍스트 버전 실행 테스트
uv run python main.py -i ./data/2023_11_KICE_flat.json -o ./output/test_results.csv
```

### 2.2 현재 파일 구조 확인

```
solve_test/
├── ai/
│   ├── __init__.py
│   └── gemini_client.py      ← 기존 (수정 안 함)
├── prompts/
│   ├── __init__.py
│   └── prompt.py             ← 기존 (수정 안 함)
├── domain/
│   └── problem.py            ← 기존 (수정 안 함)
├── service/
│   └── solver_service.py     ← 기존 (수정 안 함)
├── repository/
│   └── problem_repository.py ← 기존 (수정 안 함)
├── utils/
│   └── exceptions.py         ← 에러 타입만 추가
└── main.py                   ← 분기 로직 추가
```

### 2.3 데이터 스키마 이해

**핵심**: 기존 `Problem` 데이터클래스를 그대로 사용합니다.

```python
@dataclass
class Problem:
    id: int
    paragraph: str        # 이미지 문제: "없음"
    question: str         # 이미지 문제: 이미지 경로
    question_plus: str    # 이미지 문제: "없음"
    choices: List[str]    # 이미지 문제: ["없음", "없음", ...]
    answer: int
    score: int
```

이미지 문제에서는 `question` 필드에 이미지 경로가 들어갑니다.

---

## Step 1: 프롬프트 모듈 추가

> 이미지 문제용 프롬프트를 정의합니다. 기존 `prompt.py`는 수정하지 않습니다.

### 파일: `prompts/prompt_multi.py`

```python
"""
이미지 문제용 프롬프트 정의

기존 prompt.py를 수정하지 않고 새로운 파일로 추가합니다.
이미지에는 지문, 문제, 선택지가 모두 포함되어 있습니다.
"""
import os

# 출력 토큰 제한
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "2048"))

# 시스템 프롬프트 (이미지 분석용)
SYSTEM_PROMPT_MULTI = """당신은 수능 국어 문제를 푸는 전문가입니다.
제공된 이미지에는 지문, 문제, 선택지가 모두 포함되어 있습니다.
이미지를 꼼꼼히 분석하여 정답을 선택하세요.
반드시 선택한 답의 이유를 구체적으로 설명해야 합니다.
"""

# 유저 프롬프트 (이미지와 함께 전송)
USER_PROMPT_MULTI = """다음 이미지를 보고 수능 국어 문제를 풀어주세요.

이미지에 포함된 내용:
- 지문 (본문)
- 문제
- 선택지 (1~5번)

다음 JSON 형식으로 답변하세요:
{
  "choice": 정답번호(1-5),
  "reasoning": "왜 이 답을 선택했는지 구체적인 근거를 설명하세요."
}
"""
```

### 파일: `prompts/__init__.py` 수정

기존 내용에 새로운 import를 추가합니다.

```python
from .prompt import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    MAX_OUTPUT_TOKENS,
    build_user_prompt,
)

# 멀티모달 프롬프트 추가
from .prompt_multi import (
    SYSTEM_PROMPT_MULTI,
    USER_PROMPT_MULTI,
    MAX_OUTPUT_TOKENS as MAX_OUTPUT_TOKENS_MULTI,
)

__all__ = [
    # 기존 텍스트용
    "SYSTEM_PROMPT",
    "USER_PROMPT_TEMPLATE",
    "MAX_OUTPUT_TOKENS",
    "build_user_prompt",
    # 멀티모달용
    "SYSTEM_PROMPT_MULTI",
    "USER_PROMPT_MULTI",
    "MAX_OUTPUT_TOKENS_MULTI",
]
```

### 학습 포인트

- **OCP 적용**: 기존 `prompt.py`를 수정하지 않고 새 파일 추가
- **이미지 프롬프트 특징**: 텍스트 필드 포맷팅 불필요 (이미지에 모두 포함)
- **모듈 확장**: `__init__.py`에 새 모듈 등록

---

## Step 2: 멀티모달 AI 클라이언트 추가

> Gemini API의 멀티모달 기능을 사용하는 새 클라이언트를 추가합니다.

### 파일: `ai/gemini_multi_client.py`

```python
"""
멀티모달 Gemini API 클라이언트

기존 gemini_client.py를 수정하지 않고 새로운 파일로 추가합니다.
이미지를 포함한 멀티모달 요청을 처리합니다.
"""
import os
import json
from pathlib import Path
import typing_extensions as typing
from google import genai
from google.genai import types

from domain.problem import Problem, Answer
from utils.exceptions import AppError
from prompts.prompt_multi import (
    SYSTEM_PROMPT_MULTI,
    USER_PROMPT_MULTI,
    MAX_OUTPUT_TOKENS,
)


class SolverResponse(typing.TypedDict):
    """응답 스키마 (기존과 동일)"""
    choice: int
    reasoning: str


class GeminiMultiClient:
    """멀티모달 Gemini API 클라이언트

    기존 GeminiClient와 동일한 인터페이스(solve_problem)를 제공하여
    SolverService에서 그대로 사용할 수 있습니다.
    """

    # 지원하는 이미지 확장자
    SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}

    # 확장자별 MIME 타입
    MIME_TYPES = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }

    def __init__(self, api_key: str):
        """클라이언트 초기화

        Args:
            api_key: Gemini API 키
        """
        self.client = genai.Client(api_key=api_key)
        self.model_name = os.getenv("MODEL", "gemini-2.0-flash-lite")
        print(f"[GeminiMultiClient] Model: {self.model_name}")
        print(f"[GeminiMultiClient] Max Output Tokens: {MAX_OUTPUT_TOKENS}")

    def _load_image(self, image_path: str) -> tuple[bytes, str]:
        """이미지 파일 로드

        Args:
            image_path: 이미지 파일 경로

        Returns:
            (이미지 바이너리 데이터, MIME 타입)

        Raises:
            AppError: 파일이 없거나 지원하지 않는 형식일 때
        """
        path = Path(image_path)
        ext = path.suffix.lower()

        # 확장자 검증
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise AppError("unsupported_image_format")

        # 파일 존재 검증
        if not path.exists():
            raise AppError("image_not_found")

        # 이미지 로드
        with open(path, "rb") as f:
            image_data = f.read()

        return image_data, self.MIME_TYPES[ext]

    def _build_contents(self, problem: Problem) -> list:
        """멀티모달 콘텐츠 구성

        Args:
            problem: 문제 객체 (question 필드에 이미지 경로)

        Returns:
            Gemini API에 전송할 콘텐츠 리스트
        """
        # question 필드에서 이미지 경로 추출
        image_data, mime_type = self._load_image(problem.question)

        # 텍스트 + 이미지 + 텍스트 구조 (text= 키워드 인자 필수!)
        return [
            types.Part.from_text(text=SYSTEM_PROMPT_MULTI),
            types.Part.from_bytes(data=image_data, mime_type=mime_type),
            types.Part.from_text(text=USER_PROMPT_MULTI),
        ]

    def solve_problem(self, problem: Problem) -> Answer:
        """이미지 문제 풀이

        Args:
            problem: 문제 객체

        Returns:
            Answer 객체 (예측 답, 정답, reasoning 포함)

        Note:
            기존 GeminiClient.solve_problem()과 동일한 시그니처를 유지하여
            SolverService에서 그대로 사용할 수 있습니다.
        """
        contents = self._build_contents(problem)

        # Mode 3 스타일: JSON + Schema 강제
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SolverResponse,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
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
        """응답 파싱

        Args:
            response_text: AI 응답 텍스트 (JSON)
            problem: 원본 문제 객체

        Returns:
            Answer 객체
        """
        data = json.loads(response_text)
        predicted = data.get("choice", 0)
        reasoning = data.get("reasoning", "")

        return Answer(
            problem_id=problem.id,
            predicted=predicted,
            actual=problem.answer,
            is_correct=(predicted == problem.answer),
            reasoning=reasoning,
            score=problem.score,
        )
```

### 파일: `ai/__init__.py` 수정

```python
from .gemini_client import GeminiClient
from .gemini_multi_client import GeminiMultiClient

__all__ = ["GeminiClient", "GeminiMultiClient"]
```

### 학습 포인트

- **멀티모달 API 사용법**: `types.Part.from_bytes()`로 이미지 전송
- **키워드 인자 필수**: `Part.from_text(text=...)` 형태로 호출 (위치 인자 불가)
- **동일 인터페이스 유지**: `solve_problem()` 메서드 시그니처 동일
- **파일 I/O**: 바이너리 모드(`"rb"`)로 이미지 읽기
- **MIME 타입**: 이미지 형식별 올바른 MIME 타입 지정

### 멀티모달 콘텐츠 구조

```python
contents = [
    types.Part.from_text(text=SYSTEM_PROMPT),  # 1. 시스템 프롬프트
    types.Part.from_bytes(data=image, mime_type="image/png"),  # 2. 이미지
    types.Part.from_text(text=USER_PROMPT),  # 3. 유저 프롬프트
]
```

---

## Step 3: main.py 수정

> 기존 main.py에 `--type` 인자를 추가하고 분기 로직을 구현합니다.

### 파일: `main.py` (전체 교체)

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
    # 신규: 문제 유형 선택
    parser.add_argument(
        "-t", "--type",
        type=str,
        choices=["text", "multi"],
        default="text",
        help="문제 유형 (text: 텍스트, multi: 이미지)"
    )
    return parser.parse_args()


def run_text_solver(args, api_key: str):
    """텍스트 문제 풀이 (기존 로직)"""
    mode = os.getenv("RESPONSE_MODE", "3")

    print("=== 수능 국어 문제 풀이 AI (텍스트) ===")
    print(f"Response Mode: {mode}")
    print(f"입력: {args.input}")
    print(f"출력: {args.output}")
    print()

    # 기존과 동일한 의존성 초기화
    repository = ProblemRepository(args.input)
    client = GeminiClient(api_key)
    service = SolverService(client, repository)

    _run_solver(service, repository, args.output)


def run_multi_solver(args, api_key: str):
    """이미지 문제 풀이 (멀티모달)"""
    # 지연 임포트: multi 모드에서만 로드
    from ai.gemini_multi_client import GeminiMultiClient

    print("=== 수능 국어 문제 풀이 AI (이미지) ===")
    print(f"입력: {args.input}")
    print(f"출력: {args.output}")
    print()

    # 멀티모달 클라이언트 사용
    repository = ProblemRepository(args.input)
    client = GeminiMultiClient(api_key)  # ← 여기가 다름!
    service = SolverService(client, repository)  # 서비스는 동일

    _run_solver(service, repository, args.output)


def _run_solver(service: SolverService, repository: ProblemRepository, output_path: str):
    """공통 풀이 로직"""
    # 문제 로드
    try:
        problems = repository.load_problems()
        total_score = sum(p.score for p in problems)
        print(f"총 {len(problems)}개 문제 로드 완료 (만점: {total_score}점)")
        print()
    except FileNotFoundError:
        print("데이터 파일을 찾을 수 없습니다.")
        sys.exit(1)

    # 문제 풀이 실행
    try:
        results = service.solve_all(problems, output_path)
    except KeyboardInterrupt:
        print("\n중단됨 (진행 상황은 저장되었습니다)")
        sys.exit(0)

    # 결과 출력
    _print_results(service, output_path)


def _print_results(service: SolverService, output_path: str):
    """결과 출력"""
    print()
    print(f"결과가 {output_path}에 저장되었습니다.")

    total_count, correct_count, earned, total = service.calculate_score(output_path)
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


def main():
    args = parse_args()

    # 환경변수 로드
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("GEMINI_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 확인하거나 환경변수를 설정해주세요.")
        sys.exit(1)

    # 타입에 따라 분기
    if args.type == "text":
        run_text_solver(args, api_key)
    else:
        run_multi_solver(args, api_key)


if __name__ == "__main__":
    main()
```

### 학습 포인트

- **분기 패턴**: `--type` 인자로 실행 경로 선택
- **지연 임포트**: 필요할 때만 모듈 로드 (`from ... import ...`)
- **코드 재사용**: `_run_solver()`, `_print_results()` 공통 함수 추출
- **동일 인터페이스 활용**: `SolverService`가 두 클라이언트 모두 사용 가능

### 핵심 변경점

```python
# 텍스트 모드
client = GeminiClient(api_key)

# 멀티모달 모드
client = GeminiMultiClient(api_key)

# 서비스는 동일!
service = SolverService(client, repository)
```

**왜 이게 가능한가?**
- 두 클라이언트 모두 `solve_problem(problem: Problem) -> Answer` 메서드 제공
- `SolverService`는 이 메서드만 호출
- **덕 타이핑(Duck Typing)**: 동일한 인터페이스면 교체 가능

---

## Step 4: 에러 타입 추가 (선택)

> 이미지 관련 에러 메시지를 추가합니다.

### 파일: `utils/exceptions.py` 수정

```python
class AppError(Exception):
    """앱 전용 에러 클래스"""

    def __init__(self, error_type: str):
        self.error_type = error_type
        super().__init__(error_type)


ERROR_MESSAGES = {
    # 기존 에러
    "api_key_invalid": "API 키가 유효하지 않습니다. .env 파일을 확인해주세요.",
    "rate_limit": "요청 한도 초과. 60초 후 재시도합니다.",
    "network_error": "네트워크 연결을 확인해주세요.",
    "parse_error": "AI 응답 파싱 실패. 재시도합니다.",
    "file_not_found": "데이터 파일을 찾을 수 없습니다.",
    # 신규 에러 (이미지 관련)
    "image_not_found": "이미지 파일을 찾을 수 없습니다.",
    "unsupported_image_format": "지원하지 않는 이미지 형식입니다. (png, jpg, jpeg만 지원)",
}


def handle_error(error_type: str) -> str:
    """에러 타입에 맞는 메시지 반환"""
    return ERROR_MESSAGES.get(error_type, "알 수 없는 오류가 발생했습니다.")
```

---

## 테스트 데이터 준비

### 이미지 문제 데이터 형식

파일: `data/image_problems.json`

```json
{
    "1": {
        "id": 1,
        "paragraph": "없음",
        "question": "./images/q1.png",
        "question_plus": "없음",
        "choices": ["없음", "없음", "없음", "없음", "없음"],
        "answer": 3,
        "score": 2
    },
    "2": {
        "id": 2,
        "paragraph": "없음",
        "question": "./images/q2.jpg",
        "question_plus": "없음",
        "choices": ["없음", "없음", "없음", "없음", "없음"],
        "answer": 5,
        "score": 3
    }
}
```

### 이미지 파일 준비

```
solve_test/
├── images/
│   ├── q1.png    # 문제 1 이미지
│   ├── q2.jpg    # 문제 2 이미지
│   └── ...
└── data/
    └── image_problems.json
```

### 이미지 요구사항

- **해상도**: 최소 800x600 권장
- **형식**: PNG, JPG, JPEG
- **내용**: 지문 + 문제 + 선택지가 한 이미지에 포함

---

## 실행 및 테스트

### 텍스트 문제 실행 (기존)

```bash
# 기본 실행 (type 생략 시 text)
uv run python main.py -i ./data/2023_11_KICE_flat.json

# 명시적으로 text 지정
uv run python main.py -i ./data/2023_11_KICE_flat.json --type text
```

### 이미지 문제 실행 (신규)

```bash
# 이미지 문제 실행
uv run python main.py -i ./data/image_problems.json --type multi

# 출력 경로 지정
uv run python main.py -i ./data/image_problems.json -o ./output/image_results.csv --type multi
```

### 예상 출력

```
=== 수능 국어 문제 풀이 AI (이미지) ===
입력: ./data/image_problems.json
출력: ./output/results.csv

[GeminiMultiClient] Model: gemini-2.0-flash-lite
[GeminiMultiClient] Max Output Tokens: 2048
총 10개 문제 로드 완료 (만점: 25점)

[1/10] 문제 1 (2점): O (+2점)
[2/10] 문제 2 (3점): X (+0점)
[3/10] 문제 3 (2점): O (+2점)
...

========================================
결과
========================================
총 문제: 10개
정답: 7개 / 오답: 3개
정답률: 70.0%

획득 점수: 17점 / 25점
점수 백분율: 68.0%
========================================
```

---

## 학습 포인트 정리

### OCP (Open-Closed Principle)

| 원칙 | 적용 |
|------|------|
| 수정에 닫힘 | 기존 파일 (`gemini_client.py`, `prompt.py` 등) 수정 없음 |
| 확장에 열림 | 새 파일 추가로 기능 확장 (`gemini_multi_client.py`, `prompt_multi.py`) |

### 덕 타이핑 (Duck Typing)

```python
# 두 클라이언트 모두 동일한 메서드 시그니처 제공
class GeminiClient:
    def solve_problem(self, problem: Problem) -> Answer: ...

class GeminiMultiClient:
    def solve_problem(self, problem: Problem) -> Answer: ...

# SolverService는 둘 다 사용 가능
service = SolverService(client, repository)  # client가 누구든 상관없음!
```

### 멀티모달 API

```python
# 텍스트만
contents = "프롬프트 텍스트"

# 멀티모달 (텍스트 + 이미지) - text= 키워드 인자 필수!
contents = [
    types.Part.from_text(text="시스템 프롬프트"),
    types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
    types.Part.from_text(text="유저 프롬프트"),
]
```

### 파일 구조

```
추가된 파일:
├── prompts/prompt_multi.py      # 이미지용 프롬프트
└── ai/gemini_multi_client.py    # 멀티모달 클라이언트

수정된 파일:
├── main.py                      # 분기 로직 추가
├── prompts/__init__.py          # 새 모듈 등록
├── ai/__init__.py               # 새 클라이언트 등록
└── utils/exceptions.py          # 에러 타입 추가
```

---

## 체크리스트

### 개발 완료 확인

- [ ] `prompts/prompt_multi.py` 생성
- [ ] `prompts/__init__.py` 수정
- [ ] `ai/gemini_multi_client.py` 생성
- [ ] `ai/__init__.py` 수정
- [ ] `main.py` 수정 (분기 로직)
- [ ] `utils/exceptions.py` 에러 타입 추가

### 테스트 확인

- [ ] 텍스트 모드 정상 동작 (`--type text`)
- [ ] 이미지 모드 정상 동작 (`--type multi`)
- [ ] 이미지 파일 없을 때 에러 메시지 확인
- [ ] 지원하지 않는 이미지 형식 에러 확인

### OCP 원칙 준수 확인

- [ ] `domain/problem.py` 수정 **없음**
- [ ] `prompts/prompt.py` 수정 **없음**
- [ ] `ai/gemini_client.py` 수정 **없음**
- [ ] `service/solver_service.py` 수정 **없음**
- [ ] `repository/problem_repository.py` 수정 **없음**

---

## 다음 단계 (선택)

기능 확장 아이디어:

1. **여러 이미지 지원**: 한 문제에 이미지 여러 장
2. **혼합 문제**: 텍스트 + 이미지 조합
3. **PDF 지원**: PDF에서 이미지 추출 후 처리
4. **OCR 후처리**: 이미지에서 텍스트 추출 후 추가 분석
