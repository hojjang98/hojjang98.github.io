---
title: "Research Review: UNICORN - Runtime Provenance-Based Detector for APT"
date: 2026-01-12
categories: ["paper-review"]
tags: ["SOC", "APT-Detection", "Provenance-Graphs", "Anomaly-Detection", "Graph-Sketching", "Evolutionary-Modeling", "UNICORN", "NDSS-2020", "SK-Shieldus-Rookies"]
series: ["SOC-Expertise-Deep-Dive"]
draft: false
summary: "TB급 시스템 로그를 Graph Sketching으로 압축하고 시스템의 시계열적 변화를 학습하는 Evolutionary Modeling을 통해, 시그니처 없는 Low-and-Slow APT 공격을 실시간으로 탐지하는 프레임워크 연구"
---

# Research Review: UNICORN: Runtime Provenance-Based Detector for Advanced Persistent Threats
> **Analyzed Date:** 2026.01.08 - 2026.01.12  
> **Keywords:** APT Detection, Provenance Graphs, Anomaly Detection, Graph Sketching, Evolutionary Modeling  
> **Source:** Network and Distributed System Security Symposium (NDSS), 2020, pp. 1-18  
> **Link:** https://www.ndss-symposium.org/ndss-paper/unicorn-runtime-provenance-based-detector-for-advanced-persistent-threats/

---

## Why This Paper?

### 선정 배경

**이 논문을 선택한 이유:**  
- Beehive에서 학습한 네트워크 로그 분석을 더 깊은 레벨인 시스템 호출 수준 provenance 그래프로 확장
- SOC의 최종 보스인 APT 탐지 - 가장 탐지하기 어려운 공격 유형을 다룸
- 단순 탐지를 넘어 long-running 시스템에서 stealthy 공격을 어떻게 찾아내는지에 대한 방법론
- 그래프 기반 분석은 현대 SOC의 핵심 기술 - EDR, XDR의 기반 원리

**학습 목표:**  
1. Provenance 그래프 기반 APT 탐지의 원리와 실무 적용 방법 이해
2. Graph sketching과 evolutionary modeling이라는 새로운 접근법 학습
3. Long-running APT 캠페인을 탐지하는 SOC 역량 강화

---

## Day 1 – Research Context & Motivation
*(APT의 핵심 특성과 탐지의 근본적 어려움)*

### 1. 연구 배경: Low-and-Slow APT 탐지의 한계

**APT의 중요성**

APT는 현대 사이버 보안의 가장 심각한 위협이다. 일반 공격과 달리 APT는:
- Long timescale: 수개월에서 수년에 걸쳐 진행
- Stealthy: 정상 트래픽에 섞여 들어가 탐지 회피
- Zero-day exploits: 사전 시그니처가 없어 기존 탐지 우회
- Targeted: 특정 조직을 정교하게 공격

**현실의 한계**

기존 APT 탐지 시스템들의 문제점:

1. **Syscall trace 기반 접근법의 한계**
   - Host-based IDS는 짧은 시퀀스만 분석
   - Long-term context 부족 - APT의 긴 시간 스팬을 포착 못 함
   - 정상 행위와 구분 어려움

2. **Static model의 한계**
   - Long-running 시스템의 동적 행동 변화 포착 못 함
   - 시스템이 진화하면 false positive 급증

3. **Dynamic model의 한계**
   - Runtime 중 모델 업데이트 시 공격자가 모델을 점진적으로 poisoning 가능
   - Low-and-slow 공격이 정상으로 학습됨

**연구 문제의식**

어떻게 long-running 시스템에서 low-and-slow APT 공격을 정확하게 탐지할 것인가? 특히:
- 시그니처 없이 zero-day 탐지
- 수개월간의 시스템 실행 history를 효율적으로 분석
- 모델 poisoning 방지하면서도 시스템 진화 대응

### 2. 핵심 개념

| 개념 | 정의 | SOC 맥락에서의 의미 |
|------|------|---------------------|
| **Provenance Graph** | 시스템 전체의 인과관계를 표현하는 방향 그래프. 노드는 프로세스/파일/소켓, 엣지는 시스템 콜 관계 | 단순 로그 분석을 넘어 전체 attack chain을 추적. 공격자가 어떻게 lateral movement 했는지 시각화 |
| **Graph Sketching** | 큰 그래프를 고정 크기의 요약 벡터로 압축하는 기법. Weisfeiler-Lehman 알고리즘 기반 | 수십 GB 규모의 audit log를 메모리에 올릴 수 있는 크기로 압축하여 실시간 분석 가능 |
| **Evolutionary Modeling** | 시스템의 시간에 따른 상태 변화를 여러 sub-model로 학습하는 방법 | 시스템 업데이트, 사용자 행동 변화 등을 반영하면서도 급격한 이상은 탐지 |
| **Low-and-Slow Attack** | 수개월에 걸쳐 천천히 진행되어 탐지를 회피하는 APT 공격 패턴 | 일반 IDS는 burst traffic만 탐지. SOC는 장기 baseline과 비교하여 미세한 drift 감지 필요 |

### 3. 이론적 기반: Provenance-Based Anomaly Detection

```
[Audit Logs] → [Provenance Graph Construction]
                        ↓
            [Streaming Graph Histogram]
                        ↓
            [Graph Sketching (HistoSketch)]
                        ↓
            [Evolutionary Clustering Model]
                        ↓
            [Anomaly Detection via State Transition]
```

**핵심 아이디어:**

UNICORN은 4단계 파이프라인으로 APT를 탐지한다:

1. **Provenance graph 수집**: Linux Audit, Windows ETW 등에서 시스템 전체의 인과관계 그래프 생성
2. **Streaming histogram**: R-hop neighborhood를 탐색하여 각 vertex 주변의 구조적 특징을 histogram으로 요약
3. **Graph sketching**: Histogram을 고정 크기 벡터로 압축 (HistoSketch) - gradually forgetting 기법으로 최근 활동에 가중치
4. **Evolutionary model**: Training 중 생성된 여러 시점의 sketch를 clustering하여 시스템의 정상 상태 전이 패턴 학습

