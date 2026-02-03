# 🐍 파이썬 던전 탈출

> TrendTracker 프로젝트에서 배운 파이썬 개념을 복습하는 터미널 기반 TRPG 퀴즈 게임

## 게임 소개

당신은 파이썬 마법을 배우는 견습 마법사입니다. 전설의 "TrendTracker 던전"에는 7명의 문지기가 있습니다. 각 문지기의 시험을 통과해야만 다음 관문으로 나아갈 수 있습니다.

모든 관문을 통과하면... 당신은 진정한 **파이썬 마법사**가 됩니다!

## 실행 방법

```bash
cd learn_python_trpd
python main.py
```

## 게임 규칙

| 규칙 | 설명 |
|------|------|
| 문제 수 | 각 관문당 10문제 (5지선다) |
| 목숨 | 2개 (2번 틀리면 게임 오버) |
| 통과 조건 | 8문제 이상 정답 |
| 인증서 | 통과 시 `output/phase_{n}_clear.txt` 생성 |

### 목숨 시스템

```
❤️ ❤️  : 2개 (시작)
❤️ 🖤  : 1개 (1번 틀림)
🖤 🖤  : 0개 (게임 오버)
```

## 학습 주제

| Phase | 문지기 | 학습 주제 |
|-------|--------|----------|
| 1 | 설정술사 엔브 | 환경 설정 (uv, 가상환경, .env) |
| 2 | 도메인 현자 클래스 | 클래스, @dataclass, 타입 힌트 |
| 3 | API 수호자 리퀘스트 | API, HTTP, 예외 처리 |
| 4 | 창고지기 레포 | 파일 I/O, CSV, pandas, Repository |
| 5 | UI 마법사 스트림릿 | Streamlit UI 컴포넌트 |
| 6 | 통합 건축가 메인 | 앱 구조, 진입점, 모드 전환 |
| 7 | 완성의 수호자 독스 | 에러 핸들링, UX, 문서화 |

## 프로젝트 구조

```
learn_python_trpd/
├── data/
│   └── trpg_script.json     # 게임 데이터 (대사, 문제)
├── doc/
│   └── _01_initial_version/
│       └── learn_python_trpg.md  # 개발 명세서
├── output/                  # 인증서 저장 폴더 (자동 생성)
│   ├── phase_1_clear.txt
│   ├── ...
│   └── python_master_certificate.txt
├── exceptions.py            # 커스텀 예외 클래스
├── models.py                # 데이터 클래스
├── certificate.py           # 인증서 관리
├── display.py               # 화면 출력 함수
├── main.py                  # 메인 게임 (진입점)
└── README.md
```

## 사용된 파이썬 개념

이 프로젝트는 다음 개념들을 활용합니다:

- **@dataclass**: Question, Guardian, Player, GameState 클래스
- **타입 힌트**: 모든 함수와 클래스에 적용
- **커스텀 예외**: GameOverError, InvalidInputError
- **파일 I/O**: JSON 로드, 인증서 저장 (with문)
- **os 모듈**: 파일 존재 확인, 경로 처리

## 게임 플레이 예시

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║          🐍 파이썬 던전에 오신 것을 환영합니다 🐍          ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

모험자의 이름을 입력하세요: 홍길동

==================================================
  ⚔️  설정술사 엔브 등장!  ⚔️
==================================================

흠... 또 한 명의 도전자가 왔군.
나는 설정술사 엔브.
이 던전의 첫 번째 관문을 지키고 있지.
...
```

## 인증서

각 Phase를 통과하면 `output/` 폴더에 인증서 파일이 생성됩니다:

- `output/phase_1_clear.txt` ~ `output/phase_7_clear.txt`: 각 Phase 통과 인증서
- `output/python_master_certificate.txt`: 모든 Phase 통과 시 최종 인증서

## 개발 명세서

자세한 개발 명세서는 [doc/_01_initial_version/learn_python_trpg.md](doc/_01_initial_version/learn_python_trpg.md)를 참고하세요.
