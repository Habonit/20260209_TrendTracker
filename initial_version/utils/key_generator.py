from datetime import datetime

def generate_search_key(keyword: str) -> str:
    """
    현재 시간을 기준으로 "키워드-yyyymmddhhmm" 형식의 검색 키를 생성합니다.
    """
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M")
    return f"{keyword}-{timestamp}"
