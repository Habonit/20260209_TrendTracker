"""
프롬프트 정의 파일

이 파일을 수정하여 다양한 프롬프트 실험을 할 수 있습니다.
- SYSTEM_PROMPT: AI의 역할 정의
- USER_PROMPT_TEMPLATE: 문제 형식 템플릿
- MAX_OUTPUT_TOKENS: 출력 토큰 제한 (환경변수로 설정 가능)
"""

import os

# 출력 토큰 제한 (reasoning 길이 조절)
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "2048"))

# 시스템 프롬프트 (AI 역할 정의)
SYSTEM_PROMPT = """당신은 수능 국어 문제를 푸는 전문가입니다.
주어진 지문을 꼼꼼히 읽고, 문제의 의도를 정확히 파악하여 답을 선택하세요.
반드시 선택한 답의 이유를 구체적으로 설명해야 합니다.
"""

# 유저 프롬프트 템플릿 (문제 형식)
USER_PROMPT_TEMPLATE = """다음 수능 국어 문제를 풀어주세요.

[지문]
{paragraph}

[문제]
{question}

[보기]
{question_plus}

[선택지]
1. {choice_1}
2. {choice_2}
3. {choice_3}
4. {choice_4}
5. {choice_5}

다음 JSON 형식으로 답변하세요:
{{
  "choice": 정답번호(1-5),
  "reasoning": "왜 이 답을 선택했는지 구체적인 근거를 설명하세요. 지문의 어떤 부분이 근거가 되는지, 다른 선택지가 왜 틀렸는지 포함해주세요."
}}
"""


def build_user_prompt(problem) -> str:
    """Problem 객체로 유저 프롬프트 생성"""
    return USER_PROMPT_TEMPLATE.format(
        paragraph=problem.paragraph,
        question=problem.question,
        question_plus=problem.question_plus,
        choice_1=problem.choices[0],
        choice_2=problem.choices[1],
        choice_3=problem.choices[2],
        choice_4=problem.choices[3],
        choice_5=problem.choices[4],
    )
