---
title: "2025.11.10 (Day 11) Streamlit · OpenAI API를 활용한 보안형 챗봇 앱 구현"
date: 2025-11-10
draft: false
tags: ["Streamlit", "OpenAI", "LLM", "보안챗봇", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "Streamlit과 OpenAI API를 연결하여 API Key 보호·입력 검증·보안형 LLM 챗봇 앱 구현"
---

# 2025.11.10 (Day 11) Streamlit · OpenAI Chat App

## 1. 주요 개념 요약

* **Streamlit UI 구성**: `st.sidebar`, `st.text_area`, `st.button` 등을 활용해 사용자 입력–출력 구조를 설계한다. 빠른 프로토타이핑이 가능해 보안 로그 분석기의 대화 인터페이스로 확장 가능하다.
* **OpenAI API 연결 구조**: `.env` 파일의 API Key를 불러오거나 사용자가 직접 입력하도록 설계하여 OpenAI 클라이언트를 안전하게 초기화한다.
* **ChatCompletion 모델 호출**: GPT 모델(`gpt-4o-mini`)을 사용해 사용자의 입력 텍스트를 처리하고 응답을 반환한다. 모델 호출 로직을 함수화하면 다른 입력(로그, 이벤트, 에러 메시지)에도 재사용 가능하다.
* **보안 LLM 개념**: API Key 보호, 입력 데이터 검증, 프롬프트 인젝션 방어 등 보안 측면에서 LLM 사용의 기초를 이해해야 한다.

---

## 2. 실습 코드 및 응용

### A. Streamlit 기본 UI 구성

* 텍스트 입력과 버튼 출력 구조를 구성하여 이후 LLM 기반 보안 로그 분석기의 인터페이스 기반으로 활용한다.

```python
import streamlit as st

st.set_page_config(page_title='챗 모델을 이용한 응답')
st.header('요약 응답')

text = st.text_area('글 입력')
if st.button('요약해줘'):
    st.info('요약 결과 표시')
```

### B. OpenAI API 연결 및 챗 응답 생성

* 모델 호출 로직을 함수화하여 보안 로그, 이벤트, 에러 메시지 등 다양한 입력에 재사용할 수 있다.

```python
from openai import OpenAI

def askChat(query, key):
    client = OpenAI(api_key=key)
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': query}]
    )
    return response.choices[0].message.content
```

### C. API Key 보안 처리 및 세션 관리

* API Key는 사용자가 직접 입력하며 `st.session_state`에만 임시 저장한다. `.env` 병행 시 환경 분리와 키 노출 방지 효과를 동시에 확보할 수 있다.

```python
from dotenv import load_dotenv
import os

if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ''

with st.sidebar:
    key = st.text_input(label='input key', placeholder='api key', type='password')
    if key:
        st.session_state['api_key'] = key
```

---

## 3. 보안 관점 분석

* **SOC / 관제**: 실시간 로그나 경보 메시지를 LLM으로 요약하여 운영자 피로도를 감소시키고 탐지 피드백 속도를 향상시킨다.
* **CERT / 사고대응**: 공격 단계별 로그를 LLM에 입력하여 사건 개요·원인·조치 요약을 자동 생성하고 브리핑 효율성을 높인다.
* **DevSecOps**: 빌드 로그·취약점 스캔 결과를 ChatCompletion으로 자동 요약하여 CI/CD 파이프라인에서 자동 리포팅 시스템을 구축할 수 있다.
* **취약점 진단 / 펜테스트**: 모의해킹 결과 텍스트를 입력해 취약점 유형별 요약 및 리스크 레벨을 자동 분류한다.
* **데이터 프라이버시**: 사용자 입력값 검증 및 마스킹 처리로 민감정보 노출을 최소화하고 모델 입력 안정성을 확보한다.

---

## 4. 요약

1. Streamlit + OpenAI Chat API를 통해 LLM 응용 서비스를 빠르게 프로토타이핑하는 방법을 익혔다.
2. `.env` 또는 `session_state`를 이용한 API Key 보호 구조로 보안 환경에서의 안전한 모델 호출을 구현했다.
3. LLM 응답을 단순 대화가 아닌 보안 로그·사고 보고서 자동 요약에 적용할 수 있음을 확인했다.
4. 본 실습은 이후 LangChain, Guardrails, RAG 기반 보안 LLM 파이프라인 학습의 기초가 된다.
