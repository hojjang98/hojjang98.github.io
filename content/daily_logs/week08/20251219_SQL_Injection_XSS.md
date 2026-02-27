---
title: "2025.12.19 (Day 39) - 웹 해킹: SQL Injection과 XSS"
date: 2025-12-19
draft: false
tags: ["웹해킹", "SQL-Injection", "XSS", "OWASP", "WAF", "WebGoat", "Burp-Suite", "모의해킹"]
categories: ["daily-logs"]
summary: "OWASP Top 10 취약점 공격 시나리오 심화, SOC 관점 웹 공격 단계별 탐지 포인트, WAF ModSecurity 룰셋, 웹 보안 점검 체크리스트 정리"
---

# 📄 2025.12.19 (Day 39) - 웹 해킹: SQL Injection과 XSS

---

## 1. 핵심 개념 정리

### OWASP Top 10 (2021년 버전) - 주요 공격 유형

| # | 취약점 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| **A1** | **잘못된 접근 통제** | 접근 통제 로직 누락으로 인가되지 않은 기능/데이터 접근. 검사 애플리케이션의 3.81%가 해당 | IDOR, 권한 상승, 강제 브라우징 등. 모든 요청에서 인가 검증 필수 |
| **A2** | **암호화 오류** | 개인정보, 패스워드 등 민감 정보 평문 저장 또는 약한 암호화 | 데이터 유출 시 2차 피해. HTTPS, AES-256, bcrypt 등 강력한 암호화 필수 |
| **A3** | **인젝션** | SQL, OS 명령어, LDAP 등 외부 입력을 검증 없이 실행. DB 연동 부분에서 주로 발생 | SQL Injection이 대표적. Prepared Statement, ORM 사용으로 예방 |
| **A4** | **안전하지 않은 설계** | 2021년 신규 추가. 설계 단계부터 보안 고려 부족. 위협 모델링, 보안 패턴 적용 필요 | Secure by Design. 코딩 전에 보안 설계 검토 필수 |
| **A5** | **보안 설정 오류** | 기본 페이지 미삭제, 최신 패치 미적용, 디렉터리 리스팅 허용 등 | 가장 흔한 취약점. 정기적인 설정 점검, 하드닝 가이드 적용 |
| **A7** | **식별 및 인증 실패** | 세션 관리 오류, 쿠키 값 조작 가능, 약한 패스워드 정책 등 | 세션 고정, 무차별 대입 공격. MFA, 강력한 세션 관리 필수 |
| **A9** | **보안 로그 및 모니터링 실패** | 충분한 로그 미수집, 로그 분석 미흡. 침해사고 시 포렌식 불가 | SOC 관점에서 치명적. SIEM 연동, 실시간 모니터링 체계 구축 |
| **A10** | **서버 사이드 요청 변조(SSRF)** | 서버가 공격자 의도대로 외부/내부 요청 수행. 2021년 신규 추가 | 내부망 스캔, 메타데이터 탈취(AWS IMDS 공격). URL 검증 필수 |

### OWASP Top 10 변화 추이 (2013 -> 2017 -> 2021)

| 순위 | 2013년 | 2017년 | 2021년 | 분석 |
|:---:|:---|:---|:---|:---|
| A1 | 인젝션 취약점 | 인젝션 | **잘못된 접근 통제** | 접근 제어 문제가 1위로 급상승. 클라우드/API 시대 권한 관리 중요성 증가 |
| A2 | 인증 및 세션 관리 취약점 | 잘못된 인증 | **암호화 오류** | GDPR, 개인정보보호법 강화 반영 |
| A3 | XSS | 민감한 데이터 노출 | **인젝션** | Prepared Statement 등 방어 기법 보편화로 3위 하락 |
| A4 | 취약한 직접 객체 참조 | XXE | **안전하지 않은 설계** | 2021년 신규. Secure SDLC, Threat Modeling 중요성 |
| A8 | CSRF | 안전하지 않은 역직렬화 | **데이터 무결성 실패** | 2021년 신규. 공급망 공격, CI/CD 보안 중요성 |
| A10 | 검증되지 않은 리다이렉트 | 불충분한 로깅/모니터링 | **SSRF** | 2021년 신규. 클라우드 환경에서 메타데이터 탈취 위험 |

