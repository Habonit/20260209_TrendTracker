# CSV 처리 표준화 (pandas)

## 개요

프로젝트 전체에서 CSV 읽기/쓰기를 **pandas**로 통일

---

## 1. 변경 이유

### 기존 (csv 모듈)
```python
import csv

# 읽기
with open(path, "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        ...

# 쓰기
with open(path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([...])
```

### 변경 후 (pandas)
```python
import pandas as pd

# 읽기
df = pd.read_csv(path, encoding="utf-8-sig")

# 쓰기
df.to_csv(path, index=False, encoding="utf-8-sig")
```

### 장점
- **일관성**: analyze.ipynb와 동일한 방식
- **편의성**: DataFrame 조작, 필터링, 집계 용이
- **성능**: 대용량 데이터 처리 효율적
- **타입 안정성**: 컬럼 타입 자동 추론

---

## 2. 적용 대상

| 파일 | 기능 | 변경 내용 |
|------|------|----------|
| `repository/problem_repository.py` | 결과 저장/조회 | csv → pandas |
| `service/solver_service.py` | 점수 계산 | csv → pandas |
| `analyze.ipynb` | 분석 | 이미 pandas 사용 |

---

## 3. repository/problem_repository.py 변경

### init_output (파일 초기화)

```python
def init_output(self, output_path: str):
    """출력 파일 초기화 (헤더만 있는 빈 DataFrame 저장)"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(columns=[
        "problem_id", "score", "predicted", "actual",
        "is_correct", "earned_score", "reasoning"
    ])
    df.to_csv(path, index=False, encoding="utf-8-sig")
```

### append_result (결과 추가)

```python
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
```

### get_solved_ids (풀이된 문제 조회)

```python
def get_solved_ids(self, output_path: str) -> Set[int]:
    """이미 풀이된 문제 ID 조회"""
    path = Path(output_path)
    if not path.exists():
        return set()

    df = pd.read_csv(path, encoding="utf-8-sig")
    return set(df["problem_id"].tolist())
```

---

## 4. service/solver_service.py 변경

### calculate_score (점수 계산)

```python
def calculate_score(self, output_path: str) -> tuple[int, int, int, int]:
    """결과 파일에서 점수 계산"""
    path = Path(output_path)
    if not path.exists():
        return 0, 0, 0, 0

    df = pd.read_csv(path, encoding="utf-8-sig")

    total_count = len(df)
    correct_count = df["is_correct"].sum()
    earned_score = df["earned_score"].sum()
    total_score = df["score"].sum()

    return total_count, correct_count, earned_score, total_score
```

---

## 5. pandas 사용 규칙

### 인코딩
```python
encoding="utf-8-sig"  # Excel 호환 (BOM 포함)
```

### 읽기
```python
df = pd.read_csv(path, encoding="utf-8-sig")
```

### 쓰기 (새 파일)
```python
df.to_csv(path, index=False, encoding="utf-8-sig")
```

### 쓰기 (append)
```python
df.to_csv(path, mode="a", header=False, index=False, encoding="utf-8-sig")
```

---

## 6. 타입 힌트

```python
import pandas as pd
from typing import Set

def get_solved_ids(self, output_path: str) -> Set[int]:
    ...

def calculate_score(self, output_path: str) -> tuple[int, int, int, int]:
    ...
```

---

## 7. 의존성

```toml
# pyproject.toml
dependencies = [
    "pandas>=2.0.0",
    ...
]
```

이미 `analyze.ipynb`를 위해 pandas가 설치되어 있으므로 추가 설치 불필요
