# 환경변수 설정 가이드

## 개요

`.env` 파일을 통해 AI 모델과 응답 설정을 조정할 수 있습니다.

---

## 환경변수 목록

| 변수명 | 필수 | 기본값 | 설명 |
|--------|------|--------|------|
| `GEMINI_API_KEY` | O | - | Gemini API 키 |
| `RESPONSE_MODE` | X | `3` | 응답 형식 모드 (1, 2, 3) |
| `MODEL` | X | `gemini-2.0-flash-lite` | 사용할 Gemini 모델 |
| `MAX_OUTPUT_TOKENS` | X | `2048` | 최대 출력 토큰 수 |

---

## .env 파일 예시

```bash
# 필수
GEMINI_API_KEY=your_api_key_here

# 선택 (기본값 사용 시 생략 가능)
RESPONSE_MODE=3
MODEL=gemini-2.0-flash-lite
MAX_OUTPUT_TOKENS=2048
```

---

## 상세 설명

### GEMINI_API_KEY (필수)

Google AI Studio에서 발급받은 API 키

```bash
GEMINI_API_KEY=AIzaSy...
```

### RESPONSE_MODE

AI 응답 형식을 제어하는 모드

| 값 | 설명 | 강제 수준 |
|----|------|----------|
| `1` | 프롬프트만 | 약함 |
| `2` | Mode 1 + MIME type (`application/json`) | 중간 |
| `3` | Mode 2 + Schema 정의 | 강함 |

```bash
RESPONSE_MODE=3  # 권장
```

### MODEL

사용할 Gemini 모델명

```bash
# 기본값 (권장)
MODEL=gemini-2.0-flash-lite

# 다른 모델 사용 시
MODEL=gemini-2.0-pro
MODEL=gemini-1.5-flash
MODEL=gemini-1.5-pro
```

**참고**: 모델에 따라 Rate Limit과 비용이 다릅니다.

### MAX_OUTPUT_TOKENS

AI가 생성할 수 있는 최대 토큰 수

```bash
# 기본값
MAX_OUTPUT_TOKENS=2048

# 더 긴 추론이 필요한 경우
MAX_OUTPUT_TOKENS=4096
```

**참고**: 값이 클수록 응답이 길어질 수 있지만, 비용과 지연 시간이 증가합니다.

---

## 실행 시 환경변수 오버라이드

`.env` 파일 수정 없이 일시적으로 값을 변경할 수 있습니다.

```bash
# 모델 변경
MODEL=gemini-2.0-pro uv run python main.py

# 토큰 수 변경
MAX_OUTPUT_TOKENS=4096 uv run python main.py

# 여러 변수 동시 변경
MODEL=gemini-2.0-pro MAX_OUTPUT_TOKENS=4096 RESPONSE_MODE=2 uv run python main.py
```

---

## 코드 적용 위치

### ai/gemini_client.py

```python
class GeminiClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.mode = int(os.getenv("RESPONSE_MODE", "3"))
        self.model_name = os.getenv("MODEL", "gemini-2.0-flash-lite")
        self.max_output_tokens = int(os.getenv("MAX_OUTPUT_TOKENS", "2048"))

    def _get_generation_config(self) -> types.GenerateContentConfig:
        if self.mode == 1:
            return types.GenerateContentConfig(
                max_output_tokens=self.max_output_tokens,
            )
        elif self.mode == 2:
            return types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=self.max_output_tokens,
            )
        else:
            return types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SolverResponse,
                max_output_tokens=self.max_output_tokens,
            )
```

---

## .env.example 업데이트

```bash
# Gemini API Key (필수)
GEMINI_API_KEY=your_api_key_here

# Response Mode (1, 2, 3)
# Mode 1: 프롬프트만
# Mode 2: Mode 1 + MIME type (application/json)
# Mode 3: Mode 2 + Schema 정의
RESPONSE_MODE=3

# Model
MODEL=gemini-2.0-flash-lite

# Max Output Tokens
MAX_OUTPUT_TOKENS=2048
```