Detection 시에는 새로운 sketch가 학습한 cluster에 fit하는지, 그리고 state transition이 valid한지 검사한다.

### 4. 연구의 핵심 기여

**학술적 기여:**

1. **Graph sketching 기반 APT 탐지 프레임워크**
   - Long-running 시스템의 전체 history를 고정 크기 데이터 구조로 요약
   - Weisfeiler-Lehman 알고리즘을 streaming 환경에 적용
   - Time-weighted histogram으로 인과관계와 시간 locality 동시 반영

2. **Evolutionary modeling**
   - 단일 training trace에서 시간에 따른 여러 시스템 상태를 학습
   - Concept drift 대응하면서도 model poisoning 방지
   - State transition 기반 anomaly detection

3. **APT 특성에 특화된 4가지 설계 원칙**
   - L1: Rich historical context - R-hop graph exploration
   - L2: Contextualized analysis - Causality-based graph neighborhood
   - L3: Robust long-term modeling - Evolutionary model without runtime update
   - L4: Space efficiency - In-memory histogram, no full graph storage

**SOC 실무 기여:**

1. **시그니처 없는 Zero-day APT 탐지**
   - Anomaly-based 접근으로 unseen attack pattern 탐지
   - DARPA dataset에서 모든 APT 공격 탐지 성공

2. **기존 SOTA 대비 성능 향상**
   - StreamSpot 대비 precision 24% 향상, accuracy 30% 향상
   - False positive 대폭 감소

3. **Real-time 실용성**
   - 평균 CPU 사용률 <5%
   - Memory footprint: ~200MB (TB 규모 audit log 처리)
   - Processing speed: 평균 11,000 events/second

### 5. SOC 관점 인사이트

**실무 적용 가능성:**

UNICORN은 EDR/XDR의 차세대 백엔드 엔진으로 활용 가능하다. 현재 대부분의 EDR은 rule-based이지만, UNICORN의 provenance 기반 anomaly detection은:
- Supply chain attack 같은 신종 APT 탐지
- Insider threat의 long-term behavior 추적
- Threat hunting 시 공격 전체 kill chain 재구성

**기존 학습과의 연결:**

- **DeepLog와의 비교**: DeepLog는 단일 시스템의 log sequence anomaly. UNICORN은 전체 시스템의 graph structure anomaly
- **Lou et al.과의 비교**: Invariants mining은 rule-based. UNICORN은 clustering-based unsupervised learning
- **Beehive와의 비교**: Beehive는 network-level workflow. UNICORN은 system-level provenance graph

Progression: Log sequence → Network workflow → System provenance graph

**현실적 고려사항:**

1. **Ground truth 문제**: APT는 실제 환경에서 label이 불명확. 어떻게 모델 평가?
2. **Parameter tuning**: R, |S|, λ 등 하이퍼파라미터를 각 환경에 맞게 조정 필요
3. **Provenance overhead**: CamFlow 같은 whole-system provenance 수집의 성능 오버헤드
4. **False positive 관리**: 정상 시스템 업데이트도 anomaly로 탐지 가능 - 정기적 재학습 필요

---

## Day 2 – Research Model, Hypotheses, and Methodology
*(Graph Sketching과 Evolutionary Modeling의 설계)*

### 1. 연구 모델 개요

```
[Training Phase]
Streaming Provenance Graph
    ↓
[1] Incremental Histogram Construction (R-hop exploration)
    ↓
[2] Periodic Sketching (gradually forgetting with λ)
    ↓
[3] Sketch Collection over time: S(t₁), S(t₂), ..., S(tₙ)
    ↓
[4] Evolutionary Clustering: Group sketches into clusters
    ↓
[5] State Transition Model: Track cluster sequences

[Detection Phase]
New Streaming Graph → Histogram → Sketch → S(t_new)
    ↓
Check: (1) Does S(t_new) fit any cluster?
       (2) Is state transition valid?
    ↓
[Anomaly if either fails]
```

**설계 철학:**

UNICORN은 APT의 4가지 특성에 대응하도록 설계되었다:

1. **Long-running**: Graph sketching으로 수개월 history를 고정 크기로 요약
2. **Stealthy**: Evolutionary modeling으로 미세한 deviation 탐지
3. **Zero-day**: Unsupervised anomaly detection - 사전 시그니처 불필요
4. **Contextualized**: R-hop exploration으로 causal relationship 포함

### 2. 연구 가설 (핵심 가정)

| 가정 | 내용 | 근거 |
|------|------|------|
| **A1: Provenance graphs capture APT** | 시스템 전체의 인과관계 그래프는 APT의 전체 attack chain을 포함한다 | APT는 시스템 콜을 통해 실행되며, provenance는 모든 시스템 콜 관계를 기록 |
| **A2: APT는 정상과 구조적으로 다르다** | APT의 provenance graph 구조는 정상 시스템 행동과 통계적으로 구분 가능하다 | 공격자의 reconnaissance, exploitation, exfiltration은 정상 workflow와 다른 graph pattern 생성 |
| **A3: Sketch preserves anomaly signal** | Graph를 sketch로 압축해도 anomaly detection에 필요한 정보는 보존된다 | Weisfeiler-Lehman 기반 histogram은 graph isomorphism test에 준하는 구별력 |
| **A4: System evolution is gradual** | 정상 시스템의 행동 변화는 점진적이며, 급격한 변화는 anomaly다 | 소프트웨어 업데이트, 사용자 습관 변화는 서서히 진행되며, APT 공격은 갑작스럽게 나타남 |
| **A5: No adversarial model poisoning** | Kernel과 provenance 수집 시스템은 신뢰할 수 있다 | Attested boot, LSM integrity로 보장. 또는 off-host analysis |

### 3. 연구 방법론

#### A. 데이터 수집

**데이터 소스:**

