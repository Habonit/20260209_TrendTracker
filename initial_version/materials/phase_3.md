# Phase 3: 서비스 레이어 - API 연동

## 학습 목표
- API가 무엇이고 왜 필요한지 이해한다
- HTTP 요청/응답의 기본 개념을 익힌다
- 예외 처리(try-except)가 왜 필요하고 어떻게 사용하는지 배운다
- 서비스 레이어의 역할을 이해한다

---

## 1. API란?

### 정의
**API(Application Programming Interface)**는 프로그램들이 서로 통신하는 방법을 정의한 인터페이스이다.

| 용어 | 설명 |
|------|------|
| API | 프로그램 간 통신 규약 |
| 요청(Request) | API에 보내는 데이터 |
| 응답(Response) | API가 돌려주는 데이터 |
| API 키 | 인증 정보 (누가 요청하는지) |

### 왜 필요한가?
직접 구현하기 어려운 기능을 **다른 서비스에서 가져다 쓸 수 있다.**

- 뉴스 검색 → **Tavily API**
- AI 요약 → **Gemini API**
- 날씨 정보 → 기상청 API
- 지도 → Google Maps API

### API 동작 흐름 (식당 비유)

```python
class 식당API:
    def __init__(self):
        self.메뉴 = {"짜장면": 7000, "짬뽕": 8000}

    def 주문(self, 메뉴이름: str) -> dict:
        if 메뉴이름 in self.메뉴:
            return {"status": "성공", "음식": 메뉴이름, "가격": self.메뉴[메뉴이름]}
        else:
            return {"status": "실패", "에러": "메뉴에 없는 음식입니다"}

식당 = 식당API()
응답 = 식당.주문("짜장면")  # 성공 응답
응답 = 식당.주문("피자")    # 실패 응답
```

---

## 2. HTTP 요청/응답

### HTTP란?
HTTP는 **인터넷에서 데이터를 주고받는 프로토콜(약속)**이다.

```
[요청]
GET https://api.example.com/news?keyword=AI
Authorization: Bearer sk-xxxxx  ← API 키

[응답]
HTTP 200 OK  ← 상태 코드 (성공)
{
  "results": [{"title": "AI 뉴스", ...}]
}
```

### 주요 HTTP 상태 코드

| 코드 | 의미 | 설명 |
|------|------|------|
| **200** | OK | 성공 |
| **400** | Bad Request | 요청이 잘못됨 (오타 등) |
| **401** | Unauthorized | 인증 실패 (API 키 오류) |
| **429** | Too Many Requests | 요청이 너무 많음 (Rate Limit) |
| **500** | Server Error | 서버 문제 |

### HTTP 요청 보내기 (requests 라이브러리)

```python
import requests

url = "https://httpbin.org/get"
response = requests.get(url)

print(response.status_code)  # 200이면 성공
print(response.ok)           # True/False
data = response.json()       # JSON을 딕셔너리로 변환
```

### 핵심 정리

| 항목 | 설명 |
|------|------|
| **HTTP** | 웹에서 데이터를 주고받는 프로토콜 |
| **GET** | 데이터를 가져오는 요청 |
| **POST** | 데이터를 보내는 요청 |
| **상태 코드** | 요청 결과를 나타내는 숫자 (200=성공) |
| **JSON** | 데이터 교환 형식 (딕셔너리와 비슷) |

---

## 3. 예외 처리 (try-except)

### 왜 필요한가?
API 호출은 실패할 수 있다: 인터넷 끊김, API 키 오류, 요청 과다, 서버 문제 등.
예외 처리가 없으면 앱이 죽고, 있으면 사용자에게 친절한 메시지를 보여줄 수 있다.

### 기본 구조

```python
try:
    # 오류가 날 수 있는 코드
    result = 10 / 0
except ZeroDivisionError:
    # 해당 예외 발생 시 실행
    print("0으로 나눌 수 없습니다!")
else:
    # 예외 없이 성공 시 실행
    print(f"결과: {result}")
finally:
    # 항상 실행 (정리 작업)
    print("계산 완료!")
```

### 여러 종류의 예외 처리

```python
try:
    value = int("abc")
except ValueError:
    print("숫자로 변환할 수 없습니다!")
except TypeError:
    print("타입이 잘못되었습니다!")
```

### 파이썬 내장 예외 종류

| 예외 | 발생 상황 | 예시 |
|------|----------|------|
| `ValueError` | 값이 잘못됨 | `int("abc")` |
| `TypeError` | 타입이 잘못됨 | `"hello" + 5` |
| `KeyError` | 딕셔너리 키 없음 | `d["없는키"]` |
| `IndexError` | 리스트 인덱스 초과 | `[1,2,3][10]` |
| `AttributeError` | 속성/메서드 없음 | `"str".없는메서드()` |
| `FileNotFoundError` | 파일 없음 | `open("없는파일.txt")` |
| `ZeroDivisionError` | 0으로 나눔 | `10 / 0` |
| `ImportError` | import 실패 | `import 없는모듈` |

예외 잡는 순서: 구체적인 예외 먼저, `Exception`은 맨 마지막에:
```python
try:
    ...
except ValueError:       # 1. 구체적 예외 먼저
    ...
except TypeError:        # 2. 다른 구체적 예외
    ...
except Exception:        # 3. 나머지 모든 예외 (맨 마지막)
    ...
```

### 커스텀 예외 만들기

