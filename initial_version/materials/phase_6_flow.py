"""
# ============================================
# Phase 6-2: 데이터 흐름과 모드 전환
# ============================================
#
# 🎯 이 파일에서 배울 것:
# - 앱의 데이터 흐름 이해하기
# - 모드(mode) 전환 패턴
# - 에러 처리 (try-except)
# - st.rerun()의 올바른 사용법
#
# 📋 실행 방법:
# streamlit run materials/phase_6_flow.py
# ============================================
"""

import streamlit as st
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime
import time

st.set_page_config(page_title="Phase 6-2: 데이터 흐름", page_icon="🔄", layout="wide")

st.title("🔄 Phase 6-2: 데이터 흐름과 모드 전환")

# ============================================
# 📚 이론: 데이터 흐름
# ============================================

st.header("1️⃣ 앱의 데이터 흐름")

st.markdown("""
## 데이터 흐름이란?

데이터가 앱 안에서 **어디서 어디로 이동**하는지를 말합니다.

### TrendTracker의 데이터 흐름

```
[사용자 입력] → [서비스 호출] → [데이터 저장] → [화면 표시]
     ↓              ↓              ↓              ↓
  키워드        API 호출      CSV 저장       결과 렌더링
```

### 더 자세히 보면

```
사용자가 키워드 입력
       ↓
render_search_form() → keyword 반환
       ↓
search_news(keyword) → articles 반환
       ↓
summarize_news(articles) → summary 반환
       ↓
SearchResult 객체 생성
       ↓
repository.save(result) → CSV 저장
       ↓
render_summary(), render_news_list() → 화면 표시
```

### 비유로 이해하기

> 🍕 **피자 주문 비유**
>
> 1. 고객이 주문 (사용자 입력)
> 2. 주방에서 피자 만듦 (서비스 호출)
> 3. 주문 기록 저장 (데이터 저장)
> 4. 피자 배달 (화면 표시)
""")

st.divider()

# ============================================
# 📚 이론: 모드 전환
# ============================================

st.header("2️⃣ 모드(Mode) 전환")

st.markdown("""
## 모드란?

앱의 **현재 상태**를 나타내는 것입니다.

### TrendTracker의 모드

| 모드 | 설명 | 언제? |
|------|------|-------|
| `new_search` | 새로운 검색 모드 | 검색 버튼 클릭 시 |
| `history` | 기록 조회 모드 | 사이드바에서 기록 선택 시 |

### 코드로 보면

```python
# 상태 초기화
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "new_search"

# 모드 전환: 새 검색
if keyword:
    st.session_state.current_mode = "new_search"

# 모드 전환: 기록 조회
if selected_key:
    st.session_state.current_mode = "history"

# 모드에 따라 다른 화면 표시
if st.session_state.current_mode == "new_search":
    # 새 검색 결과 표시
    ...
elif st.session_state.current_mode == "history":
    # 기록 조회 결과 표시
    ...
```

### 왜 모드가 필요할까요?

1. **화면 분기**: 모드에 따라 다른 UI 표시
2. **상태 추적**: 사용자가 뭘 하고 있는지 파악
3. **충돌 방지**: 새 검색과 기록 조회가 동시에 안 되도록
""")

st.divider()

# ============================================
# 🔍 예제: 모드 전환 시뮬레이션
# ============================================

st.header("3️⃣ 모드 전환 시뮬레이션")

# 상태 초기화
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = "home"
if "demo_data" not in st.session_state:
    st.session_state.demo_data = None

st.markdown("### 버튼을 클릭해서 모드를 전환해보세요!")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 홈 모드", use_container_width=True):
        st.session_state.demo_mode = "home"
        st.session_state.demo_data = None

with col2:
    if st.button("🔍 검색 모드", use_container_width=True):
        st.session_state.demo_mode = "search"
        st.session_state.demo_data = {"keyword": "AI", "results": 5}

with col3:
    if st.button("📜 기록 모드", use_container_width=True):
        st.session_state.demo_mode = "history"
        st.session_state.demo_data = {"date": "2024-01-15", "keyword": "Python"}

# 현재 모드 표시
st.markdown(f"**현재 모드**: `{st.session_state.demo_mode}`")

# 모드에 따른 화면
if st.session_state.demo_mode == "home":
    st.info("🏠 홈 화면입니다. 검색을 시작해보세요!")

