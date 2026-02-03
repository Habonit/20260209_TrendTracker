"""
# ============================================
# Phase 5-1: Streamlit 기본
# ============================================
#
# 🎯 이 파일에서 배울 것:
# - Streamlit이 무엇인지
# - 텍스트 출력하기 (st.title, st.write, st.markdown)
# - 버튼 만들기 (st.button)
# - 텍스트 입력받기 (st.text_input)
#
# 📋 실행 방법:
# streamlit run materials/phase_5_basic.py
# ============================================
"""

import streamlit as st

# ============================================
# 📚 이론: Streamlit이란?
# ============================================

st.set_page_config(page_title="Phase 5-1: 기본", page_icon="📚")

st.title("📚 Phase 5-1: Streamlit 기본")

st.markdown("""
## Streamlit이란?

**Python 코드만으로 웹 UI를 만들 수 있는 프레임워크**입니다.

| 일반 프로그램 | Streamlit |
|-------------|-----------|
| 검은 터미널 화면 | 예쁜 웹 페이지 |
| print()로 출력 | st.write()로 출력 |
| input()으로 입력 | st.text_input()으로 입력 |

### 왜 필요한가요?

일반 사용자는 터미널(검은 화면)을 사용하기 어려워합니다.
웹 페이지 형태로 만들면 **누구나 쉽게** 사용할 수 있습니다.

### Streamlit의 특징

1. **Python만으로 웹 UI 생성** - HTML, CSS, JavaScript 몰라도 OK
2. **위에서 아래로 실행** - 코드 순서대로 화면에 표시
3. **자동 새로고침** - 코드 저장하면 화면이 자동 업데이트
""")

st.divider()

# ============================================
# 📚 이론: 텍스트 출력
# ============================================

st.header("1️⃣ 텍스트 출력하기")

st.markdown("""
### 텍스트 출력 함수들

| 함수 | 용도 | 예시 |
|------|------|------|
| `st.title()` | 가장 큰 제목 | 페이지 제목 |
| `st.header()` | 중간 제목 | 섹션 제목 |
| `st.subheader()` | 작은 제목 | 소제목 |
| `st.write()` | 무엇이든 출력 | 텍스트, 숫자, 리스트... |
| `st.markdown()` | 마크다운 출력 | **굵게**, *기울임* |

### 실행해서 확인해봅시다!
""")

# 실제 예제
st.subheader("🔍 예제: 텍스트 출력")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**코드:**")
    st.code('''
st.title("가장 큰 제목")
st.header("중간 제목")
st.subheader("작은 제목")
st.write("일반 텍스트")
st.markdown("**굵게** *기울임*")
    ''')

with col2:
    st.markdown("**결과:**")
    st.caption("(아래는 실제 출력)")
    st.markdown("# 가장 큰 제목")
    st.markdown("## 중간 제목")
    st.markdown("### 작은 제목")
    st.write("일반 텍스트")
    st.markdown("**굵게** *기울임*")

st.divider()

# ============================================
# 📚 이론: 버튼
# ============================================

st.header("2️⃣ 버튼 만들기")

st.markdown("""
### st.button() 사용법

버튼은 **클릭하면 True**, 클릭 안 하면 **False**를 반환합니다.

```python
if st.button("클릭하세요"):
    st.write("버튼이 클릭되었습니다!")
```

### 실행해서 확인해봅시다!
""")

st.subheader("🔍 예제: 버튼 클릭")

# 실제 버튼 예제
if st.button("👋 인사하기"):
    st.success("안녕하세요! 버튼이 클릭되었습니다!")
else:
    st.info("👆 버튼을 클릭해보세요")

st.divider()

# ============================================
# 📚 이론: 텍스트 입력
# ============================================

st.header("3️⃣ 텍스트 입력받기")

st.markdown("""
### st.text_input() 사용법

사용자가 입력한 값을 **변수에 저장**합니다.

```python
name = st.text_input("이름을 입력하세요")
if name:  # 입력값이 있으면
    st.write(f"안녕하세요, {name}님!")
```

### 주요 파라미터

| 파라미터 | 설명 | 예시 |
|---------|------|------|
| `label` | 입력창 위에 표시되는 레이블 | "이름을 입력하세요" |
| `placeholder` | 입력창 안에 희미하게 표시 | "예: 홍길동" |
| `value` | 기본값 | "기본 텍스트" |
""")

st.subheader("🔍 예제: 텍스트 입력")

# 실제 입력 예제
user_name = st.text_input(
    "이름을 입력하세요",
    placeholder="예: 홍길동",
    key="theory_name"
)

