import streamlit as st
from datetime import datetime
from config.settings import Settings
from repositories.search_repository import SearchRepository
from services.search_service import search_news
from services.ai_service import summarize_news
from domain.search_result import SearchResult
from utils.exceptions import AppError
from utils.error_handler import handle_error
from utils.key_generator import generate_search_key
from components.search_form import render_search_form
from components.sidebar import (
    render_sidebar_header, 
    render_settings, 
    render_info, 
    render_history_list, 
    render_download_button
)
from components.result_section import render_summary, render_news_list
from components.loading import show_loading

def main():
    # 1. 페이지 설정
    st.set_page_config(
        page_title="TrendTracker - AI 뉴스 트렌드 분석기",
        page_icon="🚀",
        layout="wide"
    )

    # 2. 초기화 (설정 및 리포지토리)
    try:
        settings = Settings()
    except ValueError as e:
        st.error(str(e))
        st.stop()
        
    repository = SearchRepository(settings.CSV_PATH)

    # 3. 세션 상태 초기화
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "new_search"
    if "selected_key" not in st.session_state:
        st.session_state.selected_key = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

    # 4. 사이드바 영역
    render_sidebar_header()
    num_results = render_settings()
    render_info()
    
    st.sidebar.divider()
    
    search_keys = repository.get_all_keys()
    selected_stored_key = render_history_list(search_keys)
    
    # 사이드바에서 과거 기록 선택 시 모드 변경
    if selected_stored_key:
        st.session_state.current_mode = "history"
        st.session_state.selected_key = selected_stored_key
        st.session_state.last_result = None # 결과값 초기화
        # st.rerun()은 아래 로직을 탄 후에 필요하면 사용

    st.sidebar.divider()
    
    csv_data = repository.get_all_as_csv()
    render_download_button(csv_data, len(search_keys) == 0)

    # 5. 메인 영역
    st.title("🚀 TrendTracker")
    st.markdown("최신 뉴스를 검색하고 AI(Gemini)로 핵심 내용을 빠르게 요약해드립니다.")

    # 5-1. 검색 폼 렌더링
    keyword = render_search_form()

    # 5-2. 새로운 검색 처리
    if keyword:
        st.session_state.current_mode = "new_search"
        st.session_state.selected_key = None
        
        try:
            # 뉴스 검색
            with show_loading(f"🔍 '{keyword}' 관련 최신 뉴스를 검색하고 있습니다..."):
                articles = search_news(keyword, num_results)
            
            if not articles:
                st.info(f"'{keyword}'에 대한 검색 결과가 없습니다. 다른 키워드로 시도해보세요.")
                return

            # AI 요약
            with show_loading("🤖 AI가 뉴스를 읽고 핵심 내용을 요약하고 있습니다..."):
                summary = summarize_news(articles)
            
            # 결과 객체 생성
            search_key = generate_search_key(keyword)
            result = SearchResult(
                search_key=search_key,
                search_time=datetime.now(),
                keyword=keyword,
                articles=articles,
                ai_summary=summary
            )
            
            # 저장
            with show_loading("💾 검색 결과를 저장하고 있습니다..."):
                repository.save(result)
            
            st.success(f"'{keyword}' 검색 및 요약 완료! {len(articles)}건의 뉴스를 분석했습니다.")
            st.session_state.last_result = result
            
        except AppError as e:
            handle_error(e.error_type)
        except Exception as e:
            st.error(f"알 수 없는 오류가 발생했습니다: {e}")

    # 6. 결과 표시 로직
    if st.session_state.current_mode == "new_search" and st.session_state.last_result:
        res = st.session_state.last_result
        render_summary(res.keyword, res.ai_summary)
        render_news_list(res.articles)
        
    elif st.session_state.current_mode == "history" and st.session_state.selected_key:
        # 기록 조회 모드
        history_result = repository.find_by_key(st.session_state.selected_key)
        if history_result:
            render_summary(history_result.keyword, history_result.ai_summary)
            render_news_list(history_result.articles)
        else:
            st.error("선택한 기록을 불러올 수 없습니다.")
    
    # 첫 실행 및 빈 상태 안내
    elif not keyword and not search_keys:
        st.markdown("---")
        st.info("💡 아직 검색 기록이 없습니다. 상단의 입력창에 관심 있는 키워드를 입력하여 첫 검색을 시작해보세요!")
        st.markdown("""
        ### 사용 팁:
        - **구체적인 키워드**: 'AI'보다는 '생성형 AI 트렌드'처럼 구체적으로 입력하면 더 정확한 결과를 얻을 수 있습니다.
        - **사이드바 활용**: 검색 개수를 조절하거나 과거 기록을 다시 확인하고 싶을 때 왼쪽 사이드바를 활용하세요.
        - **데이터 백업**: 하단의 'CSV 다운로드'를 통해 전체 검색 기록을 보관할 수 있습니다.
        """)

if __name__ == "__main__":
    main()
