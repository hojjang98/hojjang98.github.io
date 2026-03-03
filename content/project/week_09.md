---
title: "Week 09 — 웹 취약점 자동화 스캐너 개발"
date: 2026-01-02
draft: false
tags: ["Python", "웹보안", "자동화", "스캐너", "SQLInjection", "XSS", "CSRF", "파일업로드", "OWASP", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "Week 08에서 공격자 시점을 체험했다면, Week 09는 그 반대편 — 취약점을 자동으로 탐지하는 Python 보안 스캐너를 직접 설계하고 구현한 프로젝트"
---

# Week 09 — 웹 취약점 자동화 스캐너 개발

> 전체 소스코드는 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_09](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_09)

> **교육 목적으로 구성된 실습입니다.**
> 의도적으로 취약한 환경을 대상으로만 사용하며, 무단 스캔은 정보통신망법 위반입니다.

---

## 개요

Week 08 에서는 **공격자** 시점에서 SQL Injection 과 XSS 를 직접 수행했다.
Week 09 는 그 반대편이다. 이번에는 **방어자** 시점에서,
취약점을 자동으로 찾아내는 **Python 기반 보안 스캐너**를 직접 설계하고 구현했다.

단순히 "공격이 가능한가?"를 넘어 **어디에, 어떤 심각도로, 왜 취약한가** 를
자동으로 판단하고 리포트로 출력하는 도구를 만드는 것이 이번 주의 핵심이었다.

---

## 시스템 전체 구조

프로젝트는 **취약한 타깃 앱** 과 **이를 진단하는 스캐너** 두 부분으로 구성된다.

    vulnerable_app/          -- 의도적으로 취약하게 구현한 Flask 웹 앱 (스캔 대상)
    ├── app.py               -- 메인 애플리케이션 (SQL Injection, XSS, CSRF, 파일업로드 취약)
    ├── templates/           -- 로그인, 게시판, 검색, 업로드, 프로필 HTML
    └── uploads/             -- 업로드 파일 저장소 (확장자 검증 없음)

    scanners/                -- 자동화 취약점 스캐너 모음
    ├── sql_injection_scanner.py
    ├── xss_scanner.py
    ├── csrf_scanner.py
    ├── file_upload_scanner.py
    └── integrated_scanner.py    -- 4개 스캐너를 통합 실행하는 오케스트레이터

    reports/                 -- 스캔 결과 자동 저장
    └── FINAL_COMPREHENSIVE_REPORT_*.txt

---

## 구현된 취약점 4종 (타깃 앱)

타깃 앱은 현실적인 공격 시나리오를 테스트할 수 있도록 4가지 취약점을 의도적으로 내포하고 있다.

| 취약점 | 위치 | 심각도 | 대표 페이로드 |
|--------|------|--------|--------------|
| **SQL Injection** | 로그인 폼, 검색 기능 | CRITICAL ~ HIGH | ' OR '1'='1 |
| **XSS** | 게시판, 검색 결과 | HIGH | script 태그, img onerror |
| **CSRF** | 프로필 수정, 글 작성 | HIGH ~ MEDIUM | CSRF 토큰 미구현 |
| **File Upload** | 파일 업로드 기능 | CRITICAL | .php, .py, .exe 업로드 가능 |

테스트 계정:

    admin    / admin123    -- 관리자 계정
    user1    / password1   -- 일반 사용자
    testuser / test123     -- 테스트 사용자

---

## 핵심 코드 — 스캐너 설계 원칙

### 1. 공통 스캔 인터페이스

각 개별 스캐너는 동일한 구조의 딕셔너리를 반환한다.
이 일관된 인터페이스 덕분에 IntegratedScanner 가 결과를 타입 무관하게 수집하고 집계할 수 있다.

    # 각 스캐너의 반환 형식 (예: SQL Injection 취약점 발견 시)
    {
        "type":        "SQL Injection",
        "severity":    "CRITICAL",
        "location":    "http://localhost:5000/login",
        "payload":     "' OR '1'='1' --",
        "description": "로그인 폼에서 SQL Injection 취약점 발견. 인증 우회 가능"
    }

심각도 기준:

- **CRITICAL** — 즉각적인 데이터 탈취 또는 시스템 제어 가능 (파일 업로드, SQLi 인증 우회)
- **HIGH** — 사용자 세션 탈취 또는 중요 기능 조작 가능 (XSS, CSRF)
- **MEDIUM** — 정보 노출 또는 부분적 기능 영향

### 2. IntegratedScanner — 오케스트레이터 패턴

4개의 개별 스캐너를 순차 실행하고, 결과를 통합하여 종합 리포트를 생성하는 클래스다.

흐름:

    IntegratedScanner("http://localhost:5000")
        │
        ├── [1/4] SQLInjectionScanner.scan()  => sql_vulns 리스트
        ├── [2/4] XSSScanner.scan()           => xss_vulns 리스트
        ├── [3/4] CSRFScanner.scan()          => csrf_vulns 리스트
        └── [4/4] FileUploadScanner.scan()    => upload_vulns 리스트
                    │
                    ▼
            all_vulnerabilities 통합
                    │
                    ▼
            generate_summary_report()
            => CRITICAL / HIGH / MEDIUM 심각도별 분류
            => 취약점별 위치 + 페이로드 + 설명 상세 기록
            => 보안 권장사항 자동 추가

핵심 집계 로직 (축약):

    class IntegratedScanner:
        def __init__(self, base_url):
            self.base_url = base_url
            self.all_vulnerabilities = []
            self.scan_results = {}

        def run_all_scans(self):
            for Scanner, key in [(SQLInjectionScanner, 'SQL Injection'), ...]:
                vulns = Scanner(self.base_url).scan()
                self.scan_results[key] = vulns
                self.all_vulnerabilities.extend(vulns)  # 타입 무관 통합

        def generate_summary_report(self):
            critical = [v for v in self.all_vulnerabilities if v.get('severity') == 'CRITICAL']
            high     = [v for v in self.all_vulnerabilities if v.get('severity') == 'HIGH']
            medium   = [v for v in self.all_vulnerabilities if v.get('severity') == 'MEDIUM']
            # 심각도별 분류 후 리포트 문자열 생성

---

## 스캐너별 탐지 방식

### SQL Injection 스캐너

로그인 폼과 검색 기능에 페이로드를 자동으로 주입하고 응답을 분석한다.

    테스트 페이로드 목록:
    - ' OR '1'='1              => Boolean-based: 항상 참인 조건 삽입
    - ' OR '1'='1' --          => 주석으로 나머지 쿼리 무력화
    - ' UNION SELECT username, password FROM users--   => UNION 기반 데이터 추출 시도
    - '; DROP TABLE users--    => 구조 파괴 시도 (오류 메시지 분석용)

    탐지 기준:
    - 응답에 "Welcome", "Dashboard" 등 로그인 성공 키워드 포함 => 인증 우회 확인
    - 응답에 "SQL", "sqlite", "syntax error" 포함 => 에러 기반 SQLi 확인

### XSS 스캐너

게시판 글 작성과 검색 기능에 스크립트 페이로드를 삽입하고 응답 HTML 에 그대로 반영되는지 확인한다.

    테스트 페이로드 목록:
    - <script>alert('XSS')</script>
    - <img src=x onerror=alert('XSS')>    => 이벤트 핸들러 기반 (필터 우회 변형)
    - <svg onload=alert('XSS')>           => SVG 태그 활용 우회
    - javascript:alert('XSS')            => URL 스킴 기반

    탐지 기준:
    - 응답 HTML 에 페이로드 문자열이 이스케이프 없이 그대로 포함되면 취약으로 판정

### CSRF 스캐너

상태 변경 기능(프로필 수정, 글 작성)의 HTML 폼에 CSRF 토큰이 존재하는지 점검한다.

    탐지 기준:
    - 폼 내부에 csrf_token, _token, authenticity_token 등 토큰 필드 부재 => CSRF 취약
    - 요청 헤더에 Origin / Referer 검증 로직 부재 여부도 확인

### File Upload 스캐너

위험한 확장자의 파일을 업로드하고 서버가 수용하는지 테스트한다.

    테스트 확장자 목록:
    .php, .php5, .phtml,   => 서버사이드 코드 실행 가능
    .py, .rb, .pl,         => 스크립트 실행
    .sh, .bash,            => 쉘 스크립트
    .exe, .bat,            => 실행 파일
    .htaccess              => 서버 설정 덮어쓰기

    탐지 기준:
    - 업로드 요청 응답 코드가 200 이고 "success" 등의 키워드 포함 => CRITICAL