elif st.session_state.demo_mode == "search":
    st.success(f"🔍 검색 모드: '{st.session_state.demo_data['keyword']}' 검색 중...")
    st.write(f"예상 결과: {st.session_state.demo_data['results']}건")

elif st.session_state.demo_mode == "history":
    st.warning(f"📜 기록 조회: {st.session_state.demo_data['date']} - {st.session_state.demo_data['keyword']}")

st.divider()

# ============================================
# 📚 이론: 에러 처리
# ============================================

st.header("4️⃣ 에러 처리 (try-except)")

st.markdown("""
## 에러 처리가 필요한 이유

API 호출은 **실패할 수 있습니다**!

- 네트워크 오류
- API 키 만료
- 요청 한도 초과
- 서버 장애

### try-except 패턴

```python
try:
    # 실패할 수 있는 코드
    articles = search_news(keyword)
    summary = summarize_news(articles)
except AppError as e:
    # 에러 발생 시 처리
    handle_error(e.error_type)
    return  # 더 이상 진행하지 않음
except Exception as e:
    # 예상치 못한 에러
    st.error(f"알 수 없는 오류: {e}")
```

### Streamlit에서 에러 표시

```python
try:
    result = dangerous_operation()
except SpecificError as e:
    st.error("❌ 작업에 실패했습니다")
    st.stop()  # 앱 실행 중단 (선택)
```

### 사용자 친화적 메시지

| 에러 타입 | 사용자 메시지 |
|----------|--------------|
| `api_key_invalid` | "API 키가 유효하지 않습니다. 설정을 확인해주세요." |
| `rate_limit_exceeded` | "요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요." |
| `network_error` | "네트워크 연결을 확인해주세요." |
""")

st.divider()

# ============================================
# 🔍 예제: 에러 처리 시뮬레이션
# ============================================

st.header("5️⃣ 에러 처리 시뮬레이션")

st.markdown("### 버튼을 클릭해서 다양한 상황을 테스트해보세요!")

col1, col2, col3 = st.columns(3)

# 성공 케이스
with col1:
    if st.button("✅ 성공 케이스", use_container_width=True):
        try:
            with st.spinner("처리 중..."):
                time.sleep(0.5)
                result = "성공!"
            st.success(f"결과: {result}")
        except Exception as e:
            st.error(f"오류: {e}")

# 에러 케이스 1
with col2:
    if st.button("❌ API 에러", use_container_width=True):
        try:
            with st.spinner("처리 중..."):
                time.sleep(0.5)
                # 에러 시뮬레이션
                raise ValueError("API 키가 유효하지 않습니다")
        except ValueError as e:
            st.error(f"❌ {e}")
            st.info("💡 설정에서 API 키를 확인해주세요.")

# 에러 케이스 2
with col3:
    if st.button("⚠️ 네트워크 에러", use_container_width=True):
        try:
            with st.spinner("처리 중..."):
                time.sleep(0.5)
                raise ConnectionError("네트워크 연결 실패")
        except ConnectionError as e:
            st.warning(f"⚠️ {e}")
            st.info("💡 인터넷 연결을 확인해주세요.")

st.divider()

# ============================================
# 📚 이론: st.rerun()
# ============================================

st.header("6️⃣ st.rerun() 사용법")

st.markdown("""
## st.rerun()이란?

페이지를 **강제로 새로고침**하는 함수입니다.

### 언제 사용할까요?

1. **상태 변경 후 화면 갱신**
2. **폼 제출 후 입력창 초기화**
3. **모드 전환 후 화면 업데이트**

### 사용 예시

```python
if st.button("삭제"):
    st.session_state.items.pop()
    st.rerun()  # 변경된 목록을 바로 표시
```

### 주의사항

⚠️ **무한 루프 조심!**

```python
# ❌ 잘못된 예 - 무한 루프!
st.session_state.count += 1
st.rerun()

# ✅ 올바른 예 - 조건 안에서만
if st.button("증가"):
    st.session_state.count += 1
    st.rerun()
```

### rerun vs 자연스러운 갱신

| 상황 | rerun 필요? |
|------|------------|
| 버튼 클릭 후 상태 변경 | 대부분 불필요 (자동 갱신) |
| 리스트에서 항목 삭제 | 필요할 수 있음 |
| 사이드바에서 메인 화면 갱신 | 경우에 따라 필요 |
""")

st.divider()

# ============================================
# ✏️ 가이드 실습
# ============================================

