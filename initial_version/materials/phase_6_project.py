"""
# ============================================
# Phase 6-3: 실제 app.py 분석
# ============================================
#
# 🎯 이 파일에서 배울 것:
# - TrendTracker의 app.py 전체 구조
# - 각 부분의 역할과 연결
# - 컴포넌트 통합 패턴
# - 실제 앱 완성 과정
#
# 📋 실행 방법:
# streamlit run materials/phase_6_project.py
# ============================================
"""

import streamlit as st
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime

st.set_page_config(page_title="Phase 6-3: 프로젝트 분석", page_icon="🔎", layout="wide")

st.title("🔎 Phase 6-3: 실제 app.py 분석")

# ============================================
# 📚 이론: 전체 구조 개요
# ============================================

st.header("1️⃣ app.py 전체 구조")

st.markdown("""
## TrendTracker의 app.py

```
app.py
├── 1. import 모음
├── 2. main() 함수
│   ├── 2-1. 페이지 설정
│   ├── 2-2. 초기화 (설정, 리포지토리)
│   ├── 2-3. 세션 상태 초기화
│   ├── 2-4. 사이드바 렌더링
│   ├── 2-5. 메인 영역 (검색 폼)
│   ├── 2-6. 검색 처리 (API 호출)
│   └── 2-7. 결과 표시
└── 3. 진입점 (if __name__ == "__main__")
```

### 전체 흐름

```
[앱 시작]
    ↓
[페이지 설정 + 초기화]
    ↓
[사이드바 렌더링] ←──────────────────┐
    ↓                               │
[메인 영역 렌더링]                    │
    ↓                               │
[사용자 액션 감지] ───→ [검색 버튼 클릭?] → [새 검색 수행]
    │                                   ↓
    └───→ [기록 선택?] ─────────────→ [기록 조회]
                                        ↓
                                   [결과 표시]
```
""")

st.divider()

# ============================================
# 🔎 코드 분석: import 부분
# ============================================

st.header("2️⃣ import 분석")

with st.expander("📂 import 코드 보기", expanded=True):
    st.code('''
# 표준 라이브러리
from datetime import datetime

# 외부 패키지
import streamlit as st

# 설정
from config.settings import Settings

# 서비스 (API 호출)
from services.search_service import search_news
from services.ai_service import summarize_news

# 도메인 (데이터 구조)
from domain.search_result import SearchResult

# 리포지토리 (데이터 저장)
from repositories.search_repository import SearchRepository

# 유틸리티
from utils.exceptions import AppError
from utils.error_handler import handle_error
from utils.key_generator import generate_search_key

# UI 컴포넌트
from components.search_form import render_search_form
from components.sidebar import (
    render_sidebar_header,
    render_settings,
    render_info,
    render_history_list,
    render_download_button
)
from components.result_section import render_summary, render_news_list
from components.loading import show_loading
    ''', language="python")

st.markdown("""
### 💡 분석 포인트

| 분류 | 역할 | 파일 |
|------|------|------|
| **설정** | 환경변수, API 키 | `config/settings.py` |
| **서비스** | 외부 API 호출 | `services/` |
| **도메인** | 데이터 구조 정의 | `domain/` |
| **리포지토리** | 데이터 저장/조회 | `repositories/` |
| **컴포넌트** | UI 렌더링 | `components/` |
| **유틸리티** | 공통 기능 | `utils/` |

→ **계층 분리**: 각 폴더가 하나의 역할만 담당!
""")

st.divider()

# ============================================
# 🔎 코드 분석: 초기화 부분
# ============================================

st.header("3️⃣ 초기화 분석")

with st.expander("📂 초기화 코드 보기", expanded=True):
    st.code('''
def main():
    # 1. 페이지 설정 (항상 첫 번째!)
    st.set_page_config(
        page_title="TrendTracker - AI 뉴스 트렌드 분석기",
        page_icon="🚀",
        layout="wide"
    )

    # 2. 설정 및 리포지토리 초기화
    try:
        settings = Settings()  # 환경변수 로드
    except ValueError as e:
        st.error(str(e))  # API 키 없으면 에러
        st.stop()  # 앱 중단

    repository = SearchRepository(settings.CSV_PATH)

    # 3. 세션 상태 초기화
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "new_search"
    if "selected_key" not in st.session_state:
        st.session_state.selected_key = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    ''', language="python")

