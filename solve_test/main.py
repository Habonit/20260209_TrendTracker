import os
import sys
import argparse
from dotenv import load_dotenv

from domain.problem import Problem, Answer
from repository.problem_repository import ProblemRepository
from service.solver_service import SolverService
from ai.gemini_client import GeminiClient


def parse_args():
    """CLI 인자 파싱"""
    parser = argparse.ArgumentParser(description="수능 국어 문제 풀이 AI")
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="./data/2023_11_KICE_flat.json",
        help="입력 데이터 경로 (JSON)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="./output/results.csv",
        help="출력 결과 경로 (CSV)"
    )
    # 신규: 문제 유형 선택
    parser.add_argument(
        "-t", "--type",
        type=str,
        choices=["text", "multi"],
        default="text",
        help="문제 유형 (text: 텍스트, multi: 이미지)"
    )
    return parser.parse_args()


def run_text_solver(args, api_key: str):
    """텍스트 문제 풀이 (기존 로직)"""
    mode = os.getenv("RESPONSE_MODE", "3")

    print("=== 수능 국어 문제 풀이 AI (텍스트) ===")
    print(f"Response Mode: {mode}")
    print(f"입력: {args.input}")
    print(f"출력: {args.output}")
    print()

    # 기존과 동일한 의존성 초기화
    repository = ProblemRepository(args.input)
    client = GeminiClient(api_key)
    service = SolverService(client, repository)

    _run_solver(service, repository, args.output)


def run_multi_solver(args, api_key: str):
    """이미지 문제 풀이 (멀티모달)"""
    # 지연 임포트: multi 모드에서만 로드
    from ai.gemini_multi_client import GeminiMultiClient

    print("=== 수능 국어 문제 풀이 AI (이미지) ===")
    print(f"입력: {args.input}")
    print(f"출력: {args.output}")
    print()

    # 멀티모달 클라이언트 사용
    repository = ProblemRepository(args.input)
    client = GeminiMultiClient(api_key)  # ← 여기가 다름!
    service = SolverService(client, repository)  # 서비스는 동일

    _run_solver(service, repository, args.output)


def _run_solver(service: SolverService, repository: ProblemRepository, output_path: str):
    """공통 풀이 로직"""
    # 문제 로드
    try:
        problems = repository.load_problems()
        total_score = sum(p.score for p in problems)
        print(f"총 {len(problems)}개 문제 로드 완료 (만점: {total_score}점)")
        print()
    except FileNotFoundError:
        print("데이터 파일을 찾을 수 없습니다.")
        sys.exit(1)

    # 문제 풀이 실행
    try:
        results = service.solve_all(problems, output_path)
    except KeyboardInterrupt:
        print("\n중단됨 (진행 상황은 저장되었습니다)")
        sys.exit(0)

    # 결과 출력
    _print_results(service, output_path)


def _print_results(service: SolverService, output_path: str):
    """결과 출력"""
    print()
    print(f"결과가 {output_path}에 저장되었습니다.")

    total_count, correct_count, earned, total = service.calculate_score(output_path)
    accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
    score_rate = (earned / total * 100) if total > 0 else 0

    print()
    print("=" * 40)
    print("결과")
    print("=" * 40)
    print(f"총 문제: {total_count}개")
    print(f"정답: {correct_count}개 / 오답: {total_count - correct_count}개")
    print(f"정답률: {accuracy:.1f}%")
    print()
    print(f"획득 점수: {earned}점 / {total}점")
    print(f"점수 백분율: {score_rate:.1f}%")
    print("=" * 40)


def main():
    args = parse_args()

    # 환경변수 로드
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("GEMINI_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 확인하거나 환경변수를 설정해주세요.")
        sys.exit(1)

    # 타입에 따라 분기
    if args.type == "text":
        run_text_solver(args, api_key)
    else:
        run_multi_solver(args, api_key)


if __name__ == "__main__":
    main()
