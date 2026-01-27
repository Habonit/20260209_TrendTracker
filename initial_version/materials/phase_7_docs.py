"""
# ============================================
# Phase 7-3: 문서화
# ============================================
#
# 🎯 이 파일에서 배울 것:
# - Docstring 작성법
# - 타입 힌트의 중요성
# - README.md 작성법
# - 코드 정리 (린팅/포매팅)
#
# 📋 실행 방법:
# streamlit run materials/phase_7_docs.py
# ============================================
"""

import streamlit as st
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

st.set_page_config(page_title="Phase 7-3: 문서화", page_icon="📝", layout="wide")

st.title("📝 Phase 7-3: 문서화")

# ============================================
# 📚 이론: 왜 문서화가 중요한가?
# ============================================

st.header("1️⃣ 문서화의 중요성")

st.markdown("""
## 문서화란?

코드가 **무엇을 하는지 설명**하는 것입니다.

### 문서화가 없으면?

```python
def f(x, y, z):
    return [i for i in x if y(i) > z]
```

🤔 "이게 뭐하는 함수지...?"

### 문서화가 있으면?

```python
def filter_items_by_threshold(
    items: List[int],
    scorer: Callable[[int], float],
    threshold: float
) -> List[int]:
    \"\"\"
    점수가 임계값을 초과하는 항목만 필터링합니다.

    Args:
        items: 필터링할 항목 리스트
        scorer: 각 항목의 점수를 계산하는 함수
        threshold: 최소 점수 임계값

    Returns:
        점수가 threshold를 초과하는 항목들의 리스트
    \"\"\"
    return [item for item in items if scorer(item) > threshold]
```

✅ "아, 점수 기준으로 필터링하는 거구나!"

### 비유로 이해하기

> 📦 **택배 비유**
>
> **문서화 없음**: 상자에 아무것도 안 적힘 → 열어봐야 앎
> **문서화 있음**: "깨지기 쉬움 / 전자제품 / 위로" → 바로 이해
""")

st.divider()

# ============================================
# 📚 이론: Docstring
# ============================================

st.header("2️⃣ Docstring (문서화 문자열)")

st.markdown("""
## Docstring이란?

함수/클래스 바로 아래에 작성하는 **설명 문자열**입니다.

### 기본 형식

```python
def 함수명(인자):
    \"\"\"
    함수가 하는 일을 한 줄로 설명합니다.

    Args:
        인자명: 인자에 대한 설명

    Returns:
        반환값에 대한 설명

    Raises:
        발생할 수 있는 예외

    Example:
        >>> 함수명(예시_인자)
        예시_결과
    \"\"\"
    pass
```

### 실제 예시

```python
def search_news(keyword: str, num_results: int = 5) -> List[NewsArticle]:
    \"\"\"
    키워드로 뉴스를 검색하여 결과를 반환합니다.

    Tavily API를 사용하여 최신 뉴스를 검색하고,
    발행일 기준으로 정렬하여 반환합니다.

    Args:
        keyword: 검색할 키워드
        num_results: 반환할 결과 수 (기본값: 5)

    Returns:
        검색된 뉴스 기사 리스트

    Raises:
        AppError: API 키 오류, 요청 한도 초과 등

    Example:
        >>> articles = search_news("AI", 3)
        >>> len(articles)
        3
    \"\"\"
    pass
```
""")

st.divider()

# ============================================
# 📚 이론: 타입 힌트
# ============================================

st.header("3️⃣ 타입 힌트 (Type Hints)")