---

## 2. 실습 내용

### 실습: Burp Suite를 이용한 취약점 탐색

**Burp Suite 설정 및 활용:**
1. Burp Suite 실행 -> [Proxy] -> [Intercept] 탭
2. Windows 프록시 설정: 127.0.0.1:8080
3. 브라우저에서 대상 사이트 접속 -> [Intercept is off] 상태에서 자동 캡처
4. [Target] -> [Site map] 에서 탐색:
   - /admin/ - 관리자 페이지 노출 여부
   - /backup/ - 백업 파일 노출 여부
   - URL 파라미터, 쿠키 구조, API 엔드포인트 확인

**보안 인사이트:**
- 쿠키에 HttpOnly, Secure 플래그 없으면 XSS로 세션 탈취 가능
- 응답 헤더에 Server 버전 정보 노출 시 알려진 취약점 악용 가능
- /admin, /test, /dev 경로 발견 시 접근 제어 검증 필요

### 실습: WebGoat에서 취약점 실습

**WebGoat 실행:**
- **java -jar webgoat-container-7.1-exec.jar**
- 브라우저: http://localhost:8080/WebGoat (guest/guest)

**WebGoat 주요 학습 과정:**
- Injection Flaws: SQL Injection, Command Injection 실습
- Cross-Site Scripting: Reflected XSS, Stored XSS 실습
- Access Control: IDOR, Role Based Access Control 실습
- Session Management: 세션 고정, 세션 하이재킹 실습

**주의사항:** localhost에서만 실행, 실습 후 즉시 종료, 공인 IP 노출 절대 금지

---

## 3. 주요 공격 상세 분석

### SQL Injection 공격 원리

**취약점 발생 원인:**
- 사용자 입력을 검증 없이 SQL 쿼리에 직접 삽입
- 예: SELECT * FROM users WHERE id = '입력값'

**주요 공격 패턴:**
- 인증 우회: 입력값 = ' OR '1'='1 -> 항상 참이 되어 로그인 우회
- 데이터 추출: UNION SELECT를 이용한 다른 테이블 데이터 조회
- 에러 기반: 의도적 에러 발생으로 DB 구조 추출
- Blind SQL Injection: 참/거짓 응답 차이로 데이터 추론

**방어 방법:**
- **Prepared Statement** (가장 효과적): 쿼리 구조와 데이터를 분리
- **ORM 사용**: SQLAlchemy, Hibernate 등 ORM 프레임워크 활용
- **입력 검증**: 화이트리스트 방식으로 허용 문자만 통과
- **최소 권한**: DB 계정에 SELECT 권한만 부여 (INSERT/DELETE 불필요 시)
- **에러 메시지 숨김**: 상세 DB 오류 메시지 노출 차단

**SOC 탐지 포인트:**
- 로그에서 UNION, SELECT, OR 1=1, -- 패턴 탐지
- 500 에러 급증 (DB 오류 발생 신호)
- 동일 IP에서 다양한 파라미터 조합 시도

---

### XSS (Cross-Site Scripting) 공격 원리

**취약점 발생 원인:**
- 사용자 입력을 HTML에 그대로 출력
- 브라우저가 악성 스크립트를 실행

**공격 유형:**
- **Reflected XSS**: URL 파라미터에 스크립트 삽입, 피해자가 링크 클릭 시 실행
- **Stored XSS**: 게시판 등에 스크립트 저장, 다른 사용자 열람 시 실행 (지속성)
- **DOM XSS**: JavaScript에서 DOM 조작 시 발생

**공격 목표:**
- 쿠키/세션 탈취: document.cookie 전송으로 세션 하이재킹
- 키로깅: 폼 입력값 탈취
- 피싱 페이지 삽입: 악성 페이지로 리다이렉트