| 소스 | 수집 정보 | 용도 |
|------|-----------|------|
| **Linux Audit** | syscall trace (open, read, write, fork, exec, connect, etc.) | 프로세스-파일-네트워크 간 인과관계 그래프 생성 |
| **CamFlow** | Kernel-level provenance capture | Controlled lab 환경 supply chain attack 시나리오 |
| **DARPA TC Datasets** | CADETS, ClearScope, THEIA from 3 OS platforms | Real APT campaign 평가 |

**데이터 규모:**

- **DARPA datasets**: 2주간 adversarial engagement
  - CADETS (FreeBSD): 90.9M events, 451 GB raw data
  - ClearScope (Linux): 31.8M events, 164 GB
  - THEIA (Linux): 78.5M events, 312 GB
- **Supply Chain scenarios**: 125 benign + 25 attack graphs per scenario
- APT는 전체 audit data의 0.001% 미만 - extreme imbalance

**데이터 특성 및 문제점:**

- **Heterogeneity**: 다양한 OS, 다양한 provenance capture 시스템
- **High volume**: TB 단위 audit log - 메모리에 올릴 수 없음
- **Temporal locality**: 최근 행동이 더 중요하지만, 오래된 인과관계도 유지 필요
- **Partial ordering**: Provenance edge 도착 순서가 실제 발생 순서와 다를 수 있음

#### B. 핵심 알고리즘/기법

**[1] Incremental Histogram Construction**

목적: Streaming provenance graph의 구조적 특징을 효율적으로 추출

방법:
```
1. 초기화: 각 vertex v에 label l(v) 할당 (프로세스, 파일, 소켓 등)
2. For iteration r = 0 to R:
   a. 각 vertex v의 r-hop neighborhood 수집
   b. Multiset M(v) = {l(u) | u는 v의 r-hop neighbor}
   c. Hash M(v) → new label l'(v)
   d. Histogram H[l'(v)] += weight(v, r)
3. Weight function:
   - Temporal locality: w(t) = λ^(-Δt) (gradually forgetting)
   - Causal dependency: w(path_length) = 1 (no discount for causal edges)
```

핵심 아이디어:
- Weisfeiler-Lehman 알고리즘의 streaming 버전
- R-hop exploration으로 local graph structure를 label로 인코딩
- Gradually forgetting: 시간 경과에 따라 weight decay, 단 인과관계는 유지

**[2] Graph Sketching (HistoSketch)**

목적: 무한히 증가하는 histogram을 고정 크기 |S|로 압축

방법:
```
1. Top-|S| frequent histogram elements 선택
2. Normalize: Jaccard similarity 계산을 위해 확률 분포로 변환
3. Sketch S(t) = {(label, frequency) | top |S| elements}
4. Constant time update:
   - New edge 도착 시 affected vertices만 업데이트
   - Batch processing으로 overhead 감소
```

Trade-off:
- |S| 크면: 더 많은 정보, 더 높은 계산 비용
- |S| 작으면: 정보 손실, 빠른 계산

실험에서는 |S| = 2000이 적절함을 확인.

**[3] Evolutionary Clustering**

목적: Training execution의 여러 시점에서 생성된 sketch를 clustering하여 시스템의 정상 상태 학습

방법:
```
1. Training 중 T개의 sketch 생성: {S(t₁), S(t₂), ..., S(tₜ)}
2. Sketch 간 Jaccard distance 계산:
   d(S_i, S_j) = 1 - |S_i ∩ S_j| / |S_i ∪ S_j|
3. Hierarchical clustering with distance threshold θ
4. 각 cluster C_k는 시스템의 한 "meta-state"를 표현
5. Evolution E = ordered sequence of cluster indices
   예: [C₁, C₁, C₂, C₃, C₂, C₃, C₃, ...]
```

Evolutionary model의 장점:
- Single training trace에서 multiple system states 학습
- Concept drift 자동 반영 (시스템이 진화하면 새 cluster 생성)
- Model poisoning 방지 (training 후 model freeze)

#### C. 피처/변수 설계

**피처 설계 원칙:**

Graph의 local structure를 label로 인코딩. 각 label은 특정 r-hop neighborhood pattern을 대표.

**주요 피처:**

| 피처 | 설명 | 계산 방법 |
|------|------|-----------|
| **Vertex label** | 노드 유형 (process, file, socket, pipe) | Provenance graph의 node type |
| **Edge label** | Relation 유형 (read, write, exec, connect) | System call type |
| **R-hop subgraph hash** | r-hop neighborhood의 구조적 fingerprint | Weisfeiler-Lehman hash |
| **Histogram element** | (hash, count) pair | 각 subgraph pattern의 출현 빈도 |
| **Sketch vector** | Top-|S| histogram elements | Normalized frequency distribution |

특징:
- No manual feature engineering - 알고리즘이 자동으로 meaningful pattern 추출
- Heterogeneous graph labels 지원 - 다양한 entity와 relation type
- Temporal weighting - gradually forgetting으로 recency 반영

#### D. 평가 방법

**평가 지표:**

- **Precision**: TP / (TP + FP) - 탐지한 것 중 실제 공격 비율
- **Recall**: TP / (TP + FN) - 실제 공격 중 탐지한 비율
- **Accuracy**: (TP + TN) / (TP + TN + FP + FN)
- **F1-Score**: 2 × (Precision × Recall) / (Precision + Recall)

**비교 대상:**

- **StreamSpot**: 기존 SOTA graph-based anomaly detector
- **Holmes & Poirot**: Rule-based provenance analysis (DARPA dataset에서만)
- **Baseline configuration**: R=1 (no graph exploration)

**Cross-validation:**

- DARPA: 90% training, 10% testing
- Supply Chain: 5-fold cross-validation (100 benign training, 25 benign + 25 attack testing)

### 4. SOC 관점 인사이트

**방법론의 실무 적용성:**

장점:
- **Unsupervised learning**: SOC에 label된 APT 데이터가 없어도 작동
- **Real-time streaming**: Batch processing 불필요, 실시간 모니터링 가능
- **Explainability**: 어떤 graph structure가 anomaly인지 histogram element로 설명 가능

