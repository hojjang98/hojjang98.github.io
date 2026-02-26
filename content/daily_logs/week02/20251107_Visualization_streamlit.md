---
title: "2025.11.07 (Day 10) Folium · Plotly · Streamlit 기반 시각화 실습 학습 로그"
date: 2025-11-07
draft: false
tags: ["Python", "Folium", "Plotly", "Streamlit", "로그시각화", "보안대시보드", "보안활용", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "Folium 지도 시각화, Plotly 인터랙티브 그래프, Streamlit 대시보드 구성 실습. 공격 지점·시간대별 패턴 분석을 위한 보안 시각화 파이프라인 구성 방법 정리."
---

# 2025.11.07 (Day 10) [Folium · Plotly · Streamlit 기반 시각화 실습]

## 1. 핵심 개념 정리(Concepts & Theory)

| # | 핵심 개념 | 간결한 설명 | 적용 예시 |
|:---:|:---:|:---|:---|
| 1 | **Matplotlib 한글 폰트 설정** | Windows 환경에서 그래프 내 한글 깨짐을 방지하기 위해 `malgun.ttf`를 수동 등록, `unicode_minus` 옵션으로 마이너스 부호 오류를 해결함. | `font_manager.FontProperties(fname=path)` / `plt.rcParams['axes.unicode_minus']=False` |
| 2 | **Folium 지도 시각화** | 위도·경도 좌표를 기반으로 HTML 인터랙티브 지도를 생성하고, 마커·원형·팝업 요소를 이용해 위치 데이터를 시각적으로 표현함. | `folium.Map(location=[lat, lng])`, `folium.Marker(...).add_to(map)` |
| 3 | **Pandas 데이터 연동** | 엑셀 데이터를 불러와 반복문으로 각 위치를 지도에 표시함. | `for name, lat, lng in zip(data.index, data['위도'], data['경도']): ...` |
| 4 | **Plotly Express 시각화** | 막대그래프·산점도를 통해 수치형 데이터를 인터랙티브하게 비교·탐색함. | `px.bar(df, x='Country', y='Gdp')`, `px.scatter(df, x='Population', y='Gdp')` |
| 5 | **Streamlit 기반 대시보드 구성** | 파일 업로드, 멀티셀렉트 필터, Plotly 그래프 출력 등 UI 요소를 통해 데이터 대시보드를 구축함. | `st.file_uploader()`, `st.sidebar.multiselect()`, `st.plotly_chart()` |

**핵심 인사이트:** 오늘의 학습은 정적 시각화(Matplotlib)를 넘어, 인터랙티브 시각화(Folium, Plotly, Streamlit)를 통해 사용자가 직접 데이터를 조작하고 탐색할 수 있는 보안 시각화 대시보드의 초석을 다지는 데 초점을 맞추었다.

---

## 2. 실습 코드 & 응용 (Practice & Code)

### (1) Folium – 지도 기반 시각화
```python
import folium as g

map = g.Map(location=[37.5574771, 127.0020518])
g.Marker([37.5574771, 127.0020518], popup='동국대학교').add_to(map)
g.CircleMarker([37.5574771, 127.0020518], radius=50, color='red').add_to(map)
map
```

Folium을 통해 특정 좌표에 마커와 원형을 표시하며, 실제 위치 데이터의 시각적 탐색이 가능함을 확인했다. 이 기법은 IP 위치·보안 장비 위치 등 지리 기반 보안 데이터 시각화에 활용 가능하다.

### (2) Pandas + Folium – 엑셀 데이터 연동
```python
import pandas as pd
file_path = r"C:\Users\user\data\서울지역_대학교_위치.xlsx"
data = pd.read_excel(file_path, index_col=0)

for name, lat, lng in zip(data.index, data['위도'], data['경도']):
    folium.Marker([lat, lng], popup=name).add_to(map)
map
Pandas의 반복문을 통해 다수의 지리 데이터를 자동 시각화함으로써, 데이터프레임 → 지도 표현의 자연스러운 연결을 익혔다. 동일한 방식으로 공격 발생 지점, 로그 수집 위치 등 보안 이벤트를 지도상에 표시할 수 있다.  
### (3) Plotly Express – 인터랙티브 데이터 탐색  
python
import plotly.express as px
df = pd.DataFrame({
    'Country': ['한국', '미국', '일본', '호주'],
    'Gdp': [1000, 2000, 3000, 4000],
    'Population': [100, 200, 300, 400]
})

fig = px.bar(df, x='Country', y='Gdp', title='국가별 GDP')
fig.show()

fig02 = px.scatter(df, x='Population', y='Gdp', title='GDP vs Population')
fig02.show()
```

Plotly는 시각화 결과를 동적으로 조작할 수 있어, 보안 로그나 트래픽 데이터를 실시간 탐색하는 데 유용하다. 특히 대시보드형 보안 데이터 시각화의 기반으로 활용할 수 있다.

### (4) Streamlit – 데이터 대시보드 구현
```python
import streamlit as st
import plotly.express as px
import pandas as pd

st.title('관리자 대시보드')
file = st.file_uploader('csv 파일 업로드 : ')

if file is not None:
    rawData = pd.read_csv(file)
    st.success(f'{file.name} 업로드 성공')

    countryFilter = st.sidebar.multiselect('국가선택:', rawData['country'].unique())
    attackFilter = st.sidebar.multiselect('공격타입:', rawData['attack_type'].unique())
    filterData = rawData[(rawData['country'].isin(countryFilter)) & (rawData['attack_type'].isin(attackFilter))]

    fig = px.line(filterData, x='time', color='attack_type')
    st.plotly_chart(fig)
```

Streamlit을 통해 파일 업로드부터 필터링, Plotly 시각화까지 한 번에 구성하며 데이터 → 시각화 → UI 연결의 전체 파이프라인을 경험했다.

---

## 3. 보안 관점 분석 (Security Insight)

| 보안 영역 | 적용 방식 | 기대 효과 |
|:--|:--|:--|
| **SOC / 관제** | 국가별·시간대별 공격 패턴을 Folium과 Plotly로 시각화하여 침입 집중 구간을 탐지 | 실시간 위협 인식, 이상 트래픽 패턴의 시각적 확인 |
| **CERT / 사고대응** | 공격 발생 위치(IP 기반 지역정보) 및 시간 흐름을 지도상에 재구성 | 공격 경로 복원, 사고 시점별 이벤트 재현 |
| **DevSecOps** | 빌드 로그나 취약점 스캔 결과를 Streamlit 대시보드로 표시하여 즉시 피드백 | 빌드 안정성 향상, 자동화된 품질 모니터링 |
| **취약점 진단 / 펜테스트** | 스캐너 결과를 지도형 인터페이스로 시각화하여 취약한 시스템 구간을 직관적으로 표시 | 리스크 맵 기반 보고서 작성, 취약 구간 집중 관리 |
| **디지털 포렌식** | 특정 좌표·시간 구간을 중심으로 로그 데이터를 시각화하여 증거의 시공간적 관계 분석 | 공격자 이동 경로, 증거 연관성 강화 |
| **개인정보 보호** | 지도 시각화 시 민감정보(IP, 사용자 ID)를 익명화·마스킹 후 표시 | 개인정보 노출 최소화 및 규제 준수 |

Folium은 공간적 통찰, Plotly는 패턴 탐색, Streamlit은 실시간 대시보드의 역할을 한다. 이 세 요소를 결합하면 보안 이벤트를 단순 로그가 아닌 시각적 맥락(Context)으로 해석할 수 있다.

---

## 4. 요약 (Summary)

1. Matplotlib → Folium → Plotly → Streamlit의 시각화 확장 흐름을 다루었다.
2. 지도 기반의 Folium 실습을 통해 공격 지점·기관 위치 등 공간 데이터의 활용법을 익혔으며, Plotly로 인터랙티브 그래프를 구성해 시계열 및 비교형 분석 기법을 체득했다.
3. Streamlit 구조를 통해 데이터 업로드 → 필터링 → 시각화 출력의 전 과정을 자동화함으로써, 실시간 보안 분석 대시보드의 기초 설계를 경험했다.

---

## 개인 인사이트 (Reflection)

- **배운 점**: Folium을 통해 지리 기반 보안 데이터를 시각화하는 방법을 익히며, 단순 로그 데이터가 지도 위의 패턴으로 바뀌는 경험을 했다. 이는 보안 이벤트의 시공간적 이해(Spatial-Temporal Awareness)를 확장하는 계기가 되었다.
- **느낀 점**: Streamlit의 단순한 코드 구조로도 충분히 실무형 대시보드를 만들 수 있다는 점이 놀라웠다. 데이터를 눈으로 직접 탐색하는 과정이 기존의 정적 분석보다 훨씬 빠르고 직관적이었다.
- **심화 방향**: 앞으로는 GeoIP 변환 + Folium Heatmap + Plotly Time-Series를 결합해 공격 발생 지역·시간·유형을 동시에 분석하는 통합형 보안 시각화 시스템을 구현하고자 한다. 궁극적으로는 Streamlit을 SOC 환경에 맞춘 실시간 공격 감시 웹앱으로 발전시킬 계획이다.
- **향후 계획**: 이번에 익힌 Streamlit UI 구조와 Folium, Plotly 시각화 방식을 직접 보안 로그 시각화 프로젝트에 적용해볼 예정이다. 공격 로그를 자동 시각화하고, 필터 기반 탐색 및 리포트 기능까지 통합한 프로토타입 대시보드를 구현하여 GitHub에 정리할 계획이다.