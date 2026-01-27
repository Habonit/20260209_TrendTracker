"""
# ============================================
# Phase 5-5: 함수로 UI 분리 + 프로젝트 분석
# ============================================
#
# 🎯 이 파일에서 배울 것:
# - UI 코드를 함수로 분리하는 이유
# - 컴포넌트 함수 만드는 방법
# - 실제 프로젝트 코드 분석
# - TrendTracker의 components/ 폴더 이해
#
# 📋 실행 방법:
# streamlit run materials/phase_5_components.py
# ============================================
"""

import streamlit as st
from typing import Optional, List
from dataclasses import dataclass

st.set_page_config(page_title="Phase 5-5: 컴포넌트", page_icon="🧩", layout="wide")

st.title("🧩 Phase 5-5: 함수로 UI 분리")

# ============================================
# 📚 이론: 왜 함수로 분리할까?
# ============================================

st.header("1️⃣ 왜 함수로 분리할까?")

st.markdown("""
## 문제 상황

한 파일에 모든 코드를 넣으면...

```python
# app.py (500줄...)
st.title("앱")
st.sidebar.title("사이드바")
keyword = st.text_input("검색어")
if st.button("검색"):
    # 검색 로직 50줄...
# 결과 표시 100줄...
# 사이드바 설정 80줄...
# 기록 표시 70줄...
# ...끝이 없음
```

### 문제점

1. **코드가 너무 길어짐** - 어디가 뭔지 찾기 어려움
2. **재사용 불가** - 같은 UI를 다른 곳에서 쓸 수 없음
3. **유지보수 어려움** - 수정할 부분을 찾기 힘듦

## 해결책: 함수로 분리!

```python
# components/search_form.py
def render_search_form():
    keyword = st.text_input("검색어")
    return keyword

# components/sidebar.py
def render_sidebar():
    st.sidebar.title("사이드바")
    ...

# app.py (깔끔!)
from components.search_form import render_search_form
from components.sidebar import render_sidebar

render_sidebar()
keyword = render_search_form()
```

### 장점

| 장점 | 설명 |
|------|------|
| 재사용성 | 같은 컴포넌트를 여러 곳에서 import |
| 가독성 | 각 함수가 하나의 역할만 담당 |
| 유지보수 | 수정할 파일을 바로 찾을 수 있음 |
| 테스트 | 각 함수를 독립적으로 테스트 가능 |
""")

st.divider()

# ============================================
# 📚 이론: 컴포넌트 함수 만들기
# ============================================

st.header("2️⃣ 컴포넌트 함수 만들기")

st.markdown("""
## 기본 규칙

1. **함수 이름**: `render_xxx()` 형태로 (렌더링 = 화면에 그리기)
2. **반환값**: 사용자 입력을 반환해야 하면 return 사용
3. **타입 힌트**: `-> Optional[str]` 등으로 명확히
4. **독립성**: 다른 함수에 의존하지 않도록

## 패턴 1: 표시만 하는 함수

```python
def render_header():
    \"\"\"헤더를 렌더링합니다. (반환값 없음)\"\"\"
    st.title("앱 제목")
    st.markdown("앱 설명...")
```

## 패턴 2: 입력을 반환하는 함수

```python
def render_search_form() -> Optional[str]:
    \"\"\"검색 폼을 렌더링하고 검색어를 반환합니다.\"\"\"
    keyword = st.text_input("검색어")
    if st.button("검색"):
        if keyword:
            return keyword
    return None
```

## 패턴 3: 데이터를 받아서 표시하는 함수

```python
def render_results(items: List[str]):
    \"\"\"결과 목록을 렌더링합니다.\"\"\"
    st.subheader("결과")
    for item in items:
        st.write(f"- {item}")
```
""")

st.divider()

# ============================================
# 🔍 실습: 직접 만들어보기
# ============================================

st.header("3️⃣ 직접 만들어보기")

st.markdown("### 컴포넌트 함수들을 정의하고 사용해봅시다!")

# 컴포넌트 함수 정의
def render_greeting_form() -> Optional[str]:
    """인사 폼을 렌더링하고 이름을 반환합니다."""
    st.subheader("👋 인사하기")
    name = st.text_input("이름을 입력하세요", key="greeting_name")
    if st.button("인사", key="greeting_btn"):
        if name:
            return name
        else:
            st.warning("이름을 입력해주세요")
    return None


def render_greeting_result(name: str):
    """인사 결과를 렌더링합니다."""
    st.success(f"안녕하세요, {name}님! 반갑습니다! 🎉")


def render_settings() -> int:
    """설정을 렌더링하고 선택된 값을 반환합니다."""
    st.sidebar.subheader("⚙️ 설정")
    count = st.sidebar.slider("항목 수", 1, 10, 5, key="settings_count")
    return count


