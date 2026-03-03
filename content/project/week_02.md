---
title: "Project 02 — Streamlit Log Dashboard"
date: 2025-11-07
draft: false
tags: ["Python", "Streamlit", "Pandas", "Plotly", "보안관제", "SOC", "로그분석", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "Week1 탐지 엔진을 데이터 분석 레이어로 확장한 Streamlit 기반 보안 로그 대시보드"
---

# Project 02 — Streamlit Log Dashboard

> 전체 소스코드는 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_02](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_02)

---

## 개요

**Streamlit Log Dashboard**는 Week 1에서 구축한 Mini Security Log Monitor의 결과물(access.log)을 기반으로,
보안 로그를 **데이터프레임 형태로 가공 -> 시각화 -> 대시보드화** 하는 프로젝트다.

Week 1 코드를 단순 재사용하지 않고, **랜덤 사용자 및 랜덤 인증 반전 로직을 추가**하여
보다 현실적인 로그 패턴을 자동 생성하도록 확장하였다.
이를 통해 Pie Chart · Bar Chart 에서 다양한 분포를 시각적으로 분석할 수 있는 구조를 완성했다.

---

## 주간 학습 요약

- **Day 1 (11.03)** — Numpy 기초 및 벡터화 연산
  - 로그 데이터의 벡터화 처리 및 고속 계산

- **Day 2 (11.04)** — Pandas & EDA 기초
  - 로그 적재, 결측 보정, DataFrame 변환

- **Day 3 (11.05)** — Pandas 기반 로그 정규화
  - 데이터 표준화, 타입 변환, 결측 처리

- **Day 4 (11.06)** — Matplotlib · Seaborn 기반 시각화
  - 그룹화, 통계형 시각화, 이상치 탐지 그래프

- **Day 5 (11.07)** — Folium · Plotly · Streamlit 실습
  - 인터랙티브 지도, 동적 그래프, 웹 대시보드 구성

---

## 주요 기능

- **랜덤 로그 자동 생성** — Week 1 모니터에 랜덤 사용자 · 인증 반전 로직 추가 (현실적 분포 확보)
- **JSON 기반 데이터 로드** — access.log 의 JSON 라인을 필터링하여 Pandas DataFrame 으로 변환
- **통계 기반 시각화** — 성공 / 실패 비율(Pie), 사용자별 접근 분포(Bar) 표시
- **Streamlit 대시보드** — 사이드바 필터, 메트릭, 그래프, 데이터 테이블 UI 구성
- **실시간 반영** — 로그 파일 갱신 시 수동 새로고침으로 즉시 반영
- **확장 가능 구조** — Folium 및 GeoIP 추가 시 지역 기반 공격 맵 시각화 가능

---

## Week 1 -> Week 2 확장 포인트

Week 1의 secure_log_monitor.py 에서 달라진 핵심 부분은 **랜덤 로그 생성 로직**이다.
사용자 풀을 6명으로 늘리고, 50회 반복 실행하면서 매 시도마다 25% 확률로 인증 상태를 반전시킨다.
이를 통해 단순한 성공 / 실패 이분법이 아닌 **불규칙한 실제 접근 패턴**을 시뮬레이션한다.

    users = [
        User("admin", authenticated=True),
        User("carol", authenticated=False),
        User("root",  authenticated=True),
        User("guest", authenticated=False),
        User("analyst", authenticated=True),
        User("intern", authenticated=False)
    ]

    for _ in range(50):
        u = random.choice(users)
        if random.random() < 0.25:
            u.authenticated = not u.authenticated   # 25% 확률로 인증 상태 반전
        read_secure_log(u)
        time.sleep(0.05)   # 로그 생성 타이밍 분산 -> 시계열 분석 기반 마련

---

## 핵심 코드 설명 — dashboard.py

### 1. load_access_log — JSON 파싱 -> DataFrame 변환

