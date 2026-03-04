---
title: "Week 11 — ISO 27001 보안 컨설팅 보고서 (DNA Lab)"
date: 2026-01-11
draft: false
tags: ["ISO27001", "보안컨설팅", "취약점분석", "GapAnalysis", "CVSS", "로드맵", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "Week 10 DNA Lab 스캐너로 발견한 102개 취약점을 ISO 27001:2022 통제항목과 매핑하여 Gap Analysis 및 6개월 개선 로드맵을 도출한 보안 컨설팅 보고서"
---

# Week 11 — ISO 27001 보안 컨설팅 보고서 (DNA Lab)

> 전체 보고서 및 데이터 파일은 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_11](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_11)

---

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **클라이언트** | DNA Lab (유전자 검사 헬스케어 스타트업) |
| **컨설팅사** | SK Shields 보안 컨설팅팀 |
| **평가 기간** | 2026-01-04 ~ 2026-01-11 |
| **목표** | ISO 27001 인증 취득을 위한 취약점 분석 및 개선 로드맵 제시 |

이 프로젝트는 **Week 10 DNA Lab Security Scanner** 로 수집한 스캔 결과를
**ISO 27001:2022 통제항목** 과 직접 매핑하여 실무 수준의 보안 컨설팅 보고서를 작성한 작업이다.

---

## 배경 시나리오

DNA Lab 은 고객의 민감한 유전 정보와 의료 데이터를 다루는 헬스케어 스타트업이다.
최근 **Series B 투자 유치** 에 성공하고, 대형 병원·보험사와 B2B 계약을 추진 중이다.

문제는 계약 조건으로 **ISO 27001 인증** 을 요구받았다는 것이다.
내부 보안팀의 자체 스캔 결과 심각한 취약점이 다수 발견되어,
6개월 내 인증 취득을 목표로 외부 컨설팅을 의뢰하였다.

> 보안 개선은 단순한 비용이 아닌,
> **기업 가치를 높이고 B2B 계약을 성사시키는 투자다.**

---

## 주요 발견사항 — 취약점 통계

**총 취약점 27개 / 총 발견사항 102개 / 평균 CVSS 7.10**

    심각도별 분포:
    ┌──────────┬──────┬─────────────────────────────────────────────────┐
    │ 심각도   │  수  │ 대표 취약점                                      │
    ├──────────┼──────┼─────────────────────────────────────────────────┤
    │ CRITICAL │  4   │ SQL Injection (CVSS 9.8), OS Command Injection  │
    │          │      │ 쿠키 변조 (CVSS 9.1), 파일 전송 취약점          │
    ├──────────┼──────┼─────────────────────────────────────────────────┤
    │ HIGH     │  12  │ XSS, CSRF, IDOR, SSRF                           │
    │          │      │ OS 보안 설정 미흡, 불필요한 서비스 활성화        │
    ├──────────┼──────┼─────────────────────────────────────────────────┤
    │ MEDIUM   │  10  │ 로깅 미흡, 보안 정책 부재, 파일 권한 문제       │
    ├──────────┼──────┼─────────────────────────────────────────────────┤
    │ LOW      │  1   │ 에러 핸들링 미흡                                 │
    └──────────┴──────┴─────────────────────────────────────────────────┘

Critical + High 합산 비율 => **59.3%**

### Critical 취약점 4종 상세

**WEB-002 SQL Injection (CVSS 9.8)**
- 발견 지점 28개 — MyBatis XML 전체에서 `${}` 파라미터 바인딩 사용
- 영향: 고객 유전자 정보 및 개인정보 전체 유출 가능, GDPR / 개인정보보호법 위반 소지
- 예상 피해액: 수십억 원 (데이터 유출 시 과징금 + 손해배상 포함)

**WEB-003 OS Command Injection (CVSS 9.8)**
- Java `Runtime.getRuntime().exec()` 에 사용자 입력 직접 전달
- 영향: 서버 OS 명령 실행 가능 => 시스템 전체 제어권 탈취

**WEB-009 쿠키 기반 권한 관리 취약점 (CVSS 9.1)**
- 쿠키 값 변조로 관리자 권한 상승 가능
- 발견 지점 3개

