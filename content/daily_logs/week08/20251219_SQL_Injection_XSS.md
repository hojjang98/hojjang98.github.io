---
title: "2025.12.19 (Day 39) 웹 해킹의 기초 - SQL Injection & XSS"
date: 2025-12-19
draft: false
tags: ["웹해킹", "SQLInjection", "XSS", "BurpSuite", "OWASP", "WebGoat", "보안관제", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "웹 해킹 방법론 복습 및 심화 - SQL Injection/XSS 공격 원리, OWASP Top 10, WAF 룰셋, 보안 설정 체크리스트"
---

# 📄 2025.12.19 (Day 39) - 웹 해킹의 기초

---

## 1. 핵심 개념 정리

### 해킹 기술의 진화

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 1 | 국내 해커 역사 | 1986년 KAIST '유니콘' 동아리로 시작. 1991년 '쿠스'와 '플러스' 해킹 전쟁 후 시큐리티카이스트 설립 | 해커 문화의 양면성: 기술 연구 vs 공격. 화이트햇 해커의 중요성 인식 계기 |
| 2 | 1990년대 해킹 | PC 통신(하이텔 등) 시절, 전화 모뎀 기반 시스템/네트워크 취약점 공격이 주류 | 당시는 물리적 접근이 필요했음. 네트워크 보안 개념 미흡 |
| 3 | 1990년대 후반 | 보안 회사 설립, 언더그라운드→오버그라운드 전환. 널루트, 와우해커 등 언더해커 그룹 등장 | 해킹이 산업화되는 시점. 모의해킹, 보안 컨설팅 시장 형성 |
| 4 | 2000년대 초 | 해킹왕중왕대회(2000, 2001년) 개최. truefinder, Xpl017Elz(X82) 등 유명 해커 등장 | 해킹 기술 경연 문화. 현재 CTF 대회의 전신 |
| 5 | 웹 해킹 발전 배경 | 1990년대 중반 방화벽/IDS 도입으로 네트워크 공격 어려워짐. 2000년대 중반 이후 80번 포트(웹)만 열려있는 환경 증가 | 방화벽이 웹 해킹을 촉진시킨 역설. 외부 접점이 웹으로 집중되면서 웹이 주요 공격 대상으로 부상 |

### 일반적인 웹 해킹 과정

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 6 | 해킹 프로세스 | ① 공격 대상 선정 → ② 정보 수집 → ③ 취약점 분석 → ④ 공격 → ⑤ Report/Defacement/흔적 제거 | Kill Chain의 웹 버전. SOC는 이 각 단계에서 탐지 포인트 마련 필요 |
| 7 | 공격 대상 선정 | 방문자 많은 대표 사이트 또는 모의해킹 계약 대상. 관련 도메인 모두 검색 후 가장 취약한 곳 선정 | 공격자는 비용 대비 효과를 고려. 보안 투자가 적은 서브도메인, 테스트 서버가 주요 타겟 |
| 8 | 웹 해킹 방법론 | 1) 취약점 발견 후 침투 시도 2) 공격 표면 매트릭스 작성 후 체계적 시도 | 모의해킹 시 두 번째 방법 사용. 방어자는 공격 표면 최소화가 핵심 |
| 9 | 과거 vs 현대 해킹 | 과거: 웹 페이지 변조(Defacement)로 명성 추구. 현대: 흔적 숨기고 지속적 접근 유지(APT) | 공격 목적 변화: 과시→금전적 이익/정보 탈취. 탐지 난이도 상승 |

### 정보 수집 기법

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 10 | 정보 수집 목적 | 웹 개발 언어, 웹 서버 종류/버전, 주요 공격 대상 기능, 취약한 표면 파악 | 공격의 80%는 정보 수집 단계. 방어자는 정보 노출 최소화가 최우선 |
| 11 | 자동화 도구 | Burp Suite: 프록시 기능으로 HTTP 트래픽 가로채기, Site Map으로 디렉터리 구조 파악 | 모든 웹 보안 실무자의 필수 도구. 요청/응답 조작으로 취약점 테스트 |
| 12 | 브라우저 도구 | F12 개발자 도구: HTML/CSS/JS 소스, 네트워크 탭에서 요청/응답 확인 | 가장 기본적인 정보 수집 방법. 클라이언트 측 검증 우회에 필수 |
| 13 | 검색 엔진 해킹 | Google Dork: site:, filetype:, intitle:, inurl:, link:, cache: 연산자 활용 | OSINT의 핵심. 공개 정보만으로 상당한 정보 수집 가능. 주의: 검색만 해도 로그에 남음 |
| 14 | 웹 스캐닝 도구 | Wikto, Nikto: 웹 서버 취약점, 디렉터리 정보, 중요 파일 존재 여부 자동 검사 | 현재는 많이 사용 안 하지만 원리 이해 필요. 현대에는 OWASP ZAP, Acunetix 등 사용 |

