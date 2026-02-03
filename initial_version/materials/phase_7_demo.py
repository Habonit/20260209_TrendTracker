"""
Phase 7 인터랙티브 데모

실행: uv run streamlit run materials/phase_7_demo.py

이론은 phase_7.ipynb 참고
"""

import streamlit as st
import time
from typing import Dict

st.set_page_config(page_title="Phase 7 Demo", page_icon="🛡️", layout="wide")

st.title("🛡️ Phase 7: 인터랙티브 데모")

st.markdown("이론 내용은 `phase_7.ipynb`를 참고하세요.")

st.divider()

# ============================================
# 데모 1: 에러 메시지 매핑
# ============================================

st.header("1. 에러 메시지 매핑")

ERROR_MESSAGES: Dict[str, str] = {
    "api_key_invalid": "🔑 API 키가 유효하지 않습니다. 설정을 확인해주세요.",
    "rate_limit_exceeded": "⏳ 요청이 너무 많습니다. 30초 후 다시 시도해주세요.",
    "network_error": "🌐 네트워크 연결을 확인해주세요.",
    "no_results": "🔍 검색 결과가 없습니다. 다른 키워드로 시도해보세요.",
    "ai_error": "🤖 AI 요약 중 오류가 발생했습니다.",
}


def handle_error(error_type: str, level: str = "error"):
    message = ERROR_MESSAGES.get(error_type, "❓ 알 수 없는 오류가 발생했습니다.")
    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)


st.markdown("버튼을 클릭해서 다양한 에러 메시지를 확인해보세요.")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔑 API 키 에러", use_container_width=True):
        handle_error("api_key_invalid")
    if st.button("⏳ 요청 한도 초과", use_container_width=True):
        handle_error("rate_limit_exceeded")
    if st.button("🌐 네트워크 에러", use_container_width=True):
        handle_error("network_error")

with col2:
    if st.button("🔍 결과 없음", use_container_width=True):
        handle_error("no_results", level="warning")
    if st.button("🤖 AI 에러", use_container_width=True):
        handle_error("ai_error")
    if st.button("❓ 알 수 없는 에러", use_container_width=True):
        handle_error("unknown_type")

st.divider()

# ============================================
# 데모 2: 환경변수 검증 시뮬레이션
# ============================================

st.header("2. 환경변수 검증 시뮬레이션")

col1, col2 = st.columns(2)

with col1:
    has_tavily = st.checkbox("TAVILY_API_KEY 있음", value=True, key="check_tavily")
with col2:
    has_gemini = st.checkbox("GEMINI_API_KEY 있음", value=True, key="check_gemini")

if st.button("🔍 환경변수 검증 실행"):
    missing = []
    if not has_tavily:
        missing.append("TAVILY_API_KEY")
    if not has_gemini:
        missing.append("GEMINI_API_KEY")

    if missing:
        st.error(f"""
**환경변수가 설정되지 않았습니다.**

**누락된 변수**: {', '.join(missing)}

**설정 방법**:
1. `.env.example` 파일을 `.env`로 복사
2. 각 API 키를 발급받아 입력
        """)
    else:
        st.success("✅ 모든 환경변수가 설정되어 있습니다!")

st.divider()

# ============================================
# 데모 3: 로딩 표시
# ============================================

st.header("3. 로딩 표시")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Spinner**")
    if st.button("스피너 테스트", key="spinner_test"):
        with st.spinner("처리 중입니다..."):
            time.sleep(2)
        st.success("완료!")

with col2:
    st.markdown("**Progress Bar**")
    if st.button("진행률 테스트", key="progress_test"):
        progress = st.progress(0, text="시작...")
        for i in range(100):
            time.sleep(0.02)
            progress.progress(i + 1, text=f"진행 중... {i+1}%")
        st.success("완료!")

with col3:
    st.markdown("**Status**")
    if st.button("상태 테스트", key="status_test"):
        with st.status("작업 진행 중...", expanded=True) as status:
            st.write("1단계: 데이터 로드")
            time.sleep(0.5)
            st.write("2단계: 처리")
            time.sleep(0.5)
            st.write("3단계: 저장")
            time.sleep(0.5)
            status.update(label="완료!", state="complete")

