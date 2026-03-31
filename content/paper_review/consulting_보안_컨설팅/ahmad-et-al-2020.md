---
title: "How Integration of Cyber Security Management and Incident Response Enables Organizational Learning"
date: 2026-03-31
categories: ["paper-review"]
tags: ["보안컨설팅", "IncidentResponse", "ISM", "OrganizationalLearning", "ISM-IR", "DoubleLoopLearning", "PaperReview", "SKShieldusRookies"]
draft: false
summary: "ISM과 IR의 기능적 단절 문제를 조직학습 이론으로 분석하고, 5개 통합 프로세스(I1-I5) 프레임워크를 통해 보안 조직의 이중 루프 학습 역량 강화 방안을 제시한 Ahmad et al.(2020) 논문 리뷰"
---

# Research Review: How Integration of Cyber Security Management and Incident Response Enables Organizational Learning

>  Analyzed Date :  2026.03.31 - 2026.04.04
>  Keywords :  Incident Response, Information Security Management, Organizational Learning, ISM-IR Integration, Double-Loop Learning
>  Source :  Journal of the Association for Information Science and Technology (JASIST), 2020, Vol. 71, No. 8, pp. 939-953. https://doi.org/10.1002/asi.24311

---

## Why This Paper?

### 선정 배경

도메인 탐색 결과 :

10편의 보안 컨설팅 논문을 통해 거버넌스 → 컴플라이언스 → 리스크 분석 → 개인 행동 → 감사 → 공급망 → 투자 경제학 → 보안 문화 → 인식 캠페인 → 서드파티 평가까지 사전 예방 체계 전반을 다뤘다. 이제 침해가 실제 발생한 이후의 사후 관리 영역으로 확장할 시점이다.

이 논문을 선택한 이유 :

    - Slapničar et al.(2022)이 보안 감사의 효과성을, Da Veiga & Eloff(2010)이 보안 문화를 다뤘다면, 이 논문은 사고 이후 조직이 어떻게 학습하고 방어 체계를 개선하는지를 다루는 자연스러운 확장
    - 보안 컨설팅 현장에서 IR 체계 수립 자문 시 절차 설계보다 더 근본적인 문제, 즉 조직이 사고 경험에서 왜 배우지 못하는가에 대한 이론적 근거 제공
    - ISM과 IR의 통합 수준 진단 및 개선 로드맵 설계라는 체계 수립 역량과 직결
    - ISMS-P 2.10(정보보안 사고 관리) 통제 항목 자문에 필요한 학술적 기반 확보

학습 목표 :

    - ISM과 IR 기능의 구조적 단절  ( disconnect )이 발생하는 원인과 그 조직적 결과 이해
    - 단일 루프 학습과 이중 루프 학습의 개념 및 보안 컨설팅 시나리오에서의 차별적 의미 습득
    - 5개 통합 프로세스  ( I1 - I5 )  프레임워크를 IR 체계 수립 자문의 진단 도구로 활용하는 방법 확립

---

## Day 1 - Research Context & Motivation
*(보안에 투자했는데 왜 계속 당하는가 — ISM과 IR의 단절이 만드는 학습의 공백)*

### 1. 연구 배경: ISM과 IR의 구조적 단절

보안 투자와 침해의 역설

대규모 조직은 정보보안 관리(ISM) 기능에 상당한 자원을 투입한다. ISM은 리스크 평가, 보안 전략 수립, 정책과 교육 프로그램 운영, 방화벽·암호화 등 기술적 통제 구현을 통해 디지털 자산을 보호하는 역할을 한다. 동시에 많은 조직은 침해 발생 시 피해를 최소화하고 IT 서비스를 신속히 복구하는 IR 기능도 별도로 운영한다. 그러나 이 두 기능에 대한 투자가 늘어도 보안 사고는 줄지 않는다. Verizon의 2018년 데이터 침해 조사 보고서에 따르면 조사된 53,000건의 사고 중 73%가 외부 공격자에 의한 것이었으며, 세계 정보보안 지출은 2018년 930억 달러에 달할 것으로 예측됐다.

현실의 한계