### Google Dork 검색 연산자

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 15 | site: | 특정 도메인/사이트 내에서만 검색. 예: site:co.kr admin | 특정 조직의 관리자 페이지 찾기. 서브도메인 발견에 유용 |
| 16 | filetype: | 특정 파일 타입 검색. 예: filetype:txt 관리자 | 설정 파일, 백업 파일, 문서 유출 확인. PDF, DOC, XLS 등도 검색 가능 |
| 17 | intitle: | 페이지 제목에 특정 문자열 포함. 예: intitle:index.of name size | 디렉터리 리스팅 취약점 찾기. "Index of /"는 파일 목록 노출 의미 |
| 18 | inurl: | URL에 특정 문자열 포함. 예: inurl:admin/login.asp .com | 로그인 페이지, 관리자 페이지 찾기. site:와 유사하지만 URL 구조 검색 |
| 19 | link: | 특정 링크가 포함된 페이지 검색. 예: link:korea.ac.kr | 백링크 분석. 연관 사이트 탐색 |
| 20 | cache: | 구글 캐시에 저장된 페이지 확인. 예: cache:korea.ac.kr | 삭제된 데이터 복구. 과거 정보 확인. 현재는 제한적 |

### OWASP Top 10 (2021년 버전)

| # | 취약점 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 21 | A1. 잘못된 접근 통제 | 접근 통제 로직 누락으로 인가되지 않은 기능/데이터 접근. 검사 애플리케이션의 3.81%가 해당 | IDOR, 권한 상승, 강제 브라우징 등. 모든 요청에서 인가 검증 필수 |
| 22 | A2. 암호화 오류 | 개인정보, 패스워드 등 민감 정보 평문 저장 또는 약한 암호화 | 데이터 유출 시 2차 피해. HTTPS, AES-256, bcrypt 등 강력한 암호화 필수 |
| 23 | A3. 인젝션 | SQL, OS 명령어, LDAP 등 외부 입력을 검증 없이 실행. DB 연동 부분에서 주로 발생 | SQL Injection이 대표적. Prepared Statement, ORM 사용으로 예방 |
| 24 | A4. 안전하지 않은 설계 | 2021년 신규 추가. 설계 단계부터 보안 고려 부족. 위협 모델링, 보안 패턴 적용 필요 | Secure by Design. 코딩 전에 보안 설계 검토 필수 |
| 25 | A5. 보안 설정 오류 | 기본 페이지 미삭제, 최신 패치 미적용, 디렉터리 리스팅 허용 등 | 가장 흔한 취약점. 정기적인 설정 점검, 하드닝 가이드 적용 |
| 26 | A6. 취약하거나 오래된 컴포넌트 | 워드프레스 플러그인, 라이브러리 등 구성 요소의 취약점. 데이터 손실, 서버 장악 가능 | 의존성 관리 중요. OWASP Dependency-Check, npm audit 등 도구 활용 |
| 27 | A7. 식별 및 인증 실패 | 세션 관리 오류, 쿠키 값 조작 가능, 약한 패스워드 정책 등 | 세션 고정, 무차별 대입 공격. MFA, 강력한 세션 관리 필수 |
| 28 | A8. 소프트웨어와 데이터 무결성 실패 | 무결성 확인 없이 소프트웨어 업데이트. CI/CD 파이프라인 보안 취약 | 공급망 공격. 서명 검증, 코드 서명 적용 |
| 29 | A9. 보안 로그 및 모니터링 실패 | 충분한 로그 미수집, 로그 분석 미흡. 침해사고 시 포렌식 불가 | SOC 관점에서 치명적. SIEM 연동, 실시간 모니터링 체계 구축 |
| 30 | A10. 서버 사이드 요청 변조(SSRF) | 서버가 공격자 의도대로 외부/내부 요청 수행. 2021년 신규 추가 | 내부망 스캔, 메타데이터 탈취(AWS IMDS 공격). URL 검증 필수 |

---

## 2. 실습 내용 정리

### 실습 2-1: Burp Suite로 웹 사이트 정보 수집하기

**목표:** HTTP 프록시를 통한 웹 애플리케이션 구조 파악

**실습 환경:**
- Burp Suite Community Edition
- Microsoft Edge (또는 Chrome)
- Windows 프록시 설정

