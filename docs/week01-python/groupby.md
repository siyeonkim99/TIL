---
title: groupby 집계
date: 2026-07-27
tags: [pandas, 3주차]
---

# groupby 집계

> 원본 코드: [`groupby.py`](groupby.py)

## 데이터 불러오기

csv를 읽으면 DataFrame이 된다. 엑셀 시트 하나라고 생각하면 편하다.

```python
import pandas as pd

df = pd.read_csv("sales.csv")
```

## 지역별 매출 합계

groupby는 쪼개고(split) 계산하고(apply) 합친다(combine). 컬럼을 먼저 고르고 집계 함수를 붙이는 순서다.

!!! warning
    as_index=False를 빼면 region이 인덱스로 들어가서 이후 merge가 전부 깨진다.

```python
result = df.groupby("region", as_index=False)["sales"].sum()

result.to_csv("out.csv", index=False)
```

## 다시 볼 것

- [ ] agg로 여러 함수를 한 번에 쓰는 법 다시 확인
- [ ] pivot_table과 뭐가 다른지
