# Phase 3 실습: 실제 API 사용해보기

## 학습 목표
- Tavily API를 실제로 호출하여 뉴스 검색하기
- Gemini API를 실제로 호출하여 텍스트 생성하기
- 다양한 파라미터를 바꿔가며 실험하기
- API 응답 구조 이해하기

## 사전 준비
- `.env` 파일에 API 키 설정 완료
  - `TAVILY_API_KEY=tvly-xxxxx`
  - `GEMINI_API_KEY=xxxxx`

## 주의사항
- Tavily: 무료 플랜 월 1,000건
- Gemini: 분당 요청 제한 있음
- 불필요한 반복 실행은 피할 것

---

## 1. 환경 설정: API 키 로드

`.env` 파일에서 API 키를 불러온다.

```python
import os
from dotenv import load_dotenv

load_dotenv()

tavily_key = os.getenv("TAVILY_API_KEY", "")
gemini_key = os.getenv("GEMINI_API_KEY", "")
```

---

## 2. Tavily API

### Tavily API란?
Tavily는 **AI 에이전트를 위한 검색 API**이다.
- 공식 사이트: https://tavily.com/
- 뉴스 검색에 최적화된 `topic="news"` 모드 제공

### 기본 사용법

```python
from tavily import TavilyClient

tavily = TavilyClient(api_key=tavily_key)

response = tavily.search(
    query="AI 기술",
    max_results=3
)

# 응답 구조
# response = {
#     "query": "AI 기술",
#     "results": [
#         {
#             "title": "...",
#             "url": "...",
#             "content": "...",
#             "published_date": "...",
#             "score": 0.99
#         },
#         ...
#     ]
# }

articles = response.get('results', [])
for result in articles:
    print(result.get('title'))
    print(result.get('url'))
    print(result.get('content')[:100])
    print(result.get('published_date'))
```

### 주요 파라미터

| 파라미터 | 설명 | 옵션 |
|---------|------|------|
| `query` | 검색 키워드 | 문자열 |
| `topic` | 검색 유형 | `"general"`, `"news"`, `"finance"` |
| `search_depth` | 검색 깊이 | `"basic"`, `"advanced"` |
| `max_results` | 최대 결과 수 | 1~20 |
| `include_domains` | 특정 도메인만 검색 | 도메인 리스트 |
| `exclude_domains` | 특정 도메인 제외 | 도메인 리스트 |
| `time_range` | 시간 범위 제한 | `"day"`, `"week"`, `"month"`, `"year"` |

### topic (검색 유형)

| 값 | 설명 | 사용 예시 |
|----|------|----------|
| `"general"` | 일반 웹 검색 (기본값) | 정보 검색, 기술 문서 |
| `"news"` | 뉴스 기사 검색 | 시사, 정치, 스포츠, 연예 |
| `"finance"` | 금융/경제 뉴스 검색 | 주식, 환율, 기업 실적 |

### search_depth (검색 깊이)

| 값 | 설명 | 특징 |
|----|------|------|
| `"basic"` | 빠른 기본 검색 | 빠름, API 크레딧 1 소모 |
| `"advanced"` | 깊이 있는 고급 검색 | 더 정확, 날짜 정보 포함, API 크레딧 2 소모 |

### include_domains (도메인 필터링)

특정 도메인에서만 결과를 가져온다. 신뢰할 수 있는 출처만 사용하고 싶을 때 유용하다.

```python
# 특정 도메인만 검색
response = tavily.search(
    query="반도체 수출",
    topic="news",
    search_depth="advanced",
    include_domains=["bbc.com", "reuters.com"],
    max_results=5
)
```

### 뉴스 모드 검색 예시

```python
response = tavily.search(
    query="삼성전자",
    topic="news",
    search_depth="advanced",
    max_results=5
)

for i, result in enumerate(response.get('results', []), 1):
    title = result.get('title', '제목 없음')
    date = result.get('published_date', '날짜 없음')
    print(f"{i}. [{date}] {title}")
```

---

## 3. Gemini API

### Gemini API란?
Gemini는 **Google의 AI 모델**이다.
- 공식 사이트: https://aistudio.google.com/
- 텍스트 생성, 요약, 번역 등 다양한 작업 가능

### 주요 모델

