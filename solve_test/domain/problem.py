from dataclasses import dataclass
from typing import List


@dataclass
class Problem:
    """수능 국어 문제"""

    id: int
    paragraph: str  # 지문
    question: str  # 문제
    question_plus: str  # 보기 (없으면 "[없음]")
    choices: List[str]  # 선택지 5개
    answer: int  # 정답 (1~5)
    score: int  # 배점 (2 또는 3)


@dataclass
class Answer:
    """AI 풀이 결과"""

    problem_id: int
    predicted: int  # AI가 예측한 답
    actual: int  # 실제 정답
    is_correct: bool  # 정답 여부
    reasoning: str  # AI의 추론 과정
    score: int  # 해당 문제 배점
