# 수능 국어 문제 풀이 AI 개발 계획

## 개요

2023년 11월 수능 국어 문제(`2023_11_KICE_flat.json`)를 Gemini AI로 풀이하는 프로그램

### 기술 스택
- Python 3.11
- Google Gemini API (`gemini-2.0-flash-lite`)
- **SDK: `google-genai`** (공식 Python SDK)
- 무료 버전 Rate Limit 고려
- **패키지 관리: uv**

### 환경 설정

```bash
# uv 프로젝트 초기화 (Python 3.11)
uv init --python 3.11

# 의존성 설치
uv add google-genai python-dotenv

# .env 파일 생성
echo "GEMINI_API_KEY=your_api_key" > .env
echo "RESPONSE_MODE=3" >> .env
```

### 실행 방법

```bash
# uv로 실행
uv run python main.py

# 모드 변경 실행 (환경변수 오버라이드)
RESPONSE_MODE=1 uv run python main.py  # Mode 1
RESPONSE_MODE=2 uv run python main.py  # Mode 2
RESPONSE_MODE=3 uv run python main.py  # Mode 3
```

---

## 프로젝트 구조

```
kice_solver/
├── domain/
│   └── problem.py            # 데이터 클래스 (Problem, Answer)
├── repository/
│   └── problem_repository.py # JSON 로드/결과 저장
├── service/
│   └── solver_service.py     # 문제 풀이 비즈니스 로직
├── ai/
│   └── gemini_client.py      # Gemini API 클래스
├── utils/
│   └── exceptions.py         # 커스텀 에러 클래스
└── main.py                   # 진입점
```

---

## 1. 도메인 (Domain)

### 위치: `domain/problem.py`

데이터 구조를 정의하는 dataclass

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Problem:
    """수능 국어 문제"""
    id: int
    paragraph: str      # 지문
    question: str       # 문제
    question_plus: str  # 보기 (없으면 "[없음]")
    choices: List[str]  # 선택지 5개
    answer: int         # 정답 (1~5)

@dataclass
class Answer:
    """AI 풀이 결과"""
    problem_id: int
    predicted: int      # AI가 예측한 답
    actual: int         # 실제 정답
    is_correct: bool    # 정답 여부
    reasoning: str      # AI의 추론 과정
```

---

## 2. 레포지토리 (Repository)

### 위치: `repository/problem_repository.py`

데이터 저장/조회 담당

```python
class ProblemRepository:
    def __init__(self, data_path: str):
        self.data_path = data_path

    def load_problems(self) -> List[Problem]:
        """JSON 파일에서 문제 로드"""
        pass

    def save_results(self, results: List[Answer], output_path: str):
        """풀이 결과를 JSON으로 저장"""
        pass
```

### 책임
- `2023_11_KICE_flat.json` 파일 읽기
- 결과를 `results.json`으로 저장

---

## 3. Gemini AI 클래스

### 위치: `ai/gemini_client.py`

Gemini API 호출 담당

```python
from google import genai

class GeminiClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash-lite"

    def solve_problem(self, problem: Problem) -> Answer:
        """문제를 풀고 Answer 반환"""
        prompt = self._build_prompt(problem)
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return self._parse_response(response.text, problem)

    def _build_prompt(self, problem: Problem) -> str:
        """문제 풀이용 프롬프트 생성"""
        pass

    def _parse_response(self, response: str, problem: Problem) -> Answer:
        """AI 응답을 Answer 객체로 파싱"""
        pass
```

### 프롬프트 구조

```
다음 수능 국어 문제를 풀어주세요.

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

정답 번호와 그 이유를 설명해주세요.
형식:
정답: [번호]
이유: [설명]
```

---

## 4. 서비스 (Service)

### 위치: `service/solver_service.py`

비즈니스 로직 담당 (Rate Limit 처리 포함)

```python
import time

