import streamlit as st
from typing import List
from domain.news_article import NewsArticle

def render_summary(keyword: str, summary: str):
    """AI 요약 결과를 렌더링합니다."""
    st.markdown("---")
    st.subheader(f"🤖 '{keyword}' 핵심 요약")
    
    # 요약 내용을 박스 안에 표시
    st.info(summary)

def render_news_list(articles: List[NewsArticle]):
    """검색된 뉴스 기사 목록을 렌더링합니다."""
    st.subheader("📰 관련 뉴스 목록")
    
    if not articles:
        st.write("관련 뉴스가 없습니다.")
        return

    for article in articles:
        # 날짜 정보가 있으면 제목이나 본문에 표시
        date_str = f" ({article.pub_date})" if article.pub_date else ""
        with st.expander(f"📌 {article.title}{date_str}", expanded=False):
            if article.pub_date:
                st.caption(f"📅 발행일: {article.pub_date}")
            st.markdown(f"**기사 스니펫:**\n{article.snippet}")
            st.markdown(f"[🔗 기사 보기]({article.url})")