st.markdown("""
### 💡 분석 포인트

**페이지 설정**
- `page_title`: 브라우저 탭 제목
- `page_icon`: 탭 아이콘 (이모지 또는 이미지)
- `layout="wide"`: 넓은 레이아웃 사용

**설정 로드**
- `Settings()`: 환경변수에서 API 키 등을 로드
- 실패 시 `st.stop()`으로 앱 중단 (크래시 방지)

**세션 상태**
- `current_mode`: 현재 모드 (new_search / history)
- `selected_key`: 선택된 기록의 키
- `last_result`: 마지막 검색 결과
""")

st.divider()

# ============================================
# 🔎 코드 분석: 사이드바
# ============================================

st.header("4️⃣ 사이드바 분석")

with st.expander("📂 사이드바 코드 보기", expanded=True):
    st.code('''
    # 4. 사이드바 영역
    render_sidebar_header()          # 제목, 소개
    num_results = render_settings()  # 설정 (슬라이더)
    render_info()                    # 사용법, API 한도

    st.sidebar.divider()  # 구분선

    # 검색 기록 목록 가져오기
    search_keys = repository.get_all_keys()
    selected_stored_key = render_history_list(search_keys)

    # 과거 기록 선택 시 모드 변경
    if selected_stored_key:
        st.session_state.current_mode = "history"
        st.session_state.selected_key = selected_stored_key
        st.session_state.last_result = None

    st.sidebar.divider()

    # CSV 다운로드 버튼
    csv_data = repository.get_all_as_csv()
    render_download_button(csv_data, len(search_keys) == 0)
    ''', language="python")

st.markdown("""
### 💡 분석 포인트

**컴포넌트 조합**
```
사이드바
├── render_sidebar_header()    → 제목, 소개
├── render_settings()          → 슬라이더 (반환값 사용!)
├── render_info()              → 사용법 expander
├── ─── 구분선 ───
├── render_history_list()      → 기록 selectbox (반환값 사용!)
├── ─── 구분선 ───
└── render_download_button()   → 다운로드 버튼
```

**모드 전환 트리거**
- `render_history_list()`가 선택된 키를 반환
- 반환값이 있으면 → `history` 모드로 전환
""")

st.divider()

# ============================================
# 🔎 코드 분석: 검색 처리
# ============================================

st.header("5️⃣ 검색 처리 분석")

with st.expander("📂 검색 처리 코드 보기", expanded=True):
    st.code('''
    # 5. 메인 영역
    st.title("🚀 TrendTracker")
    st.markdown("최신 뉴스를 검색하고 AI로 핵심 내용을 요약해드립니다.")

    # 5-1. 검색 폼 렌더링
    keyword = render_search_form()

    # 5-2. 새로운 검색 처리
    if keyword:
        st.session_state.current_mode = "new_search"
        st.session_state.selected_key = None

        try:
            # 뉴스 검색 (API 호출)
            with show_loading(f"🔍 '{keyword}' 관련 최신 뉴스를 검색하고 있습니다..."):
                articles = search_news(keyword, num_results)

            if not articles:
                st.info(f"'{keyword}'에 대한 검색 결과가 없습니다.")
                return

            # AI 요약 (API 호출)
            with show_loading("🤖 AI가 뉴스를 읽고 핵심 내용을 요약하고 있습니다..."):
                summary = summarize_news(articles)

            # 결과 객체 생성
            search_key = generate_search_key(keyword)
            result = SearchResult(
                search_key=search_key,
                search_time=datetime.now(),
                keyword=keyword,
                articles=articles,
                ai_summary=summary
            )

            # CSV 저장
            with show_loading("💾 검색 결과를 저장하고 있습니다..."):
                repository.save(result)

            st.success(f"'{keyword}' 검색 완료! {len(articles)}건의 뉴스를 분석했습니다.")
            st.session_state.last_result = result

        except AppError as e:
            handle_error(e.error_type)  # 사용자 친화적 에러 메시지
        except Exception as e:
            st.error(f"알 수 없는 오류가 발생했습니다: {e}")
    ''', language="python")

