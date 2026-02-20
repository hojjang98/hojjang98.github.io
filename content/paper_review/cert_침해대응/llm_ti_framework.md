---
title: "Advancing Autonomous Incident Response: Leveraging LLMs and Cyber Threat Intelligence"
date: 2025-11-14
categories: ["paper-review"]
tags: ["CERT", "침해대응", "LLM", "ThreatIntelligence", "SOAR", "자동화"]
draft: false
summary: "LLM과 위협 인텔리전스를 결합하여 CERT의 사고 대응 프로세스를 자동화하고, 지속 학습형 보안 대응 시스템을 구현한 연구"
---

## 논문 정보

- **제목**: Advancing Autonomous Incident Response: Leveraging LLMs and Cyber Threat Intelligence
- **저자**: Tellache et al.
- **학회/저널**: arXiv
- **발표 연도**: 2025
- **논문 링크**: https://arxiv.org/abs/2508.10677

---

## 1. 연구 배경 및 동기

### CERT의 역할 한계

CERT(Computer Emergency Response Team)는 보안 사고 발생 시 탐지, 분석, 대응, 복구를 담당하는 핵심 조직이다. 그러나 대부분의 프로세스가 여전히 **사람 중심의 수동 판단**에 의존하고 있어 속도와 정확도 모두 제한적이다.

### 데이터 폭증 문제

현대 CERT는 하루 수십 GB 규모의 로그와 수백 건의 Threat Intelligence(TI) 피드를 분석해야 한다. 이런 비정형 데이터들을 사람이 직접 맥락적으로 해석하는 것은 사실상 불가능하다.

### 핵심 문제의식

- CERT의 대응 절차는 여전히 "사건 단위"로 분절되어 있으며, **지식이 누적되지 않는다**
- Threat Intelligence는 수집되지만 **실시간 대응 프로세스와 연동되지 않는다**
- 결과적으로 "속도 병목(Bottleneck)"과 "지식 단절(Knowledge Gap)"이 발생한다

---

## 2. 핵심 아이디어

논문은 CERT의 대응 체계를 **LLM(Large Language Model)**과 **Threat Intelligence**를 결합해 자동화하려는 새로운 방향을 제시한다.

### 핵심 구조

1. **로그 및 TI 입력 통합**: MISP, STIX/TAXII 포맷 데이터를 LLM 입력으로 변환
2. **맥락 분석**: LLM이 사건 로그를 해석해 공격 시퀀스 및 IOC 관계를 추론
3. **대응 제안**: SOAR(보안 오케스트레이션 자동화)와 연동하여 자동 대응 시나리오 생성
4. **지식 피드백**: 결과를 TI 데이터베이스로 되돌려 학습 루프(Feedback Loop) 완성

---

## 3. 시스템 아키텍처

시스템은 총 4개의 핵심 모듈로 구성된다.

| 계층 | 구성요소 | 역할 |
|------|-----------|------|
| **Data Ingestion Layer** | MISP Connector, STIX/TAXII Parser | 로그, IoC, Threat Feed를 표준 포맷으로 수집 및 정규화 |
| **Reasoning Layer (LLM Core)** | Domain-Tuned LLM 모델 | 사건 로그 분석, 공격 시퀀스 추론, 대응 전략 생성 |
| **Action Layer (SOAR Interface)** | Orchestrator, Response Script Engine | LLM 출력을 SOAR 플랫폼에 전달해 자동 대응 실행 |
| **Knowledge Layer** | Threat DB, Feedback Module | 대응 결과를 TI 데이터베이스로 재귀 반영하여 지식 갱신 |

### 데이터 흐름

1. 보안 시스템에서 로그 입력
2. LLM Reasoning Layer에서 공격 패턴 추론
3. SOAR Interface가 적절한 대응 시나리오 선택
4. 자동 스크립트 혹은 분석가 승인 후 조치 시행
5. 결과 및 새로운 IOC가 Threat DB로 반영