한계:
- **Parameter tuning 필요**: R, |S|, λ, θ를 각 환경에 맞게 조정
- **Initial training 필요**: Clean baseline 확보 - 이미 침투된 상태라면?
- **Concept drift 대응**: 주기적 재학습 필요 (얼마나 자주?)

**기존 SOC 툴과의 차별점:**

| 도구/방법 | 탐지 방식 | 강점 | 약점 |
|-----------|-----------|------|------|
| **Traditional SIEM** | Rule/signature-based | 알려진 공격 확실히 탐지, 설명 쉬움 | Zero-day 못 잡음, rule 유지보수 비용 |
| **UEBA** | User behavior analytics | Insider threat 탐지 | User-level만 보고 system-level 인과관계 부족 |
| **EDR (Rule-based)** | IoC matching | 빠름, FP 적음 | APT는 IoC 없이 진행 |
| **UNICORN** | Provenance graph anomaly | Zero-day APT 탐지, 전체 attack chain 추적 | Parameter tuning 필요, 초기 학습 필요 |

**SOC Workflow 통합 전략:**

```
[1] Endpoint: CamFlow/Auditd → Provenance stream
       ↓
[2] UNICORN Backend: Real-time graph sketching & anomaly detection
       ↓
[3] Alert Generation: Anomalous sketch → High-risk process/file 추출
       ↓
[4] SIEM Integration: Enrich alert with threat intelligence
       ↓
[5] SOC Analyst: Graph visualization으로 attack chain 확인
       ↓
[6] Response: Kill process, isolate host, forensic collection
```

UNICORN을 SIEM의 advanced detection engine으로 통합하면:
- L1: SIEM rule로 1차 필터링
- L2: UNICORN anomaly detection으로 APT 후보 추출
- L3: Analyst가 graph 시각화로 최종 판단

---

## Day 3 – Empirical Results and Hypothesis Testing
*(UNICORN의 APT 탐지 성능 검증)*

### 1. 평가 환경

**실험 설정:**

1. **StreamSpot Benchmark**
   - 데이터: 600 provenance graphs (5 scenario types)
   - 환경: Controlled simulation

2. **DARPA TC Engagement 3**
   - 기간: 2주간 red team vs blue team engagement
   - 데이터: 3개 OS 플랫폼 (FreeBSD, Linux, Linux)
   - 환경: Realistic enterprise network
   - 특징: APT 공격 비율 <0.001% of audit data

3. **Supply Chain Attack**
   - 환경: CamFlow on Ubuntu 16.04
   - 데이터: 2개 시나리오 (SC-1, SC-2) × 125 benign + 25 attack
   - 특징: Attackers know system a priori (harder to detect)

**실험 전략:**

- **Q1**: Can UNICORN detect APTs accurately?
- **Q2**: How important is R-hop exploration?
- **Q3**: Does λ decay (gradually forgetting) improve detection?
- **Q4**: Evolutionary vs static clustering?
- **Q5**: Real-time capability?
- **Q6**: CPU/memory overhead?

### 2. 주요 발견

**전체 결과 요약:**

| Dataset | Precision | Recall | Accuracy | F1-Score |
|---------|-----------|--------|----------|----------|
| **StreamSpot (R=1)** | ~0.94 | ~0.99 | ~0.97 | ~0.96 |
| **StreamSpot (R=3)** | **0.99** | **1.00** | **0.99** | **0.99** |
| **DARPA-CADETS** | 1.00 | 1.00 | N/A | 1.00 |
| **DARPA-ClearScope** | 1.00 | 1.00 | N/A | 1.00 |
| **DARPA-THEIA** | 1.00 | 1.00 | N/A | 1.00 |
| **SC-1** | 0.96 | 1.00 | 0.98 | 0.98 |
| **SC-2** | 0.91 | 1.00 | 0.95 | 0.95 |

**기존 방법과의 비교:**

| Method | Precision | Accuracy | Improvement |
|--------|-----------|----------|-------------|
| **StreamSpot (baseline)** | ~0.75 | ~0.69 | - |
| **UNICORN (R=3)** | 0.99 | 0.99 | +32% precision, +43% accuracy |

UNICORN은 StreamSpot 대비:
- **Precision 24% 향상** (0.75 → 0.99)
- **Accuracy 30% 향상** (0.69 → 0.99)
- R=3 (graph exploration)이 R=1보다 크게 우수

### 3. 상세 분석

#### A. DARPA Real APT Detection

**관찰:**

UNICORN은 3개 플랫폼 모두에서:
- **Precision 1.00**: False positive 0개
- **Recall 1.00**: 모든 APT 공격 탐지

**해석:**

DARPA 시나리오에서 APT가 잘 탐지된 이유:
1. **Reconnaissance phase가 명확**: 공격자가 vulnerability 찾는 과정이 trace에 나타남
2. **Unusual system call sequence**: Exploitation은 정상 user behavior와 명확히 다름
3. **Causal dependency 추적**: Data exfiltration의 전체 provenance chain 포착

Holmes와 Poirot (rule-based)도 모든 공격 탐지했지만:
- 사전 expert knowledge 필요
- New attack vector에는 대응 못 함
- UNICORN은 unsupervised로 동일한 성능

**실무 시사점:**

DARPA 수준의 APT는 SOC에서 충분히 탐지 가능하다. 단, 조건:
- Clean training data (attacker-free baseline)
- Sufficient context (R≥3 hop exploration)
- Proper tuning (|S|=2000, λ appropriate)

#### B. Supply Chain Attack Scenarios

**시나리오 설계:**

**SC-1: Simulated software update**
- Benign: User downloads Firefox updates, installs normally
- Attack: Trojanized Firefox installer executes backdoor
- 특징: Installer behavior is similar to benign

**SC-2: Document processing**
- Benign: User opens PDFs, runs office applications
- Attack: Malicious PDF exploits viewer, drops payload
- 특징: Initial trigger (open PDF) is benign

**결과:**

| Scenario | Precision | Recall | False Positives |
|----------|-----------|--------|-----------------|
| SC-1 | 0.96 | 1.00 | 1/25 |
| SC-2 | 0.91 | 1.00 | 2-3/25 |