**방어 방법:**
- **출력 이스케이핑**: <, >, &, ", ' 등 특수문자를 HTML 엔티티로 변환
- **Content-Security-Policy (CSP)**: 허용된 스크립트 소스만 실행
- **HttpOnly 쿠키**: JavaScript로 쿠키 접근 차단
- **입력 검증**: 화이트리스트 방식으로 허용 태그만 통과

---

## 4. SOC 관점 - 웹 공격 탐지 포인트

| 공격 단계 | 탐지 포인트 | 대응 방안 |
|:---:|:---|:---|
| **정보 수집** | 단시간 대량 404 에러, /admin /backup 등 민감 경로 접근, OPTIONS 메서드 사용 | Rate Limiting, 스캐너 User-Agent 차단, IP 임시 차단 |
| **취약점 스캔** | Nikto/Wikto User-Agent, 비정상 URL 패턴 (../, %00), 대량 파라미터 조합 시도 | WAF 시그니처 업데이트, 비정상 패턴 차단 룰 적용 |
| **SQL Injection 시도** | SQL 키워드 (UNION, SELECT, OR 1=1), 500 에러 급증 | Prepared Statement 강제, WAF 차단, 로그 상관 분석 |
| **XSS 시도** | script 태그, onerror=, javascript: 포함 요청 | 출력 이스케이핑, CSP 헤더, WAF 차단 |
| **권한 상승** | 파라미터 변조 (id=1 -> id=2), role=user -> role=admin, 403 이후 200 응답 | 세션 기반 권한 검증, 이상 행위 알림 |
| **지속성 확보** | 웹셸 업로드 (.php, .jsp, .aspx), 백도어 계정 생성 | 파일 업로드 제한, 파일 무결성 모니터링 |

### 로그 상관 분석 예시

- **시나리오**: 동일 IP에서 /admin 접근 시도 -> 403 -> 파라미터 변조 -> 500 에러 급증 -> SQL Injection 의심
- **SIEM 룰**: 5분 내 동일 IP에서 /admin 접근 + 500 에러 5회 이상 -> 알림 발송
- **대응**: IP 임시 차단, 해당 IP 로그 전수 분석, WAF 차단 룰 추가

---

## 5. 방어 기법 심화

### WAF ModSecurity 핵심 룰

- **SQL Injection**: ARGS에 union, select, insert, delete, drop, 세미콜론, 주석(--) 포함 -> 403 (id:1001)
- **XSS**: ARGS에 script 태그, javascript:, onerror=, onload=, img 태그, iframe 포함 -> 403 (id:1002)
- **Path Traversal**: REQUEST_URI에 ../ 패턴 -> 403 (id:1003)
- **Command Injection**: ARGS에 세미콜론, 파이프(|), 백틱, &&, $() -> 403 (id:1004)
- **PHP 웹셸 차단**: 업로드 파일명 .php, .phtml, .php3-5, .phar -> 403 (id:1005)
- **스캐너 차단**: User-Agent에 nikto, wikto, nmap, sqlmap, burp -> 403 (id:1006)

### 웹 보안 점검 체크리스트

**서버 설정:**
- [ ] 서버 정보(Server, X-Powered-By) 헤더 제거
- [ ] 불필요한 HTTP 메서드(TRACE, OPTIONS) 비활성화
- [ ] 디렉터리 리스팅 비활성화 (autoindex off)
- [ ] 에러 페이지 커스터마이징 (상세 오류 메시지 숨김)
- [ ] 최신 보안 패치 적용

**입력 검증:**
- [ ] 서버 측 입력 검증 필수 (클라이언트 측 검증만으로 불충분)
- [ ] SQL Injection 방어 (Prepared Statement, ORM)
- [ ] XSS 방어 (입력 이스케이핑, CSP)
- [ ] 파일 업로드 제한 (확장자, 크기, 내용 검증)

**HTTPS 및 쿠키:**
- [ ] TLS 1.2 이상 강제, HSTS 헤더 설정
- [ ] 쿠키에 HttpOnly, Secure, SameSite 플래그 설정