st.header("✏️ 가이드 실습: 메모 앱 만들기")

st.markdown("""
### 목표
모드 전환과 에러 처리를 적용한 간단한 메모 앱 만들기

### 요구사항
- 모드: "목록" / "작성" / "상세보기"
- 메모 추가, 조회 기능
- 빈 메모 작성 시 에러 처리
""")

st.subheader("🎯 실습 영역")

# 상태 초기화
if "memo_mode" not in st.session_state:
    st.session_state.memo_mode = "list"
if "memos" not in st.session_state:
    st.session_state.memos = ["첫 번째 메모", "두 번째 메모"]
if "selected_memo" not in st.session_state:
    st.session_state.selected_memo = None

# ============================================
# TODO 1: 모드 전환 버튼 만들기
# - "📋 목록" 버튼 → memo_mode = "list"
# - "✏️ 작성" 버튼 → memo_mode = "write"
# ============================================

# >>> 정답 <<<
# col1, col2 = st.columns(2)
# with col1:
#     if st.button("📋 목록", use_container_width=True):
#         st.session_state.memo_mode = "list"
# with col2:
#     if st.button("✏️ 작성", use_container_width=True):
#         st.session_state.memo_mode = "write"

# 정답 실행
col1, col2 = st.columns(2)
with col1:
    if st.button("📋 목록", use_container_width=True, key="list_btn"):
        st.session_state.memo_mode = "list"
with col2:
    if st.button("✏️ 작성", use_container_width=True, key="write_btn"):
        st.session_state.memo_mode = "write"

st.caption(f"현재 모드: **{st.session_state.memo_mode}**")

# ============================================
# TODO 2: 목록 모드 화면
# - 메모 목록을 expander로 표시
# - 각 메모에 "상세보기" 버튼
# ============================================

# >>> 정답 <<<
# if st.session_state.memo_mode == "list":
#     st.subheader("📋 메모 목록")
#     if st.session_state.memos:
#         for i, memo in enumerate(st.session_state.memos):
#             with st.expander(f"메모 {i+1}: {memo[:20]}..."):
#                 st.write(memo)
#                 if st.button("상세보기", key=f"detail_{i}"):
#                     st.session_state.memo_mode = "detail"
#                     st.session_state.selected_memo = i
#                     st.rerun()
#     else:
#         st.info("메모가 없습니다.")

# 정답 실행
if st.session_state.memo_mode == "list":
    st.subheader("📋 메모 목록")
    if st.session_state.memos:
        for i, memo in enumerate(st.session_state.memos):
            with st.expander(f"메모 {i+1}: {memo[:20]}..."):
                st.write(memo)
                if st.button("상세보기", key=f"detail_{i}"):
                    st.session_state.memo_mode = "detail"
                    st.session_state.selected_memo = i
                    st.rerun()
    else:
        st.info("메모가 없습니다.")

# ============================================
# TODO 3: 작성 모드 화면
# - 텍스트 입력창
# - 저장 버튼 (빈 입력 시 에러 처리)
# ============================================

# >>> 정답 <<<
# elif st.session_state.memo_mode == "write":
#     st.subheader("✏️ 새 메모 작성")
#     new_memo = st.text_area("메모 내용", height=150)
#     if st.button("💾 저장"):
#         try:
#             if not new_memo.strip():
#                 raise ValueError("메모 내용을 입력해주세요")
#             st.session_state.memos.append(new_memo)
#             st.session_state.memo_mode = "list"
#             st.success("저장되었습니다!")
#             st.rerun()
#         except ValueError as e:
#             st.error(f"❌ {e}")

# 정답 실행
elif st.session_state.memo_mode == "write":
    st.subheader("✏️ 새 메모 작성")
    new_memo = st.text_area("메모 내용", height=150, key="new_memo_input")
    if st.button("💾 저장", key="save_btn"):
        try:
            if not new_memo.strip():
                raise ValueError("메모 내용을 입력해주세요")
            st.session_state.memos.append(new_memo)
            st.session_state.memo_mode = "list"
            st.success("저장되었습니다!")
            st.rerun()
        except ValueError as e:
            st.error(f"❌ {e}")

# ============================================
# TODO 4: 상세보기 모드 화면
# - 선택된 메모 내용 표시
# - "목록으로" 버튼
# ============================================