# 컴포넌트 사용
col1, col2 = st.columns(2)

with col1:
    st.markdown("**코드:**")
    st.code('''
def render_greeting_form() -> Optional[str]:
    st.subheader("👋 인사하기")
    name = st.text_input("이름을 입력하세요")
    if st.button("인사"):
        if name:
            return name
    return None

def render_greeting_result(name: str):
    st.success(f"안녕하세요, {name}님!")

# 사용
name = render_greeting_form()
if name:
    render_greeting_result(name)
    ''')

with col2:
    st.markdown("**실행 결과:**")
    name = render_greeting_form()
    if name:
        render_greeting_result(name)

st.divider()

# ============================================
# 🔎 프로젝트 코드 분석
# ============================================

st.header("🔎 실제 프로젝트 코드 분석")

st.markdown("""
## TrendTracker의 컴포넌트 구조

```
components/
├── search_form.py      # 검색 폼
├── sidebar.py          # 사이드바 (설정, 기록, 다운로드)
├── result_section.py   # 결과 표시 (요약, 뉴스 목록)
└── loading.py          # 로딩 스피너
```

각 파일이 **하나의 UI 영역**을 담당합니다!
""")

# 탭으로 각 컴포넌트 분석
tab1, tab2, tab3, tab4 = st.tabs([
    "📂 search_form.py",
    "📂 sidebar.py",
    "📂 result_section.py",
    "📂 loading.py"
])

with tab1:
    st.markdown("""
    ### render_search_form() 함수

    **역할**: 키워드 입력 폼을 렌더링하고 검색어를 반환
    """)

    st.code('''
def render_search_form() -> Optional[str]:
    """키워드 입력을 위한 검색 폼을 렌더링합니다."""
    st.markdown("### 🔍 뉴스 검색")

    # st.form: 엔터 키로도 제출 가능
    with st.form(key="search_form", clear_on_submit=False):
        col1, col2 = st.columns([4, 1])  # 4:1 비율

        with col1:
            keyword_input = st.text_input(
                label="검색 키워드",
                placeholder="관심 있는 키워드를 입력하세요",
                label_visibility="collapsed"  # 레이블 숨김
            )

        with col2:
            submit_button = st.form_submit_button(
                label="검색",
                use_container_width=True
            )

        if submit_button:
            if not keyword_input.strip():  # 빈 입력 체크
                st.warning("검색어를 입력해주세요.")
                return None
            return keyword_input.strip()

    return None
    ''', language="python")

    st.markdown("""
    ### 💡 핵심 포인트

    1. **타입 힌트**: `-> Optional[str]` (문자열 또는 None)
    2. **st.form**: 엔터 키 제출 지원 (사용자 편의성)
    3. **컬럼 비율**: `[4, 1]`로 입력창:버튼 = 4:1
    4. **입력 검증**: `if not keyword_input.strip():` 빈 입력 체크
    5. **레이블 숨김**: `label_visibility="collapsed"` (디자인용)
    """)

with tab2:
    st.markdown("""
    ### sidebar.py의 함수들

    **역할**: 사이드바의 각 섹션을 담당
    """)

    st.code('''
def render_sidebar_header():
    """사이드바 헤더를 렌더링합니다."""
    st.sidebar.title("🚀 TrendTracker")
    st.sidebar.markdown("키워드로 뉴스를 검색하고 AI가 요약해드립니다.")
    st.sidebar.divider()

def render_settings() -> int:
    """검색 건수 슬라이더를 렌더링하고 값을 반환합니다."""
    st.sidebar.subheader("⚙️ 설정")
    num_results = st.sidebar.slider(
        "검색 결과 수",
        min_value=1,
        max_value=10,
        value=5,
        help="한 번에 검색할 뉴스 기사의 개수"
    )
    return num_results  # 선택값 반환!

def render_history_list(search_keys: List[str]) -> Optional[str]:
    """검색 기록을 selectbox로 렌더링"""
    st.sidebar.subheader("📜 검색 기록")

    if not search_keys:  # 기록 없으면
        st.sidebar.info("저장된 검색 기록이 없습니다.")
        return None

    selected = st.sidebar.selectbox(
        "과거 기록 불러오기",
        options=["선택하세요"] + search_keys
    )

    if selected == "선택하세요":
        return None
    return selected
    ''', language="python")

    st.markdown("""
    ### 💡 핵심 포인트

    1. **함수 분리**: 각 섹션을 별도 함수로 (헤더, 설정, 기록)
    2. **반환값**: 슬라이더/셀렉트박스의 선택값을 반환
    3. **빈 상태 처리**: `if not search_keys:`로 빈 리스트 체크
    4. **기본값**: "선택하세요"를 옵션 맨 앞에 추가
    """)

