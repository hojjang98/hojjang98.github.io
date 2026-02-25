---
title: "2025.11.05 (Day 8) Numpy & Pandas 기반 로그 정규화 학습 로그"
date: 2025-11-05
draft: false
tags: ["Python", "Numpy", "Pandas", "로그정규화", "이상탐지", "보안활용", "SK쉴더스루키즈"]
summary: "Numpy와 Pandas를 활용한 보안 로그 정규화 기초 학습. loadtxt, DataFrame 변환, 결측치 처리, 타입 변환을 통한 로그 전처리 파이프라인 구성 방법 정리."
---

# 2025.11.05 (Day 8) [Numpy & Pandas 기반 로그 정규화]

## 1. 핵심 개념 정리 (Concepts & Theory)

| # | 핵심 개념 | 간결한 설명 | 적용 예시 |
|:---:|:---:|:---|:---|
| 1 | **`np.loadtxt()` / `np.genfromtxt()`** | 텍스트 기반 로그 파일을 배열 형태로 고속 로드하는 함수. CSV나 공백 구분 로그의 초기 샘플링에 유용함. | `raw = np.loadtxt('log.csv', delimiter=',', dtype=str)` |
| 2 | **`pd.DataFrame()` 변환** | Numpy 배열을 Pandas의 표 형식 데이터로 전환하여, 결측치·타입 변환·정렬·슬라이싱 등 고급 처리를 수행할 수 있음. | `df = pd.DataFrame(raw[1:], columns=raw[0])` |
| 3 | **데이터 정규화 (Normalization)** | 로그 데이터의 형식·타입 불일치를 정규화하여, 이후 분석·탐지 모델의 입력 일관성을 확보함. | `df['timestamp'] = pd.to_datetime(df['timestamp'])` |
| 4 | **결측치 처리 (`fillna`, `dropna`)** | 로그 전처리의 기본으로, 비어 있는 필드를 N/A로 대체하거나 제거함. | `df.fillna('N/A', inplace=True)` |
| 5 | **타입 변환(`astype`) & 슬라이싱** | 로그의 수치형/시간형 필드를 명확히 변환해 정렬 및 비교 연산을 가능하게 함. | `df['value'] = df['value'].astype(float)` |

**핵심 인사이트:** 오늘 배운 Numpy·Pandas 기법은 로그 데이터의 표준화와 구조화(Structured Logging)를 통해 보안 분석의 신뢰도와 속도를 향상시키는 핵심이다.

---

## 2. 실습 코드 & 응용 (Practice & Code)
```python
import numpy as np
import pandas as pd

# 로그 데이터 로드
rawData = np.loadtxt('log_sample.csv', delimiter=',', dtype=str)
print(rawData[:5, :])  # 빠른 샘플 확인

# DataFrame 변환
df = pd.DataFrame(rawData[1:], columns=rawData[0])
df['timestamp'] = pd.to_datetime(df['timestamp'])  # 타입 변환
df.fillna('N/A', inplace=True)                     # 결측치 보정

# 데이터 슬라이싱 및 요약
print(df.head())
print(df.info())
```

- **핵심 코드 설명**: `np.loadtxt`는 단순 CSV/로그 파일의 고속 로딩에 유용하며, 이후 Pandas로 전환해 타입 일관성과 결측 처리 기능을 추가한다. Numpy는 속도, Pandas는 유연성을 담당하며, 보안 로그 전처리의 2단계 구조를 구성한다.
- **확장 아이디어**: Pandas의 `read_csv()`로 교체하여 대용량 ETL 파이프라인에 통합하거나, `to_sql()`로 SIEM 데이터베이스 적재 자동화까지 확장할 수 있다. 함수화하여 `def normalize_log(path):` 형태의 로그 정규화 모듈로 발전 가능하다.

---

## 3. 보안 관점 분석 (Security Insight)

- 관점1 — **SOC / 관제**
  - **적용**: 로그 파이프라인 초입에서 형식·시간 정규화를 수행해 탐지 규칙 입력의 일관성 확보
  - **효과**: False Positive 감소, 실시간 집계 속도 향상
  - **예시 흐름**: `로그 → 정규화(타입·시간) → 세션 집계 → 탐지`

- 관점2 — **CERT / 사고대응**
  - **적용**: 침해 시점 로그 정렬·결측 보정으로 공격 단계별 타임라인 복원
  - **효과**: 사고 재현 정확도 향상, 증거 신뢰성 강화

- 관점3 — **취약점 진단**
  - **적용**: 스캐너 CSV 결과를 Pandas로 통합·정렬하여 중복 취약점 제거 및 심각도별 리포트 자동화
  - **효과**: 분석 시간 단축, 보고서 자동화

- 관점4 — **개발보안 (DevSecOps)**
  - **적용**: 빌드 로그를 Pandas로 정규화 → 반복 오류 자동 라벨링
  - **효과**: CI/CD 파이프라인 품질 개선

- 관점5 — **디지털 포렌식**
  - **적용**: 로그 덤프를 시계열·필드별로 슬라이싱하여 분석 효율 향상
  - **효과**: 증거 탐색 시간 단축, 분석 노이즈 감소

- 관점6 — **개인정보 보호**
  - **적용**: Pandas를 통한 민감정보(IP, ID 등) 일괄 마스킹 처리
  - **효과**: 개인정보 보호 및 로그 활용성 유지

---

## 4. 요약 및 다음 단계 (Summary & Next Steps)

1. 오늘 배운 Numpy·Pandas 기법은 로그 데이터 정규화의 필수 기초이다.
2. 정규화와 결측 보정은 탐지 정확도와 포렌식 재현성을 좌우한다.
3. 다음 단계는 Pandas 그룹화 및 시계열 집계(`groupby`, `resample`)를 통해 세션 단위 이상행동 탐지 구조를 실습하는 것이다.

---

## 개인 인사이트 (Reflection)

- **배운 점**: 로그 정규화가 단순한 데이터 클리닝이 아니라, 보안 분석의 기반 인프라라는 점을 체감했다.
- **심화 주제**: `groupby`와 `pivot_table`을 이용한 이벤트 단위 세션 집계의 중요성을 인식했다.
- **향후 계획**: Pandas 기반 정규화 코드를 함수화해 보안 로그 ETL 모듈로 발전시키고, 다음에는 이상치 탐지(Anomaly Detection) 단계로 연결할 예정이다.