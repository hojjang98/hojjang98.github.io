---
title: "2025.11.13 (Day 14) 실시간 로그 모니터링 · RAG 보안 챗봇 통합 실습"
date: 2025-11-13
draft: false
tags: ["실시간모니터링", "RAG챗봇", "FAISS", "Streamlit", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "실시간 로그 스트리밍과 RAG 기반 보안 챗봇을 하나의 Streamlit 앱으로 통합한 모니터링 시스템 구현"
---

# 2025.11.13 (Day 14) 실시간 로그 모니터링 · RAG 보안 챗봇 통합 실습

## 1. 주요 개념 요약

* **Streamlit 기반 Real-Time Streaming**: `st.empty()` + `time.sleep()`으로 5초 간격 로그 스트림 시뮬레이션을 구성하여 실시간 로그 누적 출력을 구현한다.
* **FAISS + OpenAIEmbedding VectorDB**: 공격 로그를 텍스트화 → 분할 → 임베딩 → 벡터DB 구축하는 흐름으로 맥락 기반·근거 기반 분석을 가능하게 한다.
* **ConversationalRetrievalChain**: RAG와 챗봇 대화 기록을 결합해 문맥 기반 보안 분석을 수행한다. 이전 대화 내용을 기억하며 연속적인 질의를 처리한다.
* **Session State 관리**: 실시간 로그, 메시지 이력, 대화 메모리를 `st.session_state`에 저장하여 앱 상태를 안전하게 유지한다.
* **2-Column 대시보드 UI**: 좌측 실시간 로그 / 우측 RAG 챗봇 형태의 보안 관제 화면을 구성하여 탐지 → 분석 → 보고 흐름을 하나로 통합한다.

---

## 2. 실습 코드 및 응용

### A. 실시간 로그 모니터링

* 5초 간격으로 새 로그를 누적하고 고위험 이벤트 발생 시 경보를 표시한다. `risk_score` 임계값 기반으로 실시간 탐지를 수행한다.

```python
if 'logs' not in st.session_state:
    st.session_state['logs'] = pd.DataFrame(columns=frm.columns)

logPrt = st.empty()
warningPrt = st.empty()

for idx, row in frm.iterrows():
    newLog = row.to_dict()

    st.session_state['logs'] = pd.concat([
        pd.DataFrame([newLog]),
        st.session_state['logs']
    ])

    if newLog['risk_score'] >= 85:
        warningPrt.warning('고위험 공격 감지!! 집중')
    else:
        warningPrt.info('시스템 정상 작동 중')

    logPrt.dataframe(st.session_state['logs'])
    time.sleep(5)
```

### B. RAG 기반 보안 챗봇

* 공격 로그를 자연어 문장으로 변환하여 벡터DB를 구축하고 `ConversationalRetrievalChain`을 통해 근거 기반 위협 분석을 생성한다.

```python
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = splitter.create_documents(database)

embeddings = OpenAIEmbeddings()
vectorDB = FAISS.from_documents(docs, embeddings)

retriever = vectorDB.as_retriever(k=10)
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.9)
qa_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)

response = qa_chain({
    "question": prompt,
    "chat_history": st.session_state["chat_history"]
})
```

---

## 3. 보안 관점 분석

* **SOC / 관제**: 실시간 로그 스트림이 5초 간격으로 갱신되어 공격 유형·리스크 점수를 즉시 확인할 수 있으며, 경보 + 자동 분석 챗봇 구조를 통해 탐지 → 분석 → 보고 흐름이 하나로 통합된다.
* **CERT / 사고대응**: RAG 분석 결과가 공격자 IP·시점·공격 방식 등 사고 타임라인 재구성에 직접 활용되며, 원본 로그 근거 기반 분석으로 사고 보고서 품질이 향상된다.
* **취약점 진단 (VA)**: 벡터DB에 축적된 과거 공격 로그를 기반으로 반복적 공격 여부를 유사도로 비교하여 특정 서비스·포트에 대한 재발 위협을 식별한다.
* **DevSecOps**: 빌드 로그나 테스트 로그도 동일한 RAG 구조에 넣으면 자동 분석·요약 시스템을 구축할 수 있으며 파이프라인 오류 원인·보안 취약점을 자동으로 요약한다.
* **디지털 포렌식**: 로그의 시간·행위 기반 연속성을 바탕으로 공격 흐름을 시각적으로 재구성하여 추적·증거 확보 과정의 효율성을 강화한다.

---

## 4. 요약

1. 실시간 로그 흐름과 RAG 기반 보안 분석 모델이 어떻게 연결되는지를 직접 구현하면서 보안 관제 자동화의 기초 작동 흐름을 이해했다.
2. 벡터DB 구성을 통해 단순 텍스트 검색이 아닌 맥락 기반·근거 기반 분석이 가능해지는 흐름을 확인했다.
3. 실시간 스트림과 대화형 분석 모델이 한 화면에서 함께 동작하는 구조를 통해 현업 관제 화면 구성의 원리를 체감했다.
