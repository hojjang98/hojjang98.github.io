---
title: "2025.11.18 (Day 17) Project: Streamlit 시각화 대시보드 구현 완료"
date: 2025-11-18
draft: false
tags: ["팀프로젝트", "Streamlit", "멀티페이지", "대시보드", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "Streamlit 멀티페이지 대시보드 구현 및 RAG 기반 영화 추천 UI 완성"
---

# 📄 2025.11.18 (Day 17) [Project: Streamlit 시각화 대시보드 구현 완료]

## 1. 핵심 개념 정리 (Concepts & Theory)

| # | 핵심 개념 | 간결한 설명 | 적용 내용 |
|:---:|:---:|:---|:---|
| **1** | Streamlit Multi-Page | 하나의 `app.py`를 중심으로 여러 Python 파일을 독립된 페이지로 분리하는 구조. | `app.py`가 메인, 나머지 파일이 개별 페이지 역할. |
| **2** | @st.cache_data | 데이터 로드 함수에 적용하여 데이터가 변경되지 않는 한 재실행 없이 캐시된 결과를 재사용. | `load_data()` 함수에 적용하여 대시보드 로딩 속도 최적화. |
| **3** | RAG 기반 추천 UI | 사용자의 자연어 쿼리 또는 영화 제목으로 Vector DB를 검색하고, LLM이 추천 사유를 생성하도록 UI 구성. | `movie_recommendation.py`에서 `st.radio`로 검색 모드 선택 기능 구현. |
| **4** | 재사용 가능한 유틸리티 | 데이터 로드, Vector DB 로드, LLM 호출 등 핵심 기능을 별도 모듈로 분리하여 코드의 모듈화 및 재사용성 극대화. | `data_loader.py`, `vector_db.py`, `llm_utils.py`로 분리. |

## 2. 모듈 및 역할 분담 (Module Breakdown & Suggested Roles)

| 역할 (Suggested Role) | 파일 명 | 주요 기능/담당 업무 |
| :--- | :--- | :--- |
| **데이터/인프라 엔지니어** | `data_loader.py`, `vector_db.py` | 데이터 로드 및 전처리 데이터 제공, TMDB 포스터 URL 생성, ChromaDB 로드 및 검색 유틸리티 구현. |
| **분석/시각화 개발자** | `eda_dashboard.py`, `box_office_analysis.py` | 장르별 분석, 시계열 트렌드 분석 (Plotly), 흥행 지표(ROI, 수익) 시각화 및 흥행 영화 Top 10% 기준 분석. |
| **AI/LLM 시스템 개발자** | `llm_utils.py`, `movie_recommendation.py` | LLM 클라이언트 설정, Vector 검색 기반 추천 UI 구성, LLM 추천 설명 및 흥행 요인 분석 API 연결. |
| **프로젝트 통합 담당** | `app.py` | Streamlit 멀티페이지 구조 정의 및 통합, 메인 페이지 구현, 전체 데이터 통계 요약 및 페이지 라우팅 관리. |

## 3. 핵심 코드 (Streamlit UI 구성)

### (A) 메인 앱 구조 (app.py)

```python
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="Movie Analysis & Recommendation",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎬 Movie Analysis & Recommendation System")
st.markdown("""
## Welcome to the Movie Analysis Platform!
... (주요 기능 목록)
왼쪽 사이드바에서 원하는 페이지를 선택하세요!
""")

# 데이터 통계 요약 (data_loader.py 사용)
# ... (생략)
```

### (B) 추천 시스템 UI (movie_recommendation.py)

```python
# 검색 방식 선택
search_mode = st.radio(
    "검색 방식 선택:",
    ["자연어로 검색", "영화 제목으로 검색"],
    horizontal=True
)

# 검색 입력 창
query = st.text_input("검색어를 입력하세요:", value="")
n_results = st.slider("추천 개수", 1, 10, 5)

if st.button("검색 시작"):
    # vector_db.py의 search_similar_movies 호출
    # ... (검색 결과 출력 및 LLM 설명 호출)
```

## 4. 요약 및 다음 단계 (Summary & Next Steps)

- 팀 프로젝트의 핵심인 Streamlit 기반 대시보드 구현을 완료했습니다.
- 데이터 로드, 벡터 DB, LLM 호출 등 기능을 모듈화하여 구조적 안정성을 확보했습니다.
