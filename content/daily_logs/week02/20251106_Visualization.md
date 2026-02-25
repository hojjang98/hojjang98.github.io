---
title: "2025.11.06 (Day 9) Matplotlib · Seaborn 기반 로그 시각화 및 데이터 분석 학습 로그"
date: 2025-11-06
draft: false
tags: ["Python", "Matplotlib", "Seaborn", "Pandas", "로그시각화", "이상탐지", "보안활용", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "Matplotlib과 Seaborn을 활용한 보안 로그 시각화 기초 학습. 로그인 실패율·지연시간 분석, 사용자별 이상 패턴 탐지, 피벗 기반 히트맵 구성 방법 정리."
---

# 2025.11.06 (Day 9) [Matplotlib · Seaborn 기반 로그 시각화 및 데이터 분석]

## 1. 핵심 개념 정리(Concepts & Theory)

| # | 핵심 개념 | 간결한 설명 | 적용 예시 |
|:---:|:---:|:---|:---|
| 1 | **Matplotlib 기본 구조** | `figure`, `axes`, `subplot` 개념을 이해하고, 단일/다중 그래프를 자유롭게 배치 가능 | 라인플롯, 서브플롯, 축 설정 |
| 2 | **Pandas와 시각화의 결합** | 그룹화(`groupby`), 피벗(`pivot_table`), 집계(`agg`)를 통해 통계형 시각화 구현 | 시간대별 평균, 사용자별 실패율 계산 |
| 3 | **통계형 시각화 도구** | `boxplot`, `heatmap`, `countplot`을 이용해 이상치 탐지 및 상관관계 파악 | IQR 계산, 상관계수 시각화 |
| 4 | **보안 로그 응용 데이터셋** | 더미 로그인 로그 생성 후, 상태·지연시간·사용자 패턴을 통계적으로 시각화 | 로그인 성공률, 지연시간 평균 |
| 5 | **실제 데이터 확장 (MPG 예제)** | 차량 연비 데이터에 동일한 통계적 시각화 기법을 적용하여 일반 분석으로 확장 | 배기량별 연비 비교, 제조사별 평균 |

**핵심 인사이트:** 시각화는 단순히 데이터를 보여주는 것이 아니라, 패턴과 이상을 드러내는 과정이다. 오늘 배운 흐름은 `Matplotlib → Seaborn → Pandas 그룹화 → 실무형 데이터 응용`으로 확장되었다.

---

## 2. 실습 코드 & 응용 (Practice & Code)

### (1) Matplotlib 기초 복습
```python
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(0, 10)
y1 = x ** 2
y2 = np.sqrt(x)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(x, y1, color='tomato', marker='o', label='y = x²')
axes[1].plot(x, y2, color='steelblue', marker='s', label='y = √x')

for ax in axes:
    ax.legend()
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)

plt.suptitle("Matplotlib 기본 구조 – Subplot 예시")
plt.show()
```

figure와 axes 객체의 개념적 구조를 직접 체험하며, 하나의 캔버스 위에 여러 시각화 레이어를 올린다는 사고를 익혔다.

### (2) Pandas 기반 로그인 로그 시각화
```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(42)
timestamp = pd.date_range('2025-11-06', periods=120, freq='H')
df = pd.DataFrame({
    "timestamp": timestamp,
    "user": np.random.choice(['admin', 'guest', 'analyst', 'root'], 120),
    "status": np.random.choice(['success', 'fail'], 120, p=[0.7, 0.3]),
    "delay_ms": np.random.randint(30, 1000, 120)
})

# 상태별 시도 횟수
plt.figure(figsize=(6, 4))
sns.countplot(x='status', data=df, palette='pastel')
plt.title("로그인 상태별 시도 횟수")
plt.xlabel("Status")
plt.ylabel("Count")
plt.show()

# 시간대별 평균 지연시간
hourly_delay = df.groupby(df['timestamp'].dt.hour)['delay_ms'].mean()
plt.figure(figsize=(8, 4))
plt.plot(hourly_delay.index, hourly_delay.values, marker='o', color='orange')
plt.title("시간대별 평균 로그인 지연시간")
plt.xlabel("Hour of Day")
plt.ylabel("Mean Delay (ms)")
plt.grid(True)
plt.show()
```

Pandas의 `groupby`를 이용해 시계열 데이터를 시각적으로 표현하며, 로그 데이터를 시간 축으로 요약하는 방법을 익혔다.

### (3) 이상치 탐지 및 사용자 패턴 분석
```python
# 사용자별 통계 집계
user_stats = (
    df.groupby('user')
      .agg(total_attempts=('status', 'size'),
           fail_count=('status', lambda x: (x == 'fail').sum()),
           mean_delay=('delay_ms', 'mean'))
      .reset_index()
)
user_stats['fail_ratio'] = user_stats['fail_count'] / user_stats['total_attempts']

# 산점도 시각화
plt.figure(figsize=(8, 6))
sns.scatterplot(
    x='mean_delay', y='fail_ratio', size='total_attempts',
    hue='fail_ratio', data=user_stats, palette='viridis', legend=False, s=300
)
for _, row in user_stats.iterrows():
    plt.text(row['mean_delay'] + 5, row['fail_ratio'], row['user'], fontsize=9)
plt.title("사용자별 로그인 패턴 – 평균 지연시간 vs 실패율")
plt.xlabel("평균 지연시간 (ms)")
plt.ylabel("실패율")
plt.show()
```

비정상 사용자 탐지(Anomaly Detection)의 개념을 시각화로 접근했다. 평균 지연시간이 높고 실패율이 비정상적으로 큰 사용자는 잠재적 위험으로 분류할 수 있다.

### (4) 상관관계 및 피벗 기반 Heatmap
```python
heatmap_data = df.pivot_table(index='user', columns='status', values='delay_ms', aggfunc='mean')

plt.figure(figsize=(7, 4))
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlGnBu')
plt.title("사용자 × 로그인 상태별 평균 지연시간 Heatmap")
plt.xlabel("로그인 상태")
plt.ylabel("사용자")
plt.show()
```

피벗 테이블과 히트맵의 조합을 통해 다차원 관계(사용자 × 상태)를 한눈에 파악할 수 있었다. 특정 사용자가 fail 상태일 때 평균 지연시간이 비정상적으로 높은 경우, 이는 Brute-force나 봇 행위를 의심할 수 있는 지표가 된다.

### (5) 실제 데이터 확장 – MPG 차량 연비 분석
```python
mpg = pd.read_excel("mpg_visualization.xlsx", index_col=0)

# 배기량 구간별 고속도로 연비 비교
mpg['cyl_group'] = np.where(mpg['cyl'] <= 4, '4 이하', '5 이상')
avg_hwy = mpg.groupby('cyl_group')['hwy'].mean()

plt.figure(figsize=(5, 4))
plt.bar(avg_hwy.index, avg_hwy.values, color=['teal', 'gray'])
plt.title("배기량 구간별 고속도로 평균연비 비교")
plt.ylabel("평균 연비 (hwy)")
plt.show()

# 제조사별 평균 연비
top_brands = mpg.groupby('manufacturer')['hwy'].mean().sort_values(ascending=False).head(5)
top_brands.plot(kind='bar', color='coral', figsize=(7, 4), title='제조사별 고속도로 평균연비 상위 5')
plt.ylabel("평균 고속도로 연비")
plt.show()
```

보안 로그 외의 일반 데이터셋에서도 동일한 패턴 분석 논리를 적용할 수 있었다. 통계 기반 시각화의 원리는 도메인과 무관하게 데이터 품질 평가, 효율성 비교, 이상 탐지로 확장된다.

---

## 3. 보안 관점 분석 (Security Insight)

| 보안 영역 | 적용 방식 | 기대 효과 |
|:--|:--|:--|
| **SOC / 관제** | 사용자별 로그인 실패율(`fail_ratio`)과 평균 지연시간(`mean_delay`)을 시각화하여 공격 시도를 조기 인지 | 비정상 계정 탐지, brute-force 공격 패턴 식별 |
| **CERT / 사고대응** | 로그 타임라인을 시각화하여 공격 전·후 이벤트를 시각적으로 복원 | 사고 분석 속도 향상, 시점별 이벤트 흐름 명확화 |
| **DevSecOps** | 빌드·배포 로그에서 실패 패턴을 시각화하여 반복 오류나 취약 지점을 빠르게 파악 | 자동화된 품질 모니터링, 빌드 파이프라인 신뢰도 개선 |
| **취약점 진단 / 펜테스트** | 스캐너 결과나 응답 시간 분포를 boxplot으로 표현해 비정상 응답(outlier)을 시각화 | 응답 지연 기반 취약 시스템 탐지 |
| **디지털 포렌식** | IP, 사용자, 타임스탬프를 기준으로 heatmap을 구성해 공격 집중 구간 시각화 | 공격 클러스터 및 시간대별 집중도 분석 |
| **개인정보 보호** | 로그 내 민감정보(IP, 계정 ID)를 그룹화 단위로 시각화해 직접 노출 없이 분석 가능 | 개인정보 최소 노출, 익명화 기반 데이터 활용 |

이번 학습을 통해 단순 로그를 수치 데이터로만 보지 않고, 패턴의 형태(Shape)로 이해하는 감각을 익혔다. 시각화는 곧 데이터 기반 위협 인식의 첫 단계다.

---

## 4. 요약 및 다음 단계 (Summary & Next Steps)

1. Matplotlib과 Seaborn을 이용한 시각화의 기본에서 시작해, 보안 로그를 분석 가능한 형태로 시각화하는 실습으로 발전했다.
2. 라인플롯, 박스플롯, 히트맵 같은 기본 그래프들은 단순 도식이 아니라 로그의 품질·정상 범위·이상치 패턴을 확인하는 핵심 도구임을 알게 되었다.
3. 로그인 실패율과 평균 지연시간의 관계처럼 다차원 변수의 결합 시각화가 비정상 사용자를 탐지하는 데 얼마나 직관적인 효과를 주는지 확인했다.

**다음 단계 계획**

1. `Folium`을 이용해 위치 기반 로그(예: IP 지역별 로그인 시도)를 지도 형태로 시각화
2. `Streamlit`으로 실시간 대시보드 구성 — 시간대별 실패율, 평균 지연, 사용자별 트렌드 표시
3. 장기적으로는 이상치 탐지 모델과 시각화 대시보드를 결합해 보안 로그 자동 분석 + 실시간 알림 시스템으로 확장할 예정

---

## 개인 인사이트 (Reflection)

- **배운 점**: 데이터 시각화의 기술적인 부분보다 더 중요한 것은, 그래프를 통해 어떤 이야기를 읽을 수 있는가였다. 이번 실습을 통해 숫자 대신 패턴으로 사고하는 습관을 조금씩 익히고 있다.
- **느낀 점**: Matplotlib과 Seaborn의 기본만으로도 상당한 수준의 분석이 가능하지만, 시각화만으로 끝나는 것이 아니라 이를 탐지 규칙 설계로 연결해야 실무형 가치가 생긴다는 점이 인상 깊었다.
- **심화 방향**: 이번 주에 익힌 시각화 기법을 실제 보안 로그 분석 프로젝트에 접목해볼 예정이다. `delay_ms`, `status`, `user` 같은 필드를 활용해 이상 행위(Abnormal Behavior)를 시각적으로 탐지하는 로그 인텔리전스(Visual Threat Intelligence) 형태로 확장하고 싶다.
- **향후 계획**: 이번 주 배운 내용을 기반으로, 시간대별 로그인 실패율, 사용자별 평균 지연시간, 네트워크 세그먼트별 트래픽 분포 등을 통합 시각화하고, 실시간 관제 대시보드의 기본 구조를 설계하려 한다. 나아가 이 구조를 SOC 환경에 맞춰 로그 이상 탐지와 시각 분석(Visual Analytics) 기반 보안 자동화로 연결할 계획이다.