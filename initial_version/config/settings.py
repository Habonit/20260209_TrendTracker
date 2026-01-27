import os
from dotenv import load_dotenv

class Settings:
    """애플리케이션의 환경 변수 및 설정을 관리하는 클래스"""
    def __init__(self):
        # .env 파일 로드
        load_dotenv()
        
        # 필수 환경변수 목록 및 설명
        required_vars = {
            "TAVILY_API_KEY": "Tavily API 키가 필요합니다. https://tavily.com/ 에서 발급받으세요.",
            "GEMINI_API_KEY": "Google Gemini API 키가 필요합니다. https://aistudio.google.com/ 에서 발급받으세요.",
            "CSV_PATH": "데이터 저장을 위한 CSV 파일 경로가 필요합니다. (예: data/search_history.csv)"
        }
        
        missing_vars = []
        for var, description in required_vars.items():
            value = os.getenv(var)
            if not value:
                missing_vars.append(f"- {var}: {description}")
        
        if missing_vars:
            error_msg = f"""
❌ 환경변수가 설정되지 않았습니다.

누락된 변수:
{chr(10).join(missing_vars)}

설정 방법:
1. `.env.example` 파일을 `.env`로 복사합니다.
2. 각 API 키를 발급받아 입력합니다.

API 키 발급 안내:
- Tavily API: [https://tavily.com/](https://tavily.com/)
- Google AI Studio (Gemini): [https://aistudio.google.com/](https://aistudio.google.com/)

모든 키가 설정되어 있어야 앱이 정상 동작합니다.
"""
            raise ValueError(error_msg)

        # 설정값 할당
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.CSV_PATH = os.getenv("CSV_PATH")
        
        # 선택적 설정 (기본값 제공)
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        # SEARCH_DOMAINS 처리 (쉼표 구분 리스트로 변환)
        domains_raw = os.getenv("SEARCH_DOMAINS", "")
        self.SEARCH_DOMAINS = [d.strip() for d in domains_raw.split(",") if d.strip()]

    def __repr__(self):
        return f"<Settings(model={self.GEMINI_MODEL}, domains={len(self.SEARCH_DOMAINS)})>"