**Why lower than DARPA?**

Supply chain 시나리오가 더 어려운 이유:
1. **No reconnaissance phase**: Attacker knows system, 직접 exploit
2. **Initial benign trigger**: Software update나 PDF open은 정상 행동
3. **Gradual payload execution**: Backdoor가 천천히 실행되어 gradually forgetting에 걸릴 수 있음

**실무 시사점:**

Supply chain attack 탐지를 위해서는:
- **Contextual analysis 강화**: R을 3 이상으로
- **Evolutionary model 확장**: 더 많은 training execution으로 edge case 포함
- **Hybrid approach**: UNICORN + rule-based for known supply chain patterns

#### C. Graph Analysis Importance

**실험: R-hop 영향**

SC-1 dataset으로 R을 변화시키며 성능 측정:

| R (hop count) | Precision | Recall | F1 |
|---------------|-----------|--------|----|
| R = 1 | 0.89 | 0.96 | 0.92 |
| R = 3 (baseline) | 0.96 | 1.00 | 0.98 |
| R = 5 | 0.98 | 1.00 | 0.99 |
| R = 7 | 0.98 | 1.00 | 0.99 |

**해석:**

R-hop exploration이 중요한 이유:
- **Causal context**: R=1은 직접 연결만, R=3은 multi-step attack chain 포착
- **Disambiguation**: 동일한 local pattern이라도 wider context로 benign vs attack 구분

예시:
```
R=1: process A → read file X (정상? 공격?)
R=3: process A → read file X ← written by process B ← spawned by suspicious downloader
→ 명확히 attack chain
```

**실무 적용:**

SOC에서 R 선택:
- **R=1**: 빠르지만 부정확 → 실시간 1차 필터
- **R=3**: 균형점 → 대부분의 APT 탐지
- **R=5+**: 높은 정확도 → Threat hunting, forensic analysis

#### D. Evolutionary Modeling vs Static Clustering

**실험:**

| Approach | Description | Precision | Recall |
|----------|-------------|-----------|--------|
| **Static clustering** | Single clustering on all training sketches | 0.88 | 0.96 |
| **Evolutionary (UNICORN)** | Time-ordered clustering | 0.96 | 1.00 |

**Why evolutionary better?**

1. **Concept drift 반영**: Static은 시스템 초기와 말기를 동일하게 취급, Evolutionary는 진화 과정을 state transition으로 학습

2. **False positive 감소**: Static은 정상 업데이트가 anomaly로 탐지됨, Evolutionary는 점진적 변화를 valid state transition으로 인정

3. **Context-aware detection**: Static은 각 sketch를 독립적으로 평가, Evolutionary는 이전 상태로부터의 transition 유효성 검사

**실무 적용:**

Long-running SOC 환경에서 시스템은 끊임없이 변화 (패치, 업데이트, user behavior drift). Static model은 빠르게 obsolete. Evolutionary model은 변화를 흡수하면서도 급격한 anomaly 탐지.

### 4. 성능 효율성

**Processing Speed:**

| Dataset | Events/sec | Latency |
|---------|------------|---------|
| SC-1 | 11,000 | <100ms |
| SC-2 | 10,500 | <100ms |
| DARPA-CADETS | 9,800 | <150ms |

→ Real-time monitoring에 충분

**Resource Usage:**

| Metric | Value |
|--------|-------|
| Average CPU | <5% |
| Peak CPU | 12% |
| Memory footprint | ~200MB |
| Raw data size | TB scale |

→ Commodity hardware에서 실행 가능

### 5. SOC 관점 실무 인사이트

**탐지 측면:**

성공 사례: Multi-stage attacks, data exfiltration, credential dumping, backdoor installation

개선 필요: Fileless attacks (memory-only execution), living-off-the-land (PowerShell, wmic), low-volume exfiltration

**대응 측면:**

우선순위화 전략:

| Priority | Condition | Action | SLA |
|----------|-----------|--------|-----|
| **P1-Critical** | State transition invalid + High-risk process | Immediate isolation | <5min |
| **P2-High** | Sketch outlier (distance > 2σ) | Analyst review | <1hr |
| **P3-Medium** | Sketch outlier (distance > 1.5σ) | Queue for investigation | <24hr |

**분석 측면:**

패턴 인사이트: UNICORN이 발견한 APT 패턴 (supply chain의 subtle variation, stealthy exfiltration의 daily unusual network spike)

Ground Truth 문제: APT evaluation의 근본적 어려움 - 실제 환경에서 "benign"이라 가정한 데이터에 이미 APT가 숨어있을 수 있음

---

## Day 4 – Research Limitations and Scholarly Impact
*(UNICORN의 한계와 provenance 기반 탐지의 발전)*

### 1. 연구의 한계점

#### A. Parameter Sensitivity and Tuning Overhead

**문제:**

UNICORN은 여러 하이퍼파라미터에 의존:
- R (hop count): 1-7 범위, 성능에 큰 영향
- |S| (sketch size): 500-5000, memory-accuracy trade-off
- λ (decay factor): 0.990-0.999, forgetting rate
- θ (clustering threshold): Cluster 개수 결정

각 환경마다 optimal parameter가 다름. 논문에서는 OpenTuner로 자동 tuning했지만 grid search 비용이 크고, 새로운 환경마다 re-tuning 필요.

**해결 방안:**

1. **Transfer learning**: 유사 환경의 parameter를 starting point로 사용
2. **Adaptive parameter selection**: Runtime metric으로 자동 조정
3. **Default configuration**: 논문의 권장값 (R=3, |S|=2000, λ=0.998)을 baseline으로

#### B. Ground Truth and Labeling Challenge

**문제:**

APT 평가의 근본적 어려움:
1. Training data가 정말 clean한가? APT는 이미 수개월 전 침투했을 수 있음
2. Detection의 완전성: DARPA는 red team 공격만 labeled, 다른 숨어있는 공격은?
3. FP vs TP의 애매함: "FP"로 분류한 것 중 일부가 실제 공격일 수 있음