# >>> 정답 <<<
# elif st.session_state.memo_mode == "detail":
#     st.subheader("🔍 메모 상세")
#     idx = st.session_state.selected_memo
#     if idx is not None and idx < len(st.session_state.memos):
#         st.info(st.session_state.memos[idx])
#         if st.button("← 목록으로"):
#             st.session_state.memo_mode = "list"
#             st.session_state.selected_memo = None
#             st.rerun()

# 정답 실행
elif st.session_state.memo_mode == "detail":
    st.subheader("🔍 메모 상세")
    idx = st.session_state.selected_memo
    if idx is not None and idx < len(st.session_state.memos):
        st.info(st.session_state.memos[idx])
        if st.button("← 목록으로", key="back_btn"):
            st.session_state.memo_mode = "list"
            st.session_state.selected_memo = None
            st.rerun()

st.markdown("""
### 💡 실습 해설

**TODO 1**: 모드 전환은 버튼 클릭 → session_state 변경으로 구현합니다.

**TODO 2**: 목록 모드에서 각 항목에 버튼을 추가하고, 클릭 시 모드와 선택 인덱스를 변경합니다.

**TODO 3**: try-except로 빈 입력을 검증하고, 성공 시 목록 모드로 전환합니다.

**TODO 4**: 선택된 인덱스로 메모를 표시하고, "목록으로" 버튼으로 돌아갑니다.
""")

st.divider()

# ============================================
# 🏆 챌린지
# ============================================

st.header("🏆 챌린지: 뉴스 뷰어 앱")

st.markdown("""
### 목표
TrendTracker와 유사한 모드 전환 패턴을 가진 뉴스 뷰어 만들기

⚠️ **정답이 제공되지 않습니다.** 강사와 함께 풀어보세요!
""")

st.subheader("🎯 챌린지 영역")

st.code('''
# ============================================
# 🏆 챌린지: 뉴스 뷰어
# ============================================
# ⚠️ 정답이 제공되지 않습니다.

# 샘플 데이터
sample_news = [
    {"id": 1, "title": "AI 발전", "content": "AI 기술이...", "date": "2024-01-15"},
    {"id": 2, "title": "경제 전망", "content": "올해 경제는...", "date": "2024-01-14"},
]

# 모드: "list" / "detail" / "search"

# TODO 1: session_state 초기화
# - current_mode: "list"
# - selected_news_id: None
# - search_results: []


# TODO 2: 사이드바에 모드 전환 라디오 버튼
# st.sidebar.radio("메뉴", ["목록", "검색"])


# TODO 3: 검색 모드 구현
# - 검색어 입력
# - 검색 버튼 클릭 시 필터링
# - 결과가 없으면 에러 메시지


# TODO 4: 목록 모드 구현
# - 뉴스 카드 표시
# - 클릭 시 상세 모드로 전환


# TODO 5: 상세 모드 구현
# - 선택된 뉴스 전체 내용 표시
# - "목록으로" 버튼


# TODO 6: (심화) 삭제 기능 추가
# - 상세 모드에서 삭제 버튼
# - 삭제 확인 다이얼로그


# TODO 7: (심화) 즐겨찾기 기능
# - 즐겨찾기 추가/제거
# - 즐겨찾기 목록 표시

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
| 데이터 흐름 | 입력 → 처리 → 저장 → 표시 |
| 모드 전환 | session_state로 현재 상태 관리 |
| 에러 처리 | try-except로 안전하게 처리 |
| st.rerun() | 페이지 강제 새로고침 |

### 핵심 패턴

```python
# 모드 초기화
if "mode" not in st.session_state:
    st.session_state.mode = "default"

# 모드 전환
if some_action:
    st.session_state.mode = "new_mode"
    st.rerun()  # 필요시

# 모드별 화면
if st.session_state.mode == "mode1":
    render_mode1()
elif st.session_state.mode == "mode2":
    render_mode2()

# 에러 처리
try:
    result = risky_operation()
except SpecificError as e:
    st.error(f"오류: {e}")
```

### ✅ 체크리스트
- [ ] 데이터 흐름의 개념을 이해했다
- [ ] 모드 전환 패턴을 구현할 수 있다
- [ ] try-except로 에러를 처리할 수 있다
- [ ] st.rerun()의 용도를 안다
- [ ] 챌린지를 강사와 함께 풀어봤다
""")

st.info("다음 파일: `phase_6_project.py` - 실제 app.py 분석")
