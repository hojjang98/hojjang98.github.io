---
title: "DeepLog: Anomaly Detection and Diagnosis from System Logs 구조 분석"
date: 2025-11-08
categories: ["paper-review"]
tags: ["DeepLog", "LSTM", "Log-Analysis", "Deep-Learning", "Anomaly-Detection", "Root-Cause-Analysis", "ACM-CCS", "Sequence-Modeling"]
draft: false
summary: "LSTM을 활용하여 시스템 로그를 자연어처럼 모델링함으로써 비정상 패턴을 탐지하고, 파라미터 값 변화와 워크플로우 분석을 통해 장애의 근본 원인까지 진단하는 딥러닝 기반 로그 분석 프레임워크 연구"
---

# [Research Review] DeepLog: Anomaly Detection and Diagnosis from System Logs

> **Source:** ACM CCS 2017 | Min Du, Feifei Li, Guineng Zheng, Vivek Srikumar
> **Keywords:** Log Analysis, Deep Learning, LSTM, Anomaly Detection, Root-Cause Analysis

---

## Day 1 – 연구 배경 및 핵심 아이디어

### 1. 연구 배경과 동기

* **현대 시스템의 로그 복잡성:** 대규모 분산 시스템(Hadoop, Spark 등)은 초당 수천 건 이상의 로그를 생성한다. 이는 시스템 상태 파악의 핵심 단서이지만, 방대한 양으로 인해 수동 분석이 불가능하다.
* **기존 접근법의 한계:** * **규칙 기반(Rule-based):** 미리 정의된 패턴만 탐지 가능하며, 새로운 유형의 이상(Zero-day Anomaly)에 무력하다.
* **전통적 ML(PCA, SVM 등):** 로그의 핵심적 특징인 **순차적 의존성(Sequence Dependency)**을 반영하지 못하고 독립적인 점으로 처리한다.



### 2. 핵심 연구 질문

> "로그를 언어 시퀀스로 모델링하여, 다음에 발생할 이벤트를 예측함으로써 이상을 탐지할 수 있을까?"

### 3. 주요 기여 및 인사이트

* **로그의 언어화:** 로그를 문장(Sequence)으로, 각 이벤트를 단어(Token)로 간주하여 NLP 방법론을 도입했다.
* **LSTM 기반 예측:** 정상 시퀀스를 학습하여 다음 이벤트를 예측하고, 예측 범위를 벗어나는 실제 이벤트를 이상으로 판단한다.
* **One-class Supervised Learning:** 정상 로그만으로 학습이 가능하여, 비정상 레이블이 부족한 실제 환경에 최적화되었다.
* **자동 진단(Diagnosis):** 단순 탐지를 넘어 이상 발생 시 관련 시퀀스를 역추적하여 원인을 분석하는 기능을 제공한다.

---

## Day 2 – 프레임워크 개요 및 전처리

### 1. 로그 전처리 (Log Parsing)

비정형 문자열 로그를 모델이 이해할 수 있는 **Log Key(Event ID)** 단위로 정규화한다.

* 예: `INFO Block 1234 received from 10.1.1.5` → `Block <*> received from <*> (ID: 45)`
* Drain, Spell 등의 파서를 통해 정규화된 토큰 시퀀스로 변환한다.

### 2. 전체 프로세스

1. **학습 단계:** 정상 로그 시퀀스를 LSTM에 입력하여 패턴을 학습한다.
2. **탐지 단계:** 실제 로그 유입 시 모델이 예측한 **Top-K** 결과에 실제 로그가 포함되지 않으면 이상으로 분류한다.
3. **진단 단계:** 이상 탐지 시점의 Hidden State 변화를 분석하여 근본 원인(Root Cause)을 추정한다.

---

## Day 3 – 모델 상세 및 학습 구조

### 1. 입력 데이터 표현 (Input Representation)

* 최근 개의 이벤트를 슬라이딩 윈도우 방식으로 입력한다.
* 각 이벤트는 고차원 **임베딩 벡터**로 매핑되어 이벤트 간의 의미적 유사성을 학습한다.

### 2. LSTM 네트워크 구조

* **예측 수식:** 
* 마지막 Hidden State()를 Softmax 계층에 통과시켜 모든 이벤트 ID에 대한 확률 분포를 산출한다.

### 3. 하이퍼파라미터 설정 (논문 기준)

| 파라미터 | 설명 | 권장값 |
| --- | --- | --- |
| Window Size () | 입력 시퀀스 길이 | 10 |
| Hidden/Embedding Size | 은닉 및 임베딩 차원 | 128 |
| Top-K | 이상 탐지 허용 범위 | 9 |

---

## Day 4 – 실험 및 성능 평가

### 1. 실험 데이터셋

* **HDFS:** 1,100만 라인, 48개 이벤트 타입 (정상 데이터 위주)
* **BGL:** 400만 라인 (슈퍼컴퓨터 로그, 정상/이상 혼합)
* **OpenStack:** 클라우드 환경 로그

### 2. 주요 결과 분석

* **성능 우위:** PCA, Invariant Mining, Isolation Forest 등 기존 기법 대비 F1-Score에서 압도적 성능을 보였다. (HDFS 기준 PCA 대비 약 15% 향상)
* **시퀀스 학습의 효과:** 단순 빈도 분석이 아닌 '순서'를 학습함으로써 복잡한 논리적 오류 탐지에 성공했다.
* **진단 정확도:** Hidden State의 코사인 거리가 급변하는 지점을 통해 Root Cause를 효과적으로 식별했다.

---

## Day 5 – 결론 및 향후 과제

### 1. 연구의 의의

* **패러다임 전환:** 보안 관제를 '규칙 위반 확인'에서 '정상 맥락 학습'으로 전환시켰다.
* **XAI의 기초:** 단순 블랙박스 모델을 넘어 이상 징후에 대한 설명을 시도했다.

### 2. 한계점 및 발전 방향

* **Cold Start 문제:** 시스템 초기 구축 시 학습을 위한 정상 데이터 확보가 필수적이다.
* **실시간성 제약:** LSTM의 순차 연산 특성상 대규모 트래픽 환경에서 병목이 발생할 수 있다.
* **기술적 진화:** 본 연구는 이후 Transformer 구조를 채택한 **LogBERT, LogGPT** 등 대규모 로그 언어 모델(LLM for Logs) 연구의 모태가 되었다.