**실습 단계:**
```bash
# 1. Burp Suite 실행
# [Proxy] - [Intercept] 탭 확인

# 2. Windows 프록시 설정
# [설정] - [네트워크 및 인터넷] - [프록시]
# 수동 프록시 설정:
#   - 주소: 127.0.0.1
#   - 포트: 8080

# 3. 브라우저에서 대상 웹사이트 접속
# 예: https://www.hanbit.co.kr

# 4. Burp Suite에서 Intercept Off 설정
# [Intercept is on] 클릭 → [Intercept is off]로 변경

# 5. [Target] - [Site map] 탭에서 탐색
# 방문한 페이지의 디렉터리 구조, 파일 목록, 파라미터 확인
```

**분석 포인트:**
```
디렉터리 구조 예시:
├── /
├── /images/
├── /css/
├── /js/
├── /api/
│   ├── /user
│   └── /product
├── /admin/        # ⚠️ 관리자 페이지 노출?
└── /backup/       # ⚠️ 백업 파일 노출?

확인 항목:
✓ URL 파라미터 (GET 방식 데이터 전달)
✓ 쿠키 구조 (세션 관리 방식)
✓ 응답 헤더 (Server, X-Powered-By 등)
✓ 숨겨진 디렉터리/파일
✓ API 엔드포인트
```

**보안 인사이트:**
- Site Map에서 /admin, /test, /dev 같은 경로 발견 시 접근 제어 확인 필요
- 쿠키에 HttpOnly, Secure 플래그 없으면 XSS 공격에 취약
- 응답 헤더에 서버 버전 정보 노출 시 알려진 취약점 악용 가능

### 실습 2-2: 웹 스캐닝으로 웹 사이트 정보 수집하기

**목표:** Wikto를 사용한 자동화된 취약점 스캐닝

**실습 환경:**
- Windows 10/11
- Wikto 7.1 (SensePost)
- 테스트 대상: 허가된 서버 또는 자체 구축 환경

**실습 단계:**
```bash
# 1. Wikto 다운로드 및 설치
# https://github.com/sensepost/wikto
# C:\Scanner\Wikto 폴더에 압축 해제

# 2. Wikto 실행
# [Start] - [All Programs] - [SensePost] - [Wikto]

# 3. Nikto Database 로드
# <Load Nikto Database> 클릭
# 취약점 데이터베이스 로드 (수천 개 항목)

# 4. 스캔 설정
# Target: http://localhost:8080 (또는 테스트 서버)
# Port: 80 (HTTP) 또는 443 (HTTPS)

# ⚠️ 주의사항: 본인 소유 또는 허가받은 서버만 스캔!
# 무단 스캔 시 정보통신망법 위반 (형사 처벌 가능)
```

**스캐닝 원리:**
```
Wikto 동작 방식:
1. HTTP Request 전송
   GET /admin/ HTTP/1.1
   GET /backup/ HTTP/1.1
   GET /test/ HTTP/1.1
   ... (데이터베이스에 등록된 수천 개 경로 시도)

2. Response Code 분석
   200 OK → 존재하는 리소스
   401 Unauthorized → 인증 필요 (존재 확인)
   403 Forbidden → 접근 거부 (존재 확인)
   404 Not Found → 존재하지 않음

3. 취약점 매칭
   알려진 취약점 패턴과 응답 비교
   CVE 번호 매핑
```

**발견 가능한 취약점:**
- 디렉터리 리스팅
- 기본 관리자 페이지
- 백업 파일 (.bak, .old, .backup)
- 설정 파일 (config.php, web.config)
- 오래된 버전의 웹 서버/프레임워크
- 알려진 CVE 취약점

**보안 고려사항:**
```
웹 스캐닝 탐지 패턴:
- 단시간 대량 404 에러 발생
- User-Agent: Nikto, Wikto 등 스캐너 시그니처
- 비정상적인 URL 패턴 (/../../etc/passwd)
- 동일 IP에서 순차적인 경로 접근

방어 방법:
→ WAF에 Rate Limiting 적용
→ 스캐너 User-Agent 차단
→ Fail2ban 설정 (특정 임계값 초과 시 IP 차단)
```

### 실습 2-3: WebGoat 설치하기

**목표:** OWASP WebGoat 취약점 학습 환경 구축

**실습 환경:**
- Windows 10/11
- Java Runtime Environment (JRE)
- WebGoat 7.1

**실습 단계:**
```bash
# 1. JRE 설치 확인
java -version
# 없으면 https://www.java.com 에서 설치

# 2. WebGoat 다운로드
# https://github.com/WebGoat/WebGoat/releases/tag/7.1
# webgoat-container-7.1-exec.jar 다운로드

# 3. 폴더 생성 및 파일 복사
C:\WebGoat7.1\webgoat-container-7.1-exec.jar

# 4. WebGoat 실행
cd C:\WebGoat7.1
java -jar webgoat-container-7.1-exec.jar

# 실행 성공 메시지:
# INFO - Browse to http://localhost:8080/WebGoat and happy hacking!

# 5. 브라우저로 접속
# http://localhost:8080/WebGoat
# Username: guest
# Password: guest
```