st.markdown("""
## 타입 힌트란?

변수나 함수의 **데이터 타입을 명시**하는 것입니다.

### 기본 타입 힌트

```python
# 변수
name: str = "홍길동"
age: int = 25
is_active: bool = True
scores: List[int] = [90, 85, 88]

# 함수
def greet(name: str) -> str:
    return f"안녕하세요, {name}님!"

def add(a: int, b: int) -> int:
    return a + b
```

### typing 모듈

```python
from typing import Optional, List, Dict, Any, Callable

# Optional: 값이 없을 수도 있음
def find_user(user_id: int) -> Optional[User]:
    ...

# List: 리스트
def get_names() -> List[str]:
    ...

# Dict: 딕셔너리
def get_config() -> Dict[str, Any]:
    ...
```

### 타입 힌트의 장점

| 장점 | 설명 |
|------|------|
| 가독성 | 코드만 봐도 타입을 알 수 있음 |
| 에러 방지 | IDE가 타입 오류를 미리 알려줌 |
| 문서화 | 별도 설명 없이도 이해 가능 |
| 자동완성 | IDE가 더 정확한 제안을 함 |
""")

st.divider()

# ============================================
# 🔍 예제: Docstring과 타입 힌트
# ============================================

st.header("4️⃣ 실제 예제")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ❌ 문서화 없음")
    st.code('''
def calc(d, t):
    if t == "avg":
        return sum(d) / len(d)
    elif t == "sum":
        return sum(d)
    elif t == "max":
        return max(d)
    return None
    ''', language="python")
    st.error("무슨 함수인지 알기 어려움")

with col2:
    st.markdown("### ✅ 문서화 있음")
    st.code('''
def calculate_stats(
    data: List[float],
    stat_type: str
) -> Optional[float]:
    """
    데이터의 통계값을 계산합니다.

    Args:
        data: 숫자 데이터 리스트
        stat_type: 통계 유형
                   ("avg", "sum", "max")

    Returns:
        계산된 통계값,
        유효하지 않으면 None
    """
    if stat_type == "avg":
        return sum(data) / len(data)
    elif stat_type == "sum":
        return sum(data)
    elif stat_type == "max":
        return max(data)
    return None
    ''', language="python")
    st.success("명확하게 이해 가능!")

st.divider()

# ============================================
# 📚 이론: README.md
# ============================================

st.header("5️⃣ README.md 작성법")

st.markdown("""
## README.md란?

프로젝트의 **첫인상**이자 **사용 설명서**입니다.

### 필수 포함 항목

1. **프로젝트 이름과 설명**
2. **설치 방법**
3. **실행 방법**
4. **사용 예시**
5. **폴더 구조** (선택)
6. **라이선스** (선택)

### TrendTracker README 구조

```markdown
# TrendTracker 🚀

키워드로 뉴스를 검색하고 AI가 요약해주는 웹앱

## 🌟 주요 기능
- 최신 뉴스 검색
- AI 핵심 요약
- 검색 기록 관리
- CSV 다운로드

## 🛠 설치 방법

### 1. uv 설치
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 의존성 설치
```bash
uv sync
```

### 3. 환경변수 설정
```bash
cp .env.example .env
# .env 파일에 API 키 입력
```

### 4. 실행
```bash
uv run streamlit run app.py
```

## 🔑 API 키 발급
- Tavily: https://tavily.com/
- Gemini: https://aistudio.google.com/

## 📁 폴더 구조
(구조 설명)

## ⚠️ 주의사항
(주의사항)
```
""")

st.divider()

# ============================================
# 🔎 TrendTracker 문서화 분석
# ============================================

st.header("6️⃣ TrendTracker 문서화 분석")

with st.expander("📂 utils/error_handler.py", expanded=True):
    st.code('''
import streamlit as st

ERROR_MESSAGES = {
    "api_key_invalid": "API 키가 유효하지 않습니다. 설정을 확인해주세요.",
    "rate_limit_exceeded": "요청이 너무 많습니다. 잠시 후 다시 시도해주세요.",
    "network_error": "네트워크 연결을 확인해주세요.",
    "no_results": "검색 결과가 없습니다.",
    "ai_error": "AI 요약 중 오류가 발생했습니다.",
}

def handle_error(error_type: str, level: str = "error"):
    """
    지정된 에러 타입과 레벨에 따라 Streamlit 메시지를 출력합니다.

    Args:
        error_type: 에러 타입 키 (ERROR_MESSAGES의 키)
        level: 메시지 레벨 ("error", "warning", "info")
    """
    message = ERROR_MESSAGES.get(error_type, "알 수 없는 오류가 발생했습니다")

    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    elif level == "info":
        st.info(message)
    ''', language="python")

    st.markdown("""
    ### 💡 분석 포인트

    1. **상수 분리**: `ERROR_MESSAGES`를 딕셔너리로 관리
    2. **타입 힌트**: `error_type: str`, `level: str = "error"`
    3. **Docstring**: 함수 역할, Args 설명
    4. **기본값**: `level = "error"`로 기본 동작 정의
    """)

