"""
# ============================================
# Phase 7-1: 에러 핸들링 심화
# ============================================
#
# 🎯 이 파일에서 배울 것:
# - 에러 타입과 에러 메시지 매핑
# - 환경변수 검증
# - API 에러 상세 처리
# - 사용자 친화적 에러 메시지
#
# 📋 실행 방법:
# streamlit run materials/phase_7_error.py
# ============================================
"""

import streamlit as st
from typing import Optional, Dict
import os

st.set_page_config(page_title="Phase 7-1: 에러 핸들링", page_icon="🛡️")

st.title("🛡️ Phase 7-1: 에러 핸들링 심화")

# ============================================
# 📚 이론: 왜 에러 핸들링이 중요한가?
# ============================================

st.header("1️⃣ 에러 핸들링의 중요성")

st.markdown("""
## 에러 핸들링이란?

프로그램에서 **문제가 발생했을 때 적절히 대응**하는 것입니다.

### 에러 핸들링이 없으면?

```
❌ 앱 크래시
❌ 빨간 에러 메시지 (사용자 혼란)
❌ "뭐가 잘못된 거지?" 상태
```

### 에러 핸들링이 있으면?

```
✅ 앱 계속 동작
✅ 친절한 안내 메시지
✅ "아, 이렇게 하면 되는구나" 이해
```

### 비유로 이해하기

> 🏪 **편의점 비유**
>
> **에러 핸들링 없음**: "Error 404" (?)
> **에러 핸들링 있음**: "죄송합니다, 해당 상품이 품절입니다. 내일 입고 예정입니다."
""")

st.divider()

# ============================================
# 📚 이론: 에러 타입과 메시지 매핑
# ============================================

st.header("2️⃣ 에러 타입과 메시지 매핑")

st.markdown("""
## 에러 메시지 매핑이란?

**에러 코드 → 사용자 친화적 메시지**로 변환하는 것입니다.

### TrendTracker의 에러 매핑

```python
ERROR_MESSAGES = {
    "api_key_invalid": "API 키가 유효하지 않습니다. 설정을 확인해주세요.",
    "rate_limit_exceeded": "요청이 너무 많습니다. 잠시 후 다시 시도해주세요.",
    "network_error": "네트워크 연결을 확인해주세요.",
    "no_results": "검색 결과가 없습니다.",
    "ai_error": "AI 요약 중 오류가 발생했습니다.",
}

def handle_error(error_type: str):
    message = ERROR_MESSAGES.get(error_type, "알 수 없는 오류")
    st.error(message)
```

### 왜 매핑을 사용할까요?

| 방식 | 장점 | 단점 |
|------|------|------|
| 직접 메시지 작성 | 간단 | 중복, 일관성 없음 |
| **매핑 사용** | 일관성, 유지보수 쉬움 | 초기 설정 필요 |
""")

st.divider()

# ============================================
# 🔍 예제: 에러 매핑 시스템
# ============================================

st.header("3️⃣ 에러 매핑 시스템 예제")

# 에러 메시지 매핑
ERROR_MESSAGES: Dict[str, str] = {
    "api_key_invalid": "🔑 API 키가 유효하지 않습니다. 설정을 확인해주세요.",
    "rate_limit_exceeded": "⏳ 요청이 너무 많습니다. 30초 후 다시 시도해주세요.",
    "network_error": "🌐 네트워크 연결을 확인해주세요.",
    "no_results": "🔍 검색 결과가 없습니다. 다른 키워드로 시도해보세요.",
    "ai_error": "🤖 AI 요약 중 오류가 발생했습니다.",
    "file_error": "📁 파일 접근에 실패했습니다.",
    "empty_input": "✏️ 검색어를 입력해주세요.",
}

def handle_error(error_type: str, level: str = "error"):
    """에러 타입에 따라 적절한 메시지를 표시합니다."""
    message = ERROR_MESSAGES.get(error_type, "❓ 알 수 없는 오류가 발생했습니다.")

    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    elif level == "info":
        st.info(message)

st.markdown("### 버튼을 클릭해서 다양한 에러 메시지를 확인해보세요!")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔑 API 키 에러", use_container_width=True):
        handle_error("api_key_invalid")

    if st.button("⏳ 요청 한도 초과", use_container_width=True):
        handle_error("rate_limit_exceeded")

    if st.button("🌐 네트워크 에러", use_container_width=True):
        handle_error("network_error")

with col2:
    if st.button("🔍 결과 없음", use_container_width=True):
        handle_error("no_results", level="warning")

    if st.button("🤖 AI 에러", use_container_width=True):
        handle_error("ai_error")

    if st.button("❓ 알 수 없는 에러", use_container_width=True):
        handle_error("unknown_error_type")

st.divider()

# ============================================
# 📚 이론: 환경변수 검증
# ============================================

st.header("4️⃣ 환경변수 검증")

