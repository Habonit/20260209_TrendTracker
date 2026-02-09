# Phase 2: 도메인 모델 및 유틸리티 함수

## 학습 목표
- 클래스(class)가 무엇이고 왜 사용하는지 이해한다
- @dataclass로 데이터 구조를 쉽게 만드는 방법을 배운다
- 타입 힌트(Type Hint)로 코드를 더 안전하게 만든다
- 도메인 모델(NewsArticle, SearchResult)의 역할을 이해한다

---

## 1. 클래스(class)

### 클래스란?
클래스는 **같은 구조를 가진 객체를 여러 개 만들기 위한 설계도(템플릿)**이다.

| 용어 | 설명 |
|------|------|
| 클래스(class) | 객체의 구조를 정의하는 설계도 |
| 인스턴스(instance) | 클래스로 만든 실제 객체 |
| 속성(attribute) | 인스턴스가 가진 데이터 |
| 메서드(method) | 클래스 안에 정의된 함수 |
| `__init__` | 인스턴스 생성 시 호출되는 생성자 함수 |
| `self` | 자기 자신(인스턴스)을 가리킴 |

### 왜 필요한가?

클래스 없이 뉴스 기사 100개를 다루면 변수가 300개가 필요하다. 클래스를 쓰면 하나의 개념으로 깔끔하게 관리할 수 있다.

```python
# 클래스 없이 → 변수 폭발
title1 = "첫 번째 기사"
url1 = "https://..."
snippet1 = "내용..."

# 클래스 사용 → 깔끔한 관리
article1 = NewsArticle(title="첫 번째", url="...", snippet="...")
```

### 클래스 정의와 사용

```python
class Student:
    def __init__(self, name, age, grade):  # 생성자
        self.name = name      # 속성 저장
        self.age = age
        self.grade = grade

    def introduce(self):  # 메서드
        return f"안녕하세요! {self.grade}학년 {self.name}입니다."

# 인스턴스 생성
student1 = Student(name="김철수", age=20, grade=2)

# 속성 접근
print(student1.name)        # 김철수

# 메서드 호출
print(student1.introduce()) # 안녕하세요! 2학년 김철수입니다.
```

**핵심 정리:**
- `class 클래스명:` 으로 클래스 정의
- `__init__(self, ...)` 에서 속성 초기화
- `self.속성 = 값` 으로 데이터 저장
- `.` 으로 속성과 메서드에 접근

---

## 2. @dataclass

### @dataclass란?
`@dataclass`는 **데이터를 저장하는 클래스를 자동으로 생성해주는 기능**이다.
`@`는 **데코레이터**라고 불리며, 클래스나 함수에 추가 기능을 부여하는 문법이다.

### 일반 클래스 vs @dataclass

```python
# 일반 클래스 - 직접 다 작성해야 함
class PersonNormal:
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"PersonNormal(name='{self.name}', age={self.age}, email='{self.email}')"

# @dataclass - 자동 생성!
from dataclasses import dataclass

@dataclass
class PersonDataclass:
    name: str
    age: int
    email: str
```

| 항목 | 일반 클래스 | @dataclass |
|------|------------|------------|
| `__init__` | 직접 작성 | 자동 생성 |
| `__repr__` | 직접 작성 | 자동 생성 |
| `__eq__` | 직접 작성 | 자동 생성 |
| 코드 길이 | 길다 | 짧다 |
| 용도 | 복잡한 로직 | 데이터 저장 |

### @dataclass의 자동 기능

```python
@dataclass
class Book:
    title: str
    author: str
    price: int

book1 = Book("파이썬 입문", "홍길동", 25000)
book2 = Book("파이썬 입문", "홍길동", 25000)

print(book1)              # Book(title='파이썬 입문', author='홍길동', price=25000) → 자동 출력
print(book1 == book2)     # True → 자동 비교
print(book1.title)        # 파이썬 입문 → 속성 접근
```

### 기본값 사용하기

```python
from typing import Optional

@dataclass
class Product:
    name: str                          # 필수값 (기본값 없음)
    price: int                         # 필수값
    category: str = "기타"             # 선택값 (기본값: "기타")
    discount: int = 0                  # 선택값 (기본값: 0)
    description: Optional[str] = None  # 선택값 (None 허용)

product1 = Product("노트북", 1500000)                        # 필수값만
product2 = Product("마우스", 50000, category="전자기기")      # 일부 선택값
```

> **주의**: 기본값이 있는 속성은 반드시 기본값 없는 속성 뒤에 와야 한다.

### 데코레이터 참고

| 데코레이터 | 역할 |
|------------|------|
| `@dataclass` | 데이터 클래스 자동 생성 |
| `@property` | 메서드를 속성처럼 사용 |
| `@staticmethod` | 인스턴스 없이 호출 가능한 메서드 |

---

## 3. 타입 힌트 (Type Hint)

### 타입 힌트란?
타입 힌트는 **변수나 함수에 어떤 타입의 값이 들어오는지 명시하는 것**이다.

```python
# 타입 힌트 없이
def greet(name):
    return f"안녕, {name}!"

# 타입 힌트 있으면
def greet(name: str) -> str:
    return f"안녕, {name}!"
```

### 왜 필요한가?
1. **실수 방지**: 잘못된 타입을 넣으면 IDE가 경고
2. **자동 완성**: IDE가 어떤 속성/메서드가 있는지 알려줌
3. **문서 역할**: 코드만 봐도 어떤 값을 기대하는지 알 수 있음

### 기본 타입

```python
name: str = "홍길동"      # 문자열
age: int = 25             # 정수
height: float = 175.5     # 실수(소수점)
is_student: bool = True   # 참/거짓
```

### 컬렉션 타입