---

## 4. LLM Reasoning 메커니즘

### 추론 과정 (3단계)

| 단계 | 역할 | 입력/출력 |
|------|------|-----------|
| Event Parsing & Contextualization | 로그에서 핵심 엔터티 추출 및 위협 맥락 설정 | 입력: Syslog/MISP 데이터 → 출력: Structured Prompt |
| Threat Correlation Reasoning | IoC, TTP 간 관계를 추론해 공격 시퀀스 재구성 | 입력: Normalized Prompt → 출력: Attack Graph 설명 |
| Response Planning | 공격 단계별 대응 전략 생성 | 출력: SOAR Action Command or Playbook Draft |

### Prompt Engineering 전략

**1. Structured Prompt Format**
- Threat 데이터를 JSON 스키마 형태로 입력
- 각 필드에 명확한 의미를 부여 (attack_vector, affected_host, impact_score)
- 객체 단위 추론(Object-based Reasoning) 유도

**2. Context-Aware Prompt Chaining**
- 다단계 Prompt 연쇄로 처리
- 이벤트 요약 → 의심 행동 분석 → 공격 단계 추론 → 대응 제안
- Chain-of-Reasoning 흐름 구성

**3. Threat Schema Alignment**
- MITRE ATT&CK 및 CVE 데이터베이스 태그 활용
- LLM 출력 형식을 기존 보안 분류체계와 정렬
- 보안 온톨로지 일관성(Threat Ontology Consistency) 보장

### Human-in-the-Loop 검증

- CERT 분석가가 LLM의 추론 결과를 점검하고 오탐/과잉대응 차단
- 분석가 평가를 Knowledge Layer에 기록
- 이전 피드백을 LLM Fine-tuning에 반영해 지속적 개선

---

## 5. 실험 및 평가

### 실험 환경

- **데이터셋**: 실제 MISP 피드와 공개 로그 데이터(Zeek, Splunk Export) 혼합
- **로그**: 약 5만 건의 보안 이벤트 로그 및 500개 이상의 IoC 세트
- **LLM 구성**: GPT-4 기반 도메인 튜닝 모델
- **SOAR 시스템**: Cortex XSOAR 실험용 인스턴스 연동
- **비교 대상**: 전통 규칙기반 IR 시스템, LLM 비적용형 SOAR

### 평가 지표

| 지표 | 설명 |
|------|------|
| **Detection Accuracy** | 이벤트에서 공격 단계를 정확히 식별한 비율 |
| **Response Latency** | 사건 분석부터 대응 조치까지 소요된 시간 |
| **Automation Rate** | 인간 개입 없이 LLM-SOAR 루프로 처리된 비율 |
| **False Action Rate** | 불필요하거나 잘못된 대응이 실행된 비율 |
| **Knowledge Reuse Score** | 이전 사건 지식이 재활용된 빈도 및 효율 |

### 실험 결과

| 항목 | 기존 규칙기반 | LLM-TI 프레임워크 | 개선 |
|------|----------------|-------------------|------|
| Detection Accuracy | 82% | 95% | +13%p |
| Response Latency | 약 47초 | 19초 | -60% |
| Automation Rate | 45% | 79% | +34%p |
| False Action Rate | 7% | 3% | -4%p |
| Knowledge Reuse | 낮음 | 지속적 상승 | 질적 개선 |

---

## 6. 주요 기여

1. **Threat Intelligence 기반 CERT 자동화 프레임워크 제안**
   - 로그, IoC, TI 데이터를 LLM 입력으로 통합하여 사건의 전후 관계를 추론하는 구조 제시

2. **Human-in-the-loop 기반 설계**
   - LLM의 판단을 CERT 분석가가 검증함으로써 완전 자동화가 아닌 "지능적 보조(Assisted Intelligence)" 구조로 구성