---

## 종합 리포트 출력 구조

스캔 완료 후 자동으로 생성되는 리포트 형식:

    ======================================================================
    COMPREHENSIVE SECURITY SCAN REPORT
    ======================================================================
    Scan Date: 2026-01-02 14:30:00
    Target URL: http://localhost:5000
    ======================================================================

    VULNERABILITY SUMMARY
    ----------------------------------------------------------------------
    Total Vulnerabilities Found: 9

      - SQL Injection : 3 vulnerabilities
      - XSS           : 2 vulnerabilities
      - CSRF          : 2 vulnerabilities
      - File Upload   : 2 vulnerabilities

    SEVERITY BREAKDOWN
    ----------------------------------------------------------------------
      CRITICAL : 3
      HIGH     : 5
      MEDIUM   : 1

    DETAILED VULNERABILITY LIST
    ======================================================================
    1. [CRITICAL] SQL Injection
       Location : http://localhost:5000/login
       Payload  : ' OR '1'='1' --
       Description: 로그인 폼 인증 우회 가능
    ...

    SECURITY RECOMMENDATIONS
    ======================================================================
    1. SQL Injection Prevention:
       - Use parameterized queries (prepared statements)
       ...

---

## Week 08 -> Week 09 성장 포인트

| 관점 | Week 08 (공격자) | Week 09 (방어자) |
|------|-----------------|-----------------|
| 역할 | 취약점을 직접 익스플로잇 | 취약점을 자동으로 탐지 |
| 도구 | 브라우저 입력창 | Python requests + BeautifulSoup |
| 대상 | 단일 취약점 실습 | 4가지 취약점 종합 스캔 |
| 결과물 | 공격 성공 확인 | 심각도별 분류 + 자동 리포트 |
| 관점 | "어떻게 뚫을까?" | "어디가 뚫릴 수 있는가?" |

---

## 방어 권장사항 (리포트 내 자동 생성)

### SQL Injection

- Parameterized Queries (Prepared Statements) 사용
- ORM 프레임워크 활용 (SQLAlchemy, Django ORM)
- 입력값 화이트리스트 검증

### XSS

- Output Encoding / Escaping 구현
- Content Security Policy (CSP) 헤더 적용
- 템플릿 엔진의 Auto-escaping 유지 (\|safe 미사용)

### CSRF

- 모든 상태 변경 요청에 CSRF 토큰 구현
- SameSite 쿠키 속성 설정 (Strict 또는 Lax)
- Origin / Referer 헤더 서버 측 검증

### File Upload

- 화이트리스트 기반 확장자 검증 (허용 목록만 통과)
- 파일 내용 검증 (Magic Bytes 확인)
- 업로드 파일을 웹 루트 외부 경로에 저장
- 업로드 파일명 서버 측 재생성 (원본 파일명 사용 금지)
- 업로드 용량 제한 설정

---

## 학습 성과 정리

| 영역 | 학습 내용 |
|------|----------|
| **보안 자동화** | 반복적인 취약점 테스트를 스크립트로 자동화하는 방법론 체득 |
| **스캐너 설계** | 공통 인터페이스 기반 모듈화로 확장성 있는 구조 설계 |
| **취약점 탐지** | SQL Injection / XSS / CSRF / File Upload 자동 탐지 로직 구현 |
| **리포트 생성** | 심각도별 분류, 발견사항 상세 기록, 권장사항 자동 출력 |
| **공격-방어 연결** | 공격 기법을 이해해야 탐지 로직을 설계할 수 있다는 원칙 체감 |

---

## 향후 확장 방향

- **Path Traversal 스캐너** — ../../../etc/passwd 형태의 디렉토리 탐색 탐지
- **SSRF 스캐너** — 서버를 통한 내부 네트워크 요청 위조 탐지
- **인증/세션 스캐너** — 세션 고정, 취약한 쿠키 설정 탐지
- **HTML 리포트** — 텍스트 리포트를 색상 코드 기반 인터랙티브 HTML 로 전환
- **크롤러 통합** — 엔드포인트를 자동 탐색하여 스캔 범위 자동 확장
