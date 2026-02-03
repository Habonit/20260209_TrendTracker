"""
models.py
게임에서 사용하는 데이터 모델 정의
Phase 2에서 배운 @dataclass, 타입 힌트 적용
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Question:
    """
    퀴즈 문제를 나타내는 데이터 클래스

    Attributes:
        question: 문제 텍스트
        choices: 5개의 선택지 리스트
        answer: 정답 번호 (1-5)
        explanation: 정답 해설
    """
    question: str
    choices: List[str]
    answer: int
    explanation: str

    @classmethod
    def from_dict(cls, data: dict) -> "Question":
        """딕셔너리(JSON)에서 Question 객체를 생성합니다."""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            explanation=data["explanation"]
        )

    def display(self, number: int) -> None:
        """문제를 화면에 출력합니다."""
        print(f"\nQ{number}. {self.question}")
        print("-" * 40)
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}) {choice}")
        print()


@dataclass
class Guardian:
    """
    문지기를 나타내는 데이터 클래스

    Attributes:
        name: 문지기 이름
        phase: 담당 phase 번호
        greeting: 등장 대사
        success_message: 통과 시 대사
        failure_message: 실패 시 대사
        certificate_message: 인증서 특별 메시지
        questions: 출제할 문제 리스트
    """
    name: str
    phase: int
    greeting: str
    success_message: str
    failure_message: str
    certificate_message: str
    questions: List[Question] = field(default_factory=list)

    @classmethod
    def from_dict(cls, phase: int, data: dict) -> "Guardian":
        """딕셔너리(JSON)에서 Guardian 객체를 생성합니다."""
        guardian_data = data["guardian"]
        questions = [
            Question.from_dict(q) for q in data["questions"]
        ]

        return cls(
            name=guardian_data["name"],
            phase=phase,
            greeting="\n".join(guardian_data["greeting"]),
            success_message="\n".join(guardian_data["success"]),
            failure_message="\n".join(guardian_data["failure"]),
            certificate_message=guardian_data.get("certificate_message", ""),
            questions=questions
        )

    def greet(self) -> None:
        """문지기 등장 대사를 출력합니다."""
        print(f"\n{'='*50}")
        print(f"  ⚔️  {self.name} 등장!  ⚔️")
        print(f"{'='*50}")
        print(self.greeting)

    def congratulate(self, player_name: str) -> None:
        """통과 축하 대사를 출력합니다."""
        message = self.success_message.replace("{name}", player_name)
        print(f"\n{message}")

    def mock(self, player_name: str) -> None:
        """실패 대사를 출력합니다."""
        message = self.failure_message.replace("{name}", player_name)
        print(f"\n{message}")


@dataclass
class Player:
    """
    플레이어 정보를 나타내는 데이터 클래스

    Attributes:
        name: 플레이어 이름
        current_phase: 현재 도전 중인 phase
        lives: 남은 목숨 (기본 2)
        correct_count: 현재 phase에서 맞춘 문제 수
        cleared_phases: 통과한 phase 리스트
    """
    name: str
    current_phase: int = 1
    lives: int = 2
    correct_count: int = 0
    cleared_phases: List[int] = field(default_factory=list)

    def reset_for_new_phase(self) -> None:
        """새 phase 시작 시 상태를 초기화합니다."""
        self.lives = 2
        self.correct_count = 0

    def lose_life(self) -> None:
        """목숨을 1개 잃습니다."""
        self.lives -= 1

    def add_correct(self) -> None:
        """정답 카운트를 1 증가시킵니다."""
        self.correct_count += 1

    def is_game_over(self) -> bool:
        """게임 오버 여부를 반환합니다."""
        return self.lives <= 0

    def get_lives_display(self, script: dict) -> str:
        """현재 목숨을 이모지로 반환합니다."""
        return script["quiz"]["lives_display"].get(str(self.lives), "🖤 🖤")


@dataclass
class GameState:
    """
    전체 게임 상태를 관리하는 데이터 클래스

    Attributes:
        player: 플레이어 정보
        guardians: 모든 문지기 딕셔너리 (phase 번호 → Guardian)
        script: 로드된 JSON 스크립트
        is_running: 게임 실행 중 여부
    """
    player: Player
    guardians: dict  # {1: Guardian, 2: Guardian, ...}
    script: dict     # 로드된 JSON 전체
    is_running: bool = True

    @classmethod
    def from_script(cls, player: Player, script: dict) -> "GameState":
        """JSON 스크립트에서 GameState를 생성합니다."""
        guardians = {}
        for phase_str, phase_data in script["phases"].items():
            phase = int(phase_str)
            guardians[phase] = Guardian.from_dict(phase, phase_data)

        return cls(
            player=player,
            guardians=guardians,
            script=script
        )

    def get_guardian(self, phase: int) -> Guardian:
        """해당 phase의 문지기를 반환합니다."""
        return self.guardians[phase]

    def get_next_available_phase(self) -> int:
        """도전 가능한 다음 phase를 반환합니다."""
        for i in range(1, 8):
            if i not in self.player.cleared_phases:
                return i
        return -1  # 모든 phase 클리어