선행 연구들은 대규모 조직에서 ISM과 IR 기능이 구조적으로 분리되어 있음을 반복적으로 확인했다. ISM은 전략적 수준에서 리스크를 관리하고, IR은 운영적 수준에서 사고를 처리한다. 이 두 기능 사이에는 소통, 협력, 지식 공유가 부재한 약한 연결(weak link) 또는 단절(disconnect)이 존재한다. 그 결과 조직은 한 번의 보안 위기에서 다음 위기로 표류하면서 근본적인 보안 관리 역량을 개선하지 못한다. 기존 산업 표준(예: ISO 27000 계열)의 IR 지침은 사고 처리 후 교훈을 도출하고 표준 운영 절차에 반영하라고 권고하지만, 이는 대부분 IR 내부의 단일 루프 수준에 그친다.

연구 문제의식

조직이 ISM과 IR 기능을 어떻게 통합함으로써 능동적 학습을 가능하게 하고 보안 성과를 최적화할 수 있는가?

---

### 2. 핵심 개념

| 개념 | 정의 | 컨설팅 맥락에서의 의미 |
|------|------|---------------------|
| 정보보안 관리  ( ISM ) | 조직의 디지털 자산을 보호하기 위해 운영적·전술적·전략적 수준에서 수행되는 관리 실무의 집합. 정책, 리스크, IR, 기술, 교육/훈련/인식(SETA)의 5개 실무 영역으로 구성 | 고객사 보안 체계 진단 시 5개 실무 영역의 성숙도를 평가하는 기준 프레임 |
| 사고 대응  ( IR ) | 사고를 진단하고, 영향을 억제하며, 원인을 제거하고, IT 시스템을 정상 기능으로 복구하는 순환적 6단계 프로세스  ( 준비 - 식별 - 억제 - 제거 - 복구 - 사후 검토 ) | 고객사 IR 체계 수립 자문 시 6단계 구조를 기준으로 현행 절차의 완결성을 진단 |
| 단일 루프 학습 | 기존 조직 목표, 정책, 규범에서 벗어난 이탈을 수정하는 단순 오류 수정 과정. 취약점 패치, 기존 통제 재구성 등 점진적 개선에 해당 | 대부분의 조직이 현재 수행하는 수준. 사고 후 해당 취약점만 패치하고 구조적 원인 분석은 생략 |
| 이중 루프 학습 | 기존 전략, 규범, 프로세스의 기반이 되는 가정과 원칙 자체를 재검토하는 심층 학습. 보안 전략 변환, 방어 논리 재설계 등 근본적 개선에 해당 | 컨설팅 개입이 가장 큰 가치를 만들어내는 수준. 사고를 계기로 보안 전략과 체계를 전환할 수 있도록 경영진을 설득하는 근거 |
| 단절  ( Disconnect ) | ISM과 IR 기능 사이에서 발생하는 소통, 협력, 지식 공유의 부재 또는 약화. 전술적 수준과 전략적 수준 모두에서 발생 | 보안 컨설팅에서 조직 진단 시 ISM-IR 연결 강도를 평가하는 핵심 진단 항목 |

---

### 3. 이론적 기반: 조직학습 이론  ( Argyris & Schön, 1997 )

[ 전략적 수준 ]

    - Information Security Management  ( ISM )
    - 전략 최적화  ( 이중 루프 ) / 전략·프로세스·통제 검토 및 재평가

    >> ↕

[ 전술적 수준 ]  통합 프로세스  ( I1 - I5 )

    - I1 : 보안 리스크 인식 제고
    - I2 : 위협 인텔리전스 축적
    - I3 : 방어 취약점 제거
    - I4 : 보안 방어 논리 평가
    - I5 : 보안 대응 역량 강화

    >> ↕

[ 운영적 수준 ]

    - Incident Response  ( IR )
    - 관찰과 피드백  ( 단일 루프 )

핵심 아이디어 :

조직학습 이론의 단일 루프 학습과 이중 루프 학습 개념을 보안 관리에 적용하여, ISM과 IR의 전술적 수준 통합이 어떻게 두 층위의 학습 기회를 창출하는지를 설명한다. 단일 루프 학습은 기존 방어 체계 내의 취약점을 수정하는 것이고, 이중 루프 학습은 방어 체계의 기반이 되는 전략과 가정 자체를 재검토하고 변환하는 것이다. 두 기능 사이의 연결이 강할수록 조직은 사고로부터 더 깊이 학습하고, 진화하는 위협 환경에 능동적으로 적응하는 보안 역량을 구축할 수 있다.

---

### 4. 연구의 핵심 기여