st.markdown("""
### 💡 분석 포인트

**검색 흐름**
```
keyword 입력
    ↓
search_news(keyword) → articles
    ↓
summarize_news(articles) → summary
    ↓
SearchResult 객체 생성
    ↓
repository.save(result) → CSV 저장
    ↓
session_state.last_result = result
```

**로딩 표시**
- `with show_loading("메시지"):` 패턴
- 사용자가 진행 상황을 알 수 있음

**에러 처리**
- `AppError`: 예상된 에러 (API 키, 네트워크 등)
- `Exception`: 예상치 못한 에러
- 앱이 크래시하지 않도록 보호
""")

st.divider()

# ============================================
# 🔎 코드 분석: 결과 표시
# ============================================

st.header("6️⃣ 결과 표시 분석")

with st.expander("📂 결과 표시 코드 보기", expanded=True):
    st.code('''
    # 6. 결과 표시 로직
    if st.session_state.current_mode == "new_search" and st.session_state.last_result:
        # 새 검색 결과 표시
        res = st.session_state.last_result
        render_summary(res.keyword, res.ai_summary)
        render_news_list(res.articles)

    elif st.session_state.current_mode == "history" and st.session_state.selected_key:
        # 기록 조회 결과 표시
        history_result = repository.find_by_key(st.session_state.selected_key)
        if history_result:
            render_summary(history_result.keyword, history_result.ai_summary)
            render_news_list(history_result.articles)
        else:
            st.error("선택한 기록을 불러올 수 없습니다.")

    # 첫 실행 및 빈 상태 안내
    elif not keyword and not search_keys:
        st.info("💡 아직 검색 기록이 없습니다. 키워드를 입력해보세요!")
    ''', language="python")

st.markdown("""
### 💡 분석 포인트

**모드에 따른 분기**

| 조건 | 결과 |
|------|------|
| `new_search` + `last_result` 있음 | 새 검색 결과 표시 |
| `history` + `selected_key` 있음 | 기록 조회 결과 표시 |
| 그 외 (첫 실행) | 안내 메시지 표시 |

**결과 표시 컴포넌트**
- `render_summary(keyword, summary)`: AI 요약 박스
- `render_news_list(articles)`: 뉴스 목록 (expander)

**데이터 출처**
- 새 검색: `st.session_state.last_result`
- 기록 조회: `repository.find_by_key()`
""")

st.divider()

# ============================================
# 📊 전체 흐름 다이어그램
# ============================================

st.header("7️⃣ 전체 흐름 다이어그램")

st.markdown("""
```
┌─────────────────────────────────────────────────────────────┐
│                        app.py                                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐                                           │
│  │   Settings   │ ← 환경변수 (.env)                          │
│  └──────┬───────┘                                           │
│         ↓                                                    │
│  ┌──────────────┐                                           │
│  │  Repository  │ ← CSV 파일 (data/)                         │
│  └──────┬───────┘                                           │
│         ↓                                                    │
│  ┌──────────────────────────────────────────────────┐       │
│  │                   사이드바                         │       │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │       │
│  │  │   Header    │ │  Settings   │ │    Info     │ │       │
│  │  └─────────────┘ └──────┬──────┘ └─────────────┘ │       │
│  │                         ↓ num_results             │       │
│  │  ┌─────────────┐ ┌─────────────┐                 │       │
│  │  │   History   │ │  Download   │                 │       │
│  │  └──────┬──────┘ └─────────────┘                 │       │
│  │         ↓ selected_key                            │       │
│  └─────────┼────────────────────────────────────────┘       │
│            ↓                                                 │
│  ┌──────────────────────────────────────────────────┐       │
│  │                   메인 영역                        │       │
│  │  ┌─────────────────────────────────────────────┐ │       │
│  │  │              render_search_form()           │ │       │
│  │  └────────────────────┬────────────────────────┘ │       │
│  │                       ↓ keyword                   │       │
│  │  ┌─────────────────────────────────────────────┐ │       │
│  │  │  search_news() → summarize_news() → save()  │ │       │
│  │  └────────────────────┬────────────────────────┘ │       │
│  │                       ↓                          │       │
│  │  ┌─────────────────────────────────────────────┐ │       │
│  │  │  render_summary() + render_news_list()      │ │       │
│  │  └─────────────────────────────────────────────┘ │       │
│  └──────────────────────────────────────────────────┘       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```
""")

