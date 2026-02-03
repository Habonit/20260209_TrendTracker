# 프롬프트 및 출력 설정

## 개요

AI 응답의 품질을 높이고 분석에 유용한 결과를 얻기 위한 설정

---

## 1. 출력 토큰 제한 (MAX_OUTPUT_TOKENS)

### 목표
- AI 응답 길이 조절
- reasoning(풀이 근거)의 상세 수준 제어
- API 비용 및 응답 시간 관리

### 설정 위치

```python
# prompts/prompt.py
MAX_OUTPUT_TOKENS = 1024  # 기본값
```

### 적용

```python
# ai/gemini_client.py
from prompts.prompt import MAX_OUTPUT_TOKENS

config = types.GenerateContentConfig(
    response_mime_type="application/json",
    max_output_tokens=MAX_OUTPUT_TOKENS,  # 토큰 제한 적용
)
```

### 권장값

| 값 | 용도 |
|----|------|
| 512 | 간단한 답과 짧은 이유 |
| 1024 | 기본값, 적절한 상세도 |
| 2048 | 상세한 풀이 과정 |

---

## 2. 프롬프트 구조

### 시스템 프롬프트

```python
SYSTEM_PROMPT = """당신은 수능 국어 문제를 푸는 전문가입니다.
주어진 지문을 꼼꼼히 읽고, 문제의 의도를 정확히 파악하여 답을 선택하세요.
반드시 선택한 답의 이유를 구체적으로 설명해야 합니다.
"""
```

### 유저 프롬프트 (reasoning 강조)

```python
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
```

### 핵심 포인트
- `reasoning` 필드에 **구체적인 근거** 요청
- **지문 근거** + **오답 소거 이유** 포함 요청
- JSON 형식으로 파싱 용이

---

## 3. 응답 스키마 (Mode 3)

```python
class SolverResponse(typing.TypedDict):
    choice: int      # 정답 번호 (1~5)
    reasoning: str   # 풀이 근거
```

---

## 4. 점수 체계

### 데이터 구조

```json
{
  "1": {
    "id": 1,
    "paragraph": "지문...",
    "question": "문제...",
    "choices": ["1번", "2번", "3번", "4번", "5번"],
    "answer": 4,
    "score": 2  // 배점 (2점 또는 3점)
  }
}
```

### 수능 국어 배점
- **2점 문제**: 35개 (70점)
- **3점 문제**: 10개 (30점)
- **총점**: 100점

### 결과 CSV 구조

| 컬럼 | 설명 |
|------|------|
| problem_id | 문제 번호 |
| score | 배점 (2 또는 3) |
| predicted | AI 예측 |
| actual | 실제 정답 |
| is_correct | 정답 여부 |
| earned_score | 획득 점수 (정답 시 score, 오답 시 0) |
| reasoning | AI 풀이 근거 |

---

## 5. 분석 기능 (analyze.ipynb)

### 점수 계산

```python
# 정답률
accuracy = correct_count / total_count * 100

# 점수 백분율
score_rate = earned_score / total_score * 100
```

### 정답/오답 근거 확인

```python
# 오답 문제의 AI 근거 분석
wrong_df = results[results['is_correct'] == False]
for _, row in wrong_df.iterrows():
    print(f"문제 {row['problem_id']}")
    print(f"  AI 예측: {row['predicted']}번")
    print(f"  정답: {row['actual']}번")
    print(f"  AI 근거: {row['reasoning']}")
```

### 출력 예시

```
=== 결과 ===
총 문제: 45개
정답: 38개 / 오답: 7개
정답률: 84.4%

획득 점수: 82점 / 100점
점수 백분율: 82.0%
```

---

## 6. 프롬프트 실험 가이드

### 실험 1: 더 상세한 풀이

```python
# prompts/prompt.py
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

### 실험 2: Chain-of-Thought

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

### 실험 3: 간결한 응답

```python
MAX_OUTPUT_TOKENS = 512

SYSTEM_PROMPT = """수능 국어 전문가입니다. 정답과 핵심 이유만 간결히 답하세요."""
```

---

## 7. 결과 예시

### CLI 출력

```
=== 수능 국어 문제 풀이 AI ===
Response Mode: 3
입력: ./data/2023_11_KICE_flat.json
출력: ./output/results.csv

[GeminiClient] Mode 3 초기화 완료
[GeminiClient] Max Output Tokens: 1024
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

### analyze.ipynb 오답 분석

```
❌ 오답 문제: 7개 (-18점)

============================================================
문제 3 (2점)
  AI 예측: 2번 ❌
  정답: 1번
  AI 근거:
    지문에서 "스스로 독서 계획을 세우고" 부분이 ㉠의 "다른 독자와
    소통하는 즐거움"과 관련이 있다고 판단했습니다. 그러나 이 선택지는
    개인적인 독서 경험을 설명하고 있어...
```
