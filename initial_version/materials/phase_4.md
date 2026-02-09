# Phase 4: 리포지토리 레이어 - 데이터 관리

## 학습 목표
- 파일 입출력의 기본 (읽기/쓰기)을 익힌다
- CSV 파일이 무엇이고 왜 사용하는지 이해한다
- pandas DataFrame으로 데이터를 다룬다
- Repository 패턴이 무엇이고 왜 좋은지 이해한다

---

## 1. 파일 입출력

### 파일 입출력이란?
프로그램에서 파일에 **데이터를 저장하거나 읽어오는 작업**이다.
프로그램이 종료되면 메모리의 데이터는 사라지지만, 파일에 저장하면 영구적으로 보관할 수 있다.

| 함수 | 역할 |
|------|------|
| `open()` | 파일 열기 |
| `write()` | 파일에 쓰기 |
| `read()` | 파일 읽기 |
| `close()` | 파일 닫기 |

### 파일 모드

| 모드 | 설명 |
|------|------|
| `"r"` | 읽기 (파일 없으면 에러) |
| `"w"` | 쓰기 (파일 있으면 덮어씀) |
| `"a"` | 추가 (파일 끝에 이어씀) |
| `"r+"` | 읽기+쓰기 |

### 기본 방식 vs with 문

```python
# 기본 방식 - close 필수!
file = open("test.txt", "w", encoding="utf-8")
file.write("안녕하세요!\n")
file.close()  # 반드시 닫아야 함

# with 문 사용 (권장!) - 자동으로 닫힘
with open("test.txt", "w", encoding="utf-8") as file:
    file.write("with 문을 사용하면\n")
    file.write("자동으로 파일이 닫힙니다!\n")
# 여기서 자동으로 close() 됨
```

### 파일 읽기

```python
# 전체 읽기
with open("test.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)

# 한 줄씩 읽기
with open("test.txt", "r", encoding="utf-8") as file:
    for i, line in enumerate(file, 1):
        print(f"{i}번째 줄: {line.strip()}")  # strip()으로 줄바꿈 제거
```

### 파일/폴더 관리 (os 모듈)

```python
import os

# 파일 존재 확인
os.path.exists("test.txt")           # True/False

# 폴더 생성 (중첩 폴더도 한번에)
os.makedirs("data/sub_folder", exist_ok=True)
# exist_ok=True: 이미 있어도 에러 안 남

# 경로 분리
os.path.dirname("data/search.csv")   # "data"
os.path.basename("data/search.csv")  # "search.csv"
```

---

## 2. CSV 파일

### CSV란?
CSV는 **쉼표로 구분된 값들을 저장하는 텍스트 파일 형식**이다.
- **C**omma **S**eparated **V**alues
- 엑셀, 구글 시트 등에서 열 수 있음

```
이름,나이,도시
홍길동,25,서울
김철수,30,부산
```

### 왜 필요한가?
1. **단순함**: 메모장으로도 열어볼 수 있음
2. **호환성**: 거의 모든 프로그램에서 지원
3. **가벼움**: 복잡한 형식 없이 데이터만 저장

### CSV 파일 만들기

```python
csv_content = """이름,나이,도시
홍길동,25,서울
김철수,30,부산
이영희,28,인천"""

with open("people.csv", "w", encoding="utf-8-sig") as file:
    file.write(csv_content)
# utf-8-sig: 엑셀에서 한글 깨짐 방지
```

### csv 모듈로 읽기

```python
import csv

# 리스트 형태로 읽기
with open("people.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        if i == 0:
            print(f"헤더: {row}")
        else:
            print(f"데이터: {row}")

# 딕셔너리 형태로 읽기 (더 편리!)
with open("people.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)  # 헤더를 키로 사용
    for row in reader:
        print(f"{row['이름']}님은 {row['나이']}세, {row['도시']} 거주")
```

---

## 3. pandas DataFrame

### DataFrame이란?
**행과 열로 구성된 2차원 표 형태의 데이터 구조**이다.

| 용어 | 설명 |
|------|------|
| DataFrame | 2차원 표 데이터 |
| Index | 행 식별자 |
| Column | 열 이름 |

### DataFrame 생성