with st.expander("📂 domain/news_article.py"):
    st.code('''
from dataclasses import dataclass
from typing import Optional

@dataclass
class NewsArticle:
    """
    뉴스 기사를 나타내는 데이터 클래스입니다.

    Attributes:
        title: 기사 제목
        url: 기사 링크 URL
        snippet: 기사 요약/스니펫
        pub_date: 발행일 (없을 수 있음)
    """
    title: str
    url: str
    snippet: str
    pub_date: Optional[str] = None
    ''', language="python")

    st.markdown("""
    ### 💡 분석 포인트

    1. **@dataclass**: 간결한 데이터 클래스
    2. **타입 힌트**: 모든 속성에 타입 지정
    3. **Optional**: `pub_date`는 없을 수도 있음
    4. **Docstring**: 클래스와 각 속성 설명
    """)

st.divider()

# ============================================
# ✏️ 가이드 실습
# ============================================

st.header("✏️ 가이드 실습: 문서화 추가하기")

st.markdown("""
### 목표
문서화가 없는 코드에 Docstring과 타입 힌트 추가하기
""")

st.subheader("🎯 실습 영역")

st.markdown("**문서화가 필요한 코드:**")

st.code('''
# ============================================
# ✏️ 실습: 문서화 추가하기
# ============================================

# TODO 1: 아래 함수에 타입 힌트와 Docstring 추가

def get_greeting(name, formal):
    if formal:
        return f"안녕하십니까, {name}님."
    return f"안녕, {name}!"


# TODO 2: 아래 클래스에 Docstring 추가

class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    def is_adult(self):
        return self.age >= 18


# TODO 3: 아래 함수에 완전한 문서화 추가
# - 타입 힌트
# - Docstring (설명, Args, Returns, Raises)

def divide_numbers(a, b):
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다")
    return a / b
''', language="python")

st.markdown("**정답:**")

with st.expander("📂 정답 보기"):
    st.code('''
# TODO 1 정답
def get_greeting(name: str, formal: bool = False) -> str:
    """
    인사말을 생성합니다.

    Args:
        name: 인사 대상의 이름
        formal: True면 격식체, False면 반말

    Returns:
        생성된 인사말 문자열
    """
    if formal:
        return f"안녕하십니까, {name}님."
    return f"안녕, {name}!"


# TODO 2 정답
class User:
    """
    사용자 정보를 담는 클래스입니다.

    Attributes:
        name: 사용자 이름
        email: 이메일 주소
        age: 나이
    """

    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self.email = email
        self.age = age

    def is_adult(self) -> bool:
        """사용자가 성인인지 확인합니다."""
        return self.age >= 18


# TODO 3 정답
def divide_numbers(a: float, b: float) -> float:
    """
    두 숫자를 나눕니다.

    Args:
        a: 피제수 (나눠지는 수)
        b: 제수 (나누는 수)

    Returns:
        a를 b로 나눈 결과

    Raises:
        ValueError: b가 0일 때

    Example:
        >>> divide_numbers(10, 2)
        5.0
    """
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다")
    return a / b
    ''', language="python")

st.divider()

# ============================================
# 🏆 챌린지
# ============================================

st.header("🏆 챌린지: 완전한 문서화")

st.markdown("""
### 목표
미니 프로젝트의 모든 코드에 문서화 추가하기

⚠️ **정답이 제공되지 않습니다.** 강사와 함께 풀어보세요!
""")

st.subheader("🎯 챌린지 영역")

