from .prompt import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    MAX_OUTPUT_TOKENS,
    build_user_prompt,
)

# 멀티모달 프롬프트 추가
from .prompt_multi import (
    SYSTEM_PROMPT_MULTI,
    USER_PROMPT_MULTI,
    MAX_OUTPUT_TOKENS as MAX_OUTPUT_TOKENS_MULTI,
)

__all__ = [
    # 기존 텍스트용
    "SYSTEM_PROMPT",
    "USER_PROMPT_TEMPLATE",
    "MAX_OUTPUT_TOKENS",
    "build_user_prompt",
    # 멀티모달용
    "SYSTEM_PROMPT_MULTI",
    "USER_PROMPT_MULTI",
    "MAX_OUTPUT_TOKENS_MULTI",
]
