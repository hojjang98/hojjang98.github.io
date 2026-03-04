---
title: "Week 15 — E-Commerce 보안 컨설팅 시뮬레이션 4/4: 모니터링 & 최종 보고서"
date: 2026-02-09
draft: false
tags: ["보안컨설팅", "모니터링", "로그분석", "SIEM", "최종보고서", "보안대시보드", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "4주 보안 컨설팅 시뮬레이션 최종 주 — 보안 로그 분석 시스템 구축과 대시보드 개발, 그리고 4주간의 전체 프로세스를 담은 최종 컨설팅 보고서 작성 완료"
---

# Week 15 — E-Commerce 보안 컨설팅 시뮬레이션 4/4: 모니터링 & 최종 보고서

> 전체 소스코드 및 최종 보고서는 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_15](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_15)

---

## 4주 시리즈 완주

    Week 12 : 취약한 E-Commerce 시스템 구축
    Week 13 : 취약점 진단 (OWASP ZAP + 수동)
    Week 14 : 보안 개선 구현 (Critical/High 100% 제거)
    Week 15 : 모니터링 체계 + 최종 컨설팅 보고서  <- 이번 주

보안 컨설팅은 취약점을 고치는 것으로 끝나지 않는다.
**"앞으로 새로운 공격이 들어왔을 때 탐지할 수 있는가?"** 가 마지막 질문이다.

---

## 모니터링 시스템 구현

### SecurityLogAnalyzer 클래스

Flask 애플리케이션이 생성하는 보안 로그를 파싱하여 공격 시도를 자동 탐지하는 스크립트다.

탐지 대상 이벤트 4종:

    - SQL Injection 시도
    - XSS 공격 시도
    - 로그인 실패
    - 파일 업로드 차단

탐지 방식 — 정규식 패턴 매칭:

    # SQL Injection 탐지 패턴
    sql_patterns = [
        r"'.*OR.*'.*=.*'",   # ' OR '1'='1 계열
        r"'.*--",             # 주석 삽입 계열
        r"UNION.*SELECT",     # UNION 기반 데이터 추출
        r"';.*DROP",          # 테이블 삭제 시도
    ]

    # XSS 탐지 패턴
    xss_patterns = [
        r"<script>",          # 기본 스크립트 태그
        r"javascript:",        # 프로토콜 기반 XSS
        r"onerror=",          # 이벤트 핸들러 삽입
        r"onload=",
    ]

클래스 구조:

    class SecurityLogAnalyzer:
        def __init__(self, log_file):
            self.log_file = log_file
            self.sql_injection_attempts = []
            self.xss_attempts = []
            self.failed_logins = []

        def analyze(self):
            # 로그 파일 읽기 => 각 줄을 3개 탐지기에 순서대로 통과
            for line in logs:
                self.detect_sql_injection(line)
                self.detect_xss(line)
                self.detect_failed_login(line)

        def print_report(self):
            # 탐지 건수 + 최근 5건 출력

### 샘플 로그 기반 시연 결과

`create_sample_log()` 로 생성한 시나리오 로그에서 탐지된 결과:

    SQL Injection 시도 : 2건
      - admin' OR '1'='1 로그인 시도
      - ' OR 1=1-- 검색 쿼리

    XSS 공격 시도      : 1건
      - <script>alert('XSS')</script> 댓글 시도

    로그인 실패        : 0건 (Invalid credentials 메시지 기준)

    (별도 확인: 파일 업로드 차단 1건 — shell.php)

Week 14 의 보안 개선이 적용된 상태에서 이 로그가 생성됐다면:
**공격은 탐지되었고, 모두 차단된 상태** 다.

---

## 보안 대시보드

`dashboard.html` 은 정적 HTML 기반의 간단한 보안 이벤트 현황판이다.

표시 항목:

    - 현재 취약점 현황 (Critical 0 / High 0 / Medium 2 / Low 4)
    - 보안 이벤트 통계 (SQL Injection 시도, XSS 시도, 로그인 실패)
    - 최근 로그 타임라인
    - 시스템 상태 (정상/경고/위험)

실무에서는 이 역할을 **SIEM(Security Information and Event Management)** 솔루션이 수행한다.
(Splunk, IBM QRadar, Microsoft Sentinel 등)
이번 구현은 SIEM 의 핵심 동작 원리를 Python 으로 미니멀하게 재현한 것이다.

---

## 4주 프로젝트 최종 결과

### 취약점 해결 현황

