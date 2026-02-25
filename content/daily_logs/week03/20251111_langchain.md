---
title: "2025.11.11 (Day 12) LangChain · RAG 기반 OpenAI Dashboard 구축"
date: 2025-11-11
draft: false
tags: ["LangChain", "RAG", "FAISS", "벡터DB", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "LangChain의 RAG 구조와 FAISS 벡터스토어를 활용한 검색 기반 OpenAI Dashboard 구현"
---

# 2025.11.11 (Day 12) LangChain · Streamlit 기반 OpenAI Dashboard 구축

## 1. 주요 개념 요약

* **RAG (Retrieval-Augmented Generation)**: 외부 문서 데이터베이스에서 관련 정보를 검색(Retrieve)한 후, LLM의 응답 생성을 보강(Augment)하는 구조이다. 단순 모델 호출이 아닌 "검색 가능한 지식창고 + LLM" 구조를 구축하는 것이 핵심이다.
* **FAISS 벡터스토어**: 문서 임베딩을 벡터 공간에 저장하고, 질의(query)와 가장 유사한 벡터를 빠르게 검색하는 라이브러리이다.
* **OpenAI Embeddings API**: 텍스트를 고차원 벡터로 변환하는 임베딩 모델(`text-embedding-3-small` 등)로, RAG의 'Retrieve' 단계 검색 정확도를 결정한다.
* **LangChain Text Splitter**: 긴 문서를 일정 크기 단위의 청크(chunk)로 나누어 효율적인 검색 및 문맥 기반 답변을 가능하게 한다.
* **Streamlit 대화형 UI 구성**: 사용자 텍스트 입력 → LLM 질의 → 결과 출력 과정을 웹 인터페이스로 구현하여 직관적인 보안 대시보드형 어시스턴트로 발전시킬 수 있다.

---

## 2. 실습 코드 및 응용

### A. 문서 분할 및 벡터 임베딩

* 문서 분할과 벡터 임베딩을 통해 단순 텍스트를 검색 가능한 지식 벡터 공간으로 변환한다. 이는 RAG의 'Retrieve' 단계의 핵심이며 검색 정확도를 결정짓는다.

```python
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

docs = [
    '리스트는 변경 가능한 자료형입니다.',
    '튜플은 변경 불가능한 자료형입니다.',
    '딕셔너리는 키와 값으로 데이터를 저장합니다.'
]

splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = splitter.create_documents(docs)

embeddings = OpenAIEmbeddings(openai_api_key=api_key, model='text-embedding-3-small')
db = FAISS.from_documents(texts, embeddings)
```

### B. RAG 기반 LangChain 체인 구성

* `RetrievalQA`를 활용해 벡터스토어 검색 결과와 LLM 응답 생성을 파이프라인으로 연결한다. 보안 로그 질의 시스템, SOC 대시보드, 정책 검색 도우미 등으로 확장 가능하다.

```python
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

retriever = db.as_retriever(search_kwargs={"k": 1})
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-4o-mini", temperature=0.9),
    chain_type="stuff",
    retriever=retriever
)

query = "파이썬에서 리스트와 튜플의 차이는?"
answer = qa.run(query)
print(answer)
```

### C. Streamlit UI 구현

* Streamlit을 통해 질문 입력 → RAG 검색 → LLM 응답 확인을 직관적인 대화형 인터페이스로 전환한다.

```python
import streamlit as st

st.title('LangChain + RAG 기반 OpenAI Dashboard')

query = st.text_input('질문을 입력하세요 : ')
if query:
    with st.spinner('데이터베이스 검색 중...'):
        qa, retriever = ask_gpt()
        answer = qa.run(query)
        st.success('A - ' + answer)
        st.caption('R - ' + retriever.get_relevant_documents(query)[0].page_content)
```

---

## 3. 보안 관점 분석

* **SOC / 관제**: 실시간 로그·이벤트 데이터를 벡터로 저장하고 LLM 질의를 통해 이상 로그 요약·검색·설명을 수행하여 탐지 효율을 향상시킨다.
* **CERT / 사고대응**: 사고 시점의 로그를 검색 가능한 벡터로 관리하여 공격 경로 및 이전 유사 사고를 빠르게 조회하고 사고 원인 분석을 자동화한다.
* **DevSecOps**: 빌드 로그, 테스트 결과, 취약점 리포트를 RAG로 관리하여 개발자가 자연어로 검색할 수 있는 환경을 구축하고 자동 보고 시스템으로 발전시킨다.
* **취약점 진단 / 펜테스트**: 과거 스캔 결과와 취약점 패턴을 기반으로 질의형 검색을 수행하여 자동 리포트 초안을 작성하고 중복 검출을 강화한다.
* **디지털 포렌식**: 덤프·로그 데이터를 벡터화하여 증거 탐색을 자동화하고 데이터 범위를 축소하여 포렌식 효율을 높인다.

---

## 4. 요약

1. LangChain의 `RetrievalQA`는 RAG 기반 검색-응답 구조의 중심축으로, 외부 지식을 검색·활용하는 보안형 Dashboard 구축의 핵심 컴포넌트이다.
2. Streamlit UI를 통해 보안 로그나 정책 문서를 대화형 분석 도구로 전환할 수 있음을 확인했다.
3. `FAISS` 외에도 `Chroma`, `Milvus` 같은 대규모 벡터 DB로 확장하면 실시간 SOC 질의형 어시스턴트로 발전시킬 수 있다.