**WebGoat 구조:**
```
WebGoat 제공 학습 과정:
├── Introduction (소개)
├── General (일반 취약점)
│   ├── HTTP Basics
│   ├── HTTP Splitting
│   └── ...
├── Access Control (접근 제어)
│   ├── Bypass Business Layer
│   ├── LAB: Role Based Access Control
│   └── ...
├── AJAX Security (Ajax 보안)
├── Authentication Flaws (인증 취약점)
├── Code Quality (코드 품질)
├── Concurrency (동시성)
├── Cross-Site Scripting (XSS)
├── Improper Error Handling (오류 처리)
├── Injection Flaws (인젝션)
├── Insecure Communication (불안전한 통신)
├── Insecure Configuration (설정 오류)
├── Insecure Storage (저장소 보안)
├── Malicious Code (악성 코드)
├── Parameter Tampering (파라미터 변조)
├── Session Management (세션 관리)
└── Web Services (웹 서비스)
```

**학습 활용 방안:**
- 각 취약점별 실습 환경 제공
- 실제 취약한 코드와 공격 시나리오 학습
- Burp Suite와 연동하여 HTTP 트래픽 분석
- 모의해킹 연습 플랫폼으로 활용

**주의사항:**
```
⚠️ WebGoat는 의도적으로 취약하게 만든 교육용 애플리케이션입니다.

절대 금지:
✗ 공인 IP에 노출
✗ 방화벽 외부에서 접근 가능하게 설정
✗ 실제 운영 환경에 설치

권장 사항:
✓ localhost(127.0.0.1)에서만 실행
✓ 가상 머신(VMware, VirtualBox) 내 격리 환경에서 실습
✓ 실습 후 즉시 종료
```

---

## 3. 정보 수집 기법 비교표

### 정보 수집 도구 비교

| 도구 | 장점 | 단점 | 사용 시기 |
|:---:|:---|:---|:---|
| **Burp Suite** | - 수동 분석 가능<br>- HTTP 트래픽 상세 확인<br>- 요청/응답 조작 가능<br>- 프록시 기능으로 모든 통신 캡처 | - 수동 작업 필요<br>- 자동화 제한적<br>- Pro 버전은 유료 | 정밀 분석, 취약점 검증, 수동 침투 테스트 |
| **F12 개발자 도구** | - 브라우저 내장, 별도 설치 불필요<br>- 즉시 사용 가능<br>- JavaScript 디버깅 | - 기능 제한적<br>- 깊은 분석 어려움<br>- 프록시 기능 없음 | 빠른 소스 확인, 간단한 네트워크 분석 |
| **Google Dork** | - 광범위한 정보 수집<br>- 공개 정보만 활용 (합법)<br>- 서브도메인 발견에 유용 | - 최신 정보 아닐 수 있음<br>- 정확도 낮을 수 있음<br>- 검색 로그 남음 | 초기 OSINT, 공개 정보 조사, 도메인 발견 |
| **Wikto/Nikto** | - 자동화된 취약점 스캔<br>- 수천 개 경로 빠르게 확인<br>- CVE 매칭 | - 오탐(False Positive) 많음<br>- 탐지 쉬움(로그 대량 발생)<br>- 최신 취약점 누락 가능 | 초기 스캔, 알려진 취약점 확인, 대량 서버 점검 |

### Google Dork 실전 예시

| 검색어 | 발견 가능한 정보 | 보안 위험 |
|:---|:---|:---|
| `site:example.com filetype:pdf` | 조직의 공개 PDF 문서 (보고서, 제안서 등) | 민감 정보 유출 (이메일, 내부 구조, 프로젝트 정보) |
| `site:example.com inurl:admin` | 관리자 페이지 경로 | 인증 우회 시도 대상 발견 |
| `site:example.com intitle:"index of"` | 디렉터리 리스팅 노출 사이트 | 백업 파일, 설정 파일 다운로드 가능 |
| `site:example.com filetype:sql` | 데이터베이스 덤프 파일 | DB 스키마, 사용자 정보 노출 |
| `site:example.com inurl:login.php` | 로그인 페이지 목록 | 무차별 대입 공격 대상 |
| `site:example.com ext:log` | 로그 파일 노출 | 시스템 정보, 경로, 에러 메시지 노출 |

---

## 4. OWASP Top 10 심화 분석