st.markdown("""
## 환경변수 검증이란?

앱 시작 시 **필수 설정이 있는지 확인**하는 것입니다.

### 왜 필요할까요?

```python
# 검증 없이 실행하면...
api_key = os.getenv("API_KEY")  # None이 될 수 있음!
response = api_call(api_key)    # 에러 발생!
```

### TrendTracker의 검증 패턴

```python
class Settings:
    def __init__(self):
        self.TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

        # 검증
        missing = []
        if not self.TAVILY_API_KEY:
            missing.append("TAVILY_API_KEY")
        if not self.GEMINI_API_KEY:
            missing.append("GEMINI_API_KEY")

        if missing:
            raise ValueError(self._get_error_message(missing))

    def _get_error_message(self, missing):
        return f\"\"\"
❌ 환경변수가 설정되지 않았습니다.

누락된 변수: {', '.join(missing)}

설정 방법:
1. .env.example 파일을 .env로 복사
2. 각 API 키를 발급받아 입력

API 키 발급:
- Tavily: https://tavily.com/
- Gemini: https://aistudio.google.com/
\"\"\"
```

### Streamlit에서 사용

```python
try:
    settings = Settings()
except ValueError as e:
    st.error(str(e))
    st.stop()  # 앱 실행 중단
```
""")

st.divider()

# ============================================
# 🔍 예제: 환경변수 검증 시뮬레이션
# ============================================

st.header("5️⃣ 환경변수 검증 시뮬레이션")

st.markdown("### 가상의 환경변수 설정 상황을 시뮬레이션합니다.")

# 시뮬레이션용 체크박스
col1, col2 = st.columns(2)

with col1:
    has_tavily = st.checkbox("TAVILY_API_KEY 있음", value=True, key="check_tavily")
with col2:
    has_gemini = st.checkbox("GEMINI_API_KEY 있음", value=True, key="check_gemini")

if st.button("🔍 환경변수 검증 실행"):
    missing = []

    if not has_tavily:
        missing.append("TAVILY_API_KEY")
    if not has_gemini:
        missing.append("GEMINI_API_KEY")

    if missing:
        st.error(f"""
❌ **환경변수가 설정되지 않았습니다.**

**누락된 변수**: {', '.join(missing)}

**설정 방법**:
1. `.env.example` 파일을 `.env`로 복사
2. 각 API 키를 발급받아 입력

**API 키 발급 안내**:
- Tavily API: https://tavily.com/
- Google AI Studio (Gemini): https://aistudio.google.com/
        """)
    else:
        st.success("✅ 모든 환경변수가 설정되어 있습니다!")

st.divider()

# ============================================
# 📚 이론: API 에러 상세 처리
# ============================================

st.header("6️⃣ API 에러 상세 처리")

st.markdown("""
## HTTP 상태 코드별 처리

API는 **상태 코드**로 결과를 알려줍니다.

| 코드 | 의미 | 대응 |
|------|------|------|
| 200 | 성공 | 정상 처리 |
| 400 | 잘못된 요청 | 입력값 확인 안내 |
| 401 | 인증 실패 | API 키 확인 안내 |
| 429 | 요청 한도 초과 | 대기 후 재시도 안내 |
| 5xx | 서버 오류 | 재시도 안내 |

### 코드 예시

```python
try:
    response = tavily.search(query=keyword)
except Exception as e:
    error_str = str(e).lower()

    if "401" in error_str or "unauthorized" in error_str:
        raise AppError("api_key_invalid")
    elif "429" in error_str or "rate" in error_str:
        raise AppError("rate_limit_exceeded")
    elif "timeout" in error_str or "connection" in error_str:
        raise AppError("network_error")
    else:
        raise AppError("server_error")
```

### 에러 분기 흐름

```
API 호출
    ↓
에러 발생?
    ├─ No → 정상 처리
    └─ Yes → 에러 분석
              ↓
         상태 코드 확인
              ├─ 401 → "API 키 확인"
              ├─ 429 → "잠시 후 재시도"
              ├─ 5xx → "서버 오류"
              └─ 기타 → "알 수 없는 오류"
```
""")

st.divider()

# ============================================
# ✏️ 가이드 실습
# ============================================

st.header("✏️ 가이드 실습: 에러 핸들러 만들기")

st.markdown("""
### 목표
커스텀 에러 클래스와 에러 핸들러를 만들어보기

### 힌트
- 딕셔너리로 에러 메시지 매핑
- 함수로 에러 표시 로직 분리
""")

st.subheader("🎯 실습 영역")