| 모델 | 설명 |
|------|------|
| `gemini-2.0-flash` | 빠르고 가벼운 모델 |
| `gemini-2.5-flash` | 성능과 속도의 균형 |
| `gemini-1.5-pro` | 고성능 모델 |

### 기본 사용법

```python
from google import genai

gemini = genai.Client(api_key=gemini_key)
MODEL = "gemini-2.5-flash"

response = gemini.models.generate_content(
    model=MODEL,
    contents="안녕하세요! 간단히 자기소개해주세요."
)

print(response.text)
```

### 응답 구조

```python
print(type(response))  # <class 'google.genai.types.GenerateContentResponse'>
print(response.text)   # 생성된 텍스트

# 사용 토큰 정보
if hasattr(response, 'usage_metadata'):
    print(response.usage_metadata.prompt_token_count)     # 입력 토큰
    print(response.usage_metadata.candidates_token_count) # 출력 토큰
```

### 텍스트 요약

```python
prompt = f"""
다음 글을 3줄로 요약해주세요:
{sample_text}
"""

response = gemini.models.generate_content(
    model=MODEL,
    contents=prompt
)
print(response.text)
```

### 뉴스 요약 (프로젝트 방식)

프로젝트에서 사용하는 프롬프트 형식:

```python
# 뉴스 컨텍스트 구성
news_context = ""
for i, article in enumerate(news_articles, 1):
    news_context += f"{i}. 제목: {article['title']}\n"
    news_context += f"   내용: {article['content']}\n\n"

prompt = f"""
다음 뉴스 기사들의 핵심 내용을 한국어로 요약해주세요:
- 불릿 포인트 형식으로 최대 5개 항목
- 각 항목은 1~2문장

[뉴스 목록]
{news_context}
"""

response = gemini.models.generate_content(
    model=MODEL,
    contents=prompt
)
```

### 다양한 프롬프트 활용

```python
# 번역
"Translate to English: 인공지능이 세상을 바꾸고 있습니다."

# 감정 분석
"다음 문장의 감정을 분석해주세요 (긍정/부정/중립): ..."

# 키워드 추출
"다음 글에서 핵심 키워드 3개를 추출해주세요: ..."
```

---

## 4. 통합: 검색 + 요약 파이프라인

TrendTracker의 핵심 흐름:

```
[키워드 입력] → [Tavily로 검색] → [Gemini로 요약] → [결과 출력]
```

### 파이프라인 구현

```python
def search_and_summarize(keyword: str, num_results: int = 5) -> dict:
    result = {
        "keyword": keyword,
        "articles": [],
        "summary": "",
        "success": False
    }

    try:
        # 1단계: Tavily로 검색
        search_response = tavily.search(
            query=keyword,
            topic="news",
            search_depth="advanced",
            max_results=num_results
        )

        articles = search_response.get('results', [])
        if not articles:
            return result

        result["articles"] = articles

        # 2단계: 뉴스 컨텍스트 구성
        news_context = ""
        for i, article in enumerate(articles, 1):
            news_context += f"{i}. 제목: {article.get('title', '제목 없음')}\n"
            news_context += f"   내용: {article.get('content', '')[:200]}\n\n"

        # 3단계: Gemini로 요약
        prompt = f"""
다음 뉴스 기사들의 핵심 내용을 한국어로 요약해주세요:
- 불릿 포인트 형식으로 최대 5개 항목
- 각 항목은 1~2문장

[뉴스 목록]
{news_context}
"""
        summary_response = gemini.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        result["summary"] = summary_response.text
        result["success"] = True

    except Exception as e:
        print(f"오류 발생: {e}")

    return result
```

---

## 핵심 요약

| API | 용도 | 주요 파라미터 |
|-----|------|---------------|
| **Tavily** | 뉴스 검색 | `query`, `topic`, `search_depth`, `max_results`, `include_domains` |
| **Gemini** | 텍스트 생성/요약 | `model`, `contents` (프롬프트) |

### Tavily 핵심 코드

```python
from tavily import TavilyClient

client = TavilyClient(api_key="...")
response = client.search(
    query="키워드",
    topic="news",
    search_depth="advanced",
    max_results=5
)
articles = response.get('results', [])
```

### Gemini 핵심 코드

```python
from google import genai

client = genai.Client(api_key="...")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="프롬프트"
)
text = response.text
```