학술적 기여 :

    - ISM과 IR의 기능적 단절을 조직학습 이론으로 처음 체계화하여, 기존의 기술 중심 IR 연구에 관리적 관점을 추가
    - 단일 루프 학습에 국한된 기존 산업 표준  ( ISO 27000 계열 Follow-up 지침 )의 한계를 이중 루프 학습 개념으로 확장
    - 5개 통합 프로세스  ( I1 - I5 )와 이에 대응하는 학습 기회를 체계적으로 명시한 통합 프레임워크 제시

실무 기여 :

    - 조직이 자사의 ISM-IR 통합 수준을 진단하고 구체적인 학습 목표와 기대 효과를 기준으로 개선 방향을 설계할 수 있는 실용적 프레임워크 제공
    - 사후 검토 단계를 재설계하기 위한 인텔리전스 수집 우선순위  ( 위협, 실패, 아슬아슬한 실패, 통제 효과성 )를 명시적으로 제시
    - Forsberg Industries라는 가상 시나리오를 통해 실제 조직에서 단절이 발생하는 방식과 그 전략적 결과를 구체적으로 예시

---

### 5. 컨설팅 관점 인사이트

적용 가능성 :

이 논문의 프레임워크는 두 가지 컨설팅 시나리오에서 직접 활용할 수 있다. 첫째, 고객사의 현행 IR 체계를 진단할 때 ISM과 IR 사이의 10가지 단절 지점(Forsberg 시나리오의 Disconnect Event 3 - 10)을 점검 항목으로 활용할 수 있다. 둘째, IR 체계 개선 로드맵을 수립할 때 5개 통합 프로세스를 단계별 구현 목표로 설정하고, 각 프로세스가 창출하는 단일 루프 및 이중 루프 학습 효과를 경영진 보고의 기대 효과로 제시할 수 있다.

기존 학습과의 연결 :

Slapničar et al.(2022)의 감사 효과성 연구가 외부 감사 관점에서 보안 체계를 평가했다면, 이 논문은 조직 내부에서 사고 경험이 어떻게 학습으로 전환되는지를 다룬다. Da Veiga & Eloff(2010)의 보안 문화 프레임워크가 개인과 조직의 보안 행동 기반을 설명했다면, 이 논문은 그 행동 기반이 사고 이후에도 학습과 개선으로 이어지려면 어떤 기능 간 연결이 필요한지를 설명한다. Gashgari et al.(2017)의 거버넌스 프레임워크가 보안 의사결정 구조를 다뤘다면, 이 논문은 그 구조가 실제 사고 대응과 어떻게 연결되어 보안 역량을 강화하는지를 보완한다.

현실적 고려사항 :

이 논문은 대규모 조직을 분석 단위로 설정하고 있다. 중소기업처럼 ISM과 IR이 동일 인력에 의해 수행되는 환경에서는 기능적 통합의 의미가 달라진다. 또한 이 연구는 개념적 프레임워크를 제시하는 것이므로, 실제 조직의 통합 수준을 측정하는 구체적 지표나 도구는 제공하지 않는다. 컨설팅 적용 시에는 프레임워크를 진단 체크리스트로 변환하는 별도의 작업이 필요하다.

---

## References

[1] Ahmad, A., Maynard, S.B., & Shanks, G. (2015). A case analysis of information systems and security incident responses. *International Journal of Information Management*, 35(6), 717-723.

[2] Argyris, C., & Schön, D.A. (1997). Organizational learning: A theory of action perspective. *Addison-Wesley*.

[3] Slapničar, S., Vuko, T., Čular, M., & Drašček, M. (2022). Effectiveness of cybersecurity audit. *International Journal of Accounting Information Systems*, 44, 100548.

[4] Da Veiga, A., & Eloff, J.H.P. (2010). A framework and assessment instrument for information security culture. *Computers & Security*, 29(2), 196-207.

[5] Gashgari, G., Walters, R., & Wills, G. (2017). A Proposed Best-Practice Framework for Information Security Governance. *Proceedings of the 2nd International Conference on Internet of Things, Big Data and Security (IoTBDS)*.

---

## Tags

보안컨설팅  /  SecurityConsulting  /  IncidentResponse  /  ISM  /  OrganizationalLearning  /  ISM-IR  /  DoubleLoopLearning  /  PaperReview  /  SKShieldusRookies
