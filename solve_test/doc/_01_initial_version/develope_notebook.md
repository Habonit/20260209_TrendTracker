# 수능 AI 풀이 결과 분석 노트북 - 개발 명세서

> 이 문서는 `analyze.ipynb` 노트북의 구조와 각 셀의 역할을 설명합니다.

---

## 목차

1. [개요](#1-개요)
2. [노트북 구조](#2-노트북-구조)
3. [셀 1: 데이터 로드 및 점수 계산](#셀-1-데이터-로드-및-점수-계산)
4. [셀 2: 정답/오답 분포](#셀-2-정답오답-분포)
5. [셀 3: 배점별 정답률](#셀-3-배점별-정답률)
6. [셀 4: 정답 문제 - AI 풀이 근거 확인](#셀-4-정답-문제---ai-풀이-근거-확인)
7. [셀 5: 오답 문제 - AI 풀이 근거 분석](#셀-5-오답-문제---ai-풀이-근거-분석)
8. [셀 6: AI 예측 분포 vs 실제 정답 분포](#셀-6-ai-예측-분포-vs-실제-정답-분포)
9. [셀 7: 혼동 행렬](#셀-7-혼동-행렬)
10. [셀 8: 문제별 결과 시각화](#셀-8-문제별-결과-시각화)
11. [셀 9: 최종 요약](#셀-9-최종-요약)
12. [실행 방법](#실행-방법)
13. [학습 포인트 정리](#학습-포인트-정리)

---

## 1. 개요

### 목적

`main.py`로 생성된 AI 풀이 결과(`output/results.csv`)를 분석하고 시각화하는 노트북입니다.

### 분석 내용

| 분석 항목 | 설명 |
|----------|------|
| 점수 계산 | 정답률, 획득 점수, 점수 백분율 |
| 정답/오답 분포 | 막대 그래프로 시각화 |
| 배점별 분석 | 2점 문제 vs 3점 문제 정답률 비교 |
| 오답 분석 | AI가 왜 틀렸는지 reasoning 확인 |
| 혼동 행렬 | 예측과 실제의 관계 시각화 |
| 등급 환산 | 점수 백분율 기반 예상 등급 |

### 필수 의존성

```python
pandas        # 데이터 처리
matplotlib    # 시각화
scikit-learn  # 혼동 행렬
```

### 입력 데이터 구조

분석에 사용되는 CSV 파일(`output/results.csv`)의 컬럼:

| 컬럼명 | 타입 | 설명 |
|--------|------|------|
| `problem_id` | int | 문제 번호 (1~45) |
| `score` | int | 배점 (2 또는 3) |
| `predicted` | int | AI 예측 답 (1~5) |
| `actual` | int | 실제 정답 (1~5) |
| `is_correct` | bool | 정답 여부 |
| `earned_score` | int | 획득 점수 (정답: 배점, 오답: 0) |
| `reasoning` | str | AI의 풀이 근거 (JSON 형식) |

---

## 2. 노트북 구조

```
analyze.ipynb
├── [Markdown] 제목: 수능 문제 풀이 결과 분석
├── [Markdown] 섹션 1: 데이터 로드 및 점수 계산
├── [Code] 데이터 로드, 점수 계산, 기본 통계
├── [Markdown] 섹션 2: 정답/오답 분포
├── [Code] 막대 그래프 2개 (문제 수, 점수 기준)
├── [Markdown] 섹션 3: 배점별 정답률
├── [Code] groupby 분석, 막대 그래프
├── [Markdown] 섹션 4: 정답 문제 - AI 풀이 근거 확인
├── [Code] 정답 문제 목록 및 reasoning 출력
├── [Markdown] 섹션 5: 오답 문제 - AI 풀이 근거 분석
├── [Code] 오답 문제 상세 분석
├── [Markdown] 섹션 6: AI 예측 분포 vs 실제 정답 분포
├── [Code] 히스토그램 2개 비교
├── [Markdown] 섹션 7: 혼동 행렬
├── [Code] sklearn ConfusionMatrixDisplay
├── [Markdown] 섹션 8: 문제별 결과 시각화
├── [Code] 문제별 정답/오답 막대 그래프
├── [Markdown] 섹션 9: 최종 요약
└── [Code] 전체 요약 출력 및 등급 환산
```

---

## 셀 1: 데이터 로드 및 점수 계산

### 목적
결과 CSV 파일을 로드하고 기본 통계를 계산합니다.

### 코드

```python
import pandas as pd
import matplotlib.pyplot as plt

# 결과 파일 로드
# 여기에 결과 csv 경로를 입력하세요.
results = pd.read_csv("output/sample_results.csv", encoding="utf-8-sig")

# 기본 통계
total_count = len(results)
correct_count = results['is_correct'].sum()
wrong_count = total_count - correct_count

# 점수 계산
total_score = results['score'].sum()
earned_score = results['earned_score'].sum()
accuracy = correct_count / total_count * 100
score_rate = earned_score / total_score * 100

print("=" * 50)
print("수능 AI 풀이 결과")
print("=" * 50)
print(f"총 문제: {total_count}개")
print(f"정답: {correct_count}개 / 오답: {wrong_count}개")
print(f"정답률: {accuracy:.1f}%")
print()
print(f"획득 점수: {earned_score}점 / {total_score}점")
print(f"점수 백분율: {score_rate:.1f}%")
print("=" * 50)

results.head()
```

### 학습 포인트

- `pd.read_csv()`: CSV 파일 로드
- `encoding="utf-8-sig"`: Excel 호환 인코딩
- `results['is_correct'].sum()`: Boolean 컬럼 합계 (True=1)
- f-string 포맷팅: `{value:.1f}%` (소수점 1자리)

### 출력 예시

```
==================================================
수능 AI 풀이 결과
==================================================
총 문제: 45개
정답: 38개 / 오답: 7개
정답률: 84.4%

획득 점수: 82점 / 100점
점수 백분율: 82.0%
==================================================
```

---

## 셀 2: 정답/오답 분포

### 목적
정답/오답을 문제 수 기준과 점수 기준으로 시각화합니다.

### 코드

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 문제 수 기준
colors = ["#4CAF50", "#F44336"]
axes[0].bar(["Correct", "Wrong"], [correct_count, wrong_count], color=colors)
axes[0].set_ylabel("Count")
axes[0].set_title(f"Correct vs Wrong (Accuracy: {accuracy:.1f}%)")
for i, v in enumerate([correct_count, wrong_count]):
    axes[0].text(i, v + 0.5, str(v), ha='center', fontsize=12)

# 점수 기준
lost_score = total_score - earned_score
axes[1].bar(["Earned", "Lost"], [earned_score, lost_score], color=colors)
axes[1].set_ylabel("Score")
axes[1].set_title(f"Score: {earned_score}/{total_score} ({score_rate:.1f}%)")
for i, v in enumerate([earned_score, lost_score]):
    axes[1].text(i, v + 0.5, str(v), ha='center', fontsize=12)

plt.tight_layout()
plt.show()
```

### 학습 포인트

- `plt.subplots(1, 2)`: 1행 2열 서브플롯 생성
- `figsize=(12, 4)`: 그림 크기 지정
- `axes[0].bar()`: 막대 그래프 그리기
- `axes[0].text()`: 막대 위에 값 표시
- `plt.tight_layout()`: 레이아웃 자동 조정

### 시각화 설명

| 왼쪽 그래프 | 오른쪽 그래프 |
|------------|-------------|
| 정답/오답 **문제 수** | 획득/손실 **점수** |
| 초록: 정답, 빨강: 오답 | 초록: 획득, 빨강: 손실 |

---

## 셀 3: 배점별 정답률

### 목적
2점 문제와 3점 문제의 정답률을 비교 분석합니다.

### 코드

```python
# 2점 문제 vs 3점 문제 분석
score_analysis = results.groupby('score').agg(
    total=('problem_id', 'count'),
    correct=('is_correct', 'sum'),
    earned=('earned_score', 'sum')
).reset_index()

score_analysis['accuracy'] = score_analysis['correct'] / score_analysis['total'] * 100
score_analysis['max_score'] = score_analysis['score'] * score_analysis['total']

print("배점별 분석:")
for _, row in score_analysis.iterrows():
    print(f"  {int(row['score'])}점 문제: {int(row['correct'])}/{int(row['total'])}개 정답 ({row['accuracy']:.1f}%) - {int(row['earned'])}/{int(row['max_score'])}점")

# 시각화
fig, ax = plt.subplots(figsize=(8, 4))
x = [f"{int(s)} score problem" for s in score_analysis['score']]
bars = ax.bar(x, score_analysis['accuracy'], color=['#2196F3', '#FF9800'])
ax.set_ylabel('Accuracy (%)')
ax.set_title('Accuracy by Score Type')
ax.set_ylim(0, 100)
for bar, acc in zip(bars, score_analysis['accuracy']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f'{acc:.1f}%', ha='center')
plt.show()
```

### 학습 포인트

- `groupby().agg()`: 그룹별 집계 (count, sum 등)
- `reset_index()`: 인덱스를 컬럼으로 변환
- 새 컬럼 계산: `df['new_col'] = 계산식`
- `iterrows()`: DataFrame 행 순회

### 분석 의미

3점 문제는 보통 더 어렵습니다. 배점별 정답률 비교를 통해:
- AI가 어려운 문제(3점)에서 얼마나 잘하는지
- 쉬운 문제(2점)를 놓치지 않는지 확인

---

## 셀 4: 정답 문제 - AI 풀이 근거 확인

### 목적
AI가 맞힌 문제의 풀이 근거(reasoning)를 확인합니다.

### 코드

```python
correct_df = results[results['is_correct'] == True].copy()
print(f"정답 문제: {len(correct_df)}개 (+{correct_df['earned_score'].sum()}점)")
print()

# 정답 문제 목록 (reasoning 포함)
# 앞에 200자만 작성했습니다.
for _, row in correct_df.head(5).iterrows():
    print(f"문제 {int(row['problem_id'])} ({int(row['score'])}점) - 예측: {int(row['predicted'])}번 ✓")
    print(f"  이유: {row['reasoning'][:200]}..." if len(str(row['reasoning'])) > 200 else f"  이유: {row['reasoning']}")
    print()
```

### 학습 포인트

- Boolean 인덱싱: `df[df['col'] == True]`
- `.copy()`: 원본 수정 방지용 복사
- `.head(5)`: 상위 5개만 출력
- 문자열 슬라이싱: `text[:200]` (앞 200자)

### 분석 의미

정답 문제의 reasoning을 확인하면:
- AI가 올바른 근거로 정답을 선택했는지
- 혹시 운 좋게 맞힌 것은 아닌지 검증

---

## 셀 5: 오답 문제 - AI 풀이 근거 분석

### 목적
AI가 틀린 문제를 상세 분석하여 **왜 틀렸는지** 파악합니다.

### 코드

```python
wrong_df = results[results['is_correct'] == False].copy()
lost = wrong_df['score'].sum()
print(f"❌ 오답 문제: {len(wrong_df)}개 (-{lost}점)")
print()

if len(wrong_df) > 0:
    # 오답 문제 상세 분석
    for _, row in wrong_df.iterrows():
        print("=" * 60)
        print(f"문제 {int(row['problem_id'])} ({int(row['score'])}점)")
        print(f"  AI 예측: {int(row['predicted'])}번 ❌")
        print(f"  정답: {int(row['actual'])}번")
        print(f"  AI 근거:")
        reasoning = str(row['reasoning'])
        # 긴 텍스트 줄바꿈
        for i in range(0, len(reasoning), 80):
            print(f"    {reasoning[i:i+80]}")
        print()
else:
    print("오답이 없습니다! 🎉")
```

### 학습 포인트

- 조건문과 DataFrame: `if len(df) > 0`
- 긴 텍스트 줄바꿈: `for i in range(0, len(text), 80)`
- 오답 분석의 중요성

### 분석 의미

오답 분석은 가장 중요한 부분입니다:
- AI가 어떤 유형의 문제에서 틀리는지
- reasoning에서 잘못된 추론 패턴 발견
- 프롬프트 개선 방향 도출

---

## 셀 6: AI 예측 분포 vs 실제 정답 분포

### 목적
AI의 예측 패턴과 실제 정답 분포를 비교합니다.

### 코드

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# AI 예측 분포
pred_counts = results["predicted"].value_counts().sort_index()
axes[0].bar(pred_counts.index, pred_counts.values, color="#2196F3")
axes[0].set_xlabel("Choice")
axes[0].set_ylabel("Count")
axes[0].set_title("AI Prediction Distribution")
axes[0].set_xticks([1, 2, 3, 4, 5])

# 실제 정답 분포
actual_counts = results["actual"].value_counts().sort_index()
axes[1].bar(actual_counts.index, actual_counts.values, color="#FF9800")
axes[1].set_xlabel("Choice")
axes[1].set_ylabel("Count")
axes[1].set_title("Actual Answer Distribution")
axes[1].set_xticks([1, 2, 3, 4, 5])

plt.tight_layout()
plt.show()
```

### 학습 포인트

- `value_counts()`: 값별 빈도 계산
- `sort_index()`: 인덱스(선택지 번호) 순 정렬
- 두 분포 비교 시각화

### 분석 의미

두 분포를 비교하면:
- AI가 특정 번호를 선호하는지 (예: 4번을 자주 선택)
- 실제 정답 분포와의 차이
- 편향(bias) 존재 여부 확인

---

## 셀 7: 혼동 행렬

### 목적
예측값과 실제값의 관계를 행렬로 시각화합니다.

### 코드

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# 0이 아닌 예측만 필터링 (풀이 실패 제외)
valid_results = results[results["predicted"] > 0]

if len(valid_results) > 0:
    cm = confusion_matrix(
        valid_results["actual"],
        valid_results["predicted"],
        labels=[1, 2, 3, 4, 5]
    )

    fig, ax = plt.subplots(figsize=(8, 6))
    disp = ConfusionMatrixDisplay(cm, display_labels=[1, 2, 3, 4, 5])
    disp.plot(cmap="Blues", ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    plt.tight_layout()
    plt.show()
else:
    print("유효한 예측 결과가 없습니다.")
```

### 학습 포인트

- `sklearn.metrics.confusion_matrix`: 혼동 행렬 생성
- `ConfusionMatrixDisplay`: 시각화 도구
- `labels=[1,2,3,4,5]`: 클래스 레이블 지정
- `cmap="Blues"`: 색상 맵 지정

### 혼동 행렬 해석

```
         Predicted
         1  2  3  4  5
    1   [8  0  0  1  0]   ← 정답이 1번인 문제들
A   2   [0  7  1  0  0]   ← 정답이 2번인 문제들
c   3   [0  0  9  0  1]   ← 정답이 3번인 문제들
t   4   [0  1  0  8  0]   ← 정답이 4번인 문제들
u   5   [0  0  0  0  9]   ← 정답이 5번인 문제들
a
l
```

- 대각선: 정답 (예측 = 실제)
- 비대각선: 오답 (어떤 번호로 잘못 예측했는지)

---

## 셀 8: 문제별 결과 시각화

### 목적
전체 문제를 한눈에 보여주는 막대 그래프입니다.

### 코드

```python
fig, ax = plt.subplots(figsize=(16, 4))

# 색상: 정답=초록, 오답=빨강, 크기: 배점에 비례
colors = ["#4CAF50" if c else "#F44336" for c in results["is_correct"]]
heights = results["score"] / 2  # 2점=1, 3점=1.5

ax.bar(results["problem_id"], heights, color=colors, width=0.8)
ax.set_xlabel("Problem ID")
ax.set_ylabel("Score (scaled)")
ax.set_title("Results by Problem (Green=Correct, Red=Wrong, Height=Score)")

plt.tight_layout()
plt.show()
```

### 학습 포인트

- 리스트 컴프리헨션: `[... if c else ... for c in ...]`
- 조건부 색상 지정
- 막대 높이로 배점 표현
- `figsize=(16, 4)`: 가로로 긴 그래프

### 시각화 해석

- **초록 막대**: 정답
- **빨간 막대**: 오답
- **막대 높이**: 배점 (높으면 3점, 낮으면 2점)
- **빨간색 + 높음**: 3점짜리를 틀림 (큰 손실!)

---

## 셀 9: 최종 요약

### 목적
전체 분석 결과를 요약하고 예상 등급을 계산합니다.

### 코드

```python
print("=" * 60)
print("최종 요약")
print("=" * 60)
print()
print(f"총 문제 수: {total_count}개")
print(f"   - 2점 문제: {len(results[results['score']==2])}개")
print(f"   - 3점 문제: {len(results[results['score']==3])}개")
print()
print(f"정답: {correct_count}개")
print(f"오답: {wrong_count}개")
print(f"정답률: {accuracy:.1f}%")
print()
print(f"획득 점수: {earned_score}점 / {total_score}점")
print(f"점수 백분율: {score_rate:.1f}%")
print()
print("=" * 60)

# 등급 환산 (대략적)
if score_rate >= 96:
    grade = 1
elif score_rate >= 89:
    grade = 2
elif score_rate >= 77:
    grade = 3
elif score_rate >= 60:
    grade = 4
elif score_rate >= 40:
    grade = 5
else:
    grade = 6

print(f"예상 등급: {grade}등급 (참고용)")
```

### 학습 포인트

- 조건문 체이닝: `if-elif-else`
- 등급 환산 로직
- 최종 요약 포맷팅

### 등급 환산 기준 (참고)

| 등급 | 점수 백분율 |
|------|------------|
| 1등급 | 96% 이상 |
| 2등급 | 89% 이상 |
| 3등급 | 77% 이상 |
| 4등급 | 60% 이상 |
| 5등급 | 40% 이상 |
| 6등급 | 40% 미만 |

※ 실제 수능 등급은 상대평가이므로 참고용입니다.

---

## 실행 방법

### 사전 준비

1. `main.py` 실행으로 `output/results.csv` 생성
2. 노트북에서 결과 파일 경로 확인/수정

### 노트북 실행

```bash
# Jupyter Notebook
jupyter notebook analyze.ipynb

# 또는 VS Code에서 직접 실행
```

### 파일 경로 변경

셀 1에서 결과 파일 경로를 변경할 수 있습니다:

```python
# 기본 경로
results = pd.read_csv("output/sample_results.csv", encoding="utf-8-sig")

# 다른 결과 파일 분석 시
results = pd.read_csv("output/mode1_results.csv", encoding="utf-8-sig")
results = pd.read_csv("output/mode2_results.csv", encoding="utf-8-sig")
```

---

## 학습 포인트 정리

### pandas 기초

| 기능 | 코드 | 설명 |
|------|------|------|
| CSV 로드 | `pd.read_csv()` | 파일 읽기 |
| 컬럼 합계 | `df['col'].sum()` | 숫자/Boolean 합계 |
| 조건 필터링 | `df[df['col'] == value]` | 조건에 맞는 행 추출 |
| 그룹 집계 | `df.groupby().agg()` | 그룹별 통계 |
| 값 빈도 | `df['col'].value_counts()` | 값별 개수 |

### matplotlib 기초

| 기능 | 코드 | 설명 |
|------|------|------|
| 서브플롯 | `plt.subplots(1, 2)` | 여러 그래프 배치 |
| 막대 그래프 | `ax.bar(x, y)` | 기본 막대 그래프 |
| 레이블 | `ax.set_xlabel()` | 축 레이블 설정 |
| 값 표시 | `ax.text(x, y, text)` | 그래프 위에 텍스트 |

### scikit-learn

| 기능 | 코드 | 설명 |
|------|------|------|
| 혼동 행렬 | `confusion_matrix()` | 예측 vs 실제 행렬 |
| 행렬 시각화 | `ConfusionMatrixDisplay` | 히트맵 표시 |

---

## 체크리스트

노트북 실행 전 확인:

- [ ] `output/results.csv` 또는 분석할 결과 파일 존재
- [ ] pandas, matplotlib, scikit-learn 설치됨
- [ ] 셀 1의 파일 경로가 올바른지 확인

분석 후 확인:

- [ ] 정답률과 점수 백분율 확인
- [ ] 오답 문제의 reasoning 검토
- [ ] 혼동 행렬에서 오답 패턴 확인
- [ ] 배점별 정답률 비교 (3점 문제 취약 여부)