st.code('''
# ============================================
# ✏️ 실습: 에러 핸들링 시스템
# ============================================

# TODO 1: 커스텀 에러 클래스 만들기
# 힌트: Exception을 상속, error_type 속성 추가

# >>> 정답 <<<
# class AppError(Exception):
#     def __init__(self, error_type: str):
#         self.error_type = error_type
#         super().__init__(error_type)


# TODO 2: 에러 메시지 딕셔너리 만들기
# 최소 3개 이상의 에러 타입 정의

# >>> 정답 <<<
# ERRORS = {
#     "login_failed": "로그인에 실패했습니다.",
#     "not_found": "요청한 항목을 찾을 수 없습니다.",
#     "permission_denied": "접근 권한이 없습니다.",
# }


# TODO 3: show_error() 함수 만들기
# - 에러 타입을 받아서 메시지 표시
# - 알 수 없는 에러는 기본 메시지 표시

# >>> 정답 <<<
# def show_error(error_type: str):
#     message = ERRORS.get(error_type, "오류가 발생했습니다.")
#     st.error(message)


# TODO 4: 에러 발생 및 처리 테스트
# try-except로 AppError 발생시키고 처리

# >>> 정답 <<<
# try:
#     raise AppError("login_failed")
# except AppError as e:
#     show_error(e.error_type)
''', language="python")

# 실제 동작하는 예제
st.markdown("### 🔍 실제 동작 예제")

class AppError(Exception):
    def __init__(self, error_type: str):
        self.error_type = error_type
        super().__init__(error_type)

PRACTICE_ERRORS = {
    "login_failed": "🔐 로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.",
    "not_found": "🔍 요청한 항목을 찾을 수 없습니다.",
    "permission_denied": "🚫 접근 권한이 없습니다.",
}

def show_practice_error(error_type: str):
    message = PRACTICE_ERRORS.get(error_type, "❓ 알 수 없는 오류가 발생했습니다.")
    st.error(message)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("로그인 실패", key="practice_login"):
        try:
            raise AppError("login_failed")
        except AppError as e:
            show_practice_error(e.error_type)

with col2:
    if st.button("항목 없음", key="practice_notfound"):
        try:
            raise AppError("not_found")
        except AppError as e:
            show_practice_error(e.error_type)

with col3:
    if st.button("권한 없음", key="practice_permission"):
        try:
            raise AppError("permission_denied")
        except AppError as e:
            show_practice_error(e.error_type)

st.divider()

# ============================================
# 🏆 챌린지
# ============================================

st.header("🏆 챌린지: 완전한 에러 시스템")

st.markdown("""
### 목표
재시도 로직까지 포함한 완전한 에러 처리 시스템 만들기

⚠️ **정답이 제공되지 않습니다.** 강사와 함께 풀어보세요!
""")

st.subheader("🎯 챌린지 영역")

st.code('''
# ============================================
# 🏆 챌린지: 완전한 에러 시스템
# ============================================
# ⚠️ 정답이 제공되지 않습니다.

import time
from typing import Callable, Any

# TODO 1: ErrorHandler 클래스 만들기
# - 에러 메시지 딕셔너리 관리
# - 에러 로그 기록 (리스트에 저장)
# - 에러 통계 (각 타입별 발생 횟수)


# TODO 2: retry_on_error() 함수 만들기
# - 최대 재시도 횟수
# - 재시도 간 대기 시간
# - 재시도 가능한 에러 타입 지정
#
# def retry_on_error(
#     func: Callable,
#     max_retries: int = 3,
#     delay: float = 1.0,
#     retryable_errors: list = ["network_error", "rate_limit"]
# ) -> Any:
#     ...


# TODO 3: validate_config() 함수 만들기
# - 여러 환경변수를 한 번에 검증
# - 누락된 변수 목록 반환
# - 각 변수별 기본값 지원


# TODO 4: (심화) 에러 로그를 파일로 저장
# - 발생 시간, 에러 타입, 상세 내용


# TODO 5: (심화) 에러 발생 시 알림
# - st.toast()로 간단한 알림
# - 심각한 에러는 st.error()

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
| 에러 메시지 매핑 | 에러 코드 → 친절한 메시지 변환 |
| 환경변수 검증 | 앱 시작 시 필수 설정 확인 |
| HTTP 상태 코드 | 401, 429, 5xx 등 분기 처리 |
| 커스텀 에러 클래스 | AppError로 에러 타입 관리 |

### 핵심 패턴

```python
# 에러 메시지 매핑
ERROR_MESSAGES = {
    "error_type": "친절한 메시지",
}

# 커스텀 에러
class AppError(Exception):
    def __init__(self, error_type: str):
        self.error_type = error_type

# 에러 처리
try:
    risky_operation()
except AppError as e:
    message = ERROR_MESSAGES.get(e.error_type, "알 수 없는 오류")
    st.error(message)

# 환경변수 검증
missing = []
for key in required_keys:
    if not os.getenv(key):
        missing.append(key)
if missing:
    raise ValueError(f"누락된 변수: {missing}")
```

### ✅ 체크리스트
- [ ] 에러 메시지 매핑의 장점을 안다
- [ ] 환경변수 검증 방법을 안다
- [ ] HTTP 상태 코드별 처리를 이해했다
- [ ] 커스텀 에러 클래스를 만들 수 있다
- [ ] 챌린지를 강사와 함께 풀어봤다
""")

st.info("다음 파일: `phase_7_ux.py` - UX 개선 (로딩, 메시지)")
