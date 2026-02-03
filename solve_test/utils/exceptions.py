class AppError(Exception):
    """앱 전용 에러 클래스"""

    def __init__(self, error_type: str):
        self.error_type = error_type
        super().__init__(error_type)


ERROR_MESSAGES = {
    # 기존 에러
    "api_key_invalid": "API 키가 유효하지 않습니다. .env 파일을 확인해주세요.",
    "rate_limit": "요청 한도 초과. 60초 후 재시도합니다.",
    "network_error": "네트워크 연결을 확인해주세요.",
    "parse_error": "AI 응답 파싱 실패. 재시도합니다.",
    "file_not_found": "데이터 파일을 찾을 수 없습니다.",
    # 신규 에러 (이미지 관련)
    "image_not_found": "이미지 파일을 찾을 수 없습니다.",
    "unsupported_image_format": "지원하지 않는 이미지 형식입니다. (png, jpg, jpeg만 지원)",
}


def handle_error(error_type: str) -> str:
    """에러 타입에 맞는 메시지 반환"""
    return ERROR_MESSAGES.get(error_type, "알 수 없는 오류가 발생했습니다.")
