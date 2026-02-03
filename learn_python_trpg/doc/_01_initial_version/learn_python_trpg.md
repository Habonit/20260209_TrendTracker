# 🐍 파이썬 던전 탈출 - 개발 명세서

> **터미널 기반 TRPG 학습 퀴즈 게임**
>
> TrendTracker 프로젝트에서 배운 파이썬 개념을 복습하는 인터랙티브 게임

---

## 📋 목차

1. [게임 소개](#1-게임-소개)
2. [게임 규칙](#2-게임-규칙)
3. [사용되는 파이썬 개념](#3-사용되는-파이썬-개념)
4. [스크립트 파일 구조 (trpg_script.json)](#4-스크립트-파일-구조)
5. [데이터 구조 설계](#5-데이터-구조-설계)
6. [JSON 로딩 및 데이터 변환](#6-json-로딩-및-데이터-변환)
7. [게임 로직 구현](#7-게임-로직-구현)
8. [인증서 시스템](#8-인증서-시스템)
9. [전체 코드 구조](#9-전체-코드-구조) ⭐ **코드 복사는 여기서!**
10. [실행 방법](#10-실행-방법)
11. [부록: 확장 아이디어](#부록-확장-아이디어)

---

## 🚀 빠른 시작 (5분 완성)

> **바로 게임을 만들고 싶다면 이 섹션만 따라하세요!**

### Step 1: 폴더 생성
```bash
mkdir learn_python_trpg
cd learn_python_trpg
mkdir data
```

### Step 2: 파일 복사
[섹션 9](#9-전체-코드-구조)에서 아래 파일들의 코드를 복사하여 저장합니다:
1. `exceptions.py` → 섹션 9.3
2. `models.py` → 섹션 9.2
3. `certificate.py` → 섹션 9.4
4. `display.py` → 섹션 9.5
5. `main.py` → 섹션 9.6

### Step 3: JSON 파일 복사
`trpg_script.json` 파일을 `data/` 폴더에 복사합니다:
```
learn_python_trpg/
├── data/
│   └── trpg_script.json   ← 여기에 복사
├── main.py
├── models.py
└── ...
```

### Step 4: 실행
```bash
python main.py
```

**끝!** 이제 게임을 즐기세요! 🎮

> 나머지 섹션들은 코드가 어떻게 동작하는지 이해하고 싶을 때 읽어보세요.

---

## 1. 게임 소개

### 1.1 배경 스토리

```
당신은 파이썬 마법을 배우는 견습 마법사입니다.
전설의 "TrendTracker 던전"에는 7명의 문지기가 있습니다.
각 문지기의 시험을 통과해야만 다음 관문으로 나아갈 수 있습니다.

모든 관문을 통과하면... 당신은 진정한 파이썬 마법사가 됩니다!

하지만 조심하세요.
각 관문에서 2번 틀리면 처음부터 다시 도전해야 합니다.

당신의 여정을 시작하세요.
```

### 1.2 게임 목표

- 7개의 관문(Phase 1~7)을 모두 통과
- 각 관문에서 문지기의 10개 퀴즈를 풀이
- 모든 관문 통과 시 "파이썬 마법사" 칭호 획득

### 1.3 학습 목표

이 게임을 통해 다음 개념을 복습합니다:

| Phase | 학습 주제 |
|-------|----------|
| 1 | 환경 설정 (uv, 가상환경, .env) |
| 2 | 클래스, @dataclass, 타입 힌트 |
| 3 | API, HTTP, 예외 처리 |
| 4 | 파일 I/O, CSV, pandas, Repository |
| 5 | Streamlit UI 컴포넌트 |
| 6 | 앱 구조, 진입점, 모드 전환 |
| 7 | 에러 핸들링, UX, 문서화 |

---

## 2. 게임 규칙

### 2.1 기본 규칙

```
┌─────────────────────────────────────────────┐
│                 게임 규칙                    │
├─────────────────────────────────────────────┤
│ • 각 관문당 10문제 출제                      │
│ • 5지선다 객관식                             │
│ • 2번 틀리면 해당 관문 실패 (강제 종료)       │
│ • 8문제 이상 정답 시 통과                    │
│ • 통과 시 인증서 파일 생성                   │
│ • 이전 관문을 통과해야 다음 관문 도전 가능    │
└─────────────────────────────────────────────┘
```

### 2.2 목숨 시스템

```
❤️ ❤️  : 2개 (시작)
❤️ 🖤  : 1개 (1번 틀림)
🖤 🖤  : 0개 (2번 틀림 → 게임 오버)
```

### 2.3 통과 조건

- **통과**: 10문제 중 8문제 이상 정답 + 목숨 1개 이상 남음
- **실패**: 2번 틀림 (목숨 소진)

### 2.4 인증서 시스템

- 통과 시: `output/phase_{n}_clear.txt` 파일 생성
- 게임 시작 시 기존 인증서 확인하여 진행 상황 표시
- 인증서가 있는 관문은 다시 도전하지 않아도 됨

---

## 3. 사용되는 파이썬 개념

### 3.1 Phase 2에서 배운 개념

#### @dataclass
```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Question:
    """퀴즈 문제를 나타내는 데이터 클래스"""
    question: str           # 문제 텍스트
    choices: List[str]      # 5개의 선택지
    answer: int             # 정답 번호 (1-5)
    explanation: str        # 해설
```

#### 타입 힌트
```python
def check_answer(user_input: int, correct: int) -> bool:
    """정답 여부를 확인합니다."""
    return user_input == correct

def get_questions(phase: int) -> List[Question]:
    """해당 phase의 문제 리스트를 반환합니다."""
    pass
```

### 3.2 Phase 3에서 배운 개념

#### 커스텀 예외
```python
class GameOverError(Exception):
    """목숨을 모두 소진했을 때 발생하는 예외"""
    def __init__(self, phase: int, question_num: int):
        self.phase = phase
        self.question_num = question_num
        super().__init__(f"Phase {phase}의 {question_num}번 문제에서 탈락")

class InvalidInputError(Exception):
    """잘못된 입력이 들어왔을 때 발생하는 예외"""
    pass
```

#### 예외 처리
```python
def get_user_choice() -> int:
    """사용자 입력을 받고 유효성을 검사합니다."""
    try:
        choice = int(input("정답을 선택하세요 (1-5): "))
        if choice < 1 or choice > 5:
            raise InvalidInputError("1~5 사이의 숫자를 입력하세요.")
        return choice
    except ValueError:
        raise InvalidInputError("숫자를 입력해주세요.")
```

### 3.3 Phase 4에서 배운 개념

#### 파일 입출력 (with문)
```python
def save_certificate(player_name: str, phase: int, guardian_name: str) -> None:
    """통과 인증서를 파일로 저장합니다."""
    import os
    os.makedirs("output", exist_ok=True)
    filename = f"output/phase_{phase}_clear.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"{'='*50}\n")
        f.write(f"     🎉 {guardian_name}의 인증서 🎉\n")
        f.write(f"{'='*50}\n\n")
        f.write(f"축하합니다, {player_name}님!\n")
        # ... 축하 메시지
```

#### 파일 존재 확인
```python
import os

def check_cleared_phases() -> List[int]:
    """통과한 phase 목록을 반환합니다."""
    cleared = []
    for i in range(1, 8):
        if os.path.exists(f"output/phase_{i}_clear.txt"):
            cleared.append(i)
    return cleared
```

#### JSON 파일 읽기
```python
import json
import os

def get_script_path() -> str:
    """스크립트 파일 경로를 반환합니다."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "data", "trpg_script.json")

def load_script(filepath: str = None) -> dict:
    """게임 스크립트 JSON 파일을 로드합니다."""
    if filepath is None:
        filepath = get_script_path()
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# 사용 예
script = load_script()
print(script["meta"]["title"])  # "파이썬 던전 탈출"
```

---

## 4. 스크립트 파일 구조

### 4.1 trpg_script.json 개요

모든 게임 대사, 문지기 캐릭터, 퀴즈 데이터는 `trpg_script.json` 파일에 저장됩니다.
이렇게 하면:
- 코드와 콘텐츠가 분리되어 유지보수가 쉬움
- 다국어 지원이 필요할 때 JSON 파일만 교체하면 됨
- 퀴즈 추가/수정 시 코드 변경 없이 JSON만 수정

### 4.2 JSON 최상위 구조

```json
{
  "meta": { ... },           // 게임 메타 정보
  "intro": { ... },          // 게임 시작 화면 텍스트
  "menu": { ... },           // 관문 선택 메뉴 텍스트
  "quiz": { ... },           // 퀴즈 진행 관련 텍스트
  "result": { ... },         // 시험 결과 화면 텍스트
  "game_over": { ... },      // 게임 오버 화면 텍스트
  "certificate": { ... },    // 인증서 템플릿
  "exit": { ... },           // 종료 메시지
  "final_ending": { ... },   // 전체 클리어 엔딩
  "phases": {                // Phase 1~7 데이터
    "1": { ... },
    "2": { ... },
    ...
    "7": { ... }
  }
}
```

### 4.3 Phase 데이터 구조

각 Phase는 문지기 정보와 10개의 퀴즈를 포함합니다:

```json
{
  "1": {
    "title": "환경 설정",
    "guardian": {
      "name": "설정술사 엔브",
      "greeting": ["대사 라인1", "대사 라인2", ...],
      "success": ["통과 시 대사 라인들..."],
      "failure": ["실패 시 대사 라인들..."],
      "certificate_message": "인증서에 들어갈 특별 메시지"
    },
    "questions": [
      {
        "question": "문제 텍스트",
        "choices": ["선택지1", "선택지2", "선택지3", "선택지4", "선택지5"],
        "answer": 1,
        "explanation": "정답 해설"
      },
      // ... 총 10개 문제
    ]
  }
}
```

### 4.4 UI 텍스트 구조

게임에서 사용되는 모든 텍스트가 JSON에 정의되어 있습니다:

```json
{
  "quiz": {
    "correct": "\n✅ 정답입니다!",
    "wrong": "\n❌ 오답입니다! 정답은 {answer}번입니다.",
    "explanation": "\n📖 해설: {explanation}",
    "lives_display": {
      "2": "❤️ ❤️",
      "1": "❤️ 🖤",
      "0": "🖤 🖤"
    }
  }
}
```

---

## 5. 데이터 구조 설계

> **이 섹션의 목표**: JSON 데이터를 파이썬 객체로 변환하는 데이터 클래스를 설계합니다.

### 5.1 Question (문제)

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Question:
    """
    퀴즈 문제를 나타내는 데이터 클래스
    JSON의 questions 배열 요소에서 생성됩니다.

    Attributes:
        question: 문제 텍스트
        choices: 5개의 선택지 리스트
        answer: 정답 번호 (1-5)
        explanation: 정답 해설
    """
    question: str
    choices: List[str]
    answer: int
    explanation: str

    @classmethod
    def from_dict(cls, data: dict) -> "Question":
        """딕셔너리(JSON)에서 Question 객체를 생성합니다."""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            explanation=data["explanation"]
        )

    def display(self, number: int) -> None:
        """문제를 화면에 출력합니다."""
        print(f"\nQ{number}. {self.question}")
        print("-" * 40)
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}) {choice}")
        print()
```

### 5.2 Guardian (문지기)

```python
@dataclass
class Guardian:
    """
    문지기를 나타내는 데이터 클래스
    JSON의 phases.{n}.guardian 객체에서 생성됩니다.

    Attributes:
        name: 문지기 이름
        phase: 담당 phase 번호
        greeting: 등장 대사 (리스트 → 줄바꿈 조인)
        success_message: 통과 시 대사 (리스트 → 줄바꿈 조인)
        failure_message: 실패 시 대사 (리스트 → 줄바꿈 조인)
        certificate_message: 인증서 특별 메시지
        questions: 출제할 문제 리스트
    """
    name: str
    phase: int
    greeting: str
    success_message: str
    failure_message: str
    certificate_message: str
    questions: List[Question]

    @classmethod
    def from_dict(cls, phase: int, data: dict) -> "Guardian":
        """딕셔너리(JSON)에서 Guardian 객체를 생성합니다."""
        guardian_data = data["guardian"]
        questions = [
            Question.from_dict(q) for q in data["questions"]
        ]

        return cls(
            name=guardian_data["name"],
            phase=phase,
            greeting="\n".join(guardian_data["greeting"]),
            success_message="\n".join(guardian_data["success"]),
            failure_message="\n".join(guardian_data["failure"]),
            certificate_message=guardian_data.get("certificate_message", ""),
            questions=questions
        )

    def greet(self) -> None:
        """문지기 등장 대사를 출력합니다."""
        print(f"\n{'='*50}")
        print(f"  ⚔️  {self.name} 등장!  ⚔️")
        print(f"{'='*50}")
        print(self.greeting)

    def congratulate(self, player_name: str) -> None:
        """통과 축하 대사를 출력합니다."""
        message = self.success_message.replace("{name}", player_name)
        print(f"\n{message}")

    def mock(self, player_name: str) -> None:
        """실패 대사를 출력합니다."""
        message = self.failure_message.replace("{name}", player_name)
        print(f"\n{message}")
```

### 5.3 Player (플레이어)

```python
from dataclasses import dataclass, field

@dataclass
class Player:
    """
    플레이어 정보를 나타내는 데이터 클래스

    Attributes:
        name: 플레이어 이름
        current_phase: 현재 도전 중인 phase
        lives: 남은 목숨 (기본 2)
        correct_count: 현재 phase에서 맞춘 문제 수
        cleared_phases: 통과한 phase 리스트
    """
    name: str
    current_phase: int = 1
    lives: int = 2
    correct_count: int = 0
    cleared_phases: List[int] = field(default_factory=list)

    def reset_for_new_phase(self) -> None:
        """새 phase 시작 시 상태를 초기화합니다."""
        self.lives = 2
        self.correct_count = 0

    def lose_life(self) -> None:
        """목숨을 1개 잃습니다."""
        self.lives -= 1

    def add_correct(self) -> None:
        """정답 카운트를 1 증가시킵니다."""
        self.correct_count += 1

    def is_game_over(self) -> bool:
        """게임 오버 여부를 반환합니다."""
        return self.lives <= 0

    def get_lives_display(self, script: dict) -> str:
        """현재 목숨을 이모지로 반환합니다."""
        return script["quiz"]["lives_display"].get(str(self.lives), "🖤 🖤")
```

### 5.4 GameState (게임 상태)

```python
@dataclass
class GameState:
    """
    전체 게임 상태를 관리하는 데이터 클래스

    Attributes:
        player: 플레이어 정보
        guardians: 모든 문지기 딕셔너리 (phase 번호 → Guardian)
        script: 로드된 JSON 스크립트
        is_running: 게임 실행 중 여부
    """
    player: Player
    guardians: dict  # {1: Guardian, 2: Guardian, ...}
    script: dict     # 로드된 JSON 전체
    is_running: bool = True

    @classmethod
    def from_script(cls, player: Player, script: dict) -> "GameState":
        """JSON 스크립트에서 GameState를 생성합니다."""
        guardians = {}
        for phase_str, phase_data in script["phases"].items():
            phase = int(phase_str)
            guardians[phase] = Guardian.from_dict(phase, phase_data)

        return cls(
            player=player,
            guardians=guardians,
            script=script
        )

    def get_guardian(self, phase: int) -> Guardian:
        """해당 phase의 문지기를 반환합니다."""
        return self.guardians[phase]

    def get_next_available_phase(self) -> int:
        """도전 가능한 다음 phase를 반환합니다."""
        for i in range(1, 8):
            if i not in self.player.cleared_phases:
                return i
        return -1  # 모든 phase 클리어

    def get_text(self, *keys: str) -> str:
        """스크립트에서 텍스트를 가져옵니다."""
        result = self.script
        for key in keys:
            result = result[key]
        if isinstance(result, list):
            return "\n".join(result)
        return result
```

---

## 6. JSON 로딩 및 데이터 변환

### 6.1 스크립트 로더

> **참고**: 아래 코드는 `main.py`에 포함됩니다. 섹션 9.6의 전체 코드를 참조하세요.

```python
import json
import os
from models import Player, GameState


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

    Raises:
        FileNotFoundError: 파일이 없는 경우
        json.JSONDecodeError: JSON 파싱 실패 시
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
```

**GameState 생성 예시** (`main.py`의 `main()` 함수 내부):

```python
# 기존 클리어 현황 확인
from certificate import check_cleared_phases
cleared_phases = check_cleared_phases()

# 플레이어 생성
player = Player(name=player_name, cleared_phases=cleared_phases)

# GameState 생성 (Guardian들은 from_script에서 자동 생성)
game = GameState.from_script(player, script)
```

### 6.2 텍스트 출력 헬퍼

> **참고**: 전체 코드는 섹션 9.5를 참조하세요.

```python
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
```

### 6.3 문지기 캐릭터 (JSON에서 로드)

> **참고**: 모든 문지기 캐릭터와 대사는 `trpg_script.json`에 정의되어 있습니다.

JSON에서 문지기를 로드하면 다음과 같은 장점이 있습니다:

1. **코드와 콘텐츠 분리**: 대사를 수정할 때 Python 코드를 건드리지 않아도 됨
2. **다국어 지원 용이**: 언어별 JSON 파일만 교체하면 됨
3. **콘텐츠 관리 용이**: 기획자/작가가 코드 없이 대사 수정 가능

각 Phase의 문지기 캐릭터:

| Phase | 문지기 이름 | 성격 |
|-------|------------|------|
| 1 | 설정술사 엔브 | 깐깐하고 꼼꼼함 |
| 2 | 도메인 현자 클래스 | 고풍스럽고 지적 |
| 3 | API 수호자 리퀘스트 | 활발하고 친근함 |
| 4 | 창고지기 레포 | 무뚝뚝하지만 다정함 |
| 5 | UI 마법사 스트림릿 | 화려하고 쇼맨십 |
| 6 | 통합 건축가 메인 | 엄격하고 체계적 |
| 7 | 완성의 수호자 독스 | 온화하고 격려함 |

### 6.4 퀴즈 데이터 (JSON에서 로드)

> **참고**: 모든 퀴즈 데이터(70개 문제)는 `trpg_script.json`에 정의되어 있습니다.

각 Phase별 퀴즈 주제:

| Phase | 주제 | 문제 수 |
|-------|------|--------|
| 1 | 환경 설정 (uv, venv, .env) | 10 |
| 2 | 클래스, @dataclass, 타입 힌트 | 10 |
| 3 | API, HTTP, 예외 처리 | 10 |
| 4 | 파일 I/O, CSV, pandas, Repository | 10 |
| 5 | Streamlit UI 컴포넌트 | 10 |
| 6 | 앱 구조, 진입점, 모드 전환 | 10 |
| 7 | 에러 핸들링, UX, 문서화 | 10 |

---

## 7. 게임 로직 구현

> **참고**: 전체 코드는 섹션 9.6 (`main.py`)을 참조하세요.

### 7.1 메인 게임 루프

```python
from models import Player, GameState
from exceptions import GameOverError
from certificate import check_cleared_phases, save_certificate, save_master_certificate
from display import print_lines, print_intro, print_menu, print_quiz_header, print_result, print_final_ending


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
```

### 7.2 Phase 플레이 로직

```python
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
```

### 7.3 사용자 입력 처리

```python
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
```

---

## 8. 인증서 시스템

### 8.1 인증서 확인

```python
# 인증서 저장 폴더
OUTPUT_DIR = "output"

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
```

### 8.2 인증서 저장

```python
def ensure_output_dir() -> None:
    """output 폴더가 없으면 생성합니다."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def save_certificate(player_name: str, phase: int, guardian_name: str) -> None:
    """
    통과 인증서를 파일로 저장합니다.

    Args:
        player_name: 플레이어 이름
        phase: 통과한 phase 번호
        guardian_name: 문지기 이름
    """
    from datetime import datetime
    ensure_output_dir()

    filepath = os.path.join(OUTPUT_DIR, f"phase_{phase}_clear.txt")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""
{'='*50}
     🎉 {guardian_name}의 인증서 🎉
{'='*50}

축하합니다, {player_name}님!

Phase {phase}의 시험을 통과하셨습니다.
당신의 파이썬 실력이 한 단계 성장했습니다!

이 인증서는 당신이 이 관문을 정복했음을 증명합니다.

통과 일시: {now}

- {guardian_name} -
{'='*50}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n📜 인증서가 저장되었습니다: {filepath}")
```

### 8.3 최종 인증서 (모든 Phase 클리어)

```python
def save_master_certificate(player_name: str) -> None:
    """
    모든 phase 클리어 시 최종 인증서를 발급합니다.

    Args:
        player_name: 플레이어 이름
    """
    from datetime import datetime
    ensure_output_dir()

    filepath = os.path.join(OUTPUT_DIR, "python_master_certificate.txt")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"""
{'='*60}

        🏆 파이썬 마법사 인증서 🏆

{'='*60}

    이 인증서는

                {player_name}

    님이 파이썬 던전의 모든 관문을 통과하고
    진정한 파이썬 마법사가 되었음을 증명합니다.

{'='*60}

    ✅ Phase 1: 환경 설정 - 통과
    ✅ Phase 2: 클래스와 타입 - 통과
    ✅ Phase 3: API와 예외처리 - 통과
    ✅ Phase 4: 파일과 데이터 - 통과
    ✅ Phase 5: Streamlit UI - 통과
    ✅ Phase 6: 앱 구조 - 통과
    ✅ Phase 7: 에러 핸들링 - 통과

{'='*60}

    발급일: {now}

    "코드의 힘이 당신과 함께하길"

        - TrendTracker 던전 마스터 일동 -

{'='*60}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n🏆 최종 인증서가 발급되었습니다: {filepath}")
```

---

## 9. 전체 코드 구조

### 9.1 파일 구조

```
learn_python_trpg/
├── data/
│   └── trpg_script.json # 게임 데이터 (제공됨)
├── main.py              # 메인 게임 파일 (진입점)
├── models.py            # 데이터 클래스 정의
├── exceptions.py        # 커스텀 예외
├── certificate.py       # 인증서 관리
└── display.py           # 화면 출력 함수
```

> **중요**: `trpg_script.json` 파일은 이미 제공됩니다. `data/` 폴더를 만들고 그 안에 복사하세요.

### 9.1.1 개발 순서 (권장)

아래 순서대로 파일을 만들면 됩니다:

1. **exceptions.py** - 가장 간단하고 다른 파일에서 사용됨
2. **models.py** - 데이터 클래스 정의, exceptions.py를 사용
3. **certificate.py** - 인증서 저장/확인 기능
4. **display.py** - 화면 출력 함수들
5. **main.py** - 모든 모듈을 조합하는 메인 파일

### 9.2 models.py

> **복사해서 `models.py` 파일로 저장하세요.**

```python
"""
models.py
게임에서 사용하는 데이터 모델 정의
Phase 2에서 배운 @dataclass, 타입 힌트 적용
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Question:
    """
    퀴즈 문제를 나타내는 데이터 클래스

    Attributes:
        question: 문제 텍스트
        choices: 5개의 선택지 리스트
        answer: 정답 번호 (1-5)
        explanation: 정답 해설
    """
    question: str
    choices: List[str]
    answer: int
    explanation: str

    @classmethod
    def from_dict(cls, data: dict) -> "Question":
        """딕셔너리(JSON)에서 Question 객체를 생성합니다."""
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            explanation=data["explanation"]
        )

    def display(self, number: int) -> None:
        """문제를 화면에 출력합니다."""
        print(f"\nQ{number}. {self.question}")
        print("-" * 40)
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}) {choice}")
        print()


@dataclass
class Guardian:
    """
    문지기를 나타내는 데이터 클래스

    Attributes:
        name: 문지기 이름
        phase: 담당 phase 번호
        greeting: 등장 대사
        success_message: 통과 시 대사
        failure_message: 실패 시 대사
        certificate_message: 인증서 특별 메시지
        questions: 출제할 문제 리스트
    """
    name: str
    phase: int
    greeting: str
    success_message: str
    failure_message: str
    certificate_message: str
    questions: List[Question] = field(default_factory=list)

    @classmethod
    def from_dict(cls, phase: int, data: dict) -> "Guardian":
        """딕셔너리(JSON)에서 Guardian 객체를 생성합니다."""
        guardian_data = data["guardian"]
        questions = [
            Question.from_dict(q) for q in data["questions"]
        ]

        return cls(
            name=guardian_data["name"],
            phase=phase,
            greeting="\n".join(guardian_data["greeting"]),
            success_message="\n".join(guardian_data["success"]),
            failure_message="\n".join(guardian_data["failure"]),
            certificate_message=guardian_data.get("certificate_message", ""),
            questions=questions
        )

    def greet(self) -> None:
        """문지기 등장 대사를 출력합니다."""
        print(f"\n{'='*50}")
        print(f"  ⚔️  {self.name} 등장!  ⚔️")
        print(f"{'='*50}")
        print(self.greeting)

    def congratulate(self, player_name: str) -> None:
        """통과 축하 대사를 출력합니다."""
        message = self.success_message.replace("{name}", player_name)
        print(f"\n{message}")

    def mock(self, player_name: str) -> None:
        """실패 대사를 출력합니다."""
        message = self.failure_message.replace("{name}", player_name)
        print(f"\n{message}")


@dataclass
class Player:
    """
    플레이어 정보를 나타내는 데이터 클래스

    Attributes:
        name: 플레이어 이름
        current_phase: 현재 도전 중인 phase
        lives: 남은 목숨 (기본 2)
        correct_count: 현재 phase에서 맞춘 문제 수
        cleared_phases: 통과한 phase 리스트
    """
    name: str
    current_phase: int = 1
    lives: int = 2
    correct_count: int = 0
    cleared_phases: List[int] = field(default_factory=list)

    def reset_for_new_phase(self) -> None:
        """새 phase 시작 시 상태를 초기화합니다."""
        self.lives = 2
        self.correct_count = 0

    def lose_life(self) -> None:
        """목숨을 1개 잃습니다."""
        self.lives -= 1

    def add_correct(self) -> None:
        """정답 카운트를 1 증가시킵니다."""
        self.correct_count += 1

    def is_game_over(self) -> bool:
        """게임 오버 여부를 반환합니다."""
        return self.lives <= 0

    def get_lives_display(self, script: dict) -> str:
        """현재 목숨을 이모지로 반환합니다."""
        return script["quiz"]["lives_display"].get(str(self.lives), "🖤 🖤")


@dataclass
class GameState:
    """
    전체 게임 상태를 관리하는 데이터 클래스

    Attributes:
        player: 플레이어 정보
        guardians: 모든 문지기 딕셔너리 (phase 번호 → Guardian)
        script: 로드된 JSON 스크립트
        is_running: 게임 실행 중 여부
    """
    player: Player
    guardians: dict  # {1: Guardian, 2: Guardian, ...}
    script: dict     # 로드된 JSON 전체
    is_running: bool = True

    @classmethod
    def from_script(cls, player: Player, script: dict) -> "GameState":
        """JSON 스크립트에서 GameState를 생성합니다."""
        guardians = {}
        for phase_str, phase_data in script["phases"].items():
            phase = int(phase_str)
            guardians[phase] = Guardian.from_dict(phase, phase_data)

        return cls(
            player=player,
            guardians=guardians,
            script=script
        )

    def get_guardian(self, phase: int) -> Guardian:
        """해당 phase의 문지기를 반환합니다."""
        return self.guardians[phase]

    def get_next_available_phase(self) -> int:
        """도전 가능한 다음 phase를 반환합니다."""
        for i in range(1, 8):
            if i not in self.player.cleared_phases:
                return i
        return -1  # 모든 phase 클리어
```

### 9.3 exceptions.py

> **복사해서 `exceptions.py` 파일로 저장하세요.**

```python
"""
exceptions.py
커스텀 예외 클래스 정의
Phase 3에서 배운 예외 처리 적용
"""


class GameOverError(Exception):
    """목숨을 모두 소진했을 때 발생하는 예외"""

    def __init__(self, phase: int, question_num: int):
        self.phase = phase
        self.question_num = question_num
        super().__init__(
            f"Phase {phase}의 {question_num}번 문제에서 탈락"
        )


class InvalidInputError(Exception):
    """잘못된 입력이 들어왔을 때 발생하는 예외"""
    pass
```

### 9.4 certificate.py

> **복사해서 `certificate.py` 파일로 저장하세요.**

```python
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

    filepath = os.path.join(OUTPUT_DIR, f"phase_{phase}_clear.txt")
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

    filepath = os.path.join(OUTPUT_DIR, "python_master_certificate.txt")
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
```

### 9.5 display.py

> **복사해서 `display.py` 파일로 저장하세요.**

```python
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
```

### 9.6 main.py (메인 파일)

> **복사해서 `main.py` 파일로 저장하세요. 이 파일이 게임의 진입점입니다.**

```python
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
```

---

## 10. 실행 방법

### 10.1 파일 준비

아래 순서대로 파일을 준비합니다:

1. **폴더 생성**: `learn_python_trpg` 폴더와 `data` 하위 폴더를 만듭니다.
   ```bash
   mkdir learn_python_trpg
   cd learn_python_trpg
   mkdir data
   ```
2. **파일 복사**: 섹션 9의 코드를 각 파일로 저장합니다.
   - `exceptions.py` (섹션 9.3)
   - `models.py` (섹션 9.2)
   - `certificate.py` (섹션 9.4)
   - `display.py` (섹션 9.5)
   - `main.py` (섹션 9.6)
3. **JSON 파일 복사**: `trpg_script.json` 파일을 `data/` 폴더에 복사합니다.

최종 폴더 구조:
```
learn_python_trpg/
├── data/
│   └── trpg_script.json
├── main.py
├── models.py
├── exceptions.py
├── certificate.py
└── display.py
```

### 10.2 실행

```bash
# 폴더로 이동
cd learn_python_trpg

# 게임 실행
python main.py
```

또는 uv 사용 시:

```bash
uv run python main.py
```

> **참고**: 이 게임은 표준 라이브러리만 사용하므로 별도의 패키지 설치가 필요 없습니다.

### 10.3 게임 플레이

```
========================================
  🐍 파이썬 던전에 오신 것을 환영합니다!
========================================

모험자의 이름을 입력하세요: 홍길동

========================================
  📜 관문 선택
========================================
  1. Phase 1 - 🔓 도전 가능
  2. Phase 2 - 🔒 잠김
  3. Phase 3 - 🔒 잠김
  ...
  0. 게임 종료
========================================

도전할 관문을 선택하세요 (다음: 1): 1

==================================================
  ⚔️  설정술사 엔브 등장!  ⚔️
==================================================

흠... 또 한 명의 도전자가 왔군.
...

[Enter를 눌러 시험을 시작하세요]
```

---

## 부록: 확장 아이디어

### A. 난이도 선택

```python
DIFFICULTY = {
    "easy": {"lives": 3, "pass_score": 6},
    "normal": {"lives": 2, "pass_score": 8},
    "hard": {"lives": 1, "pass_score": 10},
}
```

### B. 힌트 시스템

```python
@dataclass
class Question:
    # ... 기존 필드
    hint: str = ""  # 힌트 추가

    def show_hint(self) -> None:
        if self.hint:
            print(f"💡 힌트: {self.hint}")
```

### C. 점수 시스템

```python
@dataclass
class Player:
    # ... 기존 필드
    total_score: int = 0

    def calculate_score(self) -> int:
        """점수 계산: 정답 수 × 10 + 남은 목숨 × 5"""
        return self.correct_count * 10 + self.lives * 5
```

### D. 랭킹 시스템

```python
def save_ranking(player_name: str, score: int) -> None:
    """랭킹을 파일에 저장합니다."""
    with open("ranking.txt", "a", encoding="utf-8") as f:
        f.write(f"{player_name},{score},{datetime.now()}\n")
```

---

## 📝 개발 체크리스트

아래 순서대로 파일을 만들고 체크하세요:

- [ ] `data/` 폴더 생성
- [ ] `data/trpg_script.json` - 게임 데이터 파일 복사 확인
- [ ] `exceptions.py` - 커스텀 예외 클래스 (GameOverError, InvalidInputError)
- [ ] `models.py` - 데이터 클래스 (Question, Guardian, Player, GameState)
- [ ] `certificate.py` - 인증서 저장/조회 기능
- [ ] `display.py` - 화면 출력 함수들
- [ ] `main.py` - 메인 게임 루프
- [ ] 테스트 - 게임 실행하여 Phase 1 플레이해보기

---

## 💡 자주 발생하는 오류와 해결법

### ModuleNotFoundError
```
ModuleNotFoundError: No module named 'models'
```
**원인**: 파일이 같은 폴더에 없거나 파일명이 다름
**해결**: 모든 `.py` 파일이 같은 폴더에 있고, `trpg_script.json`이 `data/` 폴더 안에 있는지 확인

### FileNotFoundError
```
스크립트 파일을 찾을 수 없습니다: .../data/trpg_script.json
```
**원인**: JSON 파일이 없거나 `data/` 폴더에 없음
**해결**: `data/` 폴더를 만들고 그 안에 `trpg_script.json` 파일을 복사

### JSONDecodeError
```
JSON 파싱 오류: ...
```
**원인**: JSON 파일이 손상되었거나 형식이 잘못됨
**해결**: 원본 `trpg_script.json` 파일을 다시 복사

---

**작성일**: 2026-02-03
**버전**: 1.0.0
**작성자**: TrendTracker 교육팀