**WEB-010 파일 업로드 취약점 (CVSS 9.8)**
- 확장자 / MIME 타입 검증 없음 => 웹쉘 업로드 가능
- 발견 지점 2개 => 내부망 침투 경로 제공, 랜섬웨어 감염 위험

---

## ISO 27001:2022 Gap Analysis

14개 통제항목을 평가한 결과, **단 하나도 완전 준수 상태가 아니었다.**

    준수 상태 분포:
    Compliant         :   0개  (0%)
    Partially Compliant: 10개  (71%)
    Non-Compliant     :   2개  (14%)
    Critical Gap      :   2개  (14%)

### Critical Gap 통제항목

**A.8.3 — 정보 접근 제한 (9개 취약점 연결)**
- IDOR, 권한 상승, 세션 관리 취약점이 집중적으로 연결됨
- 현재 상태: 접근 제어 로직이 일관되게 적용되지 않음

**A.8.16 — 모니터링 활동 (7개 취약점 연결)**
- 보안 이벤트 로깅 체계 자체가 부재
- 현재 상태: 비정상 접근 탐지 불가, 침해 후 추적 불가

### Non-Compliant 통제항목

**A.8.8 — 기술적 취약점 관리 (4개 취약점)**
- 취약점 식별 및 패치 프로세스 미수립

**A.5.17 — 인증 정보 관리 (4개 취약점)**
- 비밀번호 정책 미흡, 계정 잠금 미설정

---

## 핵심 취약점 개선 예시

### Before / After — SQL Injection (WEB-002)

기존 코드 — MyBatis XML `${}` 사용 (문자열 직접 삽입):

    SELECT * FROM users
    WHERE username = '${username}'
    AND password = '${password}'

    => 공격자 입력: admin' OR '1'='1 --
    => 실행 쿼리: WHERE username='admin' OR '1'='1' --' AND password='...'
    => 비밀번호 검증 완전 우회

개선 코드 — `#{}` 로 전환 (Prepared Statement 자동 적용):

    SELECT * FROM users
    WHERE username = #{username}
    AND password = #{password}

    => 동일 입력: admin' OR '1'='1 --
    => 문자열 전체가 하나의 파라미터 값으로 바인딩
    => SQL 구문으로 해석 불가 => 공격 차단

### Before / After — OS Command Injection (WEB-003)

기존 코드 — 사용자 입력을 OS 명령에 직접 연결:

    @PostMapping("/ping")
    public String ping(@RequestParam String host) {
        String command = "ping " + host;   // 명령 삽입 가능
        Runtime.getRuntime().exec(command);
        return "success";
    }

    => 공격자 입력: 8.8.8.8; rm -rf /var/www/html
    => 실행: ping 8.8.8.8; rm -rf /var/www/html  (서버 파일 삭제)

개선 코드 — 화이트리스트 검증 + ProcessBuilder 인수 분리:

    @PostMapping("/ping")
    public String ping(@RequestParam String host) {
        // 숫자와 점(.)만 허용하는 화이트리스트 검증
        if (!host.matches("^[0-9.]+$")) {
            throw new IllegalArgumentException("Invalid host");
        }
        // 인수를 배열로 분리 => 명령 삽입 원천 차단
        ProcessBuilder pb = new ProcessBuilder("ping", "-c", "4", host);
        pb.start();
        return "success";
    }

---

## 6개월 개선 로드맵

### Phase 1 — Quick Win (즉시, 1주 이내)

4개 Critical 취약점 긴급 패치:

- SQL Injection 28개 지점 전체 제거 (MyBatis `${}` => `#{}` 전환)
- OS Command Injection 차단 (Runtime.exec() 제거, ProcessBuilder + 화이트리스트)
- 쿠키 기반 권한 관리 전면 재구축 (JWT 또는 서버 세션 기반으로 전환)
- 파일 업로드 보안 강화 (화이트리스트 확장자 + Magic Bytes 검증)

### Phase 2 — Short-term (1 ~ 2개월)

12개 High 취약점 해결:

- 접근 제어 강화 (IDOR 방어, 모든 리소스에 소유자 검증 추가)
- 세션 관리 개선 (세션 고정 공격 방어, 로그아웃 시 서버 세션 삭제)
- OS 보안 설정 강화 (비밀번호 복잡도 정책, 계정 잠금 임계치 설정)
- 불필요한 서비스 비활성화 (NFS,익명 FTP, r 계열 서비스 등)

**Phase 2 완료 시점 (약 3개월) => ISO 27001 인증 신청 가능**

### Phase 3 — Mid-term (2 ~ 4개월)

10개 Medium 취약점 해결:

- 로깅 및 모니터링 체계 구축 (SIEM 연동, 보안 이벤트 실시간 감지)
- 보안 정책 수립 및 배포 (취약점 관리 절차, 사고 대응 플레이북)
- 파일 권한 전수 정비 (서버 전체 SUID/SGID 점검)

### Phase 4 — Long-term (4 ~ 6개월)

지속적 개선 체계 수립:

- 전직원 보안 인식 교육 프로그램 운영
- 정기 취약점 진단 체계 확립 (분기 1회 이상)
- 에러 핸들링 표준화 (내부 오류 정보 외부 노출 제거)

---

## 예상 비용 및 인력

### 투입 인력 계획

    보안 엔지니어  :  2명 (전담)
    백엔드 개발자  :  3명 (파트타임)
    인프라 엔지니어:  1명 (파트타임)
    외부 컨설턴트  :  1명 (주간 리뷰)

### 단계별 예상 비용

| 단계 | 기간 | 비용 |
|------|------|------|
| Phase 1 — 긴급 패치 | 1주 | 약 3,000만 원 |
| Phase 2 — High 해결 | 1~2개월 | 약 5,000만 원 |
| Phase 3~4 — 중장기 | 2~6개월 | 약 4,000만 원 |
| **합계** | **6개월** | **약 1억 2,000만 원** |

---

## 산출물 구성

| 파일 | 형식 | 대상 독자 |
|------|------|----------|
| executive_summary.txt | 텍스트 | 경영진 — 비즈니스 리스크 + 비용 + 일정 중심 |
| technical_report.txt | 텍스트 | 기술팀 — Before/After 코드 + 구체적 수정 방안 |
| all_vulnerabilities.csv | CSV | 분석용 — 27개 취약점 전체 원본 데이터 |
| gap_analysis.csv | CSV | 감사용 — ISO 27001 통제항목별 준수성 평가 |
| remediation_roadmap.csv | CSV | PM용 — 단계별 개선 작업 계획 |
| vulnerability_analysis.png | PNG | 시각화 — 심각도 분포, CVSS 히스토그램, 취약점 유형 비율 |

---

## 데이터 분석 프로세스

    1. 취약점 데이터 구조화
       Week 10 스캔 결과 => CSV / DataFrame 변환

    2. CVSS 스코어링 및 심각도 분류
       각 취약점에 CVSS v3.1 기준 점수 산정

    3. ISO 27001:2022 통제항목 매핑
       취약점 => 관련 통제항목(A.5.x, A.8.x) 연결

    4. Gap Analysis
       현재 상태 vs ISO 27001 요구사항 비교
       => Compliant / Partially Compliant / Non-Compliant / Critical Gap 분류

    5. 우선순위 기반 로드맵 생성
       CVSS 점수 + 비즈니스 영향도 조합으로 처리 순서 결정

    6. 시각화 및 이중 보고서 작성
       경영진용 Executive Summary + 기술팀용 Technical Report

---

## 학습 성과 정리

| 영역 | 학습 내용 |
|------|----------|
| **컨설팅 프로세스** | 진단 결과 => ISO 표준 매핑 => Gap Analysis => 로드맵 도출 전체 흐름 |
| **ISO 27001** | 통제항목(A.5.x, A.8.x) 구조 및 실제 취약점과의 연결 관계 |
| **리스크 커뮤니케이션** | 기술적 취약점을 비즈니스 언어(예상 피해액, 계약 리스크)로 전환 |
| **보고서 이중화** | 경영진용(Executive Summary)과 기술팀용(Technical Report) 분리 작성 |
| **데이터 기반 분석** | Pandas + Matplotlib 으로 취약점 분포 시각화 |