with tab3:
    st.markdown("""
    ### result_section.py의 함수들

    **역할**: AI 요약과 뉴스 목록을 표시
    """)

    st.code('''
def render_summary(keyword: str, summary: str):
    """AI 요약 결과를 렌더링합니다."""
    st.markdown("---")
    st.subheader(f"🤖 '{keyword}' 핵심 요약")
    st.info(summary)  # 파란색 박스

def render_news_list(articles: List[NewsArticle]):
    """검색된 뉴스 기사 목록을 렌더링합니다."""
    st.subheader("📰 관련 뉴스 목록")

    if not articles:
        st.write("관련 뉴스가 없습니다.")
        return

    for article in articles:
        # 날짜가 있으면 제목에 표시
        date_str = f" ({article.pub_date})" if article.pub_date else ""

        # expander: 클릭하면 펼쳐지는 UI
        with st.expander(f"📌 {article.title}{date_str}"):
            if article.pub_date:
                st.caption(f"📅 발행일: {article.pub_date}")
            st.markdown(f"**기사 스니펫:**\\n{article.snippet}")
            st.markdown(f"[🔗 기사 보기]({article.url})")
    ''', language="python")

    st.markdown("""
    ### 💡 핵심 포인트

    1. **데이터 받기**: 함수 파라미터로 데이터를 받음
    2. **for 반복문**: 기사 목록을 하나씩 처리
    3. **st.expander**: 클릭하면 펼쳐지는 UI (깔끔!)
    4. **조건부 표시**: `if article.pub_date:`로 있을 때만
    5. **마크다운 링크**: `[텍스트](URL)` 형식
    """)

with tab4:
    st.markdown("""
    ### show_loading() 함수

    **역할**: 로딩 중임을 사용자에게 알려주는 스피너
    """)

    st.code('''
def show_loading(message: str = "처리 중입니다..."):
    """
    로딩 스피너를 표시합니다.
    Context Manager로 'with' 문과 함께 사용합니다.

    사용 예시:
    with show_loading("데이터를 가져오는 중..."):
        data = fetch_data()  # 시간이 걸리는 작업
    """
    return st.spinner(message)
    ''', language="python")

    st.markdown("""
    ### 💡 핵심 포인트

    1. **Context Manager**: `with` 문과 함께 사용
    2. **기본값**: `message: str = "처리 중입니다..."`
    3. **래핑 함수**: `st.spinner`를 감싸서 일관된 인터페이스 제공

    ### 사용 예시

    ```python
    with show_loading("뉴스를 검색하고 있습니다..."):
        articles = search_news(keyword)  # API 호출

    # 로딩 스피너가 자동으로 사라지고 결과 표시
    render_news_list(articles)
    ```
    """)

st.divider()

# ============================================
# ✏️ 가이드 실습
# ============================================

st.header("✏️ 가이드 실습: 카드 컴포넌트 만들기")

st.markdown("""
### 목표
정보를 카드 형태로 보여주는 재사용 가능한 컴포넌트 만들기

### 힌트
- 함수로 UI 분리
- 파라미터로 데이터 받기
- for 문으로 여러 개 표시
""")

st.subheader("🎯 실습 영역")

# 샘플 데이터
@dataclass
class Product:
    name: str
    price: int
    description: str

products = [
    Product("노트북", 1500000, "고성능 노트북"),
    Product("키보드", 150000, "기계식 키보드"),
    Product("마우스", 80000, "무선 마우스"),
]

# ============================================
# TODO 1: render_product_card() 함수 정의
# 파라미터: product (Product 타입)
# - st.expander로 상품명 표시
# - 내부에 가격과 설명 표시
# ============================================

# >>> 정답 <<<
# def render_product_card(product: Product):
#     """상품 카드를 렌더링합니다."""
#     with st.expander(f"📦 {product.name}"):
#         st.write(f"💰 가격: {product.price:,}원")
#         st.write(f"📝 {product.description}")

# 정답 실행
def render_product_card(product: Product):
    """상품 카드를 렌더링합니다."""
    with st.expander(f"📦 {product.name}"):
        st.write(f"💰 가격: {product.price:,}원")
        st.write(f"📝 {product.description}")

# ============================================
# TODO 2: render_product_list() 함수 정의
# 파라미터: products (List[Product] 타입)
# - 상품 개수 표시
# - for 문으로 각 상품에 render_product_card() 호출
# ============================================

# >>> 정답 <<<
# def render_product_list(products: List[Product]):
#     """상품 목록을 렌더링합니다."""
#     st.subheader(f"🛍️ 상품 목록 ({len(products)}개)")
#     for product in products:
#         render_product_card(product)