st.divider()

# ============================================
# 데모 4: 메시지 종류
# ============================================

st.header("4. 메시지 종류")

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ 성공 메시지", key="msg_success"):
        st.success("검색 완료! 5건의 뉴스를 찾았습니다.")
        st.toast("검색이 완료되었습니다!", icon="✅")

    if st.button("❌ 에러 메시지", key="msg_error"):
        st.error("API 키가 유효하지 않습니다. 설정에서 확인해주세요.")

with col2:
    if st.button("⚠️ 경고 메시지", key="msg_warning"):
        st.warning("검색 결과가 없습니다. 다른 키워드로 시도해보세요.")

    if st.button("ℹ️ 정보 메시지", key="msg_info"):
        st.info("💡 팁: 구체적인 키워드를 입력하면 더 정확한 결과를 얻을 수 있습니다.")

st.divider()

# ============================================
# 데모 5: 빈 상태 처리
# ============================================

st.header("5. 빈 상태 처리")

if "demo_items" not in st.session_state:
    st.session_state.demo_items = []

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ 항목 추가", key="add_item"):
        st.session_state.demo_items.append(f"항목 {len(st.session_state.demo_items) + 1}")

    if st.button("🗑️ 모두 삭제", key="clear_items"):
        st.session_state.demo_items = []

with col2:
    st.markdown("**목록 상태:**")

    if st.session_state.demo_items:
        for item in st.session_state.demo_items:
            st.write(f"- {item}")
    else:
        st.info("📋 목록이 비어있습니다.")
        st.caption("왼쪽의 '➕ 항목 추가' 버튼을 클릭해보세요!")

st.divider()

# ============================================
# 데모 6: 검색 UX 통합 예제
# ============================================

st.header("6. 검색 UX 통합 예제")

if "search_results" not in st.session_state:
    st.session_state.search_results = []
if "search_keyword" not in st.session_state:
    st.session_state.search_keyword = ""

keyword = st.text_input("검색어", placeholder="키워드를 입력하세요", key="ux_keyword")
search_clicked = st.button("🔍 검색", key="ux_search")

if search_clicked:
    if not keyword.strip():
        st.warning("⚠️ 검색어를 입력해주세요.")
    else:
        with st.spinner(f"🔍 '{keyword}' 검색 중..."):
            time.sleep(1)
            results = [f"{keyword} 관련 뉴스 {i+1}" for i in range(3)]

        st.session_state.search_results = results
        st.session_state.search_keyword = keyword
        st.success(f"✅ '{keyword}' 검색 완료! {len(results)}건의 결과를 찾았습니다.")
        st.toast("검색 완료!", icon="✅")

st.markdown("---")

if st.session_state.search_results:
    st.subheader(f"📰 '{st.session_state.search_keyword}' 검색 결과")
    for result in st.session_state.search_results:
        with st.expander(result):
            st.write("기사 내용이 여기에 표시됩니다...")
else:
    st.info("💡 검색 결과가 없습니다. 키워드를 입력하고 검색해보세요!")
    st.caption("예시: AI, 경제, 기술, 스포츠")

st.divider()

# ============================================
# 코드 참고
# ============================================

st.header("7. 코드 참고")

with st.expander("에러 핸들링 패턴"):
    st.code('''
# 에러 메시지 매핑
ERROR_MESSAGES = {
    "api_key_invalid": "API 키가 유효하지 않습니다.",
    "network_error": "네트워크 연결을 확인해주세요.",
}

def handle_error(error_type: str):
    message = ERROR_MESSAGES.get(error_type, "알 수 없는 오류")
    st.error(message)

# 사용
try:
    result = risky_operation()
except AppError as e:
    handle_error(e.error_type)
''', language="python")

with st.expander("UX 패턴"):
    st.code('''
# 로딩 표시
with st.spinner("처리 중..."):
    result = long_operation()

# 성공/실패 메시지
st.success("완료!")
st.error("실패")
st.warning("주의")
st.info("정보")
st.toast("알림!", icon="✅")

# 빈 상태 처리
if not items:
    st.info("데이터가 없습니다.")
    st.caption("새 항목을 추가해보세요!")
''', language="python")