**접근 제어:**
- [ ] 관리자 페이지 IP 제한 + 2차 인증
- [ ] 세션 기반 권한 검증 (파라미터 변조로 권한 상승 방지)
- [ ] 민감 경로(/admin, /config) 접근 로그 모니터링

**모니터링:**
- [ ] 웹 접근 로그 및 에러 로그 수집
- [ ] 이상 패턴 탐지 (대량 404, 스캐너 User-Agent, SQL 키워드)
- [ ] SIEM 연동 및 실시간 알림

---

## 6. 배운 점 및 심화 방향

- **배운 점**: SQL Injection과 XSS는 OWASP Top 10의 오랜 단골 취약점이지만 여전히 현장에서 발견된다. Prepared Statement와 출력 이스케이핑이 각각의 핵심 방어 방법임을 확인했다. SOC 분석가는 단순히 알람을 확인하는 것이 아니라 공격 단계 전체를 이해하고 로그를 상관 분석해야 한다. WebGoat로 공격자 관점을 직접 체험해보니 방어의 필요성이 더 명확해졌다.
- **심화 방향**: Burp Suite의 Repeater/Intruder 기능으로 SQL Injection 자동화 공격 실습, DVWA(Damn Vulnerable Web Application)에서 다양한 난이도의 XSS 실습, ModSecurity를 실제 Nginx에 연동하여 공격 차단 테스트, SIEM 룰 작성으로 SQL Injection/XSS 탐지 자동화 구현.

---

## 7. Quick Reference

### OWASP Top 10 (2021) 방어 요약

| 순위 | 취약점 | 핵심 방어 방법 |
|:---:|:---|:---|
| A1 | 잘못된 접근 통제 | 세션 기반 권한 검증, 최소 권한 원칙 |
| A2 | 암호화 오류 | AES-256, bcrypt, TLS 1.2+ |
| A3 | 인젝션 | Prepared Statement, ORM, 입력 검증 |
| A4 | 안전하지 않은 설계 | 보안 설계 패턴, 위협 모델링 |
| A5 | 보안 설정 오류 | 보안 하드닝, 정기 점검 |
| A6 | 취약한 컴포넌트 | 의존성 관리, 정기 업데이트 |
| A7 | 식별 및 인증 실패 | MFA, 강력한 세션 관리 |
| A8 | 데이터 무결성 실패 | 코드 서명, CI/CD 보안 |
| A9 | 로그/모니터링 실패 | SIEM 연동, 실시간 모니터링 |
| A10 | SSRF | URL 검증, 화이트리스트 |

### 트러블슈팅

| 문제 | 원인 | 해결 방법 |
|:---|:---|:---|
| Burp Suite 프록시 연결 안 됨 | 브라우저 프록시 설정 오류 또는 Burp Suite 미실행 | Windows 프록시 설정 확인 (127.0.0.1:8080), Proxy Listener 활성화 확인 |
| HTTPS 사이트 인증서 경고 | Burp Suite CA 인증서 미신뢰 | Burp CA 인증서 내보내기 후 브라우저에 신뢰할 수 있는 루트 인증 기관으로 등록 |
| WebGoat "Address already in use" | 8080 포트 이미 사용 중 | netstat -ano로 프로세스 확인 후 종료, 또는 --server.port=9090으로 포트 변경 |
| 웹 스캔 시 403 Forbidden 대량 발생 | WAF 또는 Rate Limiting 작동 | 스캔 속도 낮추기, User-Agent 변경 |

---

**Today's Insight:**

웹 보안의 핵심은 "정보 노출 최소화"와 "공격 표면 축소"다. 공격자는 정보 수집 단계에서 80%의 시간을 쏟는다. 서버 정보 헤더, 디렉터리 리스팅, Google에 색인된 민감 파일 등 작은 정보 하나하나가 공격의 실마리가 된다. 방어자는 공격자의 관점을 이해하고, 같은 도구로 자사 시스템을 점검해야 한다. 공격자보다 먼저 취약점을 찾아 막는 것이 최선의 방어다. Burp Suite와 WebGoat로 공격자 언어를 배우는 것이 결국 더 나은 방어자가 되는 길이다.
