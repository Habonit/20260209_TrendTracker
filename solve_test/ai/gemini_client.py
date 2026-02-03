import os
import re
import json
import typing_extensions as typing
from google import genai
from google.genai import types

from domain.problem import Problem, Answer
from utils.exceptions import AppError
from prompts.prompt import SYSTEM_PROMPT, MAX_OUTPUT_TOKENS, build_user_prompt


class SolverResponse(typing.TypedDict):
    """Mode 3용 응답 스키마"""

    choice: int
    reasoning: str


class GeminiClient:
    """Gemini API 클라이언트 (3단계 모드 지원)"""

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.mode = int(os.getenv("RESPONSE_MODE", "3"))
        self.model_name = os.getenv("MODEL", "gemini-2.0-flash-lite")
        print(f"[GeminiClient] Model: {self.model_name}")
        print(f"[GeminiClient] Mode: {self.mode}")
        print(f"[GeminiClient] Max Output Tokens: {MAX_OUTPUT_TOKENS}")

    def _get_generation_config(self) -> types.GenerateContentConfig | None:
        """모드에 따른 generation_config 반환"""
        if self.mode == 1:
            # Mode 1: 프롬프트만 (기본 설정 + 토큰 제한)
            return types.GenerateContentConfig(
                max_output_tokens=MAX_OUTPUT_TOKENS,
            )
        elif self.mode == 2:
            # Mode 2: MIME type 추가
            return types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=MAX_OUTPUT_TOKENS,
            )
        else:
            # Mode 3: Schema 추가
            return types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SolverResponse,
                max_output_tokens=MAX_OUTPUT_TOKENS,
            )

    def _build_prompt(self, problem: Problem) -> str:
        """시스템 프롬프트 + 유저 프롬프트 결합"""
        user_prompt = build_user_prompt(problem)
        return SYSTEM_PROMPT + "\n\n" + user_prompt

    def solve_problem(self, problem: Problem) -> Answer:
        """문제 풀이 (모드에 따라 다른 설정 적용)"""
        prompt = self._build_prompt(problem)
        config = self._get_generation_config()

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config,
            )
            return self._parse_response(response.text, problem)
        except Exception as e:
            error_msg = str(e).lower()
            if "rate" in error_msg or "quota" in error_msg:
                raise AppError("rate_limit")
            elif "api" in error_msg or "key" in error_msg:
                raise AppError("api_key_invalid")
            else:
                raise AppError("network_error")

    def _parse_response(self, response_text: str, problem: Problem) -> Answer:
        """응답 파싱"""
        try:
            data = json.loads(response_text)
            predicted = data.get("choice", 0)
            reasoning = data.get("reasoning", "")
        except json.JSONDecodeError:
            # Mode 1에서 JSON 파싱 실패 시 텍스트 파싱 시도
            predicted = self._extract_answer_from_text(response_text)
            reasoning = response_text

        return Answer(
            problem_id=problem.id,
            predicted=predicted,
            actual=problem.answer,
            is_correct=(predicted == problem.answer),
            reasoning=reasoning,
            score=problem.score,
        )

    def _extract_answer_from_text(self, text: str) -> int:
        """텍스트에서 정답 번호 추출 (Mode 1 fallback)"""
        # 여러 패턴 시도
        patterns = [
            r"정답[:\s]*(\d)",
            r'"choice"[:\s]*(\d)',
            r"답[:\s]*(\d)",
            r"(\d)번",
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return int(match.group(1))
        return 0
