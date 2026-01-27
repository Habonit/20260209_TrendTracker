from typing import List
from tavily import TavilyClient
from config.settings import Settings
from domain.news_article import NewsArticle
from utils.exceptions import AppError

def search_news(keyword: str, num_results: int = 5) -> List[NewsArticle]:
    """
    Tavily API를 사용하여 뉴스 기사를 검색합니다.
    
    Args:
        keyword (str): 검색할 키워드
        num_results (int): 가져올 결과 개수 (기본값: 5)
        
    Returns:
        List[NewsArticle]: 검색된 뉴스 기사 리스트
        
    Raises:
        AppError: API 키 오설정, 한도 초과, 네트워크 오류 등 발생 시
    """
    settings = Settings()
    
    try:
        client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        
        # Tavily 검색 수행 (뉴스 모드)
        # 훨씬 더 많은 결과를 가져온 뒤 최신순으로 정렬하여 상위 n개를 반환합니다.
        # 이렇게 함으로써 단순 '관련성' 위주가 아닌 '전체 중 최신' 기사를 더 잘 확보할 수 있습니다.
        fetch_count = max(num_results * 3, 20)
        
        response = client.search(
            query=keyword,
            search_depth="advanced",
            include_domains=settings.SEARCH_DOMAINS,
            max_results=fetch_count,
            topic="news"
        )
        
        results = response.get('results', [])
        
        # 1. 날짜 정보가 있는 것과 없는 것을 분리
        # 2. 날짜 정보가 있는 것들을 최신순 정렬
        # 3. 날짜 정보가 없는 것들을 뒤에 배치
        # 4. 최종적으로 num_results 만큼 자름
        
        def get_date(x):
            d = x.get('published_date')
            return str(d) if d else ""

        results.sort(key=get_date, reverse=True)
        
        # 요청된 개수만큼 자르기
        results = results[:num_results]
            
        articles = []
        for res in results:
            articles.append(NewsArticle(
                title=res.get('title', '제목 없음'),
                url=res.get('url', ''),
                snippet=res.get('content', ''),
                pub_date=res.get('published_date')
            ))
            
        return articles

    except Exception as e:
        error_str = str(e).lower()
        # 상태 코드 또는 메시지에 따른 분기 처리
        if "401" in error_str or "api key" in error_str:
            raise AppError("api_key_invalid")
        elif "429" in error_str:
            raise AppError("rate_limit_exceeded")
        elif "400" in error_str:
            raise AppError("bad_request")
        elif "50" in error_str: # 500, 502, 503, 504
            raise AppError("server_error")
        else:
            raise AppError("network_error")