```python
from typing import List, Dict, Tuple, Optional

scores: List[int] = [90, 85, 88]            # 같은 타입의 리스트
grades: Dict[str, int] = {"철수": 90}       # 키-값 딕셔너리
point: Tuple[int, int] = (10, 20)           # 고정 개수의 값
nickname: Optional[str] = None              # str 또는 None
```

### 함수에서 타입 힌트

```python
def calculate_average(scores: List[int]) -> float:
    if not scores:
        return 0.0
    return sum(scores) / len(scores)

def find_max_score(scores: List[int]) -> Optional[int]:
    if not scores:
        return None  # Optional이므로 None 반환 가능
    return max(scores)
```

> `-> float`는 반환 타입을 나타낸다.

### Optional[str] = None의 의미

```python
nickname: Optional[str] = None
# 의미: "문자열이거나 None이고, 기본값은 None"
```

- `Optional[str]` → 타입 힌트: str이거나 None일 수 있다
- `= None` → 기본값: 값을 안 주면 None으로 설정된다

### 타입은 클래스다

파이썬에서 **타입(type) = 클래스(class)**이다. 우리가 만든 클래스도 타입으로 사용할 수 있다.

```python
@dataclass
class NewsArticle:
    title: str
    url: str

# NewsArticle을 타입으로 사용
article: NewsArticle = NewsArticle("제목", "https://...")
articles: List[NewsArticle] = [
    NewsArticle("뉴스1", "https://1.com"),
    NewsArticle("뉴스2", "https://2.com"),
]

# 함수에서 타입 힌트로 사용 → IDE 자동완성 지원
def summarize(articles: List[NewsArticle]) -> str:
    for article in articles:
        print(article.title)  # 자동완성 됨!
```

### 타입 힌트 정리

| 타입 | 설명 | 예시 |
|------|------|------|
| `str` | 문자열 | `"안녕"` |
| `int` | 정수 | `42` |
| `float` | 실수 | `3.14` |
| `bool` | 참/거짓 | `True` |
| `List[X]` | X 타입의 리스트 | `[1, 2, 3]` |
| `Dict[K, V]` | K-V 쌍의 딕셔너리 | `{"a": 1}` |
| `Optional[X]` | X 또는 None | `None` 또는 값 |

---

## 4. 도메인 모델

### 도메인 모델이란?
도메인 모델은 **프로그램이 다루는 핵심 개념을 코드로 표현**한 것이다.

| 프로그램 | 도메인 모델 |
|----------|------------|
| 도서관 | `Book`, `Member`, `Loan` |
| 쇼핑몰 | `Product`, `Order`, `Customer` |
| 뉴스 검색 | `NewsArticle`, `SearchResult` |

### 왜 필요한가?
1. **명확한 구조**: "뉴스 기사"가 무엇으로 구성되는지 정의
2. **재사용**: 한 번 정의하면 프로그램 전체에서 사용
3. **유지보수**: 변경이 필요하면 한 곳만 수정

### NewsArticle 도메인 모델

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class NewsArticle:
    """뉴스 기사 정보를 담는 데이터 클래스"""
    title: str                      # 기사 제목 (필수)
    url: str                        # 기사 URL (필수)
    snippet: str                    # 기사 요약/스니펫 (필수)
    pub_date: Optional[str] = None  # 발행일 (선택, 없을 수 있음)

article = NewsArticle(
    title="AI 기술이 바꾸는 미래",
    url="https://news.example.com/ai",
    snippet="인공지능 기술의 발전이...",
    pub_date="2024-01-20"
)
```

### SearchResult 도메인 모델

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List
import pandas as pd

@dataclass
class SearchResult:
    """검색 결과 및 AI 요약 정보를 담는 데이터 클래스"""
    search_key: str              # "키워드-yyyymmddhhmm" (고유 식별자)
    search_time: datetime        # 검색 실행 시간
    keyword: str                 # 검색 키워드
    articles: List[NewsArticle]  # 뉴스 기사 리스트 (여러 개!)
    ai_summary: str              # AI 요약 결과

    def to_dataframe(self) -> pd.DataFrame:
        """검색 결과를 DataFrame으로 변환 (기사 1건 = 1행)"""
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
        return pd.DataFrame(data)
```

### 유틸리티 함수: search_key 생성

```python
from datetime import datetime

def generate_search_key(keyword: str) -> str:
    """'키워드-yyyymmddhhmm' 형식의 검색 키를 생성"""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M")
    return f"{keyword}-{timestamp}"
```

### 매개변수(Parameter) 참고

```python
# 함수 정의 시 → 매개변수(parameter)
def greet(name):  # name이 매개변수
    return f"안녕, {name}!"

# 함수 호출 시 → 인자/인수(argument)
greet("철수")  # "철수"가 인자
```

매개변수의 종류:
```python
def example(
    required,              # 1. 필수 매개변수: 반드시 전달
    optional="기본값",      # 2. 선택 매개변수: 기본값 있음
    *args,                 # 3. 가변 매개변수: 여러 개 받음
    **kwargs               # 4. 키워드 매개변수: 이름=값 형태
):
    pass
```

---

## 핵심 요약

| 개념 | 한 줄 요약 |
|------|-----------|
| **클래스(class)** | 같은 구조의 데이터를 여러 개 만드는 틀 |
| **인스턴스** | 클래스로 만든 실제 객체 |
| **@dataclass** | 데이터 저장용 클래스를 간편하게 만드는 도구 |
| **타입 힌트** | 변수/함수에 어떤 타입이 오는지 표시 |
| **Optional** | 값이 있거나 None일 수 있음을 표시 |
| **도메인 모델** | 프로그램이 다루는 핵심 개념을 코드로 표현 |