st.divider()

# ============================================
# ✏️ 가이드 실습
# ============================================

st.header("✏️ 가이드 실습: 미니 앱 통합")

st.markdown("""
### 목표
배운 패턴을 적용하여 미니 뉴스 앱을 완성하기

### 요구사항
- 검색 폼 컴포넌트
- 결과 표시 컴포넌트
- 세션 상태로 결과 저장
- 에러 처리
""")

st.subheader("🎯 실습 영역")

# 샘플 데이터
@dataclass
class Article:
    title: str
    snippet: str

def fake_search(keyword: str) -> List[Article]:
    """가상의 검색 함수"""
    if keyword.lower() == "error":
        raise ValueError("검색 중 오류 발생!")
    return [
        Article(f"{keyword} 관련 뉴스 1", "첫 번째 기사 내용..."),
        Article(f"{keyword} 관련 뉴스 2", "두 번째 기사 내용..."),
        Article(f"{keyword} 관련 뉴스 3", "세 번째 기사 내용..."),
    ]

# ============================================
# TODO 1: 세션 상태 초기화
# - search_results: Optional[List[Article]] = None
# - last_keyword: Optional[str] = None
# ============================================

# >>> 정답 <<<
# if "search_results" not in st.session_state:
#     st.session_state.search_results = None
# if "last_keyword" not in st.session_state:
#     st.session_state.last_keyword = None

# 정답 실행
if "search_results" not in st.session_state:
    st.session_state.search_results = None
if "last_keyword" not in st.session_state:
    st.session_state.last_keyword = None

# ============================================
# TODO 2: render_mini_search_form() 함수
# - 검색어 입력
# - 검색 버튼
# - 반환: 검색어 또는 None
# ============================================

# >>> 정답 <<<
# def render_mini_search_form() -> Optional[str]:
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         keyword = st.text_input("검색어", placeholder="키워드 입력", key="mini_keyword")
#     with col2:
#         st.write("")  # 정렬용
#         clicked = st.button("🔍 검색", use_container_width=True, key="mini_search")
#     if clicked and keyword:
#         return keyword
#     return None

# 정답 실행
def render_mini_search_form() -> Optional[str]:
    col1, col2 = st.columns([4, 1])
    with col1:
        keyword = st.text_input("검색어", placeholder="키워드 입력", key="mini_keyword")
    with col2:
        st.write("")
        clicked = st.button("🔍 검색", use_container_width=True, key="mini_search")
    if clicked and keyword:
        return keyword
    return None

# ============================================
# TODO 3: render_mini_results() 함수
# - 제목과 기사 목록 표시
# - expander로 각 기사 표시
# ============================================

# >>> 정답 <<<
# def render_mini_results(keyword: str, articles: List[Article]):
#     st.subheader(f"📰 '{keyword}' 검색 결과")
#     for article in articles:
#         with st.expander(article.title):
#             st.write(article.snippet)

# 정답 실행
def render_mini_results(keyword: str, articles: List[Article]):
    st.subheader(f"📰 '{keyword}' 검색 결과")
    for article in articles:
        with st.expander(article.title):
            st.write(article.snippet)

# ============================================
# TODO 4: 메인 로직
# - 검색 폼 호출
# - 검색 시 fake_search() 호출 (에러 처리)
# - 결과를 세션에 저장
# - 결과 표시
# ============================================

# >>> 정답 <<<
# keyword = render_mini_search_form()
# if keyword:
#     try:
#         with st.spinner("검색 중..."):
#             results = fake_search(keyword)
#         st.session_state.search_results = results
#         st.session_state.last_keyword = keyword
#         st.success(f"{len(results)}건의 결과를 찾았습니다!")
#     except ValueError as e:
#         st.error(f"❌ {e}")
#
# if st.session_state.search_results and st.session_state.last_keyword:
#     render_mini_results(st.session_state.last_keyword, st.session_state.search_results)

# 정답 실행
st.markdown("---")
keyword = render_mini_search_form()

if keyword:
    try:
        with st.spinner("검색 중..."):
            import time
            time.sleep(0.5)  # 로딩 시뮬레이션
            results = fake_search(keyword)
        st.session_state.search_results = results
        st.session_state.last_keyword = keyword
        st.success(f"{len(results)}건의 결과를 찾았습니다!")
    except ValueError as e:
        st.error(f"❌ {e}")
        st.info("💡 'error'를 입력하면 에러가 발생합니다. 다른 키워드로 시도해보세요.")

