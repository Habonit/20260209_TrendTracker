# Step 5: 중급 진입

## 학습 목표
- 파일을 읽고 쓰는 방법을 익힌다
- 예외 처리로 안정적인 프로그램을 만든다
- 클래스와 객체 지향 프로그래밍의 기초를 이해한다

---

## 1. 파일 입출력

### 파일 열기 모드

| 모드 | 설명 |
|------|------|
| `'r'` | 읽기 (기본값) |
| `'w'` | 쓰기 (덮어쓰기) |
| `'a'` | 추가 (append) |
| `'r+'` | 읽기+쓰기 |

### with 문 (컨텍스트 매니저)

`with`를 사용하면 블록을 나갈 때 자동으로 `f.close()`가 호출된다.

```python
with open('파일경로', '모드', encoding='utf-8') as f:
    # 파일 작업
```

### 텍스트 파일 쓰기와 읽기

```python
# 쓰기
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("첫 번째 줄\n")
    f.write("두 번째 줄\n")
    f.write("세 번째 줄\n")

# 읽기 - 전체
with open("sample.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# 읽기 - 한 줄씩
with open("sample.txt", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"{i}번째 줄: {line.strip()}")
```

### CSV 파일

```python
import csv

# CSV 쓰기
with open("students.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["이름", "국어", "영어", "수학"])
    writer.writerow(["홍길동", 90, 85, 88])

# CSV 읽기 (DictReader: 헤더를 키로 사용)
with open("students.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['이름']}: 국어 {row['국어']}")
```

### JSON 파일

```python
import json

data = {
    "name": "홍길동",
    "age": 25,
    "hobbies": ["독서", "코딩", "운동"],
    "address": {"city": "서울", "district": "강남구"}
}

# JSON 쓰기
with open("profile.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# JSON 읽기
with open("profile.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
    print(loaded["name"])
    print(loaded["address"]["city"])
```

> `ensure_ascii=False`: 한글이 유니코드 이스케이프 없이 저장됨
> `indent=2`: 들여쓰기로 보기 좋게 저장

---

## 2. 예외 처리

### 주요 에러 종류

| 에러 | 원인 |
|------|------|
| `SyntaxError` | 문법 오류 |
| `TypeError` | 자료형 불일치 |
| `ValueError` | 잘못된 값 |
| `KeyError` | 없는 딕셔너리 키 |
| `IndexError` | 범위 초과 인덱스 |
| `ZeroDivisionError` | 0으로 나누기 |
| `FileNotFoundError` | 없는 파일 |

### try / except / else / finally

```python
try:
    # 에러가 발생할 수 있는 코드
    result = 10 / 0
except ZeroDivisionError as e:
    # 특정 에러 처리
    print(f"에러 발생: {e}")
else:
    # 에러가 없을 때만 실행
    print(f"결과: {result}")
finally:
    # 항상 실행 (에러 유무와 관계없이)
    print("계산 완료!")
```

### 다중 except

```python
try:
    num = int("abc")
except ValueError:
    print("숫자로 변환할 수 없습니다")
except TypeError:
    print("타입이 올바르지 않습니다")
```

### raise: 의도적으로 에러 발생

```python
def set_age(age):
    if age < 0:
        raise ValueError("나이는 음수가 될 수 없습니다")
    return age

try:
    set_age(-5)
except ValueError as e:
    print(f"에러: {e}")
```

### 실전: 안전한 나누기

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

print(safe_divide(10, 3))  # 3.333...
print(safe_divide(10, 0))  # None
```

---

## 3. 클래스 기초

### 클래스란?
클래스는 **객체를 만드는 설계도**이다. 관련 데이터(속성)와 기능(메서드)을 하나로 묶는다.

### 기본 구조

```python
class 클래스이름:
    def __init__(self, 속성들):
        self.속성 = 값

    def 메서드(self):
        # 동작
```

### 주요 개념

| 개념 | 설명 |
|------|------|
| `__init__` | 생성자 (인스턴스 초기화 메서드) |
| `self` | 인스턴스 자신을 가리킴 |
| `__str__` | 문자열 표현 (`print` 시 사용) |
| 상속 | 부모 클래스 기능 물려받기 |

### 클래스 정의와 인스턴스 생성

```python
class Dog:
    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

    def bark(self):
        return f"{self.name}(이)가 멍멍! 짖습니다"

    def info(self):
        return f"{self.name} | {self.breed} | {self.age}세"

    def __str__(self):
        return f"{self.name} ({self.breed}, {self.age}세)"

