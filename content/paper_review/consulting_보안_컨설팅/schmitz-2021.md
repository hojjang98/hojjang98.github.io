---
title: "Maturity Level Assessments of Information Security Controls: An Empirical Analysis of Practitioners' Assessment Capabilities"
date: 2026-04-13
categories: ["paper-review"]
tags: ["보안컨설팅", "SecurityMaturityModel", "ISO27002", "COBIT", "AssessmentCapability", "DunningKruger", "PaperReview", "SKShieldusRookies"]
draft: false
summary: "보안 전문가 56명이 ISO/IEC 27002 통제 항목의 COBIT 성숙도를 얼마나 정확하게 평가할 수 있는지를 실증한 Schmitz(2021) 논문 리뷰. 평가자 역량 편차와 던닝-크루거 효과를 분석하여 컨설팅 진단 품질 관리에 시사점을 제공한다."
---

Analyzed Date : 2026.04.13 - 2026.04.17

Keywords : Security Maturity Model  /  ISO/IEC 27002  /  COBIT  /  Assessment Capability  /  Dunning-Kruger Effect

Source : Computers & Security, 2021, Vol. 108, Article 102306  |  DOI: 10.1016/j.cose.2021.102306

---

## Why This Paper?

### 선정 배경

도메인 탐색 결과 :

8개 도메인 논문 탐색을 통해 보안 컨설팅을 전문화 방향으로 확정. 이후 12편의 논문을 통해 컴플라이언스 전술(Foorthuis & Bos), 리스크 분석(Santos-Olmo et al.), 보안 정책 준수 행동(Bulgurcu et al.), 거버넌스(Gashgari et al.), 감사 효과성(Slapničar et al.), 공급망 리스크(Ghadge et al.), 보안 투자 경제학(Gordon & Loeb), 보안 문화(Da Veiga & Eloff), 인식 제고 캠페인(Bada et al.), 제3자 리스크(Keskin et al.), 사고대응-정보보안관리 통합(Ahmad et al.), 최고경영진 주의와 위험평가(Shaikh & Siponen)를 학습. 이번 논문은 보안 성숙도 모델이라는 미탐색 영역을 다룬다.

이 논문을 선택한 이유 :

    - Slapničar et al.(감사 효과성)과 Foorthuis & Bos(컴플라이언스 전술)가 통제 체계 설계에 집중했다면, 이 논문은 그 통제 체계를 실제로 평가하는 사람의 역량 문제를 정면으로 다룬다. 진단 설계에서 진단 수행 품질로 관심의 축을 이동시킨다.
    - 보안 컨설팅의 핵심 업무인 현황 진단에서 평가자의 인지적 한계와 편향이 어떻게 작동하는지를 실증적으로 분석한다.
    - 성숙도 진단 역량이 자격증 보유 여부, 경력 연수 등 어떤 전문성 요인과 연관되는지를 제시함으로써 컨설턴트 자기 개발 방향에 직접적 시사점을 준다.
    - ISO/IEC 27001/27002, COBIT, ISMS-P 등 현장에서 실제로 사용되는 표준 체계를 평가 도구로 채택한 연구다.

학습 목표 :

    1. 성숙도 수준 평가(maturity level assessment)가 왜 어려운지, 그 인지적·방법론적 근거를 이해한다.
    2. 평가 품질에 영향을 미치는 전문성 요인(자격증, 경력, 친숙도)의 실증 결과를 파악하고 컨설팅 팀 구성과 품질관리에 적용한다.
    3. 평가 지원 수단(팀 토론, 사례집, 훈련 과정 등)의 근거를 확보하여 현장 진단 프로세스 설계에 활용한다.

---

## Day 1 – Research Context & Motivation

*(측정하기 어려운 것을 측정하는 사람의 역량을 측정한다)*

### 1. 연구 배경: 성숙도 평가의 품질 문제

보안 성숙도 모델의 중요성

정보보안 수준을 객관적으로 파악하고 개선 우선순위를 도출하기 위해 성숙도 모델은 산업 전반에 걸쳐 광범위하게 활용된다. COBIT, CMMI, C2M2, ISO/IEC 27001 기반 모델 등 다양한 체계가 존재하며, 독일 자동차 산업에서는 VDA-ISA 기반 성숙도 자가진단이 사실상 표준(de facto standard)으로 자리 잡았을 정도다. 규제 관점에서도 GDPR은 기술적·조직적 보안 조치의 효과성을 정기적으로 시험·평가·점검하는 프로세스를 조직에 명시적으로 요구한다. 결국 성숙도 평가는 컴플라이언스 이행의 증거이자 보안 투자 의사결정의 근거가 된다.

현실의 한계