class SolverService:
    def __init__(self, client: GeminiClient, repository: ProblemRepository):
        self.client = client
        self.repository = repository

    def solve_all(self, problems: List[Problem]) -> List[Answer]:
        """모든 문제 풀이 (Rate Limit 적용)"""
        results = []

        for i, problem in enumerate(problems):
            # 문제 풀이
            answer = self._solve_with_retry(problem)
            results.append(answer)

            # 진행 상황 출력
            print(f"[{i+1}/{len(problems)}] 문제 {problem.id}: {'O' if answer.is_correct else 'X'}")

            # Rate Limit 처리
            if (i + 1) % 5 == 0:
                print(">>> 60초 대기 (Rate Limit)...")
                time.sleep(60)
            else:
                time.sleep(10)

        return results

    def _solve_with_retry(self, problem: Problem, max_retries: int = 3) -> Answer:
        """재시도 로직 포함 문제 풀이"""
        pass

    def calculate_accuracy(self, results: List[Answer]) -> float:
        """정확도 계산"""
        correct = sum(1 for r in results if r.is_correct)
        return correct / len(results) * 100
```

### Rate Limit 전략

```
문제 1 → 10초 대기
문제 2 → 10초 대기
문제 3 → 10초 대기
문제 4 → 10초 대기
문제 5 → 60초 대기 (1분에 5문제 제한)
문제 6 → 10초 대기
...
```

---

## 5. 에러 처리

### 위치: `utils/exceptions.py`

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

### 에러 처리 패턴

```python
try:
    answer = self.client.solve_problem(problem)
except AppError as e:
    print(handle_error(e.error_type))
    # 재시도 또는 스킵
except Exception as e:
    print(f"예상치 못한 오류: {e}")
```

---

## 6. main 진입점

### 위치: `main.py`

```python
import os
from dotenv import load_dotenv

from domain.problem import Problem, Answer
from repository.problem_repository import ProblemRepository
from service.solver_service import SolverService
from ai.gemini_client import GeminiClient

def main():
    # 1. 환경변수 로드
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("GEMINI_API_KEY가 설정되지 않았습니다.")
        return

    # 2. 의존성 초기화
    repository = ProblemRepository("../2023_11_KICE_flat.json")
    client = GeminiClient(api_key)
    service = SolverService(client, repository)

    # 3. 문제 로드
    problems = repository.load_problems()
    print(f"총 {len(problems)}개 문제 로드 완료")

    # 4. 문제 풀이 실행
    try:
        results = service.solve_all(problems)
    except KeyboardInterrupt:
        print("\n중단됨")
        return

    # 5. 결과 저장
    repository.save_results(results, "results.json")

    # 6. 정확도 출력
    accuracy = service.calculate_accuracy(results)
    print(f"\n=== 결과 ===")
    print(f"총 문제: {len(results)}개")
    print(f"정답: {sum(1 for r in results if r.is_correct)}개")
    print(f"정확도: {accuracy:.1f}%")

if __name__ == "__main__":
    main()
```

---

## 실행 흐름

```
1. main.py 실행
   ↓
2. .env에서 GEMINI_API_KEY 로드
   ↓
3. Repository로 JSON 문제 로드 (45문제)
   ↓
4. SolverService.solve_all() 실행
   ├── 문제 1 → GeminiClient.solve_problem() → 10초 대기
   ├── 문제 2 → GeminiClient.solve_problem() → 10초 대기
   ├── ...
   ├── 문제 5 → GeminiClient.solve_problem() → 60초 대기
   ├── 문제 6 → ...
   └── 문제 45 → 완료
   ↓
5. results.json 저장
   ↓
