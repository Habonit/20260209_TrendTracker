# Python 입문 튜토리얼

## 소개
Python을 처음 배우는 분들을 위한 Jupyter Notebook 기반 튜토리얼입니다.
각 Step은 **이론 → 실습 → 챌린지** 3단계로 구성되어 있습니다.

## 환경 설정

### 사전 요구사항
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (패키지 관리자)

### 설치 및 실행

1. **uv 설치** (아직 없다면)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **의존성 설치**
```bash
cd python_tutorial
uv sync
```

3. **Jupyter 커널 등록**
```bash
uv run python -m ipykernel install --user --name python-tutorial --display-name "Python Tutorial"
```

4. **노트북 실행**
```bash
uv run jupyter notebook
```

## 커리큘럼

| Step | 파일명 | 학습 내용 |
|---|---|---|
| 1 | Step1_Basic_Syntax.ipynb | 변수, 자료형, 연산자, 문자열, 입출력 |
| 2 | Step2_Control_Flow.ipynb | 조건문, 반복문, 컴프리헨션 |
| 3 | Step3_Data_Structures.ipynb | 리스트, 튜플, 집합, 딕셔너리 |
| 4 | Step4_Functions_and_Modules.ipynb | 함수, 스코프, 람다, 모듈 |
| 5 | Step5_Intermediate.ipynb | 파일 I/O, 예외 처리, 클래스 |
| 6 | Step6_Projects.ipynb | 계산기, 가위바위보, pandas 분석 |

## 학습 방법
- **이론**: 마크다운 설명을 읽고 코드셀을 실행하며 학습
- **실습**: 직접 코드를 작성한 후 주석 해제로 정답 확인
- **챌린지**: TODO 힌트만 보고 독립적으로 풀기 (강사와 함께 리뷰)