성숙도 모델 연구의 대부분은 어떤 모델을 설계하고 어떤 통제 항목을 포함시킬 것인가에 집중되어 있다. 반면 그 모델을 실제로 적용해 평가하는 사람이 얼마나 정확하게 수행하는지, 즉 평가 품질 자체는 거의 검토되지 않았다. DeMarco의 명제처럼 측정할 수 없으면 통제할 수 없다는 전제 하에 성숙도 평가가 이루어지지만, 정작 그 측정 행위의 신뢰성과 타당성은 검증되지 않은 채로 남아 있다. 기존 SPICE 평가 신뢰성 연구(El Emam et al., Lee et al.)도 평가자 간 일치도(reliability)만을 분석했을 뿐, 사전에 정의된 정답과의 타당성(validity) 비교는 수행하지 않았다.

연구 문제의식

이 논문이 답하려는 핵심 질문은 다음과 같다: 보안 전문가들은 ISO/IEC 27002 통제 항목에 대해 COBIT 성숙도 수준을 얼마나 정확하게 평가할 수 있는가? 그리고 어떤 전문성 요인이 평가 정확도에 유의미한 영향을 미치는가? 나아가 평가자들은 자신의 평가 품질을 스스로 얼마나 정확하게 인식하는가?

---

### 2. 핵심 개념

| 개념 | 정의 | 컨설팅 맥락에서의 의미 |
|------|------|---------------------|
| 보안 성숙도 모델 | 조직의 보안 관련 프로세스·통제의 구현 수준을 단계별로 평가하는 체계. 보통 0~5 수준으로 구분 | 현황 진단의 핵심 도구. 고객사의 현재 수준을 객관적으로 측정하고 개선 경로를 제시하는 기준선 역할 |
| COBIT 성숙도 수준 | ISACA가 제시한 6단계(0~5) 성숙도 척도. 0(미구현)부터 5(지속 개선)까지 각 수준에 대한 기준 기술(description)을 제공 | ISMS 진단 시 통제 이행 수준을 수치화하는 기준으로 활용. GRC 도구와 VDA-ISA 등 산업 표준과 연계됨 |
| 시나리오 성숙도 수준(SML) | 이 연구에서 연구자가 사전에 정의한 각 통제 항목의 정답 성숙도 값. 참가자 평가의 타당성 비교 기준 | 컨설팅 진단 설계 시 평가 기준의 명확화 필요성을 시사. 내부 기준선 없이 진행되는 평가는 주관적 편차가 클 수 있음 |
| 던닝-크루거 효과 | 능력이 낮은 사람이 자신의 능력을 과대평가하고, 경험이 많은 사람이 더 확신을 가질수록 오히려 성과가 낮아지는 인지 편향 | 장기 경력 보안 전문가가 자신의 진단 능력을 과신할 수 있음을 시사. 팀 기반 검증과 외부 교차 확인의 근거 |
| 평가자 내·외부 편향 | 자사 환경을 평가할 때(내부 평가)는 관대해지고, 외부 조직을 평가할 때는 더 엄격해지는 경향 | 자가진단(self-assessment) 기반 ISMS 인증 준비의 구조적 취약점. 컨설턴트 외부 검토의 가치를 뒷받침 |

---

### 3. 이론적 기반: 평가 신뢰성·타당성 프레임워크

[ 연구 설계 구조 ]

    - 사전 정의된 시나리오 성숙도 수준(SML)

>> ↓

[ 가상 기업 시나리오 (CloudSec) ]

    - ISO/IEC 27002 통제 10개 항목
    - BSI IT-Grundschutz 조치 기술 기반
    - 각 통제별 상위·하위 수준 경계 명시

>> ↓

[ 보안 전문가 56명 온라인 설문 평가 ]

    - COBIT 5 성숙도(0~5) 직접 평가
    - 다음 수준 달성을 위한 조치 서술
    - 자기 평가 불확실성 보고

>> ↕ (분기)

[ 정량 분석 ]

    - 편차, t검정, 상관분석

[ 정성 분석 ]

    - 코딩: 오해석, 과도한 조치, 의존성

>> ↓

[ 사후 심층 인터뷰 (6명) ]

    - 어려움의 원인
    - 필요한 지원 형태

핵심 아이디어 :

성숙도 평가의 품질 검증을 위해 연구자들은 정답이 사전에 정의된 가상 시나리오를 설계하고, 실무 전문가들의 평가 결과를 그 정답과 직접 비교했다. 기존 연구들이 평가자 간 일치도만 분석한 것과 달리, 이 연구는 타당성(정답 대비 편차)까지 측정함으로써 평가 품질 문제를 입체적으로 드러낸다.

---

### 4. 연구의 핵심 기여

