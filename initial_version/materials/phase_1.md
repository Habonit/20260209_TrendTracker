# Phase 1 핵심 개념 정리

> 이 문서의 개념을 이해하면 Phase 1 전체 내용을 따라가는 데 문제가 없습니다.

---

## 1. 패키지 (Package)

다른 개발자가 미리 만들어둔 **재사용 가능한 코드 묶음**입니다.

- 직접 모든 기능을 구현할 필요 없이, 필요한 패키지를 설치해서 `import`하면 바로 사용 가능
- 예: `pandas`(데이터 처리), `streamlit`(웹 UI), `python-dotenv`(환경변수 로딩)
- Python 패키지는 [PyPI](https://pypi.org/)라는 중앙 저장소에서 배포됨

---

## 2. 패키지 관리자 (Package Manager)

패키지의 **설치, 삭제, 버전 관리, 의존성 해결**을 자동으로 처리하는 도구입니다.

| 도구 | 특징 |
|------|------|
| `pip` | Python 기본 패키지 관리자. 느리고 의존성 관리가 약함 |
| **`uv`** | Rust 기반으로 pip 대비 10~100배 빠름. 2024년 등장한 차세대 도구 |

### uv 핵심 명령어

```bash
uv init              # 프로젝트 초기화 (pyproject.toml 생성)
uv add <패키지명>     # 패키지 추가
uv sync              # pyproject.toml 기준으로 가상환경과 패키지 동기화
uv run python <file> # 가상환경 내에서 Python 스크립트 실행
uv pip list          # 설치된 패키지 목록 확인
```

---

## 3. 가상환경 (Virtual Environment)

프로젝트마다 **독립된 Python 실행 환경**을 만드는 메커니즘입니다.

### 왜 필요한가

- 프로젝트 A가 `pandas 1.0`, 프로젝트 B가 `pandas 2.0`을 요구할 때, 가상환경 없이는 **버전 충돌**이 발생
- 가상환경을 사용하면 각 프로젝트가 자체 패키지 세트를 가지므로 충돌 없음

### 동작 방식

- `uv sync` 실행 시 프로젝트 루트에 `.venv/` 디렉토리가 자동 생성됨
- `.venv/` 안에 해당 프로젝트 전용 Python 인터프리터와 패키지가 격리 저장됨
- `uv run` 명령은 자동으로 `.venv` 환경을 사용하므로 별도 활성화 불필요

---

## 4. pyproject.toml

프로젝트의 **메타데이터와 의존성을 선언하는 설정 파일**입니다. (PEP 621 표준)

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "프로젝트 설명"
requires-python = ">=3.11"
dependencies = [
    "python-dotenv>=1.0.0",
    "pandas>=2.0.0",
]
```

- `uv add`로 패키지를 추가하면 `dependencies` 항목에 자동 반영됨
- 프로젝트를 다른 환경에서 재현할 때 이 파일 기준으로 `uv sync`하면 동일한 환경 구성 가능

---

## 5. uv.lock

`pyproject.toml`에 선언된 의존성의 **정확한 버전을 고정(lock)한 파일**입니다.

- `pyproject.toml`: "pandas 2.0 이상이면 됨" (범위 지정)
- `uv.lock`: "pandas 2.2.1을 사용함" (정확한 버전 고정)
- 팀원 간, 또는 개발/운영 환경 간 **동일한 패키지 버전**을 보장하는 역할

---

## 6. 환경변수와 `.env` 파일

### 환경변수 (Environment Variable)

운영체제 수준에서 관리되는 **key-value 형태의 설정값**입니다.

- API 키, DB 접속 정보 등 **민감 정보를 코드에 직접 작성하지 않기 위해** 사용
- `os.getenv("KEY_NAME")`으로 Python에서 읽을 수 있음

### `.env` 파일

환경변수를 **파일로 관리**하는 방식입니다.

```
# .env
TEST_KEY=hello_world
API_KEY=sk-abc123...
```

- `.gitignore`에 반드시 추가하여 Git에 올라가지 않도록 관리
- `.env.example` 파일을 템플릿으로 제공하여 필요한 키 목록만 공유

### python-dotenv

`.env` 파일을 읽어서 환경변수로 자동 로딩해주는 라이브러리입니다.

```python
from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일의 내용을 환경변수로 등록
api_key = os.getenv("API_KEY")
```

---

## 7. 레이어드 아키텍처 (Layered Architecture)

코드를 **역할(책임) 기준으로 폴더를 분리**하는 구조입니다.

| 레이어 | 폴더 | 책임 |
|--------|------|------|
| **설정** | `config/` | 환경변수, 앱 설정값 로딩 |
| **도메인** | `domain/` | 핵심 데이터 모델(엔티티) 정의 |
| **서비스** | `services/` | 외부 API 호출, 비즈니스 로직 처리 |
| **저장소** | `repositories/` | 데이터 저장/조회 (DB, 파일 등) |
| **UI** | `components/` | 사용자 화면 구성 요소 |
| **유틸** | `utils/` | 여러 레이어에서 공통으로 사용하는 함수 |

### 핵심 원칙

- 각 폴더는 **하나의 책임**만 담당
- 문제 발생 시 해당 역할의 폴더만 확인하면 되므로 **디버깅이 빠름**
- 여러 명이 동시 작업할 때 **코드 충돌 최소화**

---

## 개념 간 관계 요약

```
pyproject.toml (의존성 선언)
    ↓ uv add
uv.lock (버전 고정)
    ↓ uv sync
.venv/ (가상환경에 패키지 설치)
    ↓ uv run
Python 스크립트 실행 (import로 패키지 사용)
    ↓ load_dotenv()
.env 파일에서 환경변수 로딩
```