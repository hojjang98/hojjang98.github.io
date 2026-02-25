---
title: "2025.11.12 (Day 13) RAG & LLM 기반 보안 로그 분석 대시보드"
date: 2025-11-12
draft: false
tags: ["RAG", "LLM", "보안로그분석", "Plotly", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "LLM과 RAG를 활용한 보안 로그 자동 분석, 위험도 분류, 지리적 공격 시각화 대시보드 구현"
---

# 2025.11.12 (Day 13) RAG & LLM 기반 보안 로그 분석 대시보드

## 1. 주요 개념 요약

* **LLM 기반 로그 요약**: 원시 로그 일부를 LLM에게 전달하여 공격 유형·국가·위험도 등을 JSON 구조로 자동 추출한다. JSON-only 시스템 프롬프트 설계가 핵심이다.
* **RAG (Retrieval-Augmented Generation)**: 외부 문서(보안 정책, 룰북, MITRE 문서 등)를 임베딩 후 검색하여 LLM이 맥락 기반 분석을 수행하도록 한다.
* **Streamlit 보안 대시보드**: CSV 업로드 → 전처리 → LLM 분석 → 시각화까지 한 화면에서 처리하는 파이프라인을 구축한다.
* **지리 기반 보안 시각화**: 공격 IP의 위도·경도를 기반으로 세계 지도 상에 공격 분포를 표현하여 공격 국가와 집중 지역을 직관적으로 파악한다.
* **위험도 기반 우선순위화**: LLM이 생성한 `risk_score`(1~10) 기준으로 고위험 IP를 자동 필터링하여 대응 우선순위를 결정한다.

---

## 2. 실습 코드 및 응용

### A. LLM 로그 구조화 프롬프트

* JSON-only 시스템 프롬프트를 사용하여 LLM이 로그에서 핵심 엔터티를 구조화된 형태로 추출하도록 한다.

```python
system_content = '''
당신은 사이버보안 전문가입니다.
업로드된 로그를 분석하고 JSON만 출력하세요.
[
  {"ip": "", "country": "", "attack_type": "", "risk_score": 8}
]
'''
```

### B. Streamlit 대시보드 기본 흐름

* CSV 파일 업로드부터 LLM 분석, 결과 시각화까지 하나의 대시보드로 구성하여 가벼운 SIEM 형태의 로그 분석 파이프라인을 구현한다.

```python
st.title("LLM 기반 보안 로그 분석 대시보드")

file = st.file_uploader("로그 CSV 업로드")

if file:
    df = pd.read_csv(file)
    response = ask_llm(df)
    result = pd.DataFrame(json.loads(response.choices[0].message.content))
    st.dataframe(result)
```

### C. Plotly 기반 공격 위치 시각화

* `risk_score`를 색상으로, 공격 IP의 위도·경도를 좌표로 사용하여 공격 분포를 세계 지도에 시각화한다.

```python
fig = px.scatter_geo(
    result,
    lat="latitude",
    lon="longitude",
    color="risk_score",
    hover_name="ip",
    projection="natural earth",
    color_continuous_scale="Reds",
    size="risk_score"
)
st.plotly_chart(fig)
```

---

## 3. 보안 관점 분석

* **SOC / 관제**: LLM이 로그의 핵심 엔터티를 정리하여 탐지 속도를 높이고, 지리적 분포를 통해 공격 국가·집중 지역을 빠르게 파악할 수 있다.
* **CERT / 사고대응**: IP·공격 유형·국가 자동 추출을 통해 사고 흐름(시간 → 공격자 → 피해 범위)을 재구성하고 공격자의 패턴·경로를 시각적으로 재현할 수 있다.
* **위협 인텔리전스**: 위험도 기반으로 우선 대응해야 할 공격자 그룹을 분리하고, 공격 유형 분포를 통해 최신 공격 트렌드를 파악한다.
* **DevSecOps**: 빌드·스캔 로그도 동일한 구조로 요약·분석하여 반복적 오류·취약점의 자동 분류에 활용할 수 있다.
* **개인정보 보호**: IP나 User ID를 마스킹한 뒤 요약하도록 설계하여 분석 요건과 규제 준수를 동시에 만족한다.

---

## 4. 요약

1. RAG + LLM + Streamlit을 결합해 가벼운 SIEM 형태의 로그 분석 파이프라인을 구축했다.
2. 공격 유형·국가·위험도를 구조화하고 시각화(Bar + Geo Plot)를 통해 보안 인사이트를 강화했다.
3. LLM을 단순 요약기가 아닌 보안 이벤트 해석 엔진으로 활용할 수 있음을 확인했다.
