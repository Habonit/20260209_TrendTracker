import os
import pandas as pd
from typing import List, Optional
from domain.search_result import SearchResult
from domain.news_article import NewsArticle

class SearchRepository:
    """CSV 파일을 사용하여 검색 기록을 관리하는 리포지토리 클래스"""
    
    CSV_COLUMNS = [
        "search_key", "search_time", "keyword", "article_index", 
        "title", "url", "snippet", "pub_date", "ai_summary"
    ]

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        # 데이터 폴더가 없으면 생성
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

    def load(self) -> pd.DataFrame:
        """CSV 파일에서 데이터를 로드합니다. 파일이 없으면 빈 DataFrame을 반환합니다."""
        if not os.path.exists(self.csv_path):
            return pd.DataFrame(columns=self.CSV_COLUMNS)
        
        try:
            df = pd.read_csv(self.csv_path)
            # 저장 과정에서 search_time이 문자열로 저장될 수 있으므로 datetime으로 변환
            if not df.empty:
                df['search_time'] = pd.to_datetime(df['search_time'])
            return df
        except Exception as e:
            print(f"파일 로드 중 오류 발생: {e}")
            return pd.DataFrame(columns=self.CSV_COLUMNS)

    def save(self, search_result: SearchResult) -> bool:
        """검색 결과를 CSV 파일에 추가 저장합니다."""
        try:
            # 새로운 데이터를 DataFrame으로 변환
            new_df = search_result.to_dataframe()
            
            # 기존 데이터 로드
            existing_df = self.load()
            
            # 데이터 합치기
            if existing_df.empty:
                final_df = new_df
            else:
                final_df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # CSV로 저장
            final_df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
            return True
        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")
            return False

    def get_all_keys(self) -> List[str]:
        """모든 유니크한 search_key 리스트를 최신순으로 정렬하여 반환합니다."""
        df = self.load()
        if df.empty:
            return []
        
        # search_time 기준 내림차순 정렬 후 고유값 추출 (순서 유지)
        df_sorted = df.sort_values(by="search_time", ascending=False)
        # drop_duplicates()로 순서를 유지하며 search_key만 추출
        keys = df_sorted["search_key"].drop_duplicates().tolist()
        return keys

    def find_by_key(self, search_key: str) -> Optional[SearchResult]:
        """search_key에 해당하는 검색 결과를 SearchResult 객체로 복원하여 반환합니다."""
        df = self.load()
        if df.empty:
            return None
        
        # 해당 키로 필터링
        result_df = df[df["search_key"] == search_key]
        if result_df.empty:
            return None
        
        # 첫 번째 행에서 공통 정보 추출
        first_row = result_df.iloc[0]
        
        # 기사 리스트 복원
        articles = []
        for _, row in result_df.iterrows():
            articles.append(NewsArticle(
                title=row["title"],
                url=row["url"],
                snippet=row["snippet"],
                pub_date=row.get("pub_date")
            ))
            
        return SearchResult(
            search_key=search_key,
            search_time=first_row["search_time"],
            keyword=first_row["keyword"],
            articles=articles,
            ai_summary=first_row["ai_summary"]
        )

    def get_all_as_csv(self) -> str:
        """전체 데이터를 CSV 형식의 문자열로 반환합니다. (다운로드용)"""
        df = self.load()
        return df.to_csv(index=False, encoding='utf-8-sig')