if user_name:
    st.success(f"안녕하세요, **{user_name}**님! 반갑습니다! 🎉")
else:
    st.info("이름을 입력해보세요")

st.divider()

# ============================================
# ✏️ 가이드 실습
# ============================================

st.header("✏️ 가이드 실습: 자기소개 앱 만들기")

st.markdown("""
### 목표
이름을 입력받고, 인사 버튼을 클릭하면 인사 메시지를 표시하기

### 힌트
- `st.text_input()`으로 이름 입력
- `st.button()`으로 버튼 만들기
- `if` 문으로 조건 처리
""")

st.subheader("🎯 실습 영역")

# ============================================
# TODO 1: st.text_input()으로 이름 입력창을 만드세요
# 힌트: label="이름", placeholder="이름을 입력하세요"
# 변수명: practice_name
# ============================================

# >>> 정답 (학습 후 주석 해제하여 확인) <<<
# practice_name = st.text_input(
#     "이름",
#     placeholder="이름을 입력하세요",
#     key="practice_name"
# )

# 정답 실행
practice_name = st.text_input(
    "이름",
    placeholder="이름을 입력하세요",
    key="practice_name"
)

# ============================================
# TODO 2: st.button()으로 "인사하기" 버튼을 만드세요
# 버튼 클릭 시:
#   - 이름이 있으면: st.success()로 인사
#   - 이름이 없으면: st.warning()으로 경고
# ============================================

# >>> 정답 (학습 후 주석 해제하여 확인) <<<
# if st.button("👋 인사하기", key="practice_btn"):
#     if practice_name:
#         st.success(f"안녕하세요, {practice_name}님!")
#     else:
#         st.warning("이름을 먼저 입력해주세요")

# 정답 실행
if st.button("👋 인사하기", key="practice_btn"):
    if practice_name:
        st.success(f"안녕하세요, {practice_name}님!")
    else:
        st.warning("이름을 먼저 입력해주세요")

st.markdown("""
### 💡 실습 해설

**TODO 1**: `st.text_input()`은 입력값을 반환합니다. 변수에 저장해야 나중에 사용할 수 있어요.

**TODO 2**: `st.button()`은 클릭하면 True를 반환합니다. `if` 문으로 클릭 여부를 체크하고, 내부에서 다시 입력값 유무를 체크합니다.
""")

st.divider()

# ============================================
# 🏆 챌린지
# ============================================

st.header("🏆 챌린지: 간단한 계산기")

st.markdown("""
### 목표
두 숫자를 입력받아 더하기 버튼을 클릭하면 합계를 표시하기

⚠️ **정답이 제공되지 않습니다.** 강사와 함께 풀어보세요!

### 힌트
- `st.number_input()`으로 숫자 입력 (텍스트 대신)
- 또는 `st.text_input()` 후 `int()` 또는 `float()`로 변환
""")

st.subheader("🎯 챌린지 영역")

st.code('''
# ============================================
# 🏆 챌린지: 간단한 계산기
# ============================================
# ⚠️ 정답이 제공되지 않습니다.

# TODO 1: 첫 번째 숫자 입력창 만들기
# 힌트: st.number_input("첫 번째 숫자", value=0)


# TODO 2: 두 번째 숫자 입력창 만들기


# TODO 3: "더하기" 버튼 만들기
# 클릭하면 두 숫자의 합을 st.success()로 표시


# TODO 4: (심화) 빼기, 곱하기, 나누기 버튼도 추가해보기

''', language="python")

st.divider()

# ============================================
# 📋 정리
# ============================================

st.header("📋 정리")

st.markdown("""
### 이번 파일에서 배운 것

| 개념 | 코드 | 설명 |
|------|------|------|
| 제목 | `st.title()` | 가장 큰 제목 |
| 텍스트 | `st.write()` | 무엇이든 출력 |
| 마크다운 | `st.markdown()` | 마크다운 문법 지원 |
| 버튼 | `st.button()` | 클릭하면 True 반환 |
| 텍스트 입력 | `st.text_input()` | 입력값을 문자열로 반환 |

### 핵심 패턴

```python
# 버튼 클릭 처리
if st.button("버튼"):
    st.write("클릭됨!")

# 입력값 처리
value = st.text_input("입력")
if value:
    st.write(f"입력: {value}")
```

### ✅ 체크리스트
- [ ] st.title(), st.write(), st.markdown() 차이를 안다
- [ ] st.button()의 반환값이 True/False임을 안다
- [ ] st.text_input()으로 입력받을 수 있다
- [ ] 챌린지를 강사와 함께 풀어봤다
""")

st.info("다음 파일: `phase_5_inputs.py` - 다양한 입력 컴포넌트")