```python
import pandas as pd

data = {
    "이름": ["홍길동", "김철수", "이영희"],
    "나이": [25, 30, 28],
    "도시": ["서울", "부산", "인천"]
}
df = pd.DataFrame(data)

print(df)
print(df.shape)          # (3, 3) → (행 수, 열 수)
print(list(df.columns))  # ['이름', '나이', '도시']
```

### 데이터 접근

```python
# 컬럼 접근
df["이름"]               # 이름 컬럼 (Series)

# 행 접근
df.iloc[0]               # 첫 번째 행
df.iloc[0].to_dict()     # {'이름': '홍길동', '나이': 25, '도시': '서울'}

# 특정 값 접근
df.iloc[0]['나이']        # 25
df[df['이름'] == '김철수']['도시'].values[0]  # '부산'
```

### 필터링과 정렬

```python
# 필터링: 조건에 맞는 행만
df[df["도시"] == "서울"]     # 서울 거주자만
df[df["나이"] >= 25]         # 25세 이상만

# 정렬
df.sort_values("나이")                    # 오름차순
df.sort_values("나이", ascending=False)   # 내림차순
```

### CSV 읽고 쓰기 (pandas)

```python
# CSV 읽기 (한 줄!)
df = pd.read_csv("people.csv", encoding="utf-8-sig")

# 행 추가
new_row = pd.DataFrame([{"이름": "박지민", "나이": 27, "도시": "대구"}])
df = pd.concat([df, new_row], ignore_index=True)

# CSV 쓰기 (한 줄!)
df.to_csv("people_updated.csv", index=False, encoding="utf-8-sig")
```

### pandas 핵심 정리

| 함수/메서드 | 역할 |
|-------------|------|
| `pd.DataFrame(data)` | DataFrame 생성 |
| `pd.read_csv(path)` | CSV 파일 읽기 |
| `df.to_csv(path)` | CSV 파일 쓰기 |
| `df["컬럼"]` | 컬럼 선택 |
| `df[조건]` | 조건 필터링 |
| `df.sort_values()` | 정렬 |
| `pd.concat()` | DataFrame 합치기 |
| `df.iloc[i]` | 행 접근 (숫자 인덱스) |
| `df.iterrows()` | 행 순회 |
| `df.empty` | 비어있는지 확인 |
| `df.drop_duplicates()` | 중복 제거 |

---

## 4. Repository 패턴

### Repository 패턴이란?
**데이터 저장소 접근 로직을 캡슐화하여 일관된 인터페이스를 제공하는 디자인 패턴**이다.
창고 관리자에 비유할 수 있다: 데이터 저장 방식(CSV, DB 등)을 숨기고, 간단한 인터페이스만 제공한다.

| 메서드 | 역할 |
|--------|------|
| `load()` | 데이터 불러오기 |
| `save()` | 데이터 저장 |
| `find_by_key()` | 키로 찾기 |
| `get_all_keys()` | 전체 키 목록 조회 |

### 왜 필요한가?

```python
# Repository 없이 → 복잡
df = pd.read_csv("data.csv")
filtered = df[df["key"] == "abc"]
# ... 복잡한 변환 로직 ...

# Repository 사용 → 간단
result = repository.find_by_key("abc")
```

1. **추상화**: 저장 방식을 몰라도 됨
2. **일관성**: 데이터 접근 방법이 통일됨
3. **변경 용이**: CSV → DB 변경해도 사용하는 코드는 그대로

### Repository 구현 예시

```python
import os
import pandas as pd
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Product:
    id: str
    name: str
    price: int

class ProductRepository:
    """상품 데이터를 관리하는 Repository"""

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        folder = os.path.dirname(csv_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

    def load(self) -> pd.DataFrame:
        """데이터 로드"""
        if not os.path.exists(self.csv_path):
            return pd.DataFrame(columns=["id", "name", "price"])
        return pd.read_csv(self.csv_path)

    def save(self, product: Product) -> bool:
        """상품 저장"""
        df = self.load()
        new_row = pd.DataFrame([{
            "id": product.id,
            "name": product.name,
            "price": product.price
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.csv_path, index=False)
        return True

    def find_by_id(self, product_id: str) -> Optional[Product]:
        """ID로 상품 찾기"""
        df = self.load()
        filtered = df[df["id"] == product_id]
        if filtered.empty:
            return None
        row = filtered.iloc[0]
        return Product(id=row["id"], name=row["name"], price=int(row["price"]))

    def get_all(self) -> List[Product]:
        """모든 상품 조회"""
        df = self.load()
        return [
            Product(id=row["id"], name=row["name"], price=int(row["price"]))
            for _, row in df.iterrows()
        ]
```