# 인스턴스 생성
dog1 = Dog("바둑이", "진돗개", 3)
dog2 = Dog("초코", "푸들", 2)

print(dog1.bark())   # 바둑이(이)가 멍멍! 짖습니다
print(dog2.info())   # 초코 | 푸들 | 2세
print(dog1)          # 바둑이 (진돗개, 3세)  ← __str__ 호출
```

### 상속 (Inheritance)

부모 클래스의 속성과 메서드를 자식 클래스에서 물려받아 사용한다.

```python
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name}(이)가 {self.sound}!"

class Cat(Animal):  # Animal 상속
    def __init__(self, name, indoor=True):
        super().__init__(name, "야옹")  # 부모 __init__ 호출
        self.indoor = indoor

    def purr(self):
        return f"{self.name}(이)가 그르르르..."

kitty = Cat("나비")
print(kitty.speak())    # 부모 메서드 사용: 나비(이)가 야옹!
print(kitty.purr())     # 자식 메서드: 나비(이)가 그르르르...
print(kitty.indoor)     # True
isinstance(kitty, Animal)  # True
```

### 상속의 핵심
- `class 자식(부모):` 형태로 상속 선언
- `super().__init__(...)` 으로 부모 생성자 호출
- 자식 클래스에서 부모 메서드를 그대로 사용하거나 재정의(오버라이딩) 가능
- `isinstance(객체, 클래스)` 로 상속 관계 확인 가능

---

## 실습 문제

### 실습 1: 텍스트/JSON 파일 다루기

```python
# 1. 텍스트 파일
with open("memo.txt", "w", encoding="utf-8") as f:
    f.write("오늘의 할일:\n")
    f.write("1. 파이썬 공부\n")
    f.write("2. 운동하기\n")

with open("memo.txt", "r", encoding="utf-8") as f:
    print(f.read())

# 2. JSON 파일
import json
config = {"theme": "dark", "font_size": 14, "language": "ko"}

with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

with open("config.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
    print(loaded)
```

---

### 실습 2: 예외 처리 연습

다양한 에러를 의도적으로 발생시키고 처리해보세요.

```python
# 1. ZeroDivisionError
try:
    print(10 / 0)
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다")

# 2. IndexError
try:
    lst = [1, 2, 3]
    print(lst[10])
except IndexError:
    print("인덱스 범위를 벗어났습니다")

# 3. KeyError
try:
    d = {"name": "홍길동"}
    print(d["age"])
except KeyError as e:
    print(f"없는 키: {e}")

# 4. ValueError
try:
    num = int("hello")
except ValueError:
    print("숫자로 변환할 수 없습니다")
```

---

### 실습 3: Student 클래스 작성

이름, 학년, 성적 리스트를 가진 Student 클래스를 만드세요.

```python
class Student:
    def __init__(self, name, grade, scores):
        self.name = name
        self.grade = grade
        self.scores = scores

    def average(self):
        return sum(self.scores) / len(self.scores)

    def highest(self):
        return max(self.scores)

    def __str__(self):
        return f"{self.name} ({self.grade}학년) - 평균: {self.average():.1f}"

s1 = Student("홍길동", 2, [90, 85, 88])
s2 = Student("김철수", 3, [78, 92, 85])
print(s1)    # 홍길동 (2학년) - 평균: 87.7
print(s2)    # 김철수 (3학년) - 평균: 85.0
print(f"{s1.name}의 최고 점수: {s1.highest()}")
```

---

## 핵심 요약

| 개념 | 핵심 내용 |
|------|----------|
| **파일 I/O** | `open()`, `with` 문, `read()`, `write()`, `csv` 모듈, `json` 모듈 |
| **예외 처리** | `try` / `except` / `else` / `finally`, `raise`, 에러 타입별 처리 |
| **클래스** | `class`, `__init__`, `self`, `__str__`, 상속, `super()`, `isinstance()` |
