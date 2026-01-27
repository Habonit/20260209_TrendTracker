from dataclasses import dataclass
from datetime import datetime
from typing import List
import pandas as pd
from .news_article import NewsArticle

@dataclass
class SearchResult:
    """검색 결과 및 AI 요약 정보를 담는 데이터 클래스"""
    search_key: str          # 형식: "키워드-yyyymmddhhmm"
    search_time: datetime    # 검색 실행 시간
    keyword: str             # 검색 키워드
    articles: List[NewsArticle] # 뉴스 기사 리스트
    ai_summary: str          # AI 요약 결과

    def to_dataframe(self) -> pd.DataFrame:
        """
        검색 결과를 Pandas DataFrame으로 변환합니다.
        기사 1건이 1행이 되는 Long format으로 변환합니다.
        """
        data = []
        for i, article in enumerate(self.articles, 1):
            data.append({
                "search_key": self.search_key,
                "search_time": self.search_time,
                "keyword": self.keyword,
                "article_index": i,
                "title": article.title,
                "url": article.url,
                "snippet": article.snippet,
                "pub_date": article.pub_date,
                "ai_summary": self.ai_summary
            })
        
        # 기사가 없는 경우에 대비하여 빈 리스트 처리
        if not data:
            return pd.DataFrame(columns=[
                "search_key", "search_time", "keyword", "article_index",
                "title", "url", "snippet", "pub_date", "ai_summary"
            ])
            
        return pd.DataFrame(data)
