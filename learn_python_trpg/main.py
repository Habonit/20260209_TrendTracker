"""
main.py
파이썬 던전 탈출 - 메인 게임 파일
모든 모듈을 조합하여 게임을 실행합니다.
"""

import json
import os

from models import Player, GameState
from exceptions import GameOverError
from certificate import check_cleared_phases, save_certificate, save_master_certificate
from display import (
    print_lines,
    print_intro,
    print_menu,
    print_quiz_header,
    print_result,
    print_final_ending
)


def get_script_path() -> str:
    """스크립트 파일 경로를 반환합니다."""
    # 현재 파일 위치 기준으로 data 폴더의 JSON 파일 경로 반환
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "data", "trpg_script.json")


def load_script(filepath: str = None) -> dict:
    """
    게임 스크립트 JSON 파일을 로드합니다.

    Args:
        filepath: JSON 파일 경로 (None이면 기본 경로 사용)

    Returns:
        dict: 파싱된 JSON 데이터
    """
    if filepath is None:
        filepath = get_script_path()

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"스크립트 파일을 찾을 수 없습니다: {filepath}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 파싱 오류: {e}")


def get_player_name(script: dict) -> str:
    """플레이어 이름을 입력받습니다."""
    while True:
        name = input(script["intro"]["name_prompt"]).strip()
        if name:
            return name
        print(script["intro"]["name_empty_error"])


def get_user_choice(script: dict) -> int:
    """
    사용자의 선택을 입력받습니다.

    Returns:
        int: 1~5 사이의 선택 번호
    """
    while True:
        try:
            choice = input(script["quiz"]["prompt"]).strip()
            choice = int(choice)

            if 1 <= choice <= 5:
                return choice
            else:
                print(script["quiz"]["invalid_range"])

        except ValueError:
            print(script["quiz"]["invalid_number"])


def select_phase(script: dict, cleared_phases: list, next_phase: int) -> int:
    """
    플레이할 phase를 선택합니다.

    Returns:
        int: 선택한 phase (0이면 종료)
    """
    menu = script["menu"]

    while True:
        try:
            choice = int(input(menu["prompt"]))

            if choice == 0:
                return 0

            if choice < 1 or choice > 7:
                print(menu["invalid_input"])
                continue

            if choice in cleared_phases:
                print(menu["already_cleared"])
                continue

            if choice != next_phase:
                print(menu["phase_locked"].format(phase=next_phase))
                continue

            return choice

        except ValueError:
            print(menu["invalid_input"])


def play_phase(game: GameState, phase: int) -> bool:
    """
    하나의 phase를 플레이합니다.

    Args:
        game: 게임 상태
        phase: 플레이할 phase 번호

    Returns:
        bool: 통과 여부

    Raises:
        GameOverError: 목숨을 모두 잃었을 때
    """
    script = game.script
    quiz_text = script["quiz"]
    guardian = game.get_guardian(phase)
    player = game.player

    # 플레이어 상태 초기화
    player.reset_for_new_phase()
    player.current_phase = phase

    # 문지기 등장
    guardian.greet()
    input(quiz_text["continue_prompt"])

    # 문제 풀이
    for i, question in enumerate(guardian.questions, 1):
        # 헤더 출력
        lives_display = player.get_lives_display(script)
        print_quiz_header(script, i, lives_display)

        # 문제 출력
        question.display(i)

        # 정답 입력
        user_answer = get_user_choice(script)

        # 정답 확인
        if user_answer == question.answer:
            player.add_correct()
            print(quiz_text["correct"])
        else:
            player.lose_life()
            print(quiz_text["wrong"].format(answer=question.answer))
            print(quiz_text["life_lost"])

            if player.is_game_over():
                guardian.mock(player.name)
                raise GameOverError(phase, i)

        # 해설 표시
        print(quiz_text["explanation"].format(explanation=question.explanation))
        input(quiz_text["continue_prompt"])

    # 결과 판정
    passed = player.correct_count >= 8
    print_result(script, player.correct_count, passed)

    if passed:
        guardian.congratulate(player.name)
        return True
    else:
        guardian.mock(player.name)
        return False


def main():
    """게임 메인 함수"""
    # JSON 스크립트 로드
    try:
        script = load_script()
    except FileNotFoundError as e:
        print(f"오류: {e}")
        return
    except ValueError as e:
        print(f"오류: {e}")
        return

    # 인트로 출력
    print_intro(script)

    # 플레이어 이름 입력
    player_name = get_player_name(script)

    # 기존 클리어 현황 확인
    cleared_phases = check_cleared_phases()

    # 플레이어 및 게임 상태 생성
    player = Player(name=player_name, cleared_phases=cleared_phases)
    game = GameState.from_script(player, script)

    # 환영 메시지
    welcome = script["intro"]["name_confirmed"].format(name=player_name)
    print(welcome)

    while game.is_running:
        # 다음 도전할 phase 확인
        next_phase = game.get_next_available_phase()

        if next_phase == -1:
            # 모든 phase 클리어!
            print_final_ending(script, game.player.name)
            save_master_certificate(game.player.name)
            break

        # phase 선택 메뉴
        print_menu(script, game.player.cleared_phases, next_phase)
        selected_phase = select_phase(script, game.player.cleared_phases, next_phase)

        if selected_phase == 0:
            # 게임 종료
            exit_msg = script["exit"]["goodbye"].format(name=game.player.name)
            print(exit_msg)
            break

        # 해당 phase 도전
        try:
            success = play_phase(game, selected_phase)

            if success:
                game.player.cleared_phases.append(selected_phase)
                guardian = game.get_guardian(selected_phase)
                save_certificate(
                    player_name=game.player.name,
                    phase=selected_phase,
                    guardian_name=guardian.name
                )

        except GameOverError:
            # 게임 오버 화면 출력
            print_lines(script["game_over"]["header"])
            print(script["game_over"]["message"])
            print(script["game_over"]["retry_hint"])
            break


if __name__ == "__main__":
    main()