학술적 기여 :

    - 보안 성숙도 평가의 신뢰성이 아닌 타당성을 최초로 실증 검증. 정답이 사전 정의된 시나리오 기반 실험 설계로 기존 연구의 방법론적 공백을 메웠다.
    - 던닝-크루거 효과가 보안 성숙도 평가 맥락에서도 발현됨을 통계적으로 확인. 장기 경력자 집단(10년 이상)에서 자기 확신과 실제 성과 간 약한 역상관이 관찰됐다.
    - 평가 품질 향상에 유의미한 영향을 미치는 전문성 요인(자격증 종류별 효과)을 t검정으로 분리하여 제시.

실무 기여 :

    - ISMS 및 ISO/IEC 27001 자격증 보유자가 그렇지 않은 집단 대비 통계적으로 유의미하게(1% 수준) 높은 평가 정확도를 보임. 진단 팀 구성의 실무 기준을 제공한다.
    - 평가 지원 수단으로 팀 토론, 사례 중심 성숙도 설명, 조치 목록 카탈로그, 전문 훈련 과정의 필요성을 구체적으로 제시.
    - 대기업 출신 전문가가 소규모 기업 시나리오에서 과도한 조치를 제안하는 경향을 확인. 고객사 맥락(규모, 산업, 예산)에 맞춘 평가 기준 적용의 중요성을 실증했다.

---

### 5. 컨설팅 관점 인사이트

적용 가능성 :

이 연구는 보안 컨설팅 현장에서 수행되는 ISMS 현황 진단의 품질 문제를 직접적으로 다룬다. 컨설턴트가 성숙도 평가를 수행할 때 발생하는 오류 유형(시나리오 오해석, 통제 항목 혼동, 과도한 조치 제안)은 실제 고객사 진단 보고서의 신뢰성과 직결된다. 연구 결과를 바탕으로 진단 프로세스에 팀 기반 검토, 참조 사례 제공, 규모별 맥락 정규화를 구조적으로 내재화하는 방향을 검토할 수 있다.

기존 학습과의 연결 :

    - Slapničar et al.(2022)의 사이버보안 감사 효과성 연구와 직접 연결된다. 감사 효과성은 감사인의 역량과 절차적 엄밀성에 달려 있는데, 이 논문은 그 역량의 실증적 한계를 보여준다.
    - Foorthuis & Bos(2011)의 컴플라이언스 전술 연구에서 통제 체계의 설계가 이행 결과에 영향을 준다고 봤다면, 이 논문은 통제 체계를 평가하는 행위 자체의 편차를 분석한다. 설계와 평가는 보안 관리의 두 축이다.
    - Bulgurcu et al.(2010)의 개인 행동 모델은 규범적 신념과 자기효능감이 준수 행동에 영향을 준다고 봤는데, 이 논문의 던닝-크루거 결과는 자기효능감 과잉이 평가 행동의 품질 저하로 이어질 수 있음을 보완한다.

현실적 고려사항 :

연구 참가자 56명 중 독일 소재 전문가가 대부분이며, VDA-ISA와 BSI IT-Grundschutz 기반의 독일 특유 맥락이 반영되어 있다. 한국 ISMS-P 환경에서의 직접 적용 시에는 표준 체계의 차이(COBIT vs. 국내 기준)와 진단 관행의 문화적 차이를 고려해야 한다. 또한 56명의 표본은 세부 집단 분석에서 통계적 검정력이 제한적일 수 있다는 점도 염두에 둬야 한다.

---

Day 2 Preview :

---

## References

[1] Schmitz, C. (2021). Maturity level assessments of information security controls: An empirical analysis of practitioners' assessment capabilities. *Computers & Security*, 108, Article 102306. https://doi.org/10.1016/j.cose.2021.102306

[2] DeMarco, T. (1982). *Controlling Software Projects: Management, Measurement, and Estimation*. Yourdon Press.

[3] Slapničar, S., Vuko, T., Čular, M., & Drašček, M. (2022). Effectiveness of cybersecurity audit. *International Journal of Accounting Information Systems*, 44, Article 100548.

[4] Foorthuis, R., & Bos, R. (2011). A framework for organizational compliance management tactics. *EDOCW 2011 Proceedings*.

[5] Bulgurcu, B., Cavusoglu, H., & Benbasat, I. (2010). Information security policy compliance: An empirical study of rationality-based beliefs and information security awareness. *MIS Quarterly*, 34(3), 523-548.

---

## Tags

보안컨설팅  /  SecurityConsulting  /  SecurityMaturityModel  /  ISO27002  /  COBIT  /  AssessmentCapability  /  DunningKruger  /  PaperReview  /  SKShieldusRookies
