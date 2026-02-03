"""
멀티모달 Gemini API 클라이언트

기존 gemini_client.py를 수정하지 않고 새로운 파일로 추가합니다.
이미지를 포함한 멀티모달 요청을 처리합니다.
"""
import os
import json
from pathlib import Path
import typing_extensions as typing
from google import genai
from google.genai import types

from domain.problem import Problem, Answer
from utils.exceptions import AppError
from prompts.prompt_multi import (
    SYSTEM_PROMPT_MULTI,
    USER_PROMPT_MULTI,
    MAX_OUTPUT_TOKENS,
)


class SolverResponse(typing.TypedDict):
    """응답 스키마 (기존과 동일)"""
    choice: int
    reasoning: str


class GeminiMultiClient:
    """멀티모달 Gemini API 클라이언트

    기존 GeminiClient와 동일한 인터페이스(solve_problem)를 제공하여
    SolverService에서 그대로 사용할 수 있습니다.
    """

    # 지원하는 이미지 확장자
    SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}

    # 확장자별 MIME 타입
    MIME_TYPES = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }

    def __init__(self, api_key: str):
        """클라이언트 초기화

        Args:
            api_key: Gemini API 키
        """
        self.client = genai.Client(api_key=api_key)
        self.model_name = os.getenv("MODEL", "gemini-2.0-flash-lite")
        print(f"[GeminiMultiClient] Model: {self.model_name}")
        print(f"[GeminiMultiClient] Max Output Tokens: {MAX_OUTPUT_TOKENS}")

    def _load_image(self, image_path: str) -> tuple[bytes, str]:
        """이미지 파일 로드

        Args:
            image_path: 이미지 파일 경로

        Returns:
            (이미지 바이너리 데이터, MIME 타입)

        Raises:
            AppError: 파일이 없거나 지원하지 않는 형식일 때
        """
        path = Path(image_path)
        ext = path.suffix.lower()

        # 확장자 검증
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise AppError("unsupported_image_format")

        # 파일 존재 검증
        if not path.exists():
            raise AppError("image_not_found")

        # 이미지 로드
        with open(path, "rb") as f:
            image_data = f.read()

        return image_data, self.MIME_TYPES[ext]

    def _build_contents(self, problem: Problem) -> list:
        """멀티모달 콘텐츠 구성

        Args:
            problem: 문제 객체 (question 필드에 이미지 경로)

        Returns:
            Gemini API에 전송할 콘텐츠 리스트
        """
        # question 필드에서 이미지 경로 추출
        image_data, mime_type = self._load_image(problem.question)

        # 텍스트 + 이미지 + 텍스트 구조
        return [
            types.Part.from_text(text=SYSTEM_PROMPT_MULTI),
            types.Part.from_bytes(data=image_data, mime_type=mime_type),
            types.Part.from_text(text=USER_PROMPT_MULTI),
        ]

    def solve_problem(self, problem: Problem) -> Answer:
        """이미지 문제 풀이

        Args:
            problem: 문제 객체

        Returns:
            Answer 객체 (예측 답, 정답, reasoning 포함)

        Note:
            기존 GeminiClient.solve_problem()과 동일한 시그니처를 유지하여
            SolverService에서 그대로 사용할 수 있습니다.
        """
        contents = self._build_contents(problem)

        # Mode 3 스타일: JSON + Schema 강제
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SolverResponse,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
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
        """응답 파싱

        Args:
            response_text: AI 응답 텍스트 (JSON)
            problem: 원본 문제 객체

        Returns:
            Answer 객체
        """
        data = json.loads(response_text)
        predicted = data.get("choice", 0)
        reasoning = data.get("reasoning", "")

        return Answer(
            problem_id=problem.id,
            predicted=predicted,
            actual=problem.answer,
            is_correct=(predicted == problem.answer),
            reasoning=reasoning,
            score=problem.score,
        )
