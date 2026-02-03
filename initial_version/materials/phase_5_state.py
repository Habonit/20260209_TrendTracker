"""
# ============================================
# Phase 5-4: 상태 관리 (session_state)
# ============================================
#
# 🎯 이 파일에서 배울 것:
# - Streamlit의 실행 방식 이해하기
# - session_state가 필요한 이유
# - session_state 사용법
# - 상태 초기화와 업데이트
#
# 📋 실행 방법:
# uv run streamlit run materials/phase_5_state.py
# ============================================
"""

import streamlit as st

st.set_page_config(page_title="Phase 5-4: 상태관리", page_icon="💾")

st.title("💾 Phase 5-4: 상태 관리 (session_state)")

# ============================================
# 📚 이론: Streamlit의 실행 방식
# ============================================

st.header("1️⃣ Streamlit의 실행 방식")

st.markdown("""
## 중요한 개념!

Streamlit은 **매번 전체 코드를 다시 실행**합니다.

### 무슨 말이냐면...

```python
count = 0

if st.button("증가"):
    count += 1  # 1이 됨

st.write(count)  # 하지만 다시 0이 됨!
```

### 왜 그럴까요?

1. 버튼 클릭 → 페이지 새로고침
2. 코드 처음부터 다시 실행
3. `count = 0`으로 초기화됨
4. 증가한 값이 사라짐!

→ 값을 유지하려면 **session_state**에 저장해야 합니다!
""")

st.divider()

# ============================================
# 📚 이론: session_state란?
# ============================================

st.header("2️⃣ session_state란?")

st.markdown("""
## session_state = 브라우저의 기억 창고

`st.session_state`는 **새로고침해도 유지되는 저장소**입니다.

### 사용법

```python
# 1. 초기화 (처음 한 번만)
if "count" not in st.session_state:
    st.session_state.count = 0

# 2. 값 읽기
current = st.session_state.count

# 3. 값 변경
st.session_state.count += 1
```

### 주요 포인트

| 일반 변수 | session_state |
|----------|---------------|
| 새로고침하면 초기화 | 새로고침해도 유지 |
| 페이지 벗어나면 사라짐 | 같은 탭에서 유지 |
| `x = 0` | `st.session_state.x = 0` |
""")

st.divider()

# ============================================
# 🔍 예제: 일반 변수 vs session_state
# ============================================

st.header("3️⃣ 비교: 일반 변수 vs session_state")

st.markdown("### 🔍 직접 버튼을 클릭해보세요!")

col1, col2 = st.columns(2)

# 왼쪽: 일반 변수 (동작 안 함)
with col1:
    st.subheader("❌ 일반 변수")
    st.code('''
normal_count = 0
if st.button("증가"):
    normal_count += 1
st.write(normal_count)
    ''')

    normal_count = 0
    if st.button("증가 (일반)", key="normal_btn"):
        normal_count += 1
        st.write("1 증가했지만...")

    st.metric("값", normal_count)
    st.error("항상 0! 저장 안 됨")

# 오른쪽: session_state (동작함)
with col2:
    st.subheader("✅ session_state")
    st.code('''
if "count" not in st.session_state:
    st.session_state.count = 0
if st.button("증가"):
    st.session_state.count += 1
st.write(st.session_state.count)
    ''')

    # 초기화 (처음 한 번만 실행)
    if "demo_count" not in st.session_state:
        st.session_state.demo_count = 0

    if st.button("증가 (state)", key="state_btn"):
        st.session_state.demo_count += 1

    st.metric("값", st.session_state.demo_count)
    st.success("값이 유지됨!")

# 리셋 버튼
if st.button("🔄 리셋"):
    st.session_state.demo_count = 0
    st.rerun()  # 페이지 새로고침

st.divider()

# ============================================
# 📚 이론: session_state 패턴들
# ============================================

st.header("4️⃣ session_state 패턴들")

st.markdown("""
### 패턴 1: 초기화 체크

```python
# 키가 없으면 초기화
if "my_value" not in st.session_state:
    st.session_state.my_value = "기본값"
```

### 패턴 2: 딕셔너리처럼 사용

```python
# 점 표기법
st.session_state.name = "홍길동"

# 대괄호 표기법 (같은 결과)
st.session_state["name"] = "홍길동"
```

### 패턴 3: 여러 값 한번에 초기화

```python
defaults = {
    "count": 0,
    "name": "",
    "items": []
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value
```
""")

st.divider()

# ============================================
# 🔍 예제: 실용적인 활용
# ============================================

st.header("5️⃣ 실용 예제: 장바구니")

st.markdown("### 🛒 장바구니에 상품을 추가해보세요!")

# 장바구니 초기화
if "cart" not in st.session_state:
    st.session_state.cart = []

# 상품 목록
products = ["사과", "바나나", "오렌지", "포도"]

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏪 상품 목록")
    for product in products:
        if st.button(f"➕ {product} 추가", key=f"add_{product}"):
            st.session_state.cart.append(product)
            st.toast(f"{product} 추가됨!")

with col2:
    st.subheader("🛒 장바구니")
    if st.session_state.cart:
        for i, item in enumerate(st.session_state.cart):
            st.write(f"{i+1}. {item}")
        st.write(f"**총 {len(st.session_state.cart)}개**")

        if st.button("🗑️ 비우기"):
            st.session_state.cart = []
            st.rerun()
    else:
        st.info("장바구니가 비어있습니다")

st.divider()

# ============================================
# ✏️ 가이드 실습
# ============================================

