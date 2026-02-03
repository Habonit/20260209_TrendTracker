import time
from typing import List
from pathlib import Path

import pandas as pd

from domain.problem import Problem, Answer
from ai.gemini_client import GeminiClient
from repository.problem_repository import ProblemRepository
from utils.exceptions import AppError, handle_error


class SolverService:
    """문제 풀이 비즈니스 로직 (Rate Limit 처리 포함)"""

    def __init__(self, client: GeminiClient, repository: ProblemRepository):
        self.client = client
        self.repository = repository

    def solve_all(self, problems: List[Problem], output_path: str) -> List[Answer]:
        """모든 문제 풀이 (중간 저장)"""
        # 이미 풀이된 문제 제외
        solved_ids = self.repository.get_solved_ids(output_path)
        remaining = [p for p in problems if p.id not in solved_ids]

        if solved_ids:
            print(f"이전 풀이 {len(solved_ids)}개 발견, {len(remaining)}개 남음")
        else:
            # 새 파일 초기화
            self.repository.init_output(output_path)

        if not remaining:
            print("모든 문제가 이미 풀이되었습니다.")
            return []

        results = []
        for i, problem in enumerate(remaining):
            # 문제 풀이
            answer = self._solve_with_retry(problem)
            results.append(answer)

            # 즉시 저장
            self.repository.append_result(answer, output_path)

            # 진행 상황 출력
            status = "O" if answer.is_correct else "X"
            earned = answer.score if answer.is_correct else 0
            print(f"[{i+1}/{len(remaining)}] 문제 {problem.id} ({problem.score}점): {status} (+{earned}점)")

            # Rate Limit 처리 (마지막 문제 제외)
            if i < len(remaining) - 1:
                if (i + 1) % 5 == 0:
                    print(">>> 60초 대기 (Rate Limit)...")
                    time.sleep(60)
                else:
                    time.sleep(10)

        return results

    def _solve_with_retry(self, problem: Problem, max_retries: int = 3) -> Answer:
        """재시도 로직 포함 문제 풀이"""
        for attempt in range(max_retries):
            try:
                return self.client.solve_problem(problem)
            except AppError as e:
                print(f"  [재시도 {attempt+1}/{max_retries}] {handle_error(e.error_type)}")
                if e.error_type == "rate_limit":
                    time.sleep(60)
                elif e.error_type == "parse_error":
                    time.sleep(5)
                else:
                    time.sleep(10)
            except Exception as e:
                print(f"  [재시도 {attempt+1}/{max_retries}] 예상치 못한 오류: {e}")
                time.sleep(10)

        # 모든 재시도 실패 시 빈 Answer 반환
        return Answer(
            problem_id=problem.id,
            predicted=0,
            actual=problem.answer,
            is_correct=False,
            reasoning="[풀이 실패]",
            score=problem.score,
        )

    def calculate_score(self, output_path: str) -> tuple[int, int, int, int]:
        """결과 파일에서 점수 계산

        Returns:
            (총 문제 수, 정답 수, 획득 점수, 총점)
        """
        path = Path(output_path)
        if not path.exists():
            return 0, 0, 0, 0

        df = pd.read_csv(path, encoding="utf-8-sig")
        if df.empty:
            return 0, 0, 0, 0

        total_count = len(df)
        correct_count = int(df["is_correct"].sum())
        earned_score = int(df["earned_score"].sum())
        total_score = int(df["score"].sum())

        return total_count, correct_count, earned_score, total_score