### Repository 사용

```python
repo = ProductRepository("test_data/products.csv")

# 저장
repo.save(Product("P001", "노트북", 1500000))
repo.save(Product("P002", "마우스", 50000))

# 전체 조회
products = repo.get_all()
for p in products:
    print(f"{p.name}: {p.price:,}원")

# ID로 검색
found = repo.find_by_id("P002")
if found:
    print(f"찾음: {found.name}")
```

### 프로젝트의 SearchRepository 구조

```python
class SearchRepository:
    CSV_COLUMNS = [
        "search_key", "search_time", "keyword", "article_index",
        "title", "url", "snippet", "pub_date", "ai_summary"
    ]

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)

    def load(self) -> pd.DataFrame:
        """CSV 파일에서 데이터를 로드 (없으면 빈 DataFrame)"""
        if not os.path.exists(self.csv_path):
            return pd.DataFrame(columns=self.CSV_COLUMNS)
        try:
            df = pd.read_csv(self.csv_path)
            if not df.empty:
                df['search_time'] = pd.to_datetime(df['search_time'])
            return df
        except Exception:
            return pd.DataFrame(columns=self.CSV_COLUMNS)

    def save(self, search_result: SearchResult) -> bool:
        """검색 결과를 CSV에 추가 저장"""
        try:
            new_df = search_result.to_dataframe()
            existing_df = self.load()
            final_df = pd.concat([existing_df, new_df], ignore_index=True)
            final_df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
            return True
        except Exception:
            return False

    def get_all_keys(self) -> List[str]:
        """모든 고유한 search_key를 최신순으로 반환"""
        df = self.load()
        if df.empty:
            return []
        df_sorted = df.sort_values(by="search_time", ascending=False)
        return df_sorted["search_key"].drop_duplicates().tolist()

    def find_by_key(self, search_key: str) -> Optional[SearchResult]:
        """search_key로 검색 결과를 찾아 SearchResult로 복원"""
        df = self.load()
        result_df = df[df["search_key"] == search_key]
        if result_df.empty:
            return None

        first_row = result_df.iloc[0]
        articles = []
        for _, row in result_df.iterrows():
            articles.append(NewsArticle(
                title=row["title"],
                url=row["url"],
                snippet=row["snippet"],
                pub_date=row.get("pub_date")
            ))

        return SearchResult(
            search_key=search_key,
            search_time=first_row["search_time"],
            keyword=first_row["keyword"],
            articles=articles,
            ai_summary=first_row["ai_summary"]
        )

    def get_all_as_csv(self) -> str:
        """전체 데이터를 CSV 문자열로 반환 (다운로드용)"""
        df = self.load()
        return df.to_csv(index=False, encoding='utf-8-sig')
```

---

## 핵심 요약

| 개념 | 한 줄 요약 |
|------|-----------|
| **파일 입출력** | 데이터를 영구 저장하는 방법 |
| **with 문** | 파일을 안전하게 다루는 방법 (자동 close) |
| **CSV 파일** | 쉼표로 구분된 표 형식 파일 |
| **pandas DataFrame** | 파이썬의 2차원 표 데이터 구조 |
| **Repository 패턴** | 데이터 저장소를 쉽게 다루는 클래스 |

### Repository 기본 패턴

```python
class DataRepository:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    def load(self) -> pd.DataFrame:
        if not os.path.exists(self.csv_path):
            return pd.DataFrame(columns=[...])
        return pd.read_csv(self.csv_path)

    def save(self, data) -> bool:
        new_df = data.to_dataframe()
        df = pd.concat([self.load(), new_df], ignore_index=True)
        df.to_csv(self.csv_path, index=False)
        return True
```