st.header("✏️ 가이드 실습: 투두 리스트")

st.markdown("""
### 목표
session_state를 사용하여 할 일 목록 만들기

### 힌트
- 할 일 목록은 리스트로 저장
- 추가: `list.append()`
- 삭제: `list.remove()` 또는 인덱스로
""")

st.subheader("🎯 실습 영역")

# ============================================
# TODO 1: session_state에 "todos" 리스트 초기화
# 힌트: if "키" not in st.session_state:
# ============================================

# >>> 정답 <<<
# if "todos" not in st.session_state:
#     st.session_state.todos = []

# 정답 실행
if "todos" not in st.session_state:
    st.session_state.todos = []

# ============================================
# TODO 2: 텍스트 입력창과 "추가" 버튼 만들기
# 버튼 클릭 시 할 일을 todos 리스트에 추가
# ============================================

# >>> 정답 <<<
# new_todo = st.text_input("할 일 입력", key="new_todo")
# if st.button("➕ 추가"):
#     if new_todo:
#         st.session_state.todos.append(new_todo)
#         st.rerun()
#     else:
#         st.warning("할 일을 입력해주세요")

# 정답 실행
new_todo = st.text_input("할 일 입력", key="new_todo")
if st.button("➕ 추가", key="add_todo"):
    if new_todo:
        st.session_state.todos.append(new_todo)
        st.rerun()
    else:
        st.warning("할 일을 입력해주세요")

# ============================================
# TODO 3: 할 일 목록 표시하기
# 각 항목 옆에 "완료" 버튼 추가 (클릭 시 삭제)
# ============================================

# >>> 정답 <<<
# if st.session_state.todos:
#     for i, todo in enumerate(st.session_state.todos):
#         col1, col2 = st.columns([4, 1])
#         with col1:
#             st.write(f"- {todo}")
#         with col2:
#             if st.button("✅", key=f"done_{i}"):
#                 st.session_state.todos.pop(i)
#                 st.rerun()
# else:
#     st.info("할 일이 없습니다")

# 정답 실행
if st.session_state.todos:
    for i, todo in enumerate(st.session_state.todos):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"- {todo}")
        with col2:
            if st.button("✅", key=f"done_{i}"):
                st.session_state.todos.pop(i)
                st.rerun()
else:
    st.info("할 일이 없습니다")

st.markdown("""
### 💡 실습 해설

**TODO 1**: `st.session_state.todos = []`로 빈 리스트를 초기화합니다. `if "키" not in` 조건으로 처음 한 번만 실행되게!

**TODO 2**: `append()`로 리스트에 추가하고, `st.rerun()`으로 화면을 새로고침합니다.

**TODO 3**: `enumerate()`로 인덱스와 항목을 함께 가져오고, `pop(i)`로 해당 인덱스를 삭제합니다.
""")

st.divider()

# ============================================
# 🏆 챌린지
# ============================================

st.header("🏆 챌린지: 검색 기록 저장")

st.markdown("""
### 목표
검색어를 입력하면 검색 기록에 저장하고, 기록을 클릭하면 다시 불러오기

⚠️ **정답이 제공되지 않습니다.** 강사와 함께 풀어보세요!
""")

st.subheader("🎯 챌린지 영역")

st.code('''
# ============================================
# 🏆 챌린지: 검색 기록 저장
# ============================================
# ⚠️ 정답이 제공되지 않습니다.

# TODO 1: session_state에 "search_history" 리스트 초기화


# TODO 2: 검색어 입력창과 "검색" 버튼 만들기
# 검색 버튼 클릭 시:
# - 검색어가 있으면 기록에 추가 (중복 제외)
# - 검색 결과 표시: st.success(f"'{검색어}' 검색 완료!")


# TODO 3: 사이드바에 검색 기록 표시
# st.sidebar.subheader("📜 검색 기록")
# 각 기록을 버튼으로 만들어 클릭 시 검색


# TODO 4: (심화) 검색 기록 최대 5개 유지
# 6개 이상이면 가장 오래된 것 삭제
# 힌트: list.pop(0)


# TODO 5: (심화) 타임스탬프 추가
# 각 기록에 검색 시간 저장
# 힌트: from datetime import datetime
#       datetime.now().strftime("%H:%M")

''', language="python")

st.divider()

# ============================================
# 📋 정리
# ============================================

st.header("📋 정리")

st.markdown("""
### 이번 파일에서 배운 것

| 개념 | 설명 |
|------|------|
| Streamlit 실행 방식 | 매번 전체 코드를 다시 실행 |
| session_state | 새로고침해도 유지되는 저장소 |
| 초기화 패턴 | `if "키" not in st.session_state:` |
| 값 접근 | `st.session_state.키` 또는 `["키"]` |

### 핵심 패턴

```python
# 초기화 (처음 한 번만)
if "counter" not in st.session_state:
    st.session_state.counter = 0

# 값 변경
if st.button("증가"):
    st.session_state.counter += 1

# 값 사용
st.write(st.session_state.counter)

# 화면 새로고침 (값 변경 후)
st.rerun()
```

### ✅ 체크리스트
- [ ] Streamlit이 매번 전체 코드를 실행한다는 것을 안다
- [ ] session_state가 왜 필요한지 이해했다
- [ ] 초기화 패턴을 사용할 수 있다
- [ ] 리스트를 session_state에 저장하고 관리할 수 있다
- [ ] 챌린지를 강사와 함께 풀어봤다
""")

st.info("다음 파일: `phase_5_components.py` - 함수로 UI 분리 + 프로젝트 분석")
