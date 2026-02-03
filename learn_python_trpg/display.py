"""
display.py
스크립트의 텍스트를 화면에 출력하는 함수들
"""


def print_lines(lines: list) -> None:
    """리스트의 각 요소를 줄바꿈하여 출력합니다."""
    for line in lines:
        print(line)


def print_intro(script: dict) -> None:
    """게임 인트로를 출력합니다."""
    print_lines(script["intro"]["welcome"])
    print_lines(script["intro"]["story"])


def print_menu(script: dict, cleared_phases: list, next_phase: int) -> None:
    """관문 선택 메뉴를 출력합니다."""
    menu = script["menu"]

    print_lines(menu["header"])

    for i in range(1, 8):
        phase_data = script["phases"][str(i)]
        title = phase_data["title"]

        if i in cleared_phases:
            status = menu["status_cleared"]
        elif i == next_phase:
            status = menu["status_available"]
        else:
            status = menu["status_locked"]

        line = menu["phase_format"].format(num=i, title=title, status=status)
        print(line)

    print(menu["exit_option"])
    print(menu["divider"])


def print_quiz_header(script: dict, current: int, lives: str) -> None:
    """퀴즈 헤더를 출력합니다."""
    for line in script["quiz"]["header"]:
        print(line.format(current=current, lives=lives))


def print_result(script: dict, correct: int, passed: bool) -> None:
    """시험 결과를 출력합니다."""
    result = script["result"]

    print_lines(result["header"])
    print(result["score"].format(correct=correct))
    print(result["pass_requirement"])

    if passed:
        print(result["passed"])
    else:
        print(result["failed_score"].format(correct=correct))


def print_final_ending(script: dict, player_name: str) -> None:
    """최종 엔딩을 출력합니다."""
    print_lines(script["final_ending"]["header"])
    for line in script["final_ending"]["message"]:
        print(line.format(name=player_name))