**해결 방안:**

1. **Honeypot-based baseline**: 격리된 환경에서 clean baseline 확보
2. **Multi-stage validation**: UNICORN alert → Threat intel cross-check → Analyst review
3. **Conservative labeling**: "Suspicious but unconfirmed"를 별도 카테고리로

#### C. Fileless and LOLBAS Attacks

**문제:**

UNICORN은 provenance graph에 의존하는데, 일부 공격은 흔적이 적음:

1. **Fileless malware**: Memory-only execution (reflective DLL injection)
2. **Living-off-the-land binaries**: PowerShell, wmic, certutil 등 정상 도구 악용
3. **Kernel-level rootkits**: Provenance 수집 자체를 우회

**해결 방안:**

1. **Behavioral context enrichment**: 누가, 언제, 무엇을 실행했는지 추가 context
2. **Memory forensics 통합**: Provenance 외에 periodic memory scan
3. **Hybrid approach**: UNICORN + YARA rules

#### D. Computational Scalability

**문제:**

논문의 evaluation은 수백 host 규모. 하지만 enterprise는 수만-수십만 endpoints.

**해결 방안:**

1. **Hierarchical architecture**: Endpoint → Regional aggregator → Central SOC
2. **Edge computing**: Endpoint에서 sketch 생성, 중앙에는 sketch만 전송
3. **Distributed clustering**: Apache Spark 기반 parallel processing

### 2. 후속 연구 동향

#### A. 인용 수와 영향력

- 발표: 2020년 NDSS
- 현재 인용 수: ~310회 (연평균 ~62회)
- Provenance 기반 APT 탐지의 주요 reference로 자리잡음

#### B. 연구 트렌드의 변화

```
[2015-2017] Rule-based provenance (Holmes, Poirot)
    ↓
[2017-2019] ML-based anomaly (StreamSpot)
    ↓
[2020] UNICORN (Graph sketching + Evolutionary modeling)
    ↓
[2021-현재] Advanced provenance ML (Deep learning, GNN, Transformer)
```

#### C. 주요 후속 연구

| 연구 | 연도 | 핵심 기여 |
|------|------|-----------|
| **TBDetector** | 2021 | Transformer with self-attention for long-term context |
| **PROGRAPHE** | 2022 | Graph Neural Network on provenance |
| **TFLAG** | 2023 | Temporal GNN + deviation network |
| **PROVNINJA** | 2022 | Adversarial attack on provenance detectors (UNICORN detection 100% → 35%) |
| **MirGuard** | 2023 | Robustness against graph manipulation |
| **NODLINK** | 2024 | Online fine-grained APT across hosts |

개선점: UNICORN의 hand-crafted histogram → learnable embedding, R-hop exploration → attention mechanism, Fixed sketch size → dynamic representation

Trade-off: Explainability 감소, Training 비용 증가, Parameter tuning 더 복잡

### 3. 실무 영향

#### A. 산업 표준화

**UNICORN 이후:**

- DARPA Transparent Computing Program에서 provenance 수집 표준화
- Operating System 지원: Linux eBPF, Windows ETW, macOS Endpoint Security
- Provenance 개념이 EDR/XDR의 핵심 기능으로

#### B. 주요 벤더 채택

| 벤더 | 기술 | UNICORN 영향 |
|------|------|-------------|
| **CrowdStrike Falcon** | Indicator of Attack (IoA) graph | Causal graph 기반 탐지, R-hop context |
| **Microsoft Defender ATP** | Advanced Hunting with KQL | Provenance query, multi-hop relationship |
| **SentinelOne** | Storyline behavioral AI | Process tree를 graph로 표현, anomaly detection |

#### C. 오픈소스/커뮤니티 영향

- **CamFlow**: UNICORN 저자 주도, Linux kernel provenance capture
- **SPADE**: Multi-platform provenance 수집 프레임워크
- **StreamSpot**: UNICORN baseline, community가 재현 실험 수행

### 4. SOC 관점 인사이트

**한계를 인식한 실무 적용 전략:**

전략 1: Defense-in-Depth (L1 signature-based → L2 UNICORN anomaly → L3 analyst review → L4 threat hunting)

전략 2: Hybrid Supervised + Unsupervised (Known APT TTP rule + UNICORN unsupervised + correlation)

전략 3: Continuous Model Validation and Update (월간 재학습 사이클)

**도입 로드맵:**

- **Short-term (1-3개월)**: PoC (pilot hosts, baseline training, parameter tuning)
- **Mid-term (3-6개월)**: Production rollout (critical servers, SOAR integration)
- **Long-term (6-12개월)**: Enterprise scale (all endpoints, distributed architecture)

---

## Day 5 – Conclusions and Practical Implications
*(SOC 실무에 UNICORN 적용하기)*

### 1. 5일간 학습 여정 종합

**Day 1:** APT 탐지의 근본 문제 → Provenance graph 기반 접근의 필요성

**Day 2:** UNICORN의 설계 철학 (Graph sketching + Evolutionary modeling) → Long-term, space-efficient, robust

**Day 3:** 실증적 검증 (DARPA 100% detection, StreamSpot +24% precision) → R=3의 중요성

**Day 4:** 한계와 발전 (Parameter tuning, fileless attack) → 후속 연구 → 산업 표준으로

**Day 5:** 실무 통합 - 어떻게 실제 SOC에 적용할 것인가?

### 2. 이론적 기여 정리

**학술적 의의:**

1. Graph Sketching for APT Detection (long-running provenance를 고정 크기로 압축)
2. Evolutionary Modeling (concept drift 대응 + model poisoning 방지)
3. APT-Specific Design Principles (L1-L4)

**패러다임 전환:**

Before: APT detection = Signature matching, Provenance = Forensics, Anomaly = Static baseline

After: APT detection = Unsupervised graph anomaly, Provenance = Real-time monitoring, Anomaly = Evolutionary model

### 3. SOC 실무 적용 전략

#### A. 탐지 역량 강화