# 정답 실행
def render_product_list(products: List[Product]):
    """상품 목록을 렌더링합니다."""
    st.subheader(f"🛍️ 상품 목록 ({len(products)}개)")
    for product in products:
        render_product_card(product)

# ============================================
# TODO 3: 함수 호출하여 화면에 표시
# ============================================

# >>> 정답 <<<
# render_product_list(products)

# 정답 실행
render_product_list(products)

st.markdown("""
### 💡 실습 해설

**TODO 1**: 컴포넌트 함수는 **하나의 요소**를 표시합니다. 상품 카드 하나!

**TODO 2**: 리스트 렌더링 함수는 **반복문**으로 개별 컴포넌트를 호출합니다.

**TODO 3**: 메인 코드에서는 함수를 **호출만** 하면 됩니다. 깔끔!
""")

st.divider()

# ============================================
# 🏆 챌린지
# ============================================

st.header("🏆 챌린지: 뉴스 앱 컴포넌트")

st.markdown("""
### 목표
TrendTracker와 유사한 구조로 미니 뉴스 앱의 컴포넌트들을 만들기

⚠️ **정답이 제공되지 않습니다.** 강사와 함께 풀어보세요!
""")

st.subheader("🎯 챌린지 영역")

st.code('''
# ============================================
# 🏆 챌린지: 뉴스 앱 컴포넌트
# ============================================
# ⚠️ 정답이 제공되지 않습니다.

from dataclasses import dataclass
from typing import Optional, List

@dataclass
class News:
    title: str
    summary: str
    date: str
    url: str

# 샘플 데이터
sample_news = [
    News("AI 기술 발전", "최신 AI 기술이...", "2024-01-15", "https://..."),
    News("경제 전망", "올해 경제는...", "2024-01-14", "https://..."),
]

# TODO 1: render_search_box() 함수 만들기
# - 검색어 입력창과 버튼
# - 검색어 반환 (Optional[str])
# 힌트: phase_5_basic.py의 실습 참고


# TODO 2: render_news_card(news: News) 함수 만들기
# - expander로 제목 표시
# - 내부에 날짜, 요약, 링크 표시


# TODO 3: render_news_feed(news_list: List[News]) 함수 만들기
# - 전체 개수 표시
# - for 문으로 render_news_card 호출


# TODO 4: render_sidebar_filters() 함수 만들기
# - 카테고리 선택 (st.sidebar.selectbox)
# - 날짜 범위 선택 (st.sidebar.date_input)
# - 선택값들을 딕셔너리로 반환


# TODO 5: (심화) 메인 로직 작성
# keyword = render_search_box()
# filters = render_sidebar_filters()
# if keyword:
#     filtered_news = filter_news(sample_news, keyword, filters)
#     render_news_feed(filtered_news)

''', language="python")

st.divider()

# ============================================
# 📋 정리
# ============================================

st.header("📋 정리")

st.markdown("""
### 이번 파일에서 배운 것

| 개념 | 설명 |
|------|------|
| 함수로 UI 분리 | 재사용성, 가독성, 유지보수성 향상 |
| 컴포넌트 함수 패턴 | render_xxx() 형태로 명명 |
| 반환값 활용 | 사용자 입력을 반환하여 메인에서 사용 |
| 프로젝트 구조 | components/ 폴더에 UI 함수 분리 |

### 핵심 패턴

```python
# 컴포넌트 함수 정의
def render_component(data: DataType) -> Optional[str]:
    \"\"\"컴포넌트 설명\"\"\"
    st.subheader("제목")
    user_input = st.text_input("입력")
    if st.button("확인"):
        return user_input
    return None

# 메인에서 사용
result = render_component(data)
if result:
    process(result)
```

### TrendTracker 컴포넌트 구조

```
components/
├── search_form.py      → render_search_form()
├── sidebar.py          → render_sidebar_header()
│                        → render_settings()
│                        → render_history_list()
│                        → render_download_button()
├── result_section.py   → render_summary()
│                        → render_news_list()
└── loading.py          → show_loading()
```

### ✅ 체크리스트
- [ ] UI를 함수로 분리하는 이유를 이해했다
- [ ] render_xxx() 패턴으로 컴포넌트를 만들 수 있다
- [ ] 반환값을 활용하여 입력을 처리할 수 있다
- [ ] 프로젝트의 components/ 구조를 이해했다
- [ ] 챌린지를 강사와 함께 풀어봤다

---

## 🎉 Phase 5 완료!

이제 Streamlit으로 웹 UI를 만들 수 있습니다.

**다음 Phase에서는:**
- Phase 6: 모든 컴포넌트를 조합하여 완성된 앱 만들기
- 상태 관리로 데이터 흐름 제어
- main.py 통합
""")