```python
class AppError(Exception):
    """애플리케이션 전용 예외"""
    def __init__(self, error_type: str):
        self.error_type = error_type
        super().__init__(error_type)

ERROR_MESSAGES = {
    "api_key_invalid": "API 키가 유효하지 않습니다.",
    "rate_limit_exceeded": "요청이 너무 많습니다. 잠시 후 다시 시도해주세요.",
    "network_error": "네트워크 연결을 확인해주세요."
}

# 예외 발생
def fake_api_call(api_key: str):
    if api_key == "":
        raise AppError("api_key_invalid")
    return {"data": "성공"}

# 예외 처리
try:
    result = fake_api_call("")
except AppError as e:
    message = ERROR_MESSAGES.get(e.error_type, "알 수 없는 오류")
    print(f"실패: {message}")
```

### 상속(Inheritance)과 super()

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):           # Animal을 상속
    def __init__(self, name, breed):
        super().__init__(name)  # 부모의 __init__ 호출
        self.breed = breed
```

- `class 자식(부모):` 형태로 상속 선언
- `super().__init__(...)` 으로 부모 생성자 호출
- 커스텀 예외도 `Exception`을 상속받아 만든다

| 상속의 장점 | 설명 |
|------------|------|
| 코드 재사용 | 부모의 기능을 그대로 사용 |
| 확장 | 부모 기능 + 새로운 기능 추가 |
| 일관성 | 같은 부모를 가진 클래스들은 비슷하게 동작 |

---

## 4. 서비스 레이어

### 서비스 레이어란?
**외부 API 호출과 비즈니스 로직을 담당하는 계층**이다.

```
[UI] ←→ [서비스 레이어] ←→ [외부 API]
           ↓
      [데이터 저장소]
```

### 왜 필요한가?
1. **관심사 분리**: UI는 화면만, 서비스는 로직만
2. **재사용**: 같은 서비스를 여러 곳에서 사용
3. **테스트 용이**: 서비스 로직만 독립적으로 테스트

### 서비스 레이어 패턴 예시

```python
from dataclasses import dataclass

@dataclass
class WeatherInfo:
    city: str
    temperature: float
    condition: str

class WeatherService:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_weather(self, city: str) -> WeatherInfo:
        # 실제로는 여기서 API 호출
        ...

service = WeatherService(api_key="my-api-key")
try:
    weather = service.get_weather("서울")
    print(f"기온: {weather.temperature}°C")
except ValueError as e:
    print(f"오류: {e}")
```

### 프로젝트의 서비스들

| 서비스 | 역할 |
|--------|------|
| `search_service.py` | Tavily API로 뉴스 검색 |
| `ai_service.py` | Gemini API로 뉴스 요약 |

### search_service.py 구조

```python
def search_news(keyword: str, num_results: int = 5) -> List[NewsArticle]:
    settings = Settings()
    try:
        # 1. API 클라이언트 초기화
        client = TavilyClient(api_key=settings.TAVILY_API_KEY)

        # 2. API 호출
        response = client.search(
            query=keyword,
            search_depth="advanced",
            include_domains=settings.SEARCH_DOMAINS,
            max_results=max(num_results * 3, 20),
            topic="news"
        )

        # 3. 최신순 정렬
        results = response.get('results', [])
        results.sort(key=lambda x: x.get('published_date', ''), reverse=True)
        results = results[:num_results]

        # 4. NewsArticle 리스트로 변환
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
        # 5. 예외를 AppError로 변환
        error_str = str(e).lower()
        if "401" in error_str or "api key" in error_str:
            raise AppError("api_key_invalid")
        elif "429" in error_str:
            raise AppError("rate_limit_exceeded")
        else:
            raise AppError("network_error")
```

### ai_service.py 구조

```python
def summarize_news(articles: List[NewsArticle]) -> str:
    if not articles:
        return "요약할 기사가 없습니다."

    settings = Settings()
    try:
        # 1. API 클라이언트 초기화
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # 2. 프롬프트 구성
        news_context = ""
        for i, article in enumerate(articles, 1):
            news_context += f"{i}. 제목: {article.title}\n"
            news_context += f"   내용: {article.snippet}\n\n"

        prompt = f"""
다음 뉴스 기사들의 핵심 내용을 한국어로 요약해주세요:
- 불릿 포인트 형식으로 최대 5개 항목
- 각 항목은 1~2문장

[뉴스 목록]
{news_context}
"""

        # 3. API 호출
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt
        )

        return response.text or "요약 결과를 생성하지 못했습니다."

    except Exception as e:
        error_str = str(e).lower()
        if "401" in error_str or "api key" in error_str:
            raise AppError("api_key_invalid")
        elif "429" in error_str:
            raise AppError("rate_limit_exceeded")
        else:
            raise AppError("ai_error")
```

---

## 핵심 요약

| 개념 | 한 줄 요약 |
|------|-----------|
| **API** | 프로그램 간 소통 방법 |
| **HTTP 요청/응답** | 웹에서 데이터를 주고받는 방법 |
| **상태 코드** | 요청 결과를 나타내는 숫자 (200=성공) |
| **try-except** | 오류를 안전하게 처리하는 방법 |
| **커스텀 예외** | 우리만의 예외 클래스 (AppError) |
| **서비스 레이어** | API 호출을 담당하는 계층 |

### 서비스 함수 기본 패턴

```python
def service_function(param):
    try:
        # 1. API 클라이언트 초기화
        client = APIClient(api_key=settings.API_KEY)
        # 2. API 호출
        response = client.call(param)
        # 3. 결과 변환 및 반환
        return convert_to_domain_model(response)
    except Exception as e:
        # 4. 예외를 AppError로 변환
        if "401" in str(e):
            raise AppError("api_key_invalid")
        raise AppError("network_error")
```