**시나리오 1: Supply Chain Attack**

탐지 룰: Installer process의 R=3 neighborhood 분석 → unexpected child process 발견

임계값: Distance > 0.5 (anomalous)

자동 대응: Process suspend → memory snapshot → network block

기대 효과: MTTD 수일 → 수분, MTTR 수시간 → 수분, FP <5%

**시나리오 2: Data Exfiltration**

탐지 룰: Sensitive file read → network upload correlation 분석

임계값: Volume >10MB/1hr, destination not in whitelist

자동 대응: Block connection → isolate host → notify team

**시나리오 3: Lateral Movement**

탐지 룰: Inter-host connection (SSH, RDP) → target host activity 분석

MITRE ATT&CK: T1021, T1003, T1082

자동 대응: Alert → increase logging → containment

#### B. 대응 역량 강화

**우선순위화:**

| Priority | Condition | SLA | Owner |
|----------|-----------|-----|-------|
| **P1-Critical** | State transition invalid + High-risk TTP | <5min | L3 Senior |
| **P2-High** | Sketch distance > 2σ + Medium-risk TTP | <30min | L2 |
| **P3-Medium** | Sketch distance > 1.5σ | <2hr | L1 |
| **P4-Low** | Marginal anomaly | <24hr | Auto |

**플레이북:**

Data Exfiltration (P1): [AUTO] Block network + Isolate + Capture | [MANUAL] Assess + Hunt

Lateral Movement (P2): [AUTO] Alert + Log | [MANUAL] Map path + Contain + Revoke

Supply Chain (P2): [AUTO] Suspend + Quarantine | [MANUAL] Reverse engineer + Notify vendor

**티켓 예시:**
```
🚨 UNICORN APT ALERT
제목: [P1-CRITICAL] Credential Dumping - DC01
심각도: Critical
담당자: L3-Senior-Team
SLA: <5 minutes

━━━ 탐지 정보 ━━━
Method: UNICORN Evolutionary Model
Sketch Distance: 2.34σ
State Transition: INVALID

━━━ 공격 행위 ━━━
Host: DC01 (Domain Controller)
Process: powershell.exe → lsass.exe memory → C:\temp\c.txt → 192.0.2.123

━━━ MITRE ATT&CK ━━━
• T1003.001 - LSASS Memory
• T1059.001 - PowerShell

━━━ 자동 대응 (완료) ━━━
✅ Network blocked
✅ Host isolated
✅ Memory captured

━━━ 권장 조치 ━━━
1. [URGENT] Review memory dump
2. [URGENT] Reset domain passwords
3. [URGENT] Hunt similar activity
```

#### C. 분석 역량 강화

**Threat Hunting:**

Hidden C2 Communication:
```sql
SELECT hostname, process, remote_ip, COUNT(*) as conn_count
FROM provenance_graph
WHERE timestamp > NOW() - INTERVAL '7 days'
  AND remote_ip NOT IN (SELECT ip FROM whitelist)
  AND protocol IN ('HTTPS', 'DNS')
  AND conn_count > 10
GROUP BY hostname, process, remote_ip;
```

**ROI 측정:**

경영진 보고서:
```
UNICORN 도입 6개월 성과

핵심 지표:
- APT 탐지: 12건 (+200%)
- 침해 차단: 100%
- False Positive: 92% 감소
- MTTD: 47일 → 2.3일 (95% 개선)

투자 대비 효과:
- 도입 비용: $500K
- 방지한 피해액: $8M
- ROI: 1,600%
```

### 4. 프레임워크/표준 연계

#### A. MITRE ATT&CK 매핑

| UNICORN 탐지 | ATT&CK | 탐지 로직 |
|-------------|--------|-----------|
| Credential Dumping | T1003.001 LSASS | Process → read lsass memory |
| Data Exfiltration | T1041 Exfiltration | File read → network upload |
| Lateral Movement | T1021 Remote Services | Unusual SSH/RDP connection |

#### B. NIST Cybersecurity Framework

| NIST | UNICORN 활용 | 적용 |
|------|-------------|------|
| Identify | Asset discovery | 정상 baseline 프로파일링 |
| Protect | Proactive blocking | Supply chain 설치 전 차단 |
| Detect | Real-time anomaly | APT 조기 발견 |
| Respond | Automated containment | P1 alert 시 자동 격리 |
| Recover | Attack chain reconstruction | 침해 범위 정확히 파악 |

### 5. 실전 체크리스트

#### A. 도입 전 준비

**시스템 요구사항:**
- [ ] Linux kernel 4.4+ (eBPF) 또는 CamFlow
- [ ] CPU: 4 cores+, RAM: 16GB+, Disk: 1TB+
- [ ] Network: 10Gbps+

**데이터 품질:**
- [ ] Audit logging 활성화
- [ ] Provenance completeness 검증
- [ ] Baseline period 확정 (최소 30일)

**조직 준비도:**
- [ ] SOC team training
- [ ] Stakeholder alignment
- [ ] Budget approval

#### B. Phase 1: 파일럿 (Week 1-8)

Week 1-2: Infrastructure setup
Week 3-6: Baseline training
Week 7-10: Pilot detection
Week 11-12: Evaluation & Decision

#### C. Phase 2: 확장 (Week 9-24)

Week 13-16: Critical servers (100-200대)
Week 17-20: SOAR integration
Week 21-24: Tuning and optimization

#### D. Phase 3: 최적화 (Week 25-52)

Week 25-36: Full enterprise deployment
Week 37-48: Advanced capabilities
Week 49-52: Continuous improvement

### 6. 5일간 리뷰 종합

| Day | 주제 | 핵심 학습 | 실무 적용 |
|-----|------|-----------|-----------|
| **Day 1** | APT 탐지 근본 문제 | Provenance graph 필요 | EDR/XDR 백엔드 |
| **Day 2** | UNICORN 설계 | Graph sketching + Evolutionary | Unsupervised learning |
| **Day 3** | 실증적 검증 | DARPA 100%, +24% precision | R=3 필수, real-time 가능 |
| **Day 4** | 한계와 발전 | Parameter tuning, fileless 한계 | Defense-in-depth |
| **Day 5** | 실무 통합 | Supply chain, exfiltration 탐지 | ATT&CK 매핑, SOAR |