### 2013 vs 2017 vs 2021 변화 추이

| 순위 | 2013년 | 2017년 | 2021년 | 분석 |
|:---:|:---|:---|:---|:---|
| A1 | 인젝션 취약점 | 인젝션 | **잘못된 접근 통제** | 접근 제어 문제가 1위로 급상승. 클라우드/API 시대에 권한 관리 중요성 증가 |
| A2 | 인증 및 세션 관리 취약점 | 잘못된 인증 | **암호화 오류** | 개인정보 보호 규제(GDPR, 개인정보보호법) 강화 반영 |
| A3 | XSS | 민감한 데이터 노출 | **인젝션** | 인젝션이 3위로 하락. Prepared Statement 등 방어 기법 보편화 |
| A4 | 취약한 직접 객체 참조 | XXE | **안전하지 않은 설계** | 2021년 신규. Secure SDLC, Threat Modeling 중요성 |
| A5 | 보안 설정 오류 | 잘못된 접근 통제 | **보안 설정 오류** | 여전히 Top 5. 설정 오류는 계속되는 문제 |
| A6 | 민감한 데이터 노출 | 보안 설정 오류 | **취약한 컴포넌트** | 오픈소스 사용 증가로 의존성 관리 이슈 부각 |
| A7 | 기능 수준의 접근 통제 누락 | XSS | **식별 및 인증 실패** | 세션 관리, 패스워드 정책 등 지속적 문제 |
| A8 | CSRF | 안전하지 않은 역직렬화 | **데이터 무결성 실패** | 2021년 신규. 공급망 공격, CI/CD 보안 중요성 |
| A9 | 알려진 취약점 컴포넌트 | 알려진 취약점 컴포넌트 | **로그 및 모니터링 실패** | 침해사고 대응 관점에서 중요성 인식 |
| A10 | 검증되지 않은 리다이렉트 | 불충분한 로깅/모니터링 | **SSRF** | 2021년 신규. 클라우드 환경에서 메타데이터 탈취 위험 |

### OWASP Top 10 공격 시나리오 예시
```python
# A1. 잘못된 접근 통제 - IDOR(Insecure Direct Object Reference)
# 취약한 코드:
https://bank.com/account?id=1234
# 공격: id 파라미터 변조
https://bank.com/account?id=5678
# 결과: 다른 사용자의 계좌 정보 조회

# A3. 인젝션 - SQL Injection
# 취약한 코드:
query = "SELECT * FROM users WHERE id = '" + user_input + "'"
# 공격:
user_input = "1' OR '1'='1"
# 실제 쿼리:
"SELECT * FROM users WHERE id = '1' OR '1'='1'"
# 결과: 모든 사용자 정보 반환

# A7. 식별 및 인증 실패 - 세션 고정 공격
# 1. 공격자가 자신의 세션 ID를 피해자에게 전달
https://victim.com/login?sessionid=attacker_session
# 2. 피해자가 해당 링크로 로그인
# 3. 공격자가 동일한 세션 ID로 인증된 상태 접근

# A10. SSRF - AWS 메타데이터 탈취
# 취약한 코드:
url = request.GET['url']
response = requests.get(url)
# 공격:
url = http://169.254.169.254/latest/meta-data/iam/security-credentials/
# 결과: AWS IAM 자격 증명 탈취
```

---

## 5. 실무/보안 적용

### SOC 분석가 관점 - 웹 공격 탐지 포인트

| 공격 단계 | 탐지 포인트 | 로그 예시 | 대응 방안 |
|:---:|:---|:---|:---|
| **정보 수집** | - 단시간 대량 404 에러<br>- /admin, /backup 등 민감 경로 접근<br>- OPTIONS 메서드 사용 | `192.168.1.100 - [19/Dec/2024:10:23:45] "GET /admin/ HTTP/1.1" 404`<br>`192.168.1.100 - [19/Dec/2024:10:23:46] "GET /backup/ HTTP/1.1" 404` | - Rate Limiting 적용<br>- 스캐너 User-Agent 차단<br>- IP 임시 차단 |
| **취약점 스캔** | - Nikto, Wikto User-Agent<br>- 비정상 URL 패턴 (../, %00 등)<br>- 대량 파라미터 조합 시도 | `User-Agent: Nikto/2.1.6`<br>`GET /../../../etc/passwd HTTP/1.1` | - WAF 시그니처 업데이트<br>- 비정상 패턴 차단 룰 적용 |
| **인젝션 시도** | - SQL 키워드 (UNION, SELECT 등)<br>- XSS 페이로드 (`<script>`, `onerror=` 등)<br>- 500 에러 급증 | `GET /search?q='+OR+1=1-- HTTP/1.1`<br>`POST /comment data=<script>alert(1)</script>` | - Prepared Statement 강제<br>- 입력 검증 강화<br>- WAF 차단 |
| **권한 상승** | - 파라미터 변조 (id=1 → id=2)<br>- 숨겨진 필드 조작 (role=user → role=admin)<br>- 403 이후 200 응답 | `GET /account?id=5678 (다른 사용자 ID)` | - 세션 기반 권한 검증<br>- 로그 상관 분석<br>- 이상 행위 알림 |
| **지속성 확보** | - 웹셸 업로드 (.php, .jsp, .aspx)<br>- cron/scheduled task 등록<br>- 백도어 계정 생성 | `POST /upload file=shell.php`<br>`새 계정 생성: admin2 (관리자 그룹)` | - 파일 업로드 제한<br>- 파일 무결성 모니터링<br>- 계정 생성 알림 |

