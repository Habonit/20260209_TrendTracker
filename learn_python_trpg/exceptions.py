"""
exceptions.py
커스텀 예외 클래스 정의
Phase 3에서 배운 예외 처리 적용
"""


class GameOverError(Exception):
    """목숨을 모두 소진했을 때 발생하는 예외"""

    def __init__(self, phase: int, question_num: int):
        self.phase = phase
        self.question_num = question_num
        super().__init__(
            f"Phase {phase}의 {question_num}번 문제에서 탈락"
        )


class InvalidInputError(Exception):
    """잘못된 입력이 들어왔을 때 발생하는 예외"""
    pass