if st.session_state.search_results and st.session_state.last_keyword:
    render_mini_results(st.session_state.last_keyword, st.session_state.search_results)

st.markdown("""
### 💡 실습 해설

**TODO 1**: 세션 상태로 검색 결과를 저장하면 새로고침해도 유지됩니다.

**TODO 2**: 검색 폼 컴포넌트는 입력값을 반환합니다.

**TODO 3**: 결과 표시 컴포넌트는 데이터를 받아서 렌더링합니다.

**TODO 4**: 메인 로직에서 컴포넌트들을 조합하고, 에러를 처리합니다.
""")

st.divider()

# ============================================
# 🏆 챌린지
# ============================================

st.header("🏆 챌린지: 완전한 앱 만들기")

st.markdown("""
### 목표
TrendTracker와 유사한 구조로 완전한 미니 앱 만들기

⚠️ **정답이 제공되지 않습니다.** 강사와 함께 풀어보세요!
""")

st.subheader("🎯 챌린지 영역")

st.code('''
# ============================================
# 🏆 챌린지: 완전한 미니 앱
# ============================================
# ⚠️ 정답이 제공되지 않습니다.

import streamlit as st
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime

# 데이터 클래스
@dataclass
class SearchResult:
    keyword: str
    articles: List[str]
    timestamp: datetime

# TODO 1: 세션 상태 초기화 함수
# - results_history: List[SearchResult] = []
# - current_mode: "search" | "history"
# - selected_result: Optional[SearchResult] = None


# TODO 2: render_sidebar() 함수
# - 앱 제목
# - 검색 기록 목록 (selectbox)
# - 선택 시 모드 전환


# TODO 3: render_search_section() 함수
# - 검색 폼
# - 검색 결과 처리
# - 기록 저장


# TODO 4: render_history_section() 함수
# - 선택된 기록 표시
# - "검색으로 돌아가기" 버튼


# TODO 5: main() 함수
# - 페이지 설정
# - 초기화
# - 사이드바 렌더링
# - 모드에 따른 화면 렌더링


# TODO 6: (심화) 기록 삭제 기능


# TODO 7: (심화) 검색 결과 내보내기 (JSON)


if __name__ == "__main__":
    main()
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
| app.py 구조 | import → main() → 진입점 |
| 초기화 | 설정 로드, 리포지토리, 세션 상태 |
| 사이드바 | 설정과 기록을 한 곳에 |
| 검색 처리 | API 호출 → 결과 저장 → 표시 |
| 결과 표시 | 모드에 따라 다른 데이터 출처 |

### TrendTracker 컴포넌트 통합 패턴

```python
def main():
    # 1. 설정
    st.set_page_config(...)
    settings = Settings()
    repository = SearchRepository(...)

    # 2. 세션 초기화
    if "mode" not in st.session_state:
        st.session_state.mode = "default"

    # 3. 사이드바
    render_sidebar_header()
    value = render_settings()
    selected = render_history_list(...)

    # 4. 모드 전환
    if selected:
        st.session_state.mode = "history"

    # 5. 메인 영역
    keyword = render_search_form()
    if keyword:
        try:
            result = process(keyword)
            st.session_state.last_result = result
        except AppError as e:
            handle_error(e)

    # 6. 결과 표시
    if st.session_state.mode == "new":
        render_result(st.session_state.last_result)
    elif st.session_state.mode == "history":
        render_result(repository.find(...))
```

### ✅ 체크리스트
- [ ] app.py의 전체 구조를 이해했다
- [ ] 각 부분의 역할을 알고 있다
- [ ] 컴포넌트 통합 패턴을 이해했다
- [ ] 에러 처리 방법을 안다
- [ ] 챌린지를 강사와 함께 풀어봤다

---

## 🎉 Phase 6 완료!

이제 모든 조각을 하나로 통합하는 방법을 알게 되었습니다.

**다음 Phase에서는:**
- Phase 7: 에러 핸들링과 마무리
- 사용자 친화적 에러 메시지
- 문서화 (README)
""")
