# 멀티모달 이미지 처리 개발 명세

## 1. 개요

수능 문제가 **이미지**로 제공되는 경우를 처리하기 위한 확장 기능.

### 설계 원칙
- **OCP (Open-Closed Principle)**: 수정에 닫혀있고, 확장에 열려있는 구조
- 기존 `prompt.py`, `gemini_client.py`, `solver_service.py` 등 **변경 없음**
- `main.py`에 분기 로직 추가 (유일한 수정 지점)
- 새로운 파일 추가로 기능 확장

---

## 2. 데이터 스키마

**기존 `Problem` 데이터클래스 그대로 사용** (수정 없음)

```python
@dataclass
class Problem:
    id: int
    paragraph: str        # 지문
    question: str         # 문제
    question_plus: str    # 보기
    choices: List[str]    # 선택지 5개
    answer: int           # 정답 (1~5)
    score: int            # 배점
```

### 2.1 텍스트 문제 (type: text)
```json
{
    "id": 1,
    "paragraph": "실제 지문 텍스트...",
    "question": "다음 중 올바른 것은?",
    "question_plus": "[없음]",
    "choices": ["선택지1", "선택지2", "선택지3", "선택지4", "선택지5"],
    "answer": 3,
    "score": 2
}
```

### 2.2 이미지 문제 (type: multi)
```json
{
    "id": 1,
    "paragraph": "없음",
    "question": "./images/q1.png",
    "question_plus": "없음",
    "choices": ["없음", "없음", "없음", "없음", "없음"],
    "answer": 3,
    "score": 2
}
```

| 필드 | 텍스트 문제 | 이미지 문제 |
|------|------------|------------|
| `paragraph` | 지문 텍스트 | `"없음"` |
| `question` | 문제 텍스트 | **이미지 경로** (`.png`, `.jpg`, `.jpeg`) |
| `question_plus` | 보기 텍스트 | `"없음"` |
| `choices` | 선택지 5개 | `["없음", "없음", "없음", "없음", "없음"]` |

---

## 3. 아키텍처

```
┌──────────────────────────────────────────────────────────────┐
│                         main.py                              │
│                    args.type = "text" | "multi"              │
└─────────────────────────┬────────────────────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            │                           │
            ▼                           ▼
    ┌───────────────┐           ┌───────────────────┐
    │  type: text   │           │   type: multi     │
    └───────┬───────┘           └─────────┬─────────┘
            │                             │
            ▼                             ▼
    ┌───────────────┐           ┌───────────────────┐
    │ GeminiClient  │           │ GeminiMultiClient │
    │ (기존)         │           │ (신규)             │
    └───────┬───────┘           └─────────┬─────────┘
            │                             │
            ▼                             ▼
    ┌───────────────┐           ┌───────────────────┐
    │  prompt.py    │           │  prompt_multi.py  │
    │ (기존)         │           │  (신규)            │
    └───────────────┘           └───────────────────┘
```

---

## 4. 변경/추가 파일

### 4.1 수정 파일
| 파일 | 변경 내용 |
|------|----------|
| `main.py` | `--type` 인자 추가, 분기 로직 추가 |

### 4.2 신규 파일
| 파일 | 설명 |
|------|------|
| `prompts/prompt_multi.py` | 이미지 문제용 프롬프트 |
| `ai/gemini_multi_client.py` | 멀티모달 API 클라이언트 |

---

## 5. 상세 설계

### 5.1 main.py (수정)

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

    repository = ProblemRepository(args.input)
    client = GeminiClient(api_key)
    service = SolverService(client, repository)

    try:
        problems = repository.load_problems()
        total_score = sum(p.score for p in problems)
        print(f"총 {len(problems)}개 문제 로드 완료 (만점: {total_score}점)")
        print()
    except FileNotFoundError:
        print("데이터 파일을 찾을 수 없습니다.")
        print(f"{args.input} 경로를 확인해주세요.")
        sys.exit(1)

    try:
        results = service.solve_all(problems, args.output)
    except KeyboardInterrupt:
        print("\n중단됨 (진행 상황은 저장되었습니다)")
        sys.exit(0)

    _print_results(service, args.output)


def run_multi_solver(args, api_key: str):
    """이미지 문제 풀이 (멀티모달)"""
    from ai.gemini_multi_client import GeminiMultiClient

    print("=== 수능 국어 문제 풀이 AI (이미지) ===")
    print(f"입력: {args.input}")
    print(f"출력: {args.output}")
    print()

    repository = ProblemRepository(args.input)
    client = GeminiMultiClient(api_key)
    service = SolverService(client, repository)

    try:
        problems = repository.load_problems()
        total_score = sum(p.score for p in problems)
        print(f"총 {len(problems)}개 문제 로드 완료 (만점: {total_score}점)")
        print()
    except FileNotFoundError:
        print("데이터 파일을 찾을 수 없습니다.")
        print(f"{args.input} 경로를 확인해주세요.")
        sys.exit(1)

    try:
        results = service.solve_all(problems, args.output)
    except KeyboardInterrupt:
        print("\n중단됨 (진행 상황은 저장되었습니다)")
        sys.exit(0)

    _print_results(service, args.output)


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

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("GEMINI_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 확인하거나 환경변수를 설정해주세요.")
        sys.exit(1)

    if args.type == "text":
        run_text_solver(args, api_key)
    else:
        run_multi_solver(args, api_key)


