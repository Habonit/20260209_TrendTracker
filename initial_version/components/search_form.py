import streamlit as st
from typing import Optional
from utils.input_handler import preprocess_keyword

def render_search_form() -> Optional[str]:
    """
    키워드 입력을 위한 검색 폼을 렌더링합니다.
    사용자가 검색 버튼을 클릭하면 전처리된 키워드를 반환합니다.
    """
    st.markdown("### 🔍 뉴스 검색")
    
    # on_click을 사용하지 않고 폼 형태로 구성하여 엔터 키 지원
    with st.form(key="search_form", clear_on_submit=False):
        col1, col2 = st.columns([4, 1])
        with col1:
            keyword_input = st.text_input(
                label="검색 키워드",
                placeholder="관심 있는 키워드를 입력하세요 (예: AI 생성형 기술)",
                label_visibility="collapsed"
            )
        with col2:
            submit_button = st.form_submit_button(label="검색", use_container_width=True)
            
        if submit_button:
            processed_keyword = preprocess_keyword(keyword_input)
            if not processed_keyword:
                st.warning("검색어를 입력해주세요.")
                return None
            return processed_keyword
            
    return None