access.log 에는 한 줄씩 JSON 형태로 로그가 쌓여 있다.
이 함수는 줄 단위로 읽어 { 로 시작하는 유효한 JSON 만 추출해 **Pandas DataFrame** 으로 반환한다.
파일이 없거나 JSON 파싱에 실패한 줄은 안전하게 건너뛴다.

    def load_access_log(path="access.log"):
        if not os.path.exists(path):
            return pd.DataFrame()
        records = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or not line.startswith("{"):
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return pd.DataFrame(records)

---

### 2. 사이드바 필터 — 사용자 · 결과 선택

**st.sidebar.multiselect** 를 사용해 사용자별, 결과(SUCCESS / FAIL)별 필터를 제공한다.
기본값으로 전체를 선택한 상태에서 시작하며, 선택 변경 즉시 하위 시각화에 반영된다.

    user_filter   = st.sidebar.multiselect("사용자 선택", df["user"].unique(),   default=df["user"].unique())
    result_filter = st.sidebar.multiselect("결과 선택",   df["result"].unique(), default=df["result"].unique())

    filtered = df[
        (df["user"].isin(user_filter)) &
        (df["result"].isin(result_filter))
    ]

---

### 3. 메트릭 — 총 시도 수 · 실패율 계산

필터링된 데이터 기준으로 **총 접근 시도 수**와 **실패율(%)** 을 계산해 상단에 요약 표시한다.
0으로 나누는 오류를 방지하는 안전 처리도 포함되어 있다.

    st.metric("총 접근 시도", len(filtered))

    fail_count = (filtered["result"] == "FAIL").sum()
    fail_rate  = (fail_count / len(filtered)) * 100 if len(filtered) > 0 else 0
    st.metric("실패율 (%)", f"{fail_rate:.1f}")

---

### 4. Plotly 시각화 — Pie Chart & Bar Chart

**Pie Chart** 는 SUCCESS / FAIL 비율을, **Bar Chart** 는 사용자별 접근 시도 분포를 인터랙티브하게 표시한다.
두 그래프 모두 Plotly Express 를 사용해 마우스 호버 시 세부 수치가 표시된다.

    fig_pie = px.pie(
        filtered,
        names="result",
        title="Access Result Ratio",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    fig_bar = px.bar(
        filtered,
        x="user",
        color="result",
        barmode="group",
        title="Access Attempts per User"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

---

## 대시보드 구성 요약

| 항목 | 내용 |
|------|------|
| **필터 (Sidebar)** | 사용자 선택, 결과 선택 (SUCCESS / FAIL) |
| **메트릭 (상단 요약)** | 총 접근 시도 수, 실패율 (%) |
| **그래프 ①** | Pie Chart — 접근 결과 비율 (SUCCESS vs FAIL) |
| **그래프 ②** | Bar Chart — 사용자별 접근 시도 및 결과 분포 |
| **데이터 테이블** | Raw Log Data — 필터링된 JSON 로그 목록 |

---

## SOC 관점 연계

이번 프로젝트는 **로그 -> 정제 -> 시각화 -> 인사이트 도출** 과정을
보안관제(SOC) 의 기초 분석 사이클로 옮겨온 것이다.

- **로그 수집 (Collection)** — Week 1 확장 버전에서 랜덤 로그 생성 및 수집
- **데이터 정제 (Preprocessing)** — Pandas 기반 JSON 파싱 및 구조화
- **이벤트 시각화 (Visualization)** — Plotly 로 성공 / 실패 분포 분석
- **대시보드 분석 (Dashboard)** — Streamlit UI 로 사용자별 / 시간대별 필터링
- **보고 및 판단 (Reporting)** — 보안 이벤트 패턴 및 실패율 시각화

---

## 학습 연결 포인트

- **numpy, pandas** => 로그 데이터 정규화 및 전처리
- **random 모듈** => 인증 여부를 무작위로 전환하여 다양한 로그 패턴 생성
- **groupby, pivot_table** => 사용자별 / 시간대별 탐지 이벤트 집계
- **matplotlib, seaborn** => 탐지율 및 실패율 그래프 작성
- **plotly.express** => 인터랙티브 시각화 구현
- **streamlit** => 대시보드 UI 구성 및 필터 연동
- **time.sleep()** => 로그 생성 타이밍 분산으로 시계열 분석 기반 마련

---

## 확장 아이디어

- **시계열 분석** — 로그 생성 시각 기반 시간대별 접근 추이 Line Chart
- **실시간 업데이트** — st_autorefresh(interval=5000) 로 5초마다 자동 갱신
- **지도 시각화** — Folium + GeoIP 로 공격 발생 지역 표시
- **심화 집계** — Pandas 그룹화로 사용자별 실패율 / 평균 응답시간 계산
- **위협 인텔리전스 연계** — 외부 Threat Intelligence API 결합

---

> Week 2 프로젝트는 Week 1의 탐지 엔진을 데이터 분석 레이어로 확장한 단계다.
> 로그를 "텍스트"가 아닌 **"데이터"** 로 바라보는 관점을 체득하는 것이 핵심이다.
