---
title: "2025.11.19 (Day 18) Project: LangChain/RAG 분석 모델 통합 및 PPT 초안 제작"
date: 2025-11-19
draft: false
tags: ["팀프로젝트", "RAG", "LangChain", "발표준비", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "LangChain/RAG 분석 모델 Streamlit 통합 완료 및 발표 PPT 핵심 시나리오 구성"
---

# 📄 2025.11.19 (Day 18) [Project: LangChain/RAG 분석 모델 통합 및 PPT 초안 제작]

## 1. 핵심 개념 정리 (Concepts & Theory)

| # | 핵심 개념 | 간결한 설명 | 적용 내용 |
|:---:|:---:|:---|:---|
| **1** | RAG 최종 통합 | Vector DB 검색 (Retrieval)과 LLM 응답 생성 (Generation) 모듈을 Streamlit 앱에 최종 연결하여 End-to-End 분석 기능 완성. | `movie_recommendation.py`를 통해 사용자 쿼리에 근거 기반 추천 제공. |
| **2** | 모듈식 RAG 구조 | LLM Client, Vector DB I/O, 데이터 로드 기능을 각각 독립적인 Python 파일로 분리하여 유지보수 용이성 및 코드 명확성 확보. | `llm_utils.py`, `vector_db.py`, `data_loader.py` 파일 분리. |
| **3** | PPT 핵심 내용 정의 | 구현 완료된 대시보드 기능을 중심으로 프로젝트의 목적, 기술 스택, 시각화 분석 결과 및 RAG 시연 시나리오를 구성. | 발표 시간 배분을 고려하여 내용의 깊이와 분량 조정. |

## 2. 실습 코드 & 응용 (Practice & Code Walkthrough)

### (A) Vector DB 클라이언트 로드 (vector_db.py)

```python
# vector_db.py: 11월 17일에 구축한 ChromaDB 클라이언트를 로드
db_path = Path("../vector_db/chroma_db")
chroma_client = chromadb.PersistentClient(path=str(db_path))

collection = chroma_client.get_collection(
    name="movies",
    embedding_function=embedding_function # embedding_function은 llm_utils에서 정의 가능
)
```

### (B) LLM 유틸리티 함수 (llm_utils.py)

```python
# llm_utils.py: LLM 호출 관련 유틸리티 및 RAG Chain 통합
from openai import OpenAI
import os

def get_openai_client():
    # API Key 로드 및 Client 초기화
    openai_api_key = os.getenv('OPENAI_API_KEY')
    return OpenAI(api_key=openai_api_key)

# (LangChain Chain 또는 커스텀 RAG 함수가 여기에 통합됨)
# analyze_movie_success(title)
# recommend_movies(query)
```

### (C) 추천 검색 흐름 (movie_recommendation.py)

```python
# movie_recommendation.py: 추천 검색 결과를 프론트엔드에 출력
if st.button("검색 시작"):
    # 1. vector_db.py를 통해 Vector DB에서 관련 영화 검색 (Retrieval)
    results = vector_db.search_similar_movies(query)

    # 2. llm_utils.py를 통해 LLM이 검색 결과 기반으로 추천 사유 생성 (Generation)
    llm_explanation = llm_utils.generate_explanation(results, query)

    st.subheader("LLM 추천 분석 결과")
    st.markdown(llm_explanation)
```

## 3. 요약 및 다음 단계 (Summary & Next Steps)

- LangChain의 핵심 원리(Retriever, Generator 분리)를 **모듈화된 파이썬 함수**로 구현하여 Streamlit 대시보드에 성공적으로 통합했습니다.
- RAG 기능을 활용한 **근거 기반 추천 분석**이 가능해졌음을 확인하고, 이를 중심으로 발표 자료(PPT)의 핵심 시나리오 구성을 완료했습니다.
- **다음 단계:** 11월 20일에는 발표 자료의 최종적인 디자인 수정, 분석 내용 보강, 프레젠테이션 연습 등 **최종 발표 준비**에 집중합니다.

## 4. 개인 인사이트 (Reflection)

- **배운 점:** RAG 구현 시 LangChain 라이브러리 전체를 가져오지 않고도, **ChromaDB와 OpenAI API**만으로 핵심적인 검색-생성 구조를 독립적으로 구축할 수 있음을 확인했습니다.
- **느낀 점:** Streamlit에서 `llm_utils`나 `vector_db`를 @st.cache_resource로 관리하면, LLM 호출 전에 DB를 매번 초기화할 필요가 없어 성능이 대폭 향상될 것으로 기대됩니다.
