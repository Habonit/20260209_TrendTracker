from typing import List
from google import genai
from config.settings import Settings
from domain.news_article import NewsArticle
from utils.exceptions import AppError

def summarize_news(articles: List[NewsArticle]) -> str:
    """
    Google Gemini API를 사용하여 뉴스 기사들을 요약합니다.
    
    Args:
        articles (List[NewsArticle]): 요약할 뉴스 기사 리스트
        
    Returns:
        str: 한국어 요약 결과 문자열
        
    Raises:
        AppError: API 키 오류, 할당량 초과 등 발생 시
    """
    if not articles:
        return "요약할 기사가 없습니다."

    settings = Settings()
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        # 뉴스 목록 구성
        news_context = ""
        for i, article in enumerate(articles, 1):
            news_context += f"{i}. 제목: {article.title}\n   내용: {article.snippet}\n\n"
            
        prompt = f"""
다음 뉴스 기사들의 핵심 내용을 한국어로 요약해주세요:
- 불릿 포인트 형식으로 최대 5개 항목
- 각 항목은 1~2문장

[뉴스 목록]
{news_context}
"""
        
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt
        )
        
        if not response or not response.text:
            return "요약 결과를 생성하지 못했습니다."
            
        return response.text

    except Exception as e:
        error_str = str(e).lower()
        if "401" in error_str or "api key" in error_str:
            raise AppError("api_key_invalid")
        elif "429" in error_str:
            # Gemini 무료 티어는 분당 요청 제한이 엄격함
            raise AppError("rate_limit_exceeded")
        elif "400" in error_str:
            raise AppError("bad_request")
        else:
            raise AppError("ai_error")
