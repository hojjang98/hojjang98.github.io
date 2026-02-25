---
title: "2025.11.04 (Day 7) Numpy & Pandas 기초 / 데이터 처리 및 EDA 학습 로그"
date: 2025-11-04
draft: false
tags: ["Python", "Numpy", "Pandas", "EDA", "이상탐지", "보안활용", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "Numpy & Pandas 기반 로그 적재, 결측값 처리, JSON 변환, 기초 이상 탐지 흐름 학습"
---

# 2025.11.04 (Day 7) [Numpy & Pandas 기초 / 데이터 처리 및 EDA]

## 1. 핵심 개념 정리(Concepts)

- 핵심1 — **Numpy 배열과 벡터화 연산**: 대량 로그·이벤트 데이터에서 반복문 없이 고속 연산을 수행해 실시간 피처 계산과 통계량 산출에 적합하다.
- 핵심2 — **Pandas Series / DataFrame 구조**: CSV·JSON·API로 유입되는 다양한 보안 데이터(로그, 스캐너 결과 등)를 컬럼 단위로 정형화해 전처리·분석을 일관되게 수행할 수 있다.
- 핵심3 — **결측값 처리(`fillna`)**: 데이터 수집 중 발생하는 결측을 합리적으로 보정해 모델 입력의 안정성을 높인다.
- 핵심4 — **JSON → DataFrame 변환**: 외부 위협 인텔리전스나 스캐너 출력과 같은 비정형 데이터를 바로 분석 테이블로 변환해 파이프라인에 연결할 수 있다.
- 핵심5 — **기초 시각화(matplotlib)**: 이벤트 빈도, 시간대별 추이 등을 시각화해 탐지 가설을 검증하고 인시던트 인사이트를 도출한다.

---

## 2. 실습 코드 & 응용 (Practice & Code)
```python
# 1) CSV 로그 로드 및 기본 슬라이싱 (빠른 샘플 확인)
import numpy as np
rawData = np.loadtxt('log_sample.csv', delimiter=',', dtype=str)
print(rawData[:5, :])

# 사용 맥락: 샘플 데이터 구조·값 범위 확인, 컬럼타입 추정
# 확장 아이디어: pandas.read_csv로 로드해 컬럼별 타입 자동 변환 후 ETL 파이프라인으로 연결

# 2) Pandas Series 생성 및 결측값 처리 (결측 보정)
import pandas as pd
series = pd.Series([10, 12, None, 15, 11])
series = series.fillna(series.mean())

# 사용 맥락: 센서/에이전트 누락값 보정 → 안정적 스코어링
# 확장 아이디어: 시간성 데이터면 forward-fill/backfill 또는 리샘플링 적용

# 3) JSON API 응답을 DataFrame으로 변환 (위협 인텔 통합)
import urllib.request, json
resp = urllib.request.urlopen('https://example.com/threats.json')
result = json.load(resp)
df = pd.DataFrame(result)
df.info()

# 사용 맥락: 스캐너/위협 피드 통합 → 취약점/IOC 집계
# 확장 아이디어: 소스별 신뢰도 컬럼 추가 후 가중치 기반 우선순위화

# 4) Numpy로 간단한 이상치 지표 계산 (벡터화)
vals = np.array(df['event_count'].astype(float))
zscore = (vals - vals.mean()) / vals.std()
anomaly_idx = np.where(np.abs(zscore) > 3)[0]

# 사용 맥락: 대량 이벤트에서 빠른 통계 기반 이상치 선별
# 확장 아이디어: 이동 윈도우 기반 통계로 실시간 이상치 스코어 구현
```

- **사용 맥락**: 로그 적재 → 전처리 → 결측 보정 → 피처화 → 기초 이상 탐지 흐름에 바로 적용가능하다.
- **확장 아이디어**: 위 코드를 함수화(`load_logs()`, `normalize_series()`, `score_anomaly()`)해 ETL 모듈로 만들고 결과를 경보/대시보드로 연동한다.

---

## 3. 보안 관점 분석 (Security Insight)

- 관점1 — **SOC / 관제 (실시간 탐지)**
  - **적용 방식**: Numpy 벡터화 연산과 Pandas DataFrame 전처리를 결합해 초당 요청 수, IP별 세션 길이 등 실시간 피처를 빠르게 계산한다.
  - **기대 효과**: 로그 집계 지연을 줄이고, 탐지 룰의 신뢰도를 높이며, 이상치 스코어 기반 탐지로 오탐을 감소시킨다.
  - **예시 흐름**: `raw logs → pandas 정규화 → np 벡터화 집계 → 이상치 스코어링 → 알람`

- 관점2 — **CERT / 사고대응 (Incident Response)**
  - **적용 방식**: `pd.to_datetime`과 `DatetimeIndex`를 활용해 타임스탬프를 정렬하고, `fillna`로 누락 데이터를 보정하여 세션 단위로 사건 재구성을 수행한다.
  - **기대 효과**: 사고 타임라인을 정확히 복원하여 포렌식 분석의 신뢰도 향상 및 침해 경로 식별 시간 단축.

- 관점3 — **취약점 진단 / 펜테스트**
  - **적용 방식**: 스캐너 결과(JSON/CSV)를 `pd.DataFrame`으로 변환해 중복 취약점을 병합하고, 위험도·빈도 기반으로 우선순위를 자동 산출한다.
  - **기대 효과**: 취약점 리포트 품질 향상, 노이즈 제거 및 패치 우선순위 명확화.

- 관점4 — **개발보안 (DevSecOps)**
  - **적용 방식**: 빌드 로그 및 테스트 결과를 Pandas로 정규화해 실패 패턴 및 취약점 발생 빈도를 추적한다.
  - **기대 효과**: 반복되는 빌드 오류나 취약 패턴을 조기에 탐지하고 자동화된 피드백 루프 구축 가능.

- 관점5 — **데이터 프라이버시 / 개인정보 보호**
  - **적용 방식**: Pandas의 문자열 처리 기능(`.str.replace`, `.apply`)을 이용해 로그 내 민감정보 필드를 자동 마스킹한다.
  - **기대 효과**: 개인정보 보호를 유지하면서 로그 분석 유틸리티를 확보하여 보안 감사 대응 용이.

---

## 4. 요약 (Summary)

1. Numpy와 Pandas는 로그 적재·정규화·결측 보정·이상치 탐지 등 모든 보안 데이터 처리의 핵심 기반이다.
2. `fillna`와 DataFrame 변환을 통해 CERT·SOC 환경에서 누락 로그와 비정형 데이터를 안정적으로 다룰 수 있다.
3. 향후 시간 리샘플링과 이동 평균 기반 이상 탐지로 실시간 보안 모니터링 구조를 고도화할 수 있다.

---

## 개인 인사이트 (Reflection)

- `fillna`를 단순 평균 대체로만 쓰지 않고 **소스 신뢰도 기반 가중 보정**으로 확장하면 분석 품질이 크게 개선될 것 같다.
- JSON → DataFrame 흐름은 여러 위협 인텔 소스를 통합하는 데 핵심이므로, **소스 메타(수집시간·신뢰도)** 컬럼을 표준화해 두는 습관을 들여야겠다.
- 실무 적용 목표: 위 코드를 함수화해 ETL 모듈화(`load_logs()`, `normalize()`, `score()`)하고, 1주일 단위 A/B로 알람 변화량과 처리시간을 측정해 배포 여부를 판단하겠다.