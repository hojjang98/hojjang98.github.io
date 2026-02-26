---
title: "2025.11.17 (Day 16) Project: Data Acquisition & Preprocessing"
date: 2025-11-17
draft: false
tags: ["팀프로젝트", "ChromaDB", "RAG", "데이터전처리", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "TMDB 데이터 이상치 제거·텍스트 정제 및 ChromaDB Vector DB 구축"
---

# 📄 2025.11.17 (Day 16) [Project: Data Acquisition & Preprocessing]

## 1. 핵심 개념 정리 (Concepts & Theory)

| # | 핵심 개념 | 간결한 설명 | 적용 내용 |
|:---:|:---:|:---|:---|
| **1** | 데이터 이상치 처리 | 분석 품질을 높이기 위해 비정상적인 데이터 범위를 제거. runtime 30분 미만 제거, vote_count 5 미만 제거. |
| **2** | 텍스트 정제 | title 및 overview에서 이모티콘, 특수 유니코드, 다중 공백 등 불필요한 문자를 제거. LLM 임베딩의 정확도를 높이는 전처리 과정. |
| **3** | Vector DB 구축 | TMDB 영화 데이터의 텍스트 필드(title, overview, genres, keywords)를 결합하여 임베딩 데이터베이스를 생성. ChromaDB를 사용했으며, OpenAI text-embedding-ada-002 모델을 임베딩 함수로 지정. |
| **4** | 배치 처리 | 대량의 데이터를 임베딩할 때 API 요청 제한(rate limit)을 피하기 위해 데이터를 작은 단위(BATCH_SIZE = 20)로 나누어 처리. 안정적인 Vector DB 구축을 위한 필수 기법. |

## 2. 실습 코드 & 응용 (Practice & Code Walkthrough)

### (A) 텍스트 정제 함수 (Preprocessing)

```python
# 이모티콘 및 제어문자를 제거하는 함수
def clean_text(x):
    if pd.isna(x):
        return x
    x = str(x)
    x = emoji_pattern.sub("", x) # 이모티콘 제거
    x = control_pattern.sub(" ", x) # 제어문자 제거
    x = multi_space.sub(" ", x) # 다중 공백 제거
    x = x.strip()
    return x
```

### (B) 임베딩용 텍스트 결합 및 Vector DB 생성

```python
# 임베딩 정확도 향상을 위해 텍스트 필드를 결합하는 함수
def create_movie_text(row):
    return f"{row['title']} {row['title']} {row['overview']} Genres: {row['genres']} Keywords: {row['keywords']}"

# 컬렉션 생성 및 임베딩 함수 지정
embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-ada-002"
)
collection = chroma_client.create_collection(
    name="movies",
    embedding_function=embedding_function
)
```

### (C) 데이터 품질 관리 (이상치 제거)

```python
# runtime 30분 미만, vote_count 5 미만 영화 데이터 제거
df = df[df["runtime"] >= 30]
df = df[df["vote_count"] >= 5]
```

## 3. 요약 및 다음 단계 (Summary & Next Steps)

- TMDB 영화 데이터를 latin-1 인코딩으로 성공적으로 로드하고, 이상치 및 결측치 제거, 텍스트 정제 과정을 거쳐 데이터 품질을 확보했습니다.
- RAG 분석을 위한 **ChromaDB Vector DB 구축**을 완료했으며, 배치 처리 기법(BATCH_SIZE = 20)을 적용하여 안정성을 높였습니다.
- **다음 단계:** 구축된 Vector DB와 데이터 분석 결과를 Streamlit 기반의 시각화 대시보드에 통합하는 작업을 진행합니다 (11월 18일 활동).

## 4. 개인 인사이트 (Reflection)

- **배운 점:** 데이터 분석 프로젝트에서 전처리 단계가 RAG와 같은 LLM 기반 시스템의 최종 검색 품질(임베딩 품질)에 얼마나 결정적인 영향을 미치는지 체감했습니다.
- **느낀 점:** title, overview, genres, keywords를 결합하여 임베딩 텍스트를 구성한 것이 검색 맥락을 풍부하게 만들 것으로 기대됩니다. 그리고 얼마나 교육용 데이터가 아닌 데이터가 까다로운지 다시 체감했습니다.
