"""
certificate.py
인증서 관리 모듈
Phase 4에서 배운 파일 I/O 적용
"""

import os
from datetime import datetime
from typing import List

# 인증서 저장 폴더
OUTPUT_DIR = "output"


def ensure_output_dir() -> None:
    """output 폴더가 없으면 생성합니다."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def check_cleared_phases() -> List[int]:
    """
    기존에 클리어한 phase 목록을 확인합니다.

    Returns:
        List[int]: 클리어한 phase 번호 리스트
    """
    cleared = []
    for i in range(1, 8):
        filepath = os.path.join(OUTPUT_DIR, f"phase_{i}_clear.txt")
        if os.path.exists(filepath):
            cleared.append(i)
    return cleared


def save_certificate(player_name: str, phase: int, guardian_name: str) -> None:
    """
    통과 인증서를 파일로 저장합니다.

    Args:
        player_name: 플레이어 이름
        phase: 통과한 phase 번호
        guardian_name: 문지기 이름
    """
    ensure_output_dir()

    filename = f"phase_{phase}_clear.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""{'='*50}
     🎉 {guardian_name}의 인증서 🎉
{'='*50}

축하합니다, {player_name}님!
Phase {phase} 시험을 통과하셨습니다.

통과 일시: {now}

- {guardian_name} -
{'='*50}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n📜 인증서 저장됨: {filepath}")


def save_master_certificate(player_name: str) -> None:
    """
    모든 phase 클리어 시 최종 인증서를 발급합니다.

    Args:
        player_name: 플레이어 이름
    """
    ensure_output_dir()

    filename = "python_master_certificate.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""{'='*60}
        🏆 파이썬 마법사 인증서 🏆
{'='*60}

    {player_name} 님이
    파이썬 던전의 모든 관문을 통과하고
    진정한 파이썬 마법사가 되었음을 증명합니다.

    발급일: {now}

        - TrendTracker 던전 마스터 -
{'='*60}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n🏆 최종 인증서 발급: {filepath}")
