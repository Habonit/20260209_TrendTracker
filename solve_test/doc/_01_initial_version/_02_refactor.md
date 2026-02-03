# 리팩토링 계획

## 개요

초기 버전(`_01_start.md`)을 기반으로 실용성과 확장성을 높이기 위한 리팩토링

---

## 1. argparse로 입출력 경로 지정

### 목표
- 입력 데이터와 출력 데이터 경로를 CLI 인자로 받음
- 환경변수(`GEMINI_API_KEY`, `RESPONSE_MODE`)는 그대로 유지

### 구현

```python
# main.py
import argparse

def parse_args():
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
    args = parse_args()
    # args.input, args.output 사용
```

### 사용 예시

```bash
# 기본값 사용
uv run python main.py

# 경로 지정
uv run python main.py -i ./data/2024_수능.json -o ./output/2024_results.csv

# 모드 변경 + 경로 지정
RESPONSE_MODE=2 uv run python main.py -i ./data/test.json -o ./output/test_mode2.csv
```

---

## 2. 중간 저장 (Append 방식)

### 목표
- 한 문제 풀 때마다 결과를 파일에 append
- 20분 풀이 중 중단되어도 이전 결과 보존
- 재실행 시 이어서 풀이 가능

### 구현

```python
# repository/problem_repository.py
import csv
from pathlib import Path

class ProblemRepository:
    def init_output(self, output_path: str):
        """출력 파일 초기화 (헤더 작성)"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "problem_id", "predicted", "actual",
                "is_correct", "reasoning"
            ])

    def append_result(self, answer: Answer, output_path: str):
        """결과 한 줄 추가 (append)"""
        with open(output_path, "a", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                answer.problem_id,
                answer.predicted,
                answer.actual,
                answer.is_correct,
                answer.reasoning
            ])

    def get_solved_ids(self, output_path: str) -> set:
        """이미 풀이된 문제 ID 조회 (재시작 시 사용)"""
        path = Path(output_path)
        if not path.exists():
            return set()

        with open(path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            return {int(row["problem_id"]) for row in reader}
```

### 서비스 수정

```python
# service/solver_service.py
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

    results = []
    for i, problem in enumerate(remaining):
        answer = self._solve_with_retry(problem)
        results.append(answer)

        # 즉시 저장
        self.repository.append_result(answer, output_path)

        # 진행 상황 출력
        status = "O" if answer.is_correct else "X"
        print(f"[{i+1}/{len(remaining)}] 문제 {problem.id}: {status}")

        # Rate Limit 처리...
```

### 장점
- 중단 시에도 결과 보존
- 재실행 시 자동으로 이어서 풀이
- 실시간으로 결과 확인 가능

---

## 3. 데이터 분석 노트북 (analyze.ipynb)

### 목표
- pandas로 결과 데이터 분석
- 정확도, 문제 유형별 성능 시각화
- 오답 분석

### 구현

```python
# analyze.ipynb

# 셀 1: 데이터 로드
import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv("./output/results.csv", encoding="utf-8-sig")
print(f"총 문제: {len(results)}개")
print(f"정답: {results['is_correct'].sum()}개")
print(f"정확도: {results['is_correct'].mean() * 100:.1f}%")

# 셀 2: 정답/오답 분포
results["is_correct"].value_counts().plot(kind="bar")
plt.title("정답/오답 분포")
plt.xticks([0, 1], ["오답", "정답"], rotation=0)
plt.show()

# 셀 3: 오답 문제 분석
wrong = results[results["is_correct"] == False]
print(f"오답 문제 수: {len(wrong)}개")
print(wrong[["problem_id", "predicted", "actual"]])

# 셀 4: 예측 분포
results["predicted"].value_counts().sort_index().plot(kind="bar")
plt.title("AI 예측 분포 (1~5번)")
plt.xlabel("선택지")
plt.ylabel("빈도")
plt.show()

# 셀 5: 혼동 행렬 (Confusion Matrix)
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(results["actual"], results["predicted"], labels=[1,2,3,4,5])
disp = ConfusionMatrixDisplay(cm, display_labels=[1,2,3,4,5])
disp.plot(cmap="Blues")
plt.title("혼동 행렬")
plt.show()
```

