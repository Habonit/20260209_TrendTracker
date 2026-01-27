import streamlit as st
from typing import List, Optional
from datetime import datetime

def render_sidebar_header():
    """사이드바 헤더를 렌더링합니다."""
    st.sidebar.title("🚀 TrendTracker")
    st.sidebar.markdown("키워드로 뉴스를 검색하고 AI가 핵심 내용을 요약해드립니다.")
    st.sidebar.divider()

def render_settings() -> int:
    """검색 건수 설정을 위한 슬라이더를 렌더링하고 선택된 값을 반환합니다."""
    st.sidebar.subheader("⚙️ 설정")
    num_results = st.sidebar.slider(
        "검색 결과 수",
        min_value=1,
        max_value=10,
        value=5,
        help="한 번에 검색할 뉴스 기사의 개수를 설정합니다."
    )
    return num_results

def render_info():
    """사용법 및 서비스 정보를 렌더링합니다."""
    st.sidebar.subheader("ℹ️ 정보")
    
    with st.sidebar.expander("📖 사용법", expanded=False):
        st.markdown("""
        1. 메인 화면에서 **키워드**를 입력합니다.
        2. **검색** 버튼을 클릭합니다.
        3. 최신 뉴스와 AI 요약 결과를 확인합니다.
        4. 사이드바에서 과거 기록을 다시 볼 수 있습니다.
        """)
        
    with st.sidebar.expander("📊 API 한도", expanded=False):
        st.markdown("""
        - **Tavily**: 무료 플랜 기준 월 1,000건 검색 가능
        - **Gemini**: 무료 플랜 기준 분당 요청 횟수 제한이 있을 수 있습니다.
        """)
        
    with st.sidebar.expander("💾 데이터 저장 안내", expanded=False):
        st.markdown("""
        - 검색 기록은 `data/search_history.csv` 파일에 자동 저장됩니다.
        - CSV 파일을 삭제하거나 경로를 변경하면 이전 기록이 사라집니다.
        - 중요한 기록은 **CSV 다운로드** 기능을 통해 백업하세요.
        """)

def render_history_list(search_keys: List[str]) -> Optional[str]:
    """과거 검색 기록 목록을 selectbox로 렌더링하고 선택된 키를 반환합니다."""
    st.sidebar.subheader("📜 검색 기록")
    
    if not search_keys:
        st.sidebar.info("저장된 검색 기록이 없습니다.")
        return None
    
    # "키워드 (yyyy-mm-dd HH:MM)" 형식으로 표시하기 위해 가공
    # search_key 형식: "키워드-yyyyMMddHHmm"
    display_options = []
    key_map = {}
    
    for key in search_keys:
        try:
            parts = key.rsplit("-", 1)
            if len(parts) == 2:
                keyword, ts = parts
                dt = datetime.strptime(ts, "%Y%m%d%H%M")
                display_str = f"{keyword} ({dt.strftime('%Y-%m-%d %H:%M')})"
                display_options.append(display_str)
                key_map[display_str] = key
            else:
                display_options.append(key)
                key_map[key] = key
        except:
            display_options.append(key)
            key_map[key] = key
            
    selected_display = st.sidebar.selectbox(
        "과거 기록 불러오기",
        options=["선택하세요"] + display_options,
        index=0
    )
    
    if selected_display == "선택하세요":
        return None
        
    return key_map.get(selected_display)

def render_download_button(csv_data: str, is_empty: bool):
    """전체 데이터를 CSV로 다운로드할 수 있는 버튼을 렌더링합니다."""
    st.sidebar.subheader("📥 백업")
    
    today = datetime.now().strftime("%Y%m%d")
    filename = f"trendtracker_export_{today}.csv"
    
    if is_empty:
        st.sidebar.button("CSV 다운로드", disabled=True, help="저장된 데이터가 없습니다.")
    else:
        st.sidebar.download_button(
            label="CSV 다운로드",
            data=csv_data,
            file_name=filename,
            mime="text/csv",
            use_container_width=True
        )