6. 정확도 출력
```

---

## 예상 소요 시간

- 45문제 기준
- 5문제당 1분 대기 = 9회 × 60초 = 540초
- 문제 간 10초 대기 = 40회 × 10초 = 400초
- API 호출 시간 ≈ 45 × 5초 = 225초
- **총 예상 시간: 약 20분**

---

## 7. 응답 형식 강제 (Response Format Control)

AI 응답을 원하는 형태로 고정하기 위한 3단계 모드 (누적 방식)

### 환경변수 설정

```bash
# .env 파일
GEMINI_API_KEY=your_api_key
RESPONSE_MODE=3  # 1, 2, 3 중 선택
```

### Mode 설명

| Mode | 포함 기능 | 강제 수준 |
|------|----------|----------|
| 1 | 시스템 프롬프트 | 약함 |
| 2 | Mode 1 + MIME type (`application/json`) | 중간 |
| 3 | Mode 2 + Enum/Schema 정의 | 강함 |

---

### Mode 1: 시스템 프롬프트만

프롬프트에서 JSON 형식을 요청. AI가 무시할 수 있음.

```python
def _build_prompt_mode1(self, problem: Problem) -> str:
    """Mode 1: 프롬프트로 JSON 형식 요청"""
    return f"""다음 수능 국어 문제를 풀어주세요.

[지문]
{problem.paragraph}

[문제]
{problem.question}

[보기]
{problem.question_plus}

[선택지]
1. {problem.choices[0]}
2. {problem.choices[1]}
3. {problem.choices[2]}
4. {problem.choices[3]}
5. {problem.choices[4]}

반드시 아래 JSON 형식으로만 답변하세요:
{{"choice": 정답번호, "reasoning": "풀이 과정"}}
"""
```

---

### Mode 2: Mode 1 + MIME Type 설정

API 설정으로 JSON 구조를 강제. 형식은 확실하지만 값은 자유.

```python
def _create_model_mode2(self):
    """Mode 2: MIME type으로 JSON 강제"""
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite",
        generation_config={
            "response_mime_type": "application/json"
        }
    )
```

---

### Mode 3: Mode 2 + Schema 정의

응답 스키마를 정의하여 값의 범위까지 통제.

```python
import typing_extensions as typing

class SolverResponse(typing.TypedDict):
    """응답 스키마 정의"""
    choice: int      # 1~5 중 하나
    reasoning: str   # 풀이 과정

def _create_model_mode3(self):
    """Mode 3: Schema로 완벽한 통제"""
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash-lite",
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": SolverResponse
        }
    )
```

---

### GeminiClient 통합 구현

```python
import os
import json
import typing_extensions as typing
from google import genai

class SolverResponse(typing.TypedDict):
    """Mode 3용 응답 스키마"""
    choice: int
    reasoning: str

class GeminiClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.mode = int(os.getenv("RESPONSE_MODE", "3"))
        self.model_name = "gemini-2.0-flash-lite"

    def _get_generation_config(self) -> dict:
        """모드에 따른 generation_config 반환"""
        if self.mode == 1:
            # Mode 1: 프롬프트만 (기본 설정)
            return {}
        elif self.mode == 2:
            # Mode 2: MIME type 추가
            return {
                "response_mime_type": "application/json"
            }
        else:
            # Mode 3: Schema 추가
            return {
                "response_mime_type": "application/json",
                "response_schema": SolverResponse
            }

    def _build_prompt(self, problem: Problem) -> str:
        """모든 모드 공통: JSON 형식 요청 프롬프트"""
        return f"""다음 수능 국어 문제를 풀어주세요.

[지문]
{problem.paragraph}

[문제]
{problem.question}

[보기]
{problem.question_plus}

[선택지]
1. {problem.choices[0]}
2. {problem.choices[1]}
3. {problem.choices[2]}
4. {problem.choices[3]}
5. {problem.choices[4]}

반드시 아래 JSON 형식으로만 답변하세요:
{{"choice": 정답번호(1-5), "reasoning": "풀이 과정"}}
"""

    def solve_problem(self, problem: Problem) -> Answer:
        """문제 풀이 (모드에 따라 다른 설정 적용)"""
        prompt = self._build_prompt(problem)
        config = self._get_generation_config()

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config if config else None
        )

        return self._parse_response(response.text, problem)

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
            reasoning=reasoning
        )

    def _extract_answer_from_text(self, text: str) -> int:
        """텍스트에서 정답 번호 추출 (Mode 1 fallback)"""
        import re
        match = re.search(r'정답[:\s]*(\d)', text)
        if match:
            return int(match.group(1))
        return 0
```

---

### 교육 포인트

```
Mode 1 실행 → JSON 파싱 실패 경험 → "프롬프트만으론 부족하구나"
    ↓
Mode 2 실행 → JSON은 오지만 이상한 값 → "구조는 맞는데 값이..."
    ↓
Mode 3 실행 → 완벽한 응답 → "스키마로 값까지 통제!"
```

학생들이 직접 모드를 바꿔가며 실행해보면서 **왜 점점 더 엄격한 방법이 필요한지** 체감할 수 있음.