### 7. 최종 개인 인사이트

#### A. 이 논문이 나의 SOC 역량에 기여한 점

**핵심 배움 1: APT 탐지는 Context가 전부**

UNICORN의 R-hop exploration이 증명: 단순 local pattern이 아니라 wider causal context를 보는 것이 핵심. SOC analyst가 수동으로 하던 "공격 연결고리 찾기"를 자동화.

**핵심 배움 2: Evolutionary Modeling은 현실적 필연**

시스템은 변한다. Static model은 빠르게 obsolete. Evolutionary model은 점진적 변화는 흡수하면서 급격한 anomaly 탐지.

**핵심 배움 3: 완벽한 솔루션은 없다**

UNICORN도 한계가 있다 (fileless, LOLBAS, parameter tuning). 실무에서는 multi-layer defense가 답.

**핵심 배움 4: 학술 연구가 산업을 바꾼다**

UNICORN 발표 후 5년 만에 provenance 기반 탐지가 EDR/XDR 표준이 됨.

**핵심 배움 5: 이론과 실무의 균형**

논문의 "100% detection"과 실제 배포는 다르다. 하지만 이론적 기반 없이 경험만으로는 한계. 균형이 필요.

#### B. [4편의 논문]과의 비교 종합

| 논문 | 핵심 아이디어 | 강점 | 약점 | 적용 시나리오 |
|------|--------------|------|------|---------------|
| **DeepLog** | Deep learning on log sequence | Zero-day 탐지 | Single-host only | 단일 시스템 anomaly |
| **Lou et al.** | Invariants mining | Explainable rules | Rule extraction 비용 | Stable system |
| **Beehive** | Network workflow graph | Enterprise-wide view | Network-level만 | Network intrusion |
| **UNICORN** | Provenance graph sketching | System-level causality | Parameter tuning | APT detection |

통합 전략: L1 DeepLog (endpoint) → L2 Beehive (network) → L3 UNICORN (system APT) → L4 Lou et al. (validation)

#### C. 면접 대비 핵심 메시지 (1분)

"UNICORN은 APT 탐지의 핵심 문제를 해결한 연구입니다.

첫째, Low-and-slow APT는 기존 탐지를 우회합니다. UNICORN은 provenance graph와 evolutionary modeling으로 수개월 공격도 탐지합니다.

둘째, Graph sketching으로 TB 규모를 200MB로 실시간 분석. DARPA에서 100% 탐지율 달성.

셋째, 2020년 발표 후 CrowdStrike, Microsoft 등이 provenance 기반 탐지를 채택하는 계기가 되었습니다.

결론적으로, 이 논문을 통해 APT 탐지에서 context와 causality의 중요성을 배웠고, 실무에서 UNICORN을 SIEM의 advanced detection engine으로 통합하여 supply chain attack, credential dumping, lateral movement를 조기 차단하는 전략을 수립할 수 있게 되었습니다."

#### D. 다음 학습 방향

**우선순위 1: Deep Learning 기반 Provenance 분석**
- TBDetector (Transformer), PROGRAPHE (GNN)
- 학습 목표: UNICORN의 hand-crafted feature를 deep learning으로 대체

**우선순위 2: Adversarial Robustness**
- PROVNINJA, MirGuard
- 학습 목표: 공격자가 UNICORN 우회하는 방법과 방어

**우선순위 3: Cross-Host Attack Campaign**
- NODLINK, Cyber Persistence Detector
- 학습 목표: Multi-host correlation 기법

**우선순위 4: Explainable AI for Security**
- Provenance graph visualization
- 학습 목표: Black-box detector 결과를 analyst가 이해

**장기 목표:**
- 6개월 후: UNICORN 기반 APT 탐지 시스템 PoC 구현
- 1년 후: 자체 탐지 룰 개발
- 2년 후: Provenance 기반 탐지 전문가로 컨퍼런스 발표

### 8. 최종 결론

#### A. UNICORN의 유산

2020년 논문 하나가 provenance 기반 APT 탐지를 학술 연구에서 산업 표준으로 끌어올림. 2025년 현재도 DARPA TC dataset의 baseline detector로 사용. 후속 연구들의 비교 대상.

#### B. SOC 분석가로서의 다짐

"알고 있다"에서 "할 수 있다"로

Phase 1 (완료): 논문 이해 (DeepLog, Lou et al., Beehive, UNICORN)
Phase 2 (진행 중): 실습 (CamFlow + Python으로 PoC)
Phase 3 (다음): 실무 적용 (SOC 환경에 배포)
Phase 4 (목표): 기여 (오픈소스, 컨퍼런스)

단순한 "도구 사용자"가 아닌 원리를 이해하는 전문가, 실무 적용 전략을 세우는 설계자, 새로운 방법을 만드는 연구자.

**다음 논문에서 또 만나요!**

---

## References

[1] Han, X., Pasquier, T., Bates, A., Mickens, J., & Seltzer, M. (2020). UNICORN: Runtime Provenance-Based Detector for Advanced Persistent Threats. *Network and Distributed System Security Symposium (NDSS)*, pp. 1-18. https://doi.org/10.14722/ndss.2020.24046

[2] Manzoor, E., Milajerdi, S. M., & Akoglu, L. (2016). Fast Memory-efficient Anomaly Detection in Streaming Heterogeneous Graphs. *ACM SIGKDD*.

[3] Milajerdi, S. M., Gjomemo, R., Eshete, B., Sekar, R., & Venkatakrishnan, V. (2019). HOLMES: Real-time APT Detection through Correlation of Suspicious Information Flows. *IEEE S&P*.

---

## Tags
`#SOC` `#APTDetection` `#ProvenanceGraphs` `#AnomalyDetection` `#GraphSketching` `#EvolutionaryModeling` `#UNICORN` `#NDSS2020` `#SKShieldusRookies`