### 위치

```
solve_test/
├── output/
│   └── results.csv
└── analyze.ipynb
```

---

## 4. 인코딩 utf-8-sig

### 목표
- CSV 파일을 Excel에서 바로 열 수 있도록 BOM 포함
- 한글 깨짐 방지

### 적용 위치

```python
# 모든 CSV 읽기/쓰기에 적용
encoding="utf-8-sig"

# 읽기
pd.read_csv("results.csv", encoding="utf-8-sig")

# 쓰기
with open("results.csv", "w", encoding="utf-8-sig", newline="") as f:
    ...

# pandas 저장
df.to_csv("results.csv", encoding="utf-8-sig", index=False)
```

### 참고
- `utf-8`: BOM 없음, 일부 Excel에서 한글 깨짐
- `utf-8-sig`: BOM 포함, Excel 호환

---

## 5. 프롬프트 분리 (prompts/prompt.py)

### 목표
- 프롬프트를 별도 파일로 분리하여 실험 용이
- 시스템 프롬프트와 유저 프롬프트 구분
- 커스터마이징 가능

### 구조

```
solve_test/
└── prompts/
    ├── __init__.py
    └── prompt.py
```

### 구현

```python
# prompts/prompt.py

# 시스템 프롬프트 (AI 역할 정의)
SYSTEM_PROMPT = """당신은 수능 국어 문제를 푸는 전문가입니다.
주어진 지문을 꼼꼼히 읽고, 문제의 의도를 정확히 파악하여 답을 선택하세요.
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

반드시 아래 JSON 형식으로만 답변하세요:
{{"choice": 정답번호(1-5), "reasoning": "풀이 과정"}}
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

### GeminiClient 수정

```python
# ai/gemini_client.py
from prompts.prompt import SYSTEM_PROMPT, build_user_prompt

class GeminiClient:
    def solve_problem(self, problem: Problem) -> Answer:
        user_prompt = build_user_prompt(problem)

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                {"role": "user", "parts": [{"text": SYSTEM_PROMPT + "\n\n" + user_prompt}]}
            ],
            config=self._get_generation_config(),
        )
        # ...
```

### 실험 방법

```python
# prompts/prompt.py 수정 예시

# 실험 1: 더 구체적인 시스템 프롬프트
SYSTEM_PROMPT = """당신은 대한민국 수능 국어 영역 전문가입니다.
- 지문의 핵심 논지를 파악하세요
- 선택지를 하나씩 검토하세요
- 소거법을 활용하세요
"""

# 실험 2: Chain-of-Thought 유도
USER_PROMPT_TEMPLATE = """...
단계별로 생각해주세요:
1. 지문의 핵심 내용
2. 문제가 묻는 것
3. 각 선택지 분석
4. 최종 답변
...
"""
```

---

## 리팩토링 후 프로젝트 구조

```
solve_test/
├── ai/
│   └── gemini_client.py      # 프롬프트는 prompts에서 import
├── data/
│   └── 2023_11_KICE_flat.json
├── doc/
│   └── _01_initial_version/
│       ├── _01_start.md
│       └── _02_refactor.md
├── domain/
│   └── problem.py
├── output/                    # 결과 저장 디렉토리
│   └── results.csv
├── prompts/                   # 프롬프트 분리
│   ├── __init__.py
│   └── prompt.py
├── repository/
│   └── problem_repository.py  # append 방식 저장
├── service/
│   └── solver_service.py      # 중간 저장 로직
├── utils/
│   └── exceptions.py
├── main.py                    # argparse 추가
├── analyze.ipynb              # 데이터 분석
├── pyproject.toml
└── .env.example
```

---

## 실행 예시

```bash
# 기본 실행
uv run python main.py

# 경로 지정
uv run python main.py -i ./data/2024_수능.json -o ./output/2024.csv

# 중단 후 재실행 (자동으로 이어서 풀이)
uv run python main.py -o ./output/results.csv

# 분석
jupyter notebook analyze.ipynb
```