| 심각도 | 진단 (Week 13) | 개선 후 (Week 14) | 해결률 |
|--------|---------------|------------------|--------|
| Critical | 2 | **0** | **100%** |
| High | 2 | **0** | **100%** |
| Medium | 3 | 2 | 33% |
| Low | 5 | 4 | 20% |

**총 6개 취약점 해결 — Critical / High 완전 제거**

### Executive Summary (최종 보고서 요약)

**클라이언트**: 중소기업 E-Commerce 웹 애플리케이션 (시뮬레이션)
**컨설팅 기간**: 2026년 1월 26일 ~ 2026년 2월 22일 (4주)
**컨설턴트**: 호짱 (개인 솔로 프로젝트)

주요 성과:

    1. Critical/High 취약점 4개 완전 제거
       - SQL Injection (로그인, 검색) : Prepared Statement 전환
       - XSS (댓글) : |safe 필터 제거, CSP 헤더 추가
       - 파일 업로드 : 화이트리스트 검증 + secure_filename() 적용

    2. CSRF 방어 구축
       - Flask-WTF CSRF 토큰 전역 적용

    3. 보안 헤더 설정
       - X-Frame-Options, X-Content-Type-Options, CSP, X-XSS-Protection

    4. 모니터링 체계 구축
       - 보안 로그 분석 스크립트
       - 보안 이벤트 대시보드

권고사항 — 잔존 과제:

    단기 (1개월):
    - CSP 정책 강화 (Nonce 기반 적용)
    - 로그 모니터링 자동 알림 시스템 구축

    장기 (3개월):
    - 비밀번호 bcrypt 해싱 적용
    - 분기별 정기 취약점 스캔
    - 개발팀 시큐어 코딩 교육

---

## 4주 시리즈 회고

### 자동화 vs 수동의 교훈

이 프로젝트에서 가장 인상적인 발견은 **OWASP ZAP 이 Critical 취약점을 전혀 탐지하지 못했다** 는 것이다.

    OWASP ZAP 결과:
    취약 버전 (Week 12) : High 0 / Medium 3 / Low 5
    개선 버전 (Week 14) : High 0 / Medium 2 / Low 4

    수동 테스트 결과:
    취약 버전 : Critical 2 (SQL Injection) 탐지
    개선 버전 : Critical 0 (공격 차단 확인)

자동화 스캐너는 보안 헤더 누락처럼 **응답만 보면 알 수 있는 것** 을 잘 잡는다.
반면 인증 로직이나 비즈니스 맥락이 필요한 Critical 취약점은 **사람이 직접 공격해봐야** 탐지된다.

**실무 결론: 자동화 스캔 + 수동 진단의 병행은 선택이 아닌 필수다.**

### 공격자와 방어자를 모두 경험하다

    Week 12 : 공격자의 시선으로 취약한 코드를 의도적으로 작성
    Week 13 : 외부 진단자의 시선으로 시스템을 공격하고 발굴
    Week 14 : 개발자의 시선으로 코드를 수정하고 검증
    Week 15 : 운영자의 시선으로 로그를 모니터링하고 보고

보안 컨설팅은 **이 네 가지 시선을 동시에 가져야 하는 직군** 임을 체감했다.

---

## 학습 성과 정리

| 영역 | 학습 내용 |
|------|------------|
| **컨설팅 전체 흐름** | 구축 → 진단 → 개선 → 모니터링 A to Z 독립 수행 |
| **로그 분석** | 정규식 기반 보안 이벤트 탐지 패턴 구현 |
| **SIEM 원리** | 로그 수집 → 패턴 매칭 → 알람의 핵심 흐름 이해 |
| **보고서 작성** | Executive Summary + 기술 상세 + 권고사항 구조화 |
| **자동화의 한계** | 도구와 사람의 역할 분리를 직접 경험으로 확인 |

---

## 다음 프로젝트 예고 — Week 16~17: 파이널 프로젝트 준비

개인 보안 컨설팅 시뮬레이션에서 **팀 단위 실무 수준 컨설팅 프로젝트** 로 이동한다.

주제: **개인정보 위·수탁 관리체계 컨설팅**

    위탁사  : 국내 기업 선정 (팀 결정)
    수탁사  : 복수의 가상 업체 (업종별 구성)
    산출물  : 보안협약서 + 진단 체크리스트 + 수탁사별 진단보고서 + 최종 통합보고서

4주 솔로 프로젝트에서 체득한 **컨설팅 방법론** 을 팀 프로젝트에 적용하는 시간이다.
