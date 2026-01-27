# TrendTracker 학습 가이드

이 문서는 TrendTracker 프로젝트를 7단계 프롬프트 순서에 따라 이해하기 위한 학습 가이드입니다. 각 Phase별로 **프롬프트 역할**, **학습 목표**, **이해를 위한 핵심 개념**, **주요 코드**, **데이터 흐름**을 설명합니다.

---

# 목차

1. [Phase 1: 프로젝트 초기화 및 환경 설정](#phase-1-프로젝트-초기화-및-환경-설정)
2. [Phase 2: 도메인 모델 및 유틸리티 함수](#phase-2-도메인-모델-및-유틸리티-함수)
3. [Phase 3: 서비스 레이어 - API 연동](#phase-3-서비스-레이어---api-연동)
4. [Phase 4: 리포지토리 레이어 - 데이터 관리](#phase-4-리포지토리-레이어---데이터-관리)
5. [Phase 5: UI 컴포넌트](#phase-5-ui-컴포넌트)
6. [Phase 6: 메인 앱 통합](#phase-6-메인-앱-통합)
7. [Phase 7: 에러 핸들링 강화 및 마무리](#phase-7-에러-핸들링-강화-및-마무리기)
8. [전체 데이터 흐름 및 구조](#전체-데이터-흐름-및-구조)

---

# Phase 1: 프로젝트 초기화 및 환경 설정

## 이 프롬프트의 역할
- 프로젝트의 기본 뼈대를 구성하고 패키지 관리자(`uv`)를 통해 개발 환경을 구축합니다.
- API 키와 같은 민감한 정보를 안전하게 관리하기 위한 환경 설정 로더를 생성합니다.

**생성된 파일 목록:**
- `.env.example`: 환경변수 템플릿
- `config/settings.py`: 환경 설정 로드 클래스

## 학습 목표
- `uv`를 사용한 파이썬 가상환경 및 패키지 관리 방법을 익힙니다.
- 환경변수(`.env`)의 필요성과 `python-dotenv` 사용법을 이해합니다.
- 프로젝트 계층 구조(Layered Architecture)의 기초를 다집니다.

## 이해를 위한 핵심 개념

### 1.1 패키지 관리자 (uv)
`uv`는 Rust로 작성된 매우 빠른 파이썬 패키지 관리자입니다. `pip`보다 훨씬 빠르며 가상환경 생성, 패키지 설치, 의존성 잠금(`uv.lock`) 기능을 통합하여 제공합니다.

### 1.2 환경변수와 Settings 클래스
API 키나 파일 경로 같이 실행 환경에 따라 변하는 설정값은 코드에 직접 쓰는 대신 환경변수로 관리합니다. `Settings` 클래스는 이를 중앙에서 관리하고, 필수 값이 누락되었을 때 친절한 에러 메시지를 제공하여 안정성을 높입니다.

## 주요 코드 인용

### config/settings.py - 환경 설정 로더
```python
# config/settings.py:11-40
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
...
"""
            raise ValueError(error_msg)
```

**코드 설명:**
- `required_vars`: 앱 실행에 꼭 필요한 환경변수들을 정의합니다.
- `missing_vars`: `.env` 파일에 설정되지 않은 변수들을 체크하여 사용자에게 알립니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 1 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│  [.env 파일] → [load_dotenv] → [Settings 객체]
│                                     │
└─────────────────────────────────────┘
```

---

# Phase 2: 도메인 모델 및 유틸리티 함수

## 이 프롬프트의 역할
- 비즈니스 로직에서 공통으로 사용될 데이터 구조(도메인 모델)를 정의합니다.
- 키 생성, 입력 전처리, 에러 메시지 관리 등 반복되는 유틸리티 기능을 구현합니다.

**생성된 파일 목록:**
- `domain/news_article.py`: 뉴스 기사 모델
- `domain/search_result.py`: 검색 결과 모델
- `utils/key_generator.py`: 검색 키 생성기
- `utils/input_handler.py`: 입력 전처리
- `utils/error_handler.py`: 에러 메시지 통합 관리

## 학습 목표
- `dataclass`를 사용하여 구조화된 데이터를 정의하는 방법을 배웁니다.
- `Optional`, `List` 등 타입 힌트를 활용하여 코드 안정성을 높이는 방법을 이해합니다.
- 관심사 분리(Separation of Concerns)를 위해 유틸리티 코드를 분리하는 이유를 학습합니다.

## 이해를 위한 핵심 개념

### 2.1 도메인 모델 (Entity)
도메인 모델은 프로그램이 해결하려는 핵심 데이터의 형태입니다. 뉴스 기사(`NewsArticle`)나 검색 결과(`SearchResult`)와 같이 실제 "사물"이나 "개념"을 코드로 표현한 것입니다.

### 2.2 Dataclass와 타입 힌트
`@dataclass`는 데이터를 저장하기 위한 클래스를 아주 간단하게 만들어줍니다. 타입 힌트(`keyword: str`)는 어떤 종류의 데이터가 들어가야 하는지 개발자와 도구(IDE)에게 알려주어 실수를 방지합니다.

## 주요 코드 인용

### domain/search_result.py - 데이터 변환 로직
```python
# domain/search_result.py:16-33
    def to_dataframe(self) -> pd.DataFrame:
        """
        검색 결과를 Pandas DataFrame으로 변환합니다.
        기사 1건이 1행이 되는 Long format으로 변환합니다.
        """
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

**코드 설명:**
- `to_dataframe`: 복잡한 객체 리스트를 엑셀 형식과 유사한 Pandas DataFrame으로 펼쳐서 저장하기 쉽게 만듭니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 2 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│  [사용자 입력] → [preprocess_keyword] → [SearchResult 객체]
│                                     │
└─────────────────────────────────────┘
```

---

# Phase 3: 서비스 레이어 - API 연동

## 이 프롬프트의 역할
- 외부 세상(Tavily API, Gemini API)과 통신하여 데이터를 가져오는 핵심 비즈니스 로직을 구현합니다.
- API 응답을 도메인 모델(`NewsArticle`)로 변환합니다.

**생성된 파일 목록:**
- `services/search_service.py`: Tavily 뉴스 검색 서비스
- `services/ai_service.py`: Gemini AI 요약 서비스
- `utils/exceptions.py`: 커스텀 예외 클래스

## 학습 목표
- 외부 API(HTTP 통신)를 호출하고 응답을 받는 과정을 이해합니다.
- 검색 엔진(Tavily)과 LLM(Gemini) SDK 사용법을 익힙니다.
- API 호출 중 발생할 수 있는 오류를 `AppError`로 통합하여 제어하는 방법을 배웁니다.

## 이해를 위한 핵심 개념

### 3.1 서비스 레이어 (Service Layer)
사용자의 요청을 받아 실제로 뉴스 검색을 하거나 요약을 수행하는 "작업자" 역할을 합니다. 데이터의 원천(API)과 UI를 연결하는 징검다리입니다.

### 3.2 최신순 정렬 및 고급 검색
최신 정보를 제공하기 위해 Tavily의 `advanced` 검색 기능을 사용하고, 가져온 결과 중 날짜 정보가 있는 기사들을 우선적으로 최신순 정렬하는 수동 처리 로직이 포함됩니다.

## 주요 코드 인용

### services/search_service.py - 최신 뉴스 검색 로직
```python
# services/search_service.py:28-48
        fetch_count = max(num_results * 3, 20)
        
        response = client.search(
            query=keyword,
            search_depth="advanced",
            include_domains=settings.SEARCH_DOMAINS,
            max_results=fetch_count,
            topic="news"
        )
        
        results = response.get('results', [])
        
        def get_date(x):
            d = x.get('published_date')
            return str(d) if d else ""

        results.sort(key=get_date, reverse=True)
        results = results[:num_results]
```

**코드 설명:**
- `max_results`: 충분한 기사 후보군을 확보하기 위해 요청보다 많은 양을 가져옵니다.
- `search_depth="advanced"`: 더 정확한 날짜 메타데이터를 확보합니다.
- `sort`: 발행일(`published_date`) 기준 내림차순으로 정렬하여 사용자에게 가장 최신 정보를 제공합니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 3 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│  [키워드] → [Tavily API] → [정렬/가공] → [NewsArticle 목록]
│  [NewsArticle] → [Gemini API] → [AI 요약 텍스트]
│                                     │
└─────────────────────────────────────┘
```

---

# Phase 4: 리포지토리 레이어 - 데이터 관리

## 이 프롬프트의 역할
- 검색 결과와 AI 요약을 로컬 CSV 파일에 영구적으로 기록하고 불러오는 기능을 담당합니다.
- 과거 검색 목록을 확인하거나 특정 기록을 조회하는 인터페이스를 제공합니다.

**생성된 파일 목록:**
- `repositories/search_repository.py`: CSV 데이터 접근 리포지토리

## 학습 목표
- Pandas를 사용하여 CSV 파일을 읽고 쓰는 실무 중심 코딩 패턴을 익힙니다.
- 리포지토리 패턴(Repository Pattern)을 통해 데이터 저장 방식을 추상화하는 이유를 배웁니다.
- 로컬 파일 시스템(`os.makedirs`)을 안전하게 다루는 방법을 학습합니다.

## 이해를 위한 핵심 개념

### 4.1 리포지토리 패턴 (Repository Pattern)
데이터 저장소(DB, CSV 파일 등)가 어디에 있든, 프로그램의 다른 부분은 "데이터를 저장해줘" 혹은 "데이터를 찾아줘"라고만 요청하면 되도록 감싸는 패턴입니다. 나중에 CSV 대신 DB로 바꿔도 다른 코드를 수정할 필요가 없게 해줍니다.

### 4.2 중복 제거와 정렬
저장된 CSV는 기사 단위로 기록되어 있으므로, 검색 기록 목록(`get_all_keys`)을 만들 때는 중복된 키를 제거하고 최신 시간순으로 보여주는 처리가 필요합니다.

## 주요 코드 인용

### repositories/search_repository.py - 데이터 로드 및 정렬
```python
# repositories/search_repository.py:57-67
    def get_all_keys(self) -> List[str]:
        """모든 유니크한 search_key 리스트를 최신순으로 정렬하여 반환합니다."""
        df = self.load()
        if df.empty:
            return []
        
        # search_time 기준 내림차순 정렬 후 고유값 추출 (순서 유지)
        df_sorted = df.sort_values(by="search_time", ascending=False)
        keys = df_sorted["search_key"].drop_duplicates().tolist()
        return keys
```

**코드 설명:**
- `drop_duplicates`: 여러 행으로 저장된 동일한 검색 키를 하나로 합쳐 목록을 만듭니다.
- `sort_values`: 가장 최근에 검색한 내용이 목록 상단에 오도록 합니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 4 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│  [SearchResult] → [to_dataframe] → [CSV 파일 저장]
│  [CSV 파일] → [filter by key] → [SearchResult 객체 복원]
│                                     │
└─────────────────────────────────────┘
```

---

# Phase 5: UI 컴포넌트

## 이 프롬프트의 역할
- Streamlit을 사용하여 웹 화면의 각 구성 요소를 함수 단위로 제작합니다.
- 사용자 입력 폼, 사이드바, 결과 표시 영역 등 독립적인 UI 조각을 만듭니다.

**생성된 파일 목록:**
- `components/search_form.py`: 검색 입력 UI
- `components/sidebar.py`: 각종 설정 및 기록 목록
- `components/result_section.py`: 요약 및 뉴스 리스트 카드
- `components/loading.py`: 로딩 스피너 애니메이션

## 학습 목표
- Streamlit의 레이아웃(columns, sidebar, expander) 활용법을 익힙니다.
- 사용자와 상호작용(Button, Slider, Selectbox)하는 UI 구현 방법을 배웁니다.
- 복잡한 UI 코드를 함수로 분리하여 메인 코드 가독성을 높이는 방법을 이해합니다.

## 이해를 위한 핵심 개념

### 5.1 선언적 UI (Streamlit)
Streamlit은 "버튼을 그려라", "텍스트 상자를 그려라"라고 코드를 쓰면 즉시 웹 화면에 나타나는 방식입니다. Python 코드만으로 복잡한 프런트엔드 지식 없이 웹앱을 만들 수 있게 해줍니다.

### 5.2 Context Manager (`with` 문)
로딩 상태를 보여줄 때 `with show_loading(...):` 구문을 사용하면 해당 블록 안의 작업이 끝날 때까지 자동으로 화면에 빙글빙글 도는 스피너를 보여줄 수 있습니다.

## 주요 코드 인용

### components/result_section.py - 뉴스 기사 카드 표시
```python
# components/result_section.py:21-28
    for article in articles:
        # 날짜 정보가 있으면 제목이나 본문에 표시
        date_str = f" ({article.pub_date})" if article.pub_date else ""
        with st.expander(f"📌 {article.title}{date_str}", expanded=False):
            if article.pub_date:
                st.caption(f"📅 발행일: {article.pub_date}")
            st.markdown(f"**기사 스니펫:**\n{article.snippet}")
            st.markdown(f"[🔗 기사 보기]({article.url})")
```

**코드 설명:**
- `st.expander`: 기사 제목만 보여주다가 클릭하면 상세 내용을 펼쳐볼 수 있게 하여 화면 공간을 효율적으로 사용합니다.

## 데이터 흐름에서의 역할

```
┌─────────────────────────────────────┐
│         Phase 5 데이터 흐름          │
├─────────────────────────────────────┤
│                                     │
│  [UI 상호작용] → [이벤트 발생] → [데이터 반환/표시]
│                                     │
└─────────────────────────────────────┘
```

---

# Phase 6: 메인 앱 통합

## 이 프롬프트의 역할
- 지금까지 만든 모든 조각(도메인, 서비스, 리포지토리, UI 컴포넌트)을 `app.py` 하나에 조립합니다.
- 전체적인 앱의 실행 흐름과 상태(`session_state`)를 제어합니다.

**생성된 파일 목록:**
- `app.py`: 메인 애플리케이션

## 학습 목표
- 프로그램의 전체 생명주기(Lifecycle)와 실행 순서를 이해합니다.
- `st.session_state`를 사용하여 페이지가 새로고침되어도 데이터를 유지하는 방법을 배웁니다.
- 조립식 개발(Composition)을 통해 거대한 앱을 효율적으로 조립하는 경험을 합니다.

## 이해를 위한 핵심 개념

### 6.1 세션 상태 (Session State)
Streamlit은 웹페이지를 조작할 때마다 코드 전체가 처음부터 끝까지 다시 실행됩니다. 이때 변수가 초기화되는 것을 막고, 현재 검색한 결과나 선택한 모드를 기억하기 위해 `st.session_state`라는 저장소를 사용합니다.

## 주요 코드 인용

### app.py - 검색 버튼 클릭 이벤트 처리
```python
# app.py:83-102
            with show_loading(f"🔍 '{keyword}' 관련 최신 뉴스를 검색하고 있습니다..."):
                articles = search_news(keyword, num_results)
            
            with show_loading("🤖 AI가 뉴스를 읽고 핵심 내용을 요약하고 있습니다..."):
                summary = summarize_news(articles)
            
            # 결과 객체 생성 및 저장
            result = SearchResult(
                search_key=search_key,
                search_time=datetime.now(),
                keyword=keyword,
                articles=articles,
                ai_summary=summary
            )
            repository.save(result)
            st.session_state.last_result = result
```

**코드 설명:**
- 여러 서비스를 결합하여 하나의 시나리오(검색→요약→저장)를 완성하는 통합 로직입니다.

---

# Phase 7: 에러 핸들링 강화 및 마무리

## 이 프롬프트의 역할
- 실제 사용 환경에서 발생할 수 있는 각종 예외 상황에 대비하여 견고한 앱을 만듭니다.
- 사용자에게 친절한 가이드(README)와 에러 메시지를 제공합니다.

**생성된 파일 목록:**
- `README.md`: 프로젝트 안내서

## 학습 목표
- 방어적 프로그래밍(Defensive Programming)의 중요성을 배웁니다.
- 사용자 경험(UX) 측면에서 좋은 에러 메시지가 무엇인지 고민해봅니다.
- 문서화의 가치를 이해하고 프로젝트를 완성도 있게 마무리합니다.

## 이해를 위한 핵심 개념

### 7.1 사용자 친화적 에러 핸들링
프로그램 내부의 기술적인 에러(예: `401 Unauthorized`)를 사용자에게 그대로 보여주는 것이 아니라, "API 키가 유효하지 않습니다"와 같이 사용자가 무엇을 해야 하는지 알려주는 한글 메시지로 변환합니다.

## 주요 코드 인용

### utils/error_handler.py - 에러 메시지 매핑
```python
# utils/error_handler.py:3-14
ERROR_MESSAGES = {
    "api_key_invalid": "API 키가 유효하지 않습니다. 설정을 확인해주세요.",
    "rate_limit_exceeded": "요청이 너무 많습니다. 잠시 후(약 30초~1분) 다시 시도해주세요.",
    "network_error": "네트워크 연결을 확인해주세요 (또는 검색 서버 오류).",
    "ai_error": "AI 요약 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
    # ...
}
```

**코드 설명:**
- `AppError`에 담긴 에러 타입 키값을 사람이 이해하기 쉬운 한글 문장으로 바꿔주는 사전을 관리합니다.

---

# 전체 데이터 흐름 및 구조

## 시나리오: 새로운 키워드 검색 및 요약

```
[사용자] → 키워드 입력 ("AI 트렌드")
    │
    ▼
[input_handler] → 공백 제거, 길이 제한 필터링
    │
    ▼
[search_service] → Tavily API (뉴스 검색 & 최신순 정렬)
    │
    ▼
[ai_service] → Gemini API (뉴스 스니펫 요약)
    │
    ▼
[search_repository] → CSV 파일에 결과 영구 저장
    │
    ▼
[result_section] → 화면에 요약문과 뉴스 리스트 표시
```

## 폴더 구조 요약

```
initial_version/
├── app.py                ← [Phase 6] 메인 실행 및 통합
├── config/               ← [Phase 1] 환경 설정 로더
├── domain/               ← [Phase 2] 핵심 데이터 모델
├── services/             ← [Phase 3] 외부 API 연동 비즈니스 로직
├── repositories/         ← [Phase 4] CSV 데이터 저장 및 관리
├── components/           ← [Phase 5] UI 각 부분 함수화
├── utils/                ← [Phase 2, 7] 유틸리티 및 에러 처리
└── data/                 ← [Phase 4] 실제 데이터 저장소
```

---

## 학습 체크리스트

### 기능 이해
- [ ] 특정 도메인(뉴스 사이트)에서만 정보를 가져오게 하는 설정이 어디에 있는지 이해했나요? (`.env`의 `SEARCH_DOMAINS`)
- [ ] 검색 결과가 왜 항상 최신순으로 정렬되어 나오는지 로직을 설명할 수 있나요? (`search_service.py`의 정렬 로직)
- [ ] 과거 기록을 선택했을 때 어떻게 코드가 다시 실행되지 않고 해당 데이터를 찾아내는지 아나요? (`find_by_key`)

### 구현 스킬
- [ ] `uv sync`와 `uv add`를 통해 라이브러리를 관리할 수 있나요?
- [ ] `@dataclass`를 사용하여 나만의 새로운 데이터 타입을 만들 수 있나요?
- [ ] Streamlit의 `st.session_state`를 어떨 때 사용해야 하는지 이해했나요?
- [ ] `try-except`와 커스텀 예외를 사용해 에러를 우아하게 처리할 수 있나요?