st.code('''
# ============================================
# 🏆 챌린지: 완전한 문서화
# ============================================
# ⚠️ 정답이 제공되지 않습니다.

# TODO: 아래 모든 코드에 문서화 추가
# - 타입 힌트
# - Docstring (클래스, 함수, 메서드)
# - 상수에 주석

ERROR_CODES = {
    "E001": "Invalid input",
    "E002": "Not found",
    "E003": "Permission denied",
}


class ValidationError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(message)


class DataProcessor:
    def __init__(self, data, options=None):
        self.data = data
        self.options = options or {}
        self.results = []

    def validate(self):
        if not self.data:
            raise ValidationError("E001", "데이터가 비어있습니다")
        return True

    def process(self):
        self.validate()
        for item in self.data:
            result = self._process_item(item)
            self.results.append(result)
        return self.results

    def _process_item(self, item):
        # 내부 처리 로직
        return item.upper() if isinstance(item, str) else item

    def get_summary(self):
        return {
            "total": len(self.results),
            "processed": len([r for r in self.results if r]),
        }


def create_processor(data, options=None):
    processor = DataProcessor(data, options)
    return processor


def run_pipeline(data, options=None):
    processor = create_processor(data, options)
    results = processor.process()
    summary = processor.get_summary()
    return results, summary
''', language="python")

st.markdown("""
### 💡 힌트

1. **클래스 Docstring**: 클래스가 무엇을 나타내는지, Attributes 설명
2. **메서드 Docstring**: 무엇을 하는지, Args, Returns, Raises
3. **프라이빗 메서드**: `_process_item`도 간단히 설명
4. **상수 주석**: 각 에러 코드의 의미
""")

st.divider()

# ============================================
# 📋 정리
# ============================================

st.header("📋 정리")

st.markdown("""
### 이번 파일에서 배운 것

| 개념 | 설명 |
|------|------|
| Docstring | 함수/클래스 설명 문자열 |
| 타입 힌트 | 데이터 타입 명시 |
| README | 프로젝트 사용 설명서 |
| 코드 정리 | 일관된 스타일, 불필요한 코드 제거 |

### Docstring 템플릿

```python
def function_name(arg1: Type1, arg2: Type2 = default) -> ReturnType:
    \"\"\"
    함수가 하는 일을 한 줄로 설명합니다.

    더 자세한 설명이 필요하면 여기에 씁니다.

    Args:
        arg1: 첫 번째 인자 설명
        arg2: 두 번째 인자 설명 (기본값: default)

    Returns:
        반환값 설명

    Raises:
        ErrorType: 에러 발생 조건

    Example:
        >>> function_name(value1, value2)
        expected_result
    \"\"\"
    pass
```

### README 템플릿

```markdown
# 프로젝트명

한 줄 설명

## 주요 기능
- 기능 1
- 기능 2

## 설치 방법
```bash
설치 명령어
```

## 실행 방법
```bash
실행 명령어
```

## API 키 발급
- 서비스1: URL
- 서비스2: URL
```

### ✅ 체크리스트
- [ ] Docstring 작성법을 안다
- [ ] 타입 힌트를 사용할 수 있다
- [ ] README의 필수 항목을 안다
- [ ] 좋은 문서화의 중요성을 이해했다
- [ ] 챌린지를 강사와 함께 풀어봤다

---

## 🎉 Phase 7 완료! 전체 과정 완료!

축하합니다! TrendTracker의 모든 Phase를 학습했습니다.

### 전체 복습

| Phase | 주제 |
|-------|------|
| 1 | 프로젝트 초기화 (uv, 환경변수, 구조) |
| 2 | 도메인 모델 (클래스, dataclass, 타입) |
| 3 | 서비스 레이어 (API, 예외 처리) |
| 4 | 리포지토리 (파일 I/O, CSV, pandas) |
| 5 | UI 컴포넌트 (Streamlit) |
| 6 | 메인 앱 통합 |
| 7 | 에러 핸들링 & 마무리 |

### 다음 단계

1. **실제 프로젝트 실행**: `uv run streamlit run app.py`
2. **코드 수정해보기**: 기능 추가, UI 변경
3. **나만의 프로젝트**: 배운 패턴으로 새 프로젝트 시작!
""")
