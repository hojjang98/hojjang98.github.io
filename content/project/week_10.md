---
title: "Mini Project 02 — DNA Lab Security Scanner"
date: 2026-01-16
draft: false
tags: ["Python", "보안스캐너", "OWASP", "모의침투", "자동화", "팀프로젝트", "화이트박스", "블랙박스", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "23andMe 데이터 유출 사건을 배경으로, 유전 정보를 다루는 DNA Lab 웹앱을 대상으로 웹 15종 + OS 50종 총 65개 스캐너를 구현한 두 번째 팀 미니프로젝트 (리드 보안 엔지니어)"
---

# Mini Project 02 — DNA Lab Security Scanner

> 전체 소스코드는 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_10](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_10)

> **승인된 환경에서의 보안 테스트 목적으로만 사용됩니다.**
> 소유하거나 명시적 테스트 권한이 있는 시스템에만 사용하세요.

---

## 프로젝트 소개

**DNA Lab Security Scanner** 는 SK쉴더스 루키즈 28기 **두 번째 팀 미니프로젝트**로,
유전 정보를 다루는 웹 애플리케이션을 대상으로 한 종합 취약점 진단 프레임워크다.

본인은 이번 프로젝트에서 **리드 보안 엔지니어** 를 맡아
전체 스캐너 아키텍처 설계, 핵심 스캐너 개발, 팀 기술 방향 결정을 총괄했다.

**Team Helix 구성:**

| 역할 | 팀원 |
|------|------|
| **리드 보안 엔지니어 / 스캐너 개발** | 호짱 (본인) |
| **백엔드 · 프론트엔드 개발 / OS 스캐너** | 김기남 |
| **웹 서비스 스캐너 개발** | 신동원 |
| **OS 스캐너 개발** | 이진주 |
| **시스템 통합** | 최호준 |

---

## 프로젝트 배경 — 23andMe 데이터 유출 사건

> 2023년, 유전자 검사 기업 **23andMe** 는 **690만 명** 사용자의 유전 정보가 유출되는 대규모 침해 사고를 겪었다.

이 사건은 단순한 개인정보 유출이 아니다.
유전 정보는 변경이 불가능하다. 신용카드 번호나 비밀번호는 바꿀 수 있지만,
**DNA 는 평생 바뀌지 않는다.**

이 배경에서 출발해, 우리 팀은 가상의 DNA 검사 서비스 "Rookies DNA" 를 시뮬레이션하고
이를 대상으로 한 **종합 보안 진단 도구**를 개발했다.
취약점을 찾는 것에서 끝나지 않고, 각 발견 사항에 대한 **구체적인 개선 방안**까지 제공하는 것이 목표였다.

---

## 스캐너 전체 구성 — 65개

Week 09 의 4개 스캐너에서 이번에는 **65개** 로 대폭 확장했다.

    웹 애플리케이션 스캐너 (15개)
    ─────────────────────────────
    01. XSS               — Stored / Reflected / DOM 기반 XSS 탐지
    02. SQL Injection      — MyBatis XML 정적 분석 + 동적 페이로드 테스트
    03. Code Injection     — Thymeleaf 템플릿 취약점 스캔
    04. CSRF               — 토큰 검증 및 SameSite 쿠키 확인
    05. Weak Password      — 복잡도 및 무차별 대입 방어 테스트
    06. Access Control     — IDOR, 인증 우회, 수평/수직 권한 상승
    07. Password Recovery  — 취약한 비밀번호 재설정 메커니즘
    08. Session Management — 세션 고정 및 로그아웃 검증
    09. Cookie Security    — 쿠키 변조, HttpOnly / Secure 플래그 확인
    10. File Transfer      — 악성 파일 업로드 및 경로 조작
    11. Path Traversal     — 디렉토리 순회 취약점 탐지
    12. Error Handling     — 에러 메시지를 통한 내부 정보 노출
    13. Format String      — 포맷 스트링 인젝션 취약점
    14. HTTP Methods       — 불필요한 메서드 노출 (TRACE, PUT, DELETE)
    15. SSRF               — 서버측 요청 위조 및 명령어 인젝션

    운영체제 보안 스캐너 (50개)
    ─────────────────────────────
    인증 및 계정 관리 (12개)
    - Root 원격 로그인 허용 여부, 비밀번호 정책, 계정 잠금, 중복 UID,
      패스워드 해싱 알고리즘, 세션 타임아웃 등

    파일 및 디렉토리 권한 (10개)
    - /etc/passwd, /etc/shadow, sudoers 권한, SUID/SGID 파일 점검,
      시작 스크립트 권한 등

    네트워크 서비스 (20개)
    - Finger, 익명 FTP, r 계열 서비스, NFS, SNMP community string,
      Sendmail 버전, TFTP/TALK 서비스 등 레거시 위험 서비스

    시스템 설정 (8개)
    - NTP 설정, 로깅 정책, 로그 디렉토리 권한, 콘솔 로그인 제한 등