### 웹 방화벽(WAF) 룰셋 예시
```bash
# ModSecurity Core Rule Set (CRS) 예시

# SQL Injection 탐지
SecRule ARGS "@rx (union|select|insert|update|delete|drop|;|--|\/\*|\*\/)" \
    "id:1001,phase:2,deny,status:403,msg:'SQL Injection Attempt'"

# XSS 탐지
SecRule ARGS "@rx (<script|javascript:|onerror=|onload=|<img|<iframe)" \
    "id:1002,phase:2,deny,status:403,msg:'XSS Attempt'"

# Path Traversal 탐지
SecRule REQUEST_URI "@rx (\.\./|\.\.\\)" \
    "id:1003,phase:1,deny,status:403,msg:'Path Traversal Attempt'"

# Command Injection 탐지
SecRule ARGS "@rx (;|\||`|\$\(|&&)" \
    "id:1004,phase:2,deny,status:403,msg:'Command Injection Attempt'"

# 파일 업로드 제한 (PHP 웹셸)
SecRule FILES "@rx \.(php|phtml|php3|php4|php5|phps|phar)$" \
    "id:1005,phase:2,deny,status:403,msg:'Malicious File Upload'"

# 스캐너 User-Agent 차단
SecRule REQUEST_HEADERS:User-Agent "@rx (nikto|wikto|nmap|sqlmap|burp)" \
    "id:1006,phase:1,deny,status:403,msg:'Scanner Detected'"

# Rate Limiting (동일 IP에서 10초에 100회 이상 요청)
SecAction "id:1007,phase:1,nolog,pass,initcol:ip=%{REMOTE_ADDR}"
SecRule IP:REQUEST_COUNT "@gt 100" \
    "id:1008,phase:1,deny,status:429,msg:'Rate Limit Exceeded'"
SecAction "id:1009,phase:5,pass,setvar:ip.request_count=+1,expirevar:ip.request_count=10"
```

### 보안 설정 체크리스트
```bash
# 웹 서버 보안 설정 (Nginx 예시)

# 1. 서버 정보 숨기기
server_tokens off;
more_clear_headers 'Server';
more_clear_headers 'X-Powered-By';

# 2. 불필요한 HTTP 메서드 차단
if ($request_method !~ ^(GET|POST|HEAD)$) {
    return 405;
}

# 3. 디렉터리 리스팅 비활성화
autoindex off;

# 4. HTTPS 리다이렉션
server {
    listen 80;
    return 301 https://$host$request_uri;
}

# 5. 보안 헤더 추가
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'" always;

# 6. 쿠키 보안 플래그
proxy_cookie_flags ~ secure httponly samesite=strict;

# 7. 파일 업로드 제한
location /upload {
    client_max_body_size 10M;
    if ($request_filename ~* \.(php|phtml|php3|php4|php5|phps|phar)$) {
        return 403;
    }
}

