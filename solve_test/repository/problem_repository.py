import json
from typing import List, Set
from pathlib import Path

import pandas as pd

from domain.problem import Problem, Answer


class ProblemRepository:
    """문제 데이터 저장/조회 담당"""

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def load_problems(self) -> List[Problem]:
        """JSON 파일에서 문제 로드"""
        with open(self.data_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)

        problems = []
        for _, item in data.items():
            problem = Problem(
                id=item["id"],
                paragraph=item["paragraph"],
                question=item["question"],
                question_plus=item["question_plus"],
                choices=item["choices"],
                answer=item["answer"],
                score=item.get("score", 2),
            )
            problems.append(problem)

        return sorted(problems, key=lambda p: p.id)

    def init_output(self, output_path: str):
        """출력 파일 초기화 (헤더만 있는 빈 DataFrame 저장)"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(columns=[
            "problem_id", "score", "predicted", "actual",
            "is_correct", "earned_score", "reasoning"
        ])
        df.to_csv(path, index=False, encoding="utf-8-sig")

    def append_result(self, answer: Answer, output_path: str):
        """결과 한 줄 추가 (기존 파일에 append)"""
        earned = answer.score if answer.is_correct else 0
        new_row = pd.DataFrame([{
            "problem_id": answer.problem_id,
            "score": answer.score,
            "predicted": answer.predicted,
            "actual": answer.actual,
            "is_correct": answer.is_correct,
            "earned_score": earned,
            "reasoning": answer.reasoning,
        }])
        new_row.to_csv(output_path, mode="a", header=False, index=False, encoding="utf-8-sig")

    def get_solved_ids(self, output_path: str) -> Set[int]:
        """이미 풀이된 문제 ID 조회 (재시작 시 사용)"""
        path = Path(output_path)
        if not path.exists():
            return set()

        df = pd.read_csv(path, encoding="utf-8-sig")
        if df.empty:
            return set()

        return set(df["problem_id"].tolist())