---

## 아키텍처 — 하이브리드 스캔 방식

단순 블랙박스 테스트에서 나아가, **화이트박스 + 블랙박스** 를 결합한 하이브리드 방식을 채택했다.

    스캔 모드 선택:
    1. Static Scan   (화이트박스 + 기본 블랙박스)
    2. Dynamic Scan  (크롤러 + 능동 테스트)
    3. Full Scan     (정적 + 동적 전체 실행)

**화이트박스 (정적 분석)**:
- Java 소스코드에서 보안 취약 패턴 정규식 매칭
- **MyBatis XML** 파싱 — 안전하지 않은 **${}** 파라미터 바인딩 탐지
- **Thymeleaf 템플릿** 분석 — **th:utext** 및 인라인 표현식 탐지

**블랙박스 (동적 테스트)**:
- 크롤러로 엔드포인트 및 폼 자동 탐색
- 인증 / 비인증 세션으로 각 기능에 페이로드 주입
- 응답 코드, 헤더, 본문을 분석하여 취약 여부 판단

---

## 핵심 코드 설명

### 1. 통합 오케스트레이터 — web_main.py

모든 스캐너는 **동일한 scan() API** 를 통해 결과를 반환하므로,
오케스트레이터가 스캐너 종류와 무관하게 결과를 수집하고 리포트로 통합할 수 있다.

스캐너 공통 반환 형식:

    def scan(target_url, login_info=None):
        return {
            'name':           '취약점 이름',
            'vulnerable':     True / False,
            'details':        ['발견사항 1', '발견사항 2'],
            'recommendation': '구체적인 수정 권장사항'
        }

오케스트레이터의 스캐너 순차 실행 (15개):

    scanners = [
        (1,  "XSS",              "01_xss_scanner"),
        (2,  "SQL Injection",    "02_sqli_scanner"),
        (3,  "Code Injection",   "03_code_injection_scanner"),
        ...
        (15, "SSRF",             "15_ssrf_scanner"),
    ]

    for num, name, mod_name in scanners:
        print(f"[*] Running {name} scanner ({num}/15)...", end=' ')
        module = importlib.import_module(mod_name)
        res = module.scan(config['target_url'], config['login'])
        results.append(res)
        print("[!] VULNERABLE" if res['vulnerable'] else "[+] Safe")

### 2. CLI 인자 + config.json 우선순위 설계

