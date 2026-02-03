"""
Phase 6 인터랙티브 데모

실행: uv run streamlit run materials/phase_6_demo.py

이론은 phase_6.ipynb 참고
"""

import streamlit as st
import time

st.set_page_config(page_title="Phase 6 Demo", page_icon="🔄", layout="wide")

st.title("🔄 Phase 6: 인터랙티브 데모")

st.markdown("이론 내용은 `phase_6.ipynb`를 참고하세요.")

st.divider()

# ============================================
# 데모 1: 모드 전환
# ============================================

st.header("1. 모드 전환 시뮬레이션")

if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = "home"
if "demo_data" not in st.session_state:
    st.session_state.demo_data = None

st.markdown("버튼을 클릭해서 모드를 전환해보세요.")

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

st.markdown(f"**현재 모드**: `{st.session_state.demo_mode}`")

if st.session_state.demo_mode == "home":
    st.info("🏠 홈 화면입니다. 검색을 시작해보세요!")
elif st.session_state.demo_mode == "search":
    st.success(f"🔍 검색 모드: '{st.session_state.demo_data['keyword']}' 검색 중...")
    st.write(f"예상 결과: {st.session_state.demo_data['results']}건")
elif st.session_state.demo_mode == "history":
    st.warning(f"📜 기록 조회: {st.session_state.demo_data['date']} - {st.session_state.demo_data['keyword']}")

st.divider()

# ============================================
# 데모 2: 에러 처리
# ============================================

st.header("2. 에러 처리 시뮬레이션")

st.markdown("버튼을 클릭해서 다양한 상황을 테스트해보세요.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("✅ 성공 케이스", use_container_width=True):
        try:
            with st.spinner("처리 중..."):
                time.sleep(0.5)
                result = "성공!"
            st.success(f"결과: {result}")
        except Exception as e:
            st.error(f"오류: {e}")

with col2:
    if st.button("❌ API 에러", use_container_width=True):
        try:
            with st.spinner("처리 중..."):
                time.sleep(0.5)
                raise ValueError("API 키가 유효하지 않습니다")
        except ValueError as e:
            st.error(f"❌ {e}")
            st.info("💡 설정에서 API 키를 확인해주세요.")

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
# 데모 3: 메모 앱 (모드 + 에러 처리 통합)
# ============================================

st.header("3. 메모 앱 (통합 예제)")

if "memo_mode" not in st.session_state:
    st.session_state.memo_mode = "list"
if "memos" not in st.session_state:
    st.session_state.memos = ["첫 번째 메모", "두 번째 메모"]
if "selected_memo" not in st.session_state:
    st.session_state.selected_memo = None

# 모드 전환 버튼
col1, col2 = st.columns(2)
with col1:
    if st.button("📋 목록", use_container_width=True, key="list_btn"):
        st.session_state.memo_mode = "list"
with col2:
    if st.button("✏️ 작성", use_container_width=True, key="write_btn"):
        st.session_state.memo_mode = "write"

st.caption(f"현재 모드: **{st.session_state.memo_mode}**")

# 목록 모드
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

# 작성 모드
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

# 상세보기 모드
elif st.session_state.memo_mode == "detail":
    st.subheader("🔍 메모 상세")
    idx = st.session_state.selected_memo
    if idx is not None and idx < len(st.session_state.memos):
        st.info(st.session_state.memos[idx])
        if st.button("← 목록으로", key="back_btn"):
            st.session_state.memo_mode = "list"
            st.session_state.selected_memo = None
            st.rerun()

st.divider()

# ============================================
# 코드 참고
# ============================================

st.header("4. 코드 구조")

with st.expander("메모 앱 핵심 코드"):
    st.code('''
# 상태 초기화
if "memo_mode" not in st.session_state:
    st.session_state.memo_mode = "list"
if "memos" not in st.session_state:
    st.session_state.memos = []

# 모드 전환
if st.button("작성"):
    st.session_state.memo_mode = "write"

# 모드별 화면
if st.session_state.memo_mode == "list":
    # 목록 표시
    for memo in st.session_state.memos:
        st.write(memo)

elif st.session_state.memo_mode == "write":
    # 입력 + 저장
    new_memo = st.text_area("내용")
    if st.button("저장"):
        try:
            if not new_memo.strip():
                raise ValueError("내용 필요")
            st.session_state.memos.append(new_memo)
            st.session_state.memo_mode = "list"
            st.rerun()
        except ValueError as e:
            st.error(str(e))
''', language="python")