if __name__ == "__main__":
    main()
```

### 5.2 prompts/prompt_multi.py (신규)

```python
"""
이미지 문제용 프롬프트 정의
"""
import os

MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "2048"))

SYSTEM_PROMPT_MULTI = """당신은 수능 국어 문제를 푸는 전문가입니다.
제공된 이미지에는 지문, 문제, 선택지가 모두 포함되어 있습니다.
이미지를 꼼꼼히 분석하여 정답을 선택하세요.
반드시 선택한 답의 이유를 구체적으로 설명해야 합니다.
"""

USER_PROMPT_MULTI = """다음 이미지를 보고 수능 국어 문제를 풀어주세요.

다음 JSON 형식으로 답변하세요:
{
  "choice": 정답번호(1-5),
  "reasoning": "왜 이 답을 선택했는지 구체적인 근거를 설명하세요."
}
"""
```

### 5.3 ai/gemini_multi_client.py (신규)

```python
"""
멀티모달 Gemini API 클라이언트
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
    choice: int
    reasoning: str


class GeminiMultiClient:
    """멀티모달 Gemini API 클라이언트"""

    SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}
    MIME_TYPES = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_name = os.getenv("MODEL", "gemini-2.0-flash-lite")
        print(f"[GeminiMultiClient] Model: {self.model_name}")
        print(f"[GeminiMultiClient] Max Output Tokens: {MAX_OUTPUT_TOKENS}")

    def _load_image(self, image_path: str) -> tuple[bytes, str]:
        """이미지 파일 로드 및 MIME 타입 반환"""
        path = Path(image_path)
        ext = path.suffix.lower()

        if ext not in self.SUPPORTED_EXTENSIONS:
            raise AppError("unsupported_image_format")

        if not path.exists():
            raise AppError("image_not_found")

        with open(path, "rb") as f:
            image_data = f.read()

        return image_data, self.MIME_TYPES[ext]

    def _build_contents(self, problem: Problem) -> list:
        """이미지 + 텍스트 프롬프트 구성"""
        image_data, mime_type = self._load_image(problem.question)

        return [
            types.Part.from_text(SYSTEM_PROMPT_MULTI),
            types.Part.from_bytes(data=image_data, mime_type=mime_type),
            types.Part.from_text(USER_PROMPT_MULTI),
        ]

    def solve_problem(self, problem: Problem) -> Answer:
        """이미지 문제 풀이"""
        contents = self._build_contents(problem)

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
        """응답 파싱"""
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

---

## 6. 에러 처리

### utils/exceptions.py에 추가

```python
# 신규 에러 타입
ERROR_MESSAGES = {
    # ... 기존 에러 ...
    "image_not_found": "이미지 파일을 찾을 수 없습니다.",
    "unsupported_image_format": "지원하지 않는 이미지 형식입니다. (png, jpg, jpeg만 지원)",
}
```

---

## 7. 실행 방법

### 텍스트 문제 (기존)
```bash
python main.py -i ./data/text_problems.json -o ./output/text_results.csv
# 또는
python main.py -i ./data/text_problems.json -o ./output/text_results.csv --type text
```

### 이미지 문제 (신규)
```bash
python main.py -i ./data/image_problems.json -o ./output/image_results.csv --type multi
```

---

## 8. 파일 구조

```
solve_test/
├── main.py                          # 수정: --type 분기 추가
├── domain/
│   └── problem.py                   # 유지 (변경 없음)
├── prompts/
│   ├── prompt.py                    # 유지 (텍스트용)
│   └── prompt_multi.py              # 신규 (이미지용)
├── ai/
│   ├── gemini_client.py             # 유지 (텍스트용)
│   └── gemini_multi_client.py       # 신규 (이미지용)
├── service/
│   └── solver_service.py            # 유지 (공통 사용)
├── repository/
│   └── problem_repository.py        # 유지 (공통 사용)
└── utils/
    └── exceptions.py                # 에러 타입 추가
```

---

## 9. 체크리스트

- [ ] `prompts/prompt_multi.py` 생성
- [ ] `ai/gemini_multi_client.py` 생성
- [ ] `main.py` 수정 (`--type` 인자 및 분기 로직)
- [ ] `utils/exceptions.py` 에러 타입 추가
- [ ] 이미지 테스트 데이터 준비
- [ ] 통합 테스트