target URL 은 세 단계의 우선순위로 결정된다.

    우선순위:  CLI 인자  >  config.json  >  기본값 (http://127.0.0.1:8080)

    # 실행 예시
    python main.py -t http://192.168.1.100:8080

    # config.json 구조
    {
        "target_url": "http://localhost:8080",
        "admin_login": {"username": "admin", "password": "your_password"},
        "guest_login": {"username": "guest", "password": "guest"}
    }

이 설계 덕분에 동일한 스캐너를 **여러 환경** (로컬 / 스테이징 / 심사 대상 서버) 에 유연하게 적용할 수 있다.

### 3. 3종 리포트 자동 생성

스캔 완료 후 타임스탬프 기반으로 3가지 형식의 리포트를 자동 저장한다.

    save_report(results, config)
    ├── reports/scan_report_20260116_143022.txt    -- 빠른 검토용 텍스트 요약
    ├── reports/scan_report_20260116_143022.html   -- 색상 코드 인터랙티브 대시보드
    └── reports/scan_report_20260116_143022.pdf    -- 이해관계자용 전문 문서 (WeasyPrint)

HTML 리포트 구성:

    ┌─────────────────────────────────────────────┐
    │  DNA Lab Security Scan Report               │
    │  Date: 2026-01-16   Target: localhost:8080  │
    ├──────────┬──────────┬──────────┬───────────┤
    │  Total   │ Vuln     │  Safe    │ Findings  │
    │   15     │  12 (빨강)│  3 (초록) │   28      │
    ├─────────────────────────────────────────────┤
    │ 1. XSS Scanner          [!] VULNERABLE      │
    │    Details: Stored XSS via /dna/result...   │
    │    Fix: Output encoding + CSP 적용          │
    ├─────────────────────────────────────────────┤
    │ 3. Code Injection       [+] Safe            │
    │    (초록 배경)                               │
    └─────────────────────────────────────────────┘

### 4. MyBatis XML 정적 분석 — 화이트박스의 핵심

이번 타깃 앱은 Python/Flask 가 아닌 **Java Spring Boot + MyBatis** 기반이다.
MyBatis 에서 `${}` 문법은 값을 SQL 에 문자열로 직접 삽입하기 때문에 SQL Injection 에 취약하다.
반면 `#{}` 는 Prepared Statement 로 바인딩되어 안전하다.

    # 위험한 MyBatis XML (SQL Injection 가능)
    SELECT * FROM users WHERE username = '${username}'

    # 안전한 MyBatis XML (Prepared Statement)
    SELECT * FROM users WHERE username = #{username}

SQL Injection 스캐너는 프로젝트 디렉토리를 재귀 탐색하며
**모든 .xml 파일에서 ${ 패턴을 정규식으로 탐색**한다.

    # 정적 분석 핵심 로직 (축약)
    for xml_file in Path(project_path).rglob("*.xml"):
        content = xml_file.read_text()
        if re.search(r'\$\{', content):
            # ${} 파라미터 바인딩 발견 => VULNERABLE 판정

---

## 스캔 실행 예시 (콘솔 출력)

    ============================================================
     DNA Lab Security Vulnerability Scanner
    ============================================================
     Target: http://localhost:8080
    ------------------------------------------------------------
     Select Scan Mode:
      1. Static Scan  (Whitebox + Basic Blackbox)
      2. Dynamic Scan (Crawler + Active Scan)
      3. Full Scan    (Static + Dynamic)

     > Choice [1]: 3

    [ Phase 1: Static Scan ]
    [*] Running XSS scanner (1/15)...           [!] VULNERABLE
    [*] Running SQL Injection scanner (2/15)...  [!] VULNERABLE
    [*] Running Code Injection scanner (3/15)... [+] Safe
    [*] Running CSRF scanner (4/15)...           [!] VULNERABLE
    ...

    [ Phase 2: Dynamic Scan ]
    [*] Crawling target endpoints...
    [*] Running active injection tests...

    ============================================================
     Scan Complete
    ============================================================
     Reports generated:
      - TXT:  reports/scan_report_20260116_143022.txt
      - HTML: reports/scan_report_20260116_143022.html
      - PDF:  reports/scan_report_20260116_143022.pdf (Created)

     Summary: 12 Vulnerabilities found.

---

## Week 09 vs Week 10 — 스케일 비교

| 항목 | Week 09 (개인) | Week 10 (팀) |
|------|--------------|-------------|
| 스캐너 수 | 4개 | **65개** (웹 15 + OS 50) |
| 스캔 방식 | 블랙박스 | **화이트박스 + 블랙박스 하이브리드** |
| 타깃 앱 | Python Flask | **Java Spring Boot + MyBatis + Thymeleaf** |
| 정적 분석 | 없음 | **XML 파싱, Java 소스 정규식, 설정 파일 검토** |
| 리포트 형식 | TXT | **TXT + HTML + PDF** |
| 팀 구성 | 개인 | **5인 팀 (Team Helix)** |
| 배경 | 교육 실습 | **실제 침해 사건 (23andMe) 기반** |

---

## 유전 정보 보안의 특수성

이 프로젝트가 일반 웹 보안 실습과 다른 이유는 **데이터 특성** 때문이다.

- **변경 불가능성** — 유전 정보는 유출 후 변경이 불가능하다
- **가족 연관성** — 한 명의 DNA 로 혈연관계 전체가 추론 가능하다
- **영구적 피해** — 비밀번호 재설정이나 카드 재발급 같은 회복 수단이 없다
- **차별 위험** — 유전 정보는 건강보험, 고용, 보험 등에서 차별의 근거로 악용될 수 있다

따라서 유전 정보를 다루는 플랫폼은 일반적인 웹 보안 기준보다 **훨씬 높은 수준**의 보안이 요구된다.
이번 프로젝트는 그 필요성을 코드 레벨에서 직접 검증하는 경험이었다.

---

## 리드 보안 엔지니어로서의 회고

팀장이었던 Mini Project 01 과 달리, 이번에는 **기술 리더** 역할에 집중했다.

- **아키텍처 결정** — 65개 스캐너가 동일한 API 를 따르도록 인터페이스를 먼저 설계하고 팀에 공유
- **기술 분배** — 웹 스캐너와 OS 스캐너를 명확히 분리하여 팀원별 전문화 유도
- **통합 기준 설정** — `vulnerable: True/False` 와 `details`, `recommendation` 필드를 공통 규격으로 확정
- **품질 검증** — 각 스캐너가 실제 취약점을 탐지하는지 타깃 앱에서 직접 검증

> 팀원이 각자 스캐너를 독립적으로 개발해도 오케스트레이터가 결과를 수집할 수 있었던 것은,
> **처음에 공통 인터페이스를 명확히 정의했기 때문**이다.
> 기술 설계의 선행이 얼마나 중요한지 실감한 프로젝트였다.

---

## 학습 성과 정리

| 영역 | 학습 내용 |
|------|----------|
| **하이브리드 보안 테스트** | 정적 코드 분석과 동적 침투 테스트를 결합하는 방법론 체득 |
| **정적 분석** | MyBatis XML `${}` 패턴, Thymeleaf `th:utext` 자동 탐지 |
| **OS 보안 점검** | 계정 관리, 파일 권한, 네트워크 서비스, 시스템 설정 50개 항목 |
| **리포트 엔지니어링** | TXT / HTML / PDF 3종 리포트 자동 생성 구조 설계 |
| **팀 기술 리더십** | 공통 API 설계로 5인 병렬 개발 품질 일관성 확보 |
| **보안 컨텍스트 이해** | 유전 정보 보안의 특수성과 높은 기준의 필요성 |

---

## 향후 확장 방향

- **능동 크롤러 강화** — JavaScript 렌더링 페이지까지 탐색하는 Selenium 기반 크롤러
- **CVE 데이터베이스 연동** — 탐지된 소프트웨어 버전을 CVE DB 와 대조하여 알려진 취약점 매핑
- **CVSS 점수 자동 계산** — 각 취약점에 표준 CVSS 점수를 부여하여 우선순위 판단 지원
- **CI/CD 파이프라인 통합** — 배포 전 자동 보안 스캔으로 DevSecOps 파이프라인 구성
- **실시간 대시보드** — Streamlit 으로 스캔 결과를 실시간 시각화하는 웹 UI 구성