3. **운영 지식의 순환 체계화**
   - 사건별 분석 결과가 TI로 재귀적 업데이트되어, 조직 차원의 지식 성장을 유도

4. **실험적 검증**
   - 탐지 정확도, 대응 속도, 지식 재활용 효율 모두 향상

---

## 7. 한계점

1. **데이터 다양성 부족**
   - 실험 환경이 제한된 로그·TI 데이터셋에 기반하여 실제 기업·국가 단위 CERT 환경의 복잡성을 완전히 반영하진 못함

2. **LLM 비용 및 지연**
   - 고성능 LLM의 연산비용과 응답 지연(latency)이 여전히 실시간 대응에 부담

3. **TI 품질 의존성**
   - Threat Intelligence 데이터의 정확도·갱신 주기에 따라 전체 성능이 크게 달라질 수 있음

4. **모델 보안 리스크**
   - 공격자가 LLM의 입력이나 Prompt를 조작(Prompt Injection)할 가능성에 대한 보안 검토는 미흡

---

## 8. 향후 연구 방향

| 방향 | 설명 |
|------|------|
| **Multi-Agent CERT Collaboration** | 여러 LLM 에이전트가 역할을 분담(탐지/대응/보고)하여 협력하는 구조 연구 |
| **Lightweight On-Prem LLMs** | 클라우드 의존도를 줄이고, 로컬 환경에서 구동 가능한 소형 보안 특화 LLM 개발 |
| **Reinforcement Learning 기반 대응 정책 최적화** | RL을 이용해 실제 공격 시나리오에서 대응 전략을 자가 학습하도록 개선 |
| **Threat Data Augmentation** | 실험 데이터를 확대하고, 비정형 로그를 구조화하는 자동 파이프라인 연구 |
| **Secure Prompting** | LLM 입력(Prompt)에 대한 보안 방어 연구 - Prompt Injection·Data Poisoning 대응 |

---

## 9. 실무적 시사점

### CERT 운영 관점

- LLM을 탐지 이후의 '분석-대응-지식화' 단계를 자동화하는 CERT의 두뇌 역할로 활용 가능
- 사건별 분석 결과가 조직 지식으로 누적되는 구조 구현
- Human-in-the-Loop 구조로 완전 자동화의 위험 최소화

### 보안 자동화 관점

- 단순 규칙이나 플레이북 자동화가 아닌, **의미 기반 추론(Semantic Reasoning)**이 보안 자동화의 핵심
- Threat Intelligence 데이터를 직접 활용해 "이유 있는 결정" 가능
- SOAR 통합을 통해 "탐지→분석→대응→학습"의 전 주기를 폐쇄형 루프로 완성

### AI 활용 관점

- LLM은 보안 분석가의 대체물이 아니라 **지식 증폭기(Knowledge Amplifier)**로 작용
- Prompt Engineering 전략을 통해 보안 도메인에 특화된 추론 수행 가능
- 피드백 루프를 통해 시간이 지날수록 조직의 정책·환경에 맞게 진화

---

## 평가

이 논문은 LLM을 보안 도구로 사용하는 것이 아니라 **AI가 스스로 사고 대응을 이해하고 실행하는 단계**로의 진입을 의미한다. SOC·CERT·TI 간의 단절된 워크플로를 하나의 순환 구조로 연결했다는 점에서 실제 현업 적용 가능성이 매우 높다.

DeepLog가 로그 시퀀스를 통해 **탐지 자동화**의 가능성을 열었다면, 이 논문은 **대응 자동화**의 시대를 여는 출발점이라 볼 수 있다. 특히 LLM을 단순 텍스트 생성기가 아닌 **사고 분석 엔진(Analytical Reasoner)**으로 활용했다는 점에서 실무적 의미가 크다.

결국 이 연구는 "AI가 보안 사고를 이해하고 기억하며 대응하는" **자율 보안의 시작점**으로 평가할 수 있다.