# 8. 민감 경로 접근 제어
location ~ /(admin|config|backup) {
    allow 192.168.1.0/24;  # 내부 IP만 허용
    deny all;
    auth_basic "Restricted Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

---

## 6. 배운 점 및 인사이트

### 새로 알게 된 점

- **웹 해킹의 역사적 맥락:** 방화벽과 IDS가 도입되면서 역설적으로 웹 해킹이 발전했다는 점이 흥미롭다. 네트워크 공격이 어려워지자 80번 포트로 공격이 집중된 것.
- **정보 수집의 중요성:** 실제 공격의 80%가 정보 수집 단계. Burp Suite, Google Dork, 웹 스캐너 등 다양한 도구를 조합하면 놀라울 정도로 많은 정보 획득 가능.
- **OWASP Top 10의 변화:** 시대에 따라 취약점 트렌드가 변한다. 2021년 "안전하지 않은 설계", "SSRF"가 신규 추가된 것은 클라우드 환경과 공급망 공격을 반영한 것.
- **Google Dork의 위력:** 검색 연산자만으로도 관리자 페이지, 백업 파일, 민감 문서를 찾을 수 있다. 공개 정보 관리의 중요성 실감.
- **WebGoat의 교육적 가치:** 안전하게 웹 취약점을 실습할 수 있는 환경. 공격자 관점을 이해해야 방어할 수 있다는 점에서 모든 보안 직무 종사자에게 필수.

### 이전 학습과의 연결고리

- **인터넷과 웹의 이해와 연계:** HTTP 프로토콜, 메서드, 상태 코드를 이해했기에 웹 공격 원리 파악이 수월했다. 특히 500 에러가 SQL Injection 탐지 신호가 된다는 연결고리.
- **Burp Suite 실습 확장:** 이전에는 HTTP 패킷 분석에 집중했다면, 오늘은 Site Map을 통한 디렉터리 탐색, 취약점 발견으로 확장.
- **네트워크 보안 → 웹 보안 전환:** 방화벽, IDS 같은 네트워크 보안 장비가 웹 해킹 발전의 촉매제가 되었다는 역사적 맥락. 방어 수단이 새로운 공격 벡터를 만든 아이러니.

### 실무 적용 아이디어

**SOC 분석가 관점:**
- **웹 공격 탐지 시나리오 작성:** 정보 수집 → 스캔 → 공격 → 권한 상승 → 지속성 확보 단계별 탐지 룰 개발. 특히 스캐너 User-Agent, 대량 404 에러 패턴 모니터링.
- **로그 상관 분석:** 동일 IP에서 /admin, /backup 접근 시도 후 500 에러 발생 → SQL Injection 의심. 이런 패턴을 SIEM 룰로 구현.
- **정보 노출 사전 점검:** 정기적으로 자사 도메인에 Google Dork 적용하여 민감 정보 노출 여부 확인. `site:company.com filetype:pdf` 같은 검색으로 유출된 문서 탐지.

**보안 컨설턴트 관점:**
- **모의해킹 방법론:** 오늘 배운 정보 수집 기법(Burp Suite, Google Dork, 웹 스캐너)을 체계화하여 모의해킹 초기 단계 프로세스로 활용.
- **OWASP Top 10 기반 점검:** 고객사 웹 애플리케이션 점검 시 OWASP Top 10을 체크리스트로 사용. 특히 2021년 신규 항목(안전하지 않은 설계, SSRF)은 최신 트렌드 반영.

---

## 7. Quick Reference

### 정보 수집 도구 명령어 모음
```bash
# Burp Suite 프록시 설정
# 브라우저 프록시: 127.0.0.1:8080
# Intercept Off로 설정 후 Site Map 확인

# Google Dork 예시
site:example.com admin
site:example.com filetype:pdf
site:example.com inurl:login
site:example.com intitle:"index of"
site:example.com ext:sql

# Wikto/Nikto 스캔
nikto -h http://target.com -Tuning 1234567890
wikto -h target.com -p 80

# cURL로 응답 헤더 확인
curl -I https://example.com
curl -v https://example.com

# Nmap으로 웹 서버 정보 수집
nmap -p 80,443 --script http-headers target.com
nmap -p 80,443 --script http-methods target.com
```

### OWASP Top 10 (2021) 요약표

| 순위 | 취약점 | 핵심 키워드 | 대표 공격 | 방어 방법 |
|:---:|:---|:---|:---|:---|
| A1 | 잘못된 접근 통제 | IDOR, 권한 상승 | URL 파라미터 변조 | 세션 기반 권한 검증, 최소 권한 원칙 |
| A2 | 암호화 오류 | 평문 저장, 약한 암호화 | DB 덤프 후 패스워드 크랙 | AES-256, bcrypt, TLS 1.2+ |
| A3 | 인젝션 | SQL Injection, Command Injection | `' OR '1'='1` | Prepared Statement, ORM, 입력 검증 |
| A4 | 안전하지 않은 설계 | Secure SDLC, Threat Modeling | 설계 단계 보안 누락 | 보안 설계 패턴, 위협 모델링 |
| A5 | 보안 설정 오류 | 기본 설정, 패치 미적용 | 디렉터리 리스팅, 정보 노출 | 보안 하드닝, 정기 점검 |
| A6 | 취약한 컴포넌트 | 오래된 라이브러리, 플러그인 | 워드프레스 플러그인 취약점 | 의존성 관리, 정기 업데이트 |
| A7 | 식별 및 인증 실패 | 세션 고정, 약한 패스워드 | 세션 하이재킹, 무차별 대입 | MFA, 강력한 세션 관리 |
| A8 | 데이터 무결성 실패 | 무결성 검증 부재 | 공급망 공격, 변조된 업데이트 | 코드 서명, CI/CD 보안 |
| A9 | 로그/모니터링 실패 | 로그 미수집, 분석 미흡 | 침해사고 탐지 지연 | SIEM 연동, 실시간 모니터링 |
| A10 | SSRF | 서버 요청 변조 | AWS 메타데이터 탈취 | URL 검증, 화이트리스트 |

### 웹 보안 점검 체크리스트

**서버 설정:**
- [ ] 서버 정보(Server, X-Powered-By) 헤더 제거
- [ ] 불필요한 HTTP 메서드(TRACE, OPTIONS, PUT, DELETE) 비활성화
- [ ] 디렉터리 리스팅 비활성화
- [ ] 에러 페이지 커스터마이징 (상세 오류 메시지 숨김)
- [ ] 최신 보안 패치 적용

**HTTPS 설정:**
- [ ] TLS 1.2 이상 강제
- [ ] HSTS 헤더 설정
- [ ] HTTP → HTTPS 리다이렉션
- [ ] 인증서 체인 확인

**쿠키 보안:**
- [ ] HttpOnly 플래그 설정
- [ ] Secure 플래그 설정 (HTTPS 전용)
- [ ] SameSite 속성 설정 (CSRF 방어)
- [ ] 쿠키 유효 기간 적절히 설정

**입력 검증:**
- [ ] 서버 측 입력 검증 (클라이언트 측만 의존하지 않음)
- [ ] 화이트리스트 방식 적용
- [ ] SQL Injection 방어 (Prepared Statement)
- [ ] XSS 방어 (입력 이스케이핑, CSP)

**접근 제어:**
- [ ] 관리자 페이지 IP 제한
- [ ] 세션 기반 권한 검증
- [ ] 민감한 경로(/admin, /config) 접근 로그 모니터링
- [ ] 파일 업로드 제한 (확장자, 크기)

**모니터링:**
- [ ] 웹 접근 로그 수집
- [ ] 에러 로그 수집 및 분석
- [ ] 이상 패턴 탐지 (대량 404, 스캐너 User-Agent)
- [ ] SIEM 연동

---

## 8. 트러블슈팅

| 문제 | 원인 | 해결 방법 |
|:---|:---|:---|
| Burp Suite 프록시 연결 안 됨 | 브라우저 프록시 설정 오류 또는 Burp Suite 미실행 | - Windows 프록시 설정 확인 (127.0.0.1:8080)<br>- Burp Suite에서 Proxy Listener 활성화 확인<br>- 방화벽에서 8080 포트 허용 |
| HTTPS 사이트 접속 시 인증서 경고 | Burp Suite CA 인증서 미신뢰 | - Burp Suite에서 CA 인증서 내보내기<br>- 브라우저에 CA 인증서 등록 (신뢰할 수 있는 루트 인증 기관) |
| Wikto 실행 시 "Nikto database not found" | Nikto 데이터베이스 미로드 | - <Load Nikto Database> 버튼 클릭<br>- nikto_db.txt 파일 경로 확인 |
| WebGoat 실행 시 "Address already in use" | 8080 포트가 이미 사용 중 | - `netstat -ano \| findstr :8080`으로 프로세스 확인<br>- 해당 프로세스 종료 또는 다른 포트로 실행<br>- `java -jar webgoat-container-7.1-exec.jar --server.port=9090` |
| Google Dork 검색 결과 없음 | 검색어 오타 또는 최근 크롤링 안 됨 | - 검색어 재확인<br>- cache: 연산자로 과거 데이터 확인<br>- Wayback Machine 활용 |
| 웹 스캔 시 403 Forbidden 대량 발생 | WAF 또는 Rate Limiting 작동 | - 스캔 속도 낮추기 (Delay 설정)<br>- User-Agent 변경<br>- IP 주소 변경 (프록시 사용) |

---

**Today's Insight:**

웹 보안의 핵심은 "정보 노출 최소화"와 "공격 표면 축소"다. 공격자는 정보 수집 단계에서 80%의 시간을 쏟는다. 서버 정보 헤더, 디렉터리 리스팅, Google에 색인된 민감 파일 등 작은 정보 하나하나가 공격의 실마리가 된다. 방어자는 공격자의 정보 수집 방법을 이해하고, 같은 도구로 자사 시스템을 점검해야 한다. 공격자보다 먼저 취약점을 찾아 막는 것이 최선의 방어다. Burp Suite와 Google Dork를 능숙하게 다루는 것은 공격자의 언어를 배우는 것과 같다.
