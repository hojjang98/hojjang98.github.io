---
title: "2025.12.16 (Day 36) - 인터넷과 웹의 이해"
date: 2025-12-16
draft: false
tags: ["웹", "HTTP", "인터넷", "Burp-Suite", "보안헤더", "HTTPS", "RFC"]
categories: ["daily-logs"]
summary: "인터넷/웹의 역사와 구조, HTTP 메서드/상태코드 분석, Burp Suite를 이용한 HTTP 패킷 분석 실습, 웹 서버 보안 헤더 설정"
---

# 📄 2025.12.16 (Day 36) - 인터넷과 웹의 이해

---

## 1. 핵심 개념 정리

### 인터넷의 탄생과 발전

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| **1** | **ARPANET** | 1969년 10월 29일 미국 국방부 산하 ARPA의 연구용 네트워크. UCLA에서 스탠퍼드대 SRI 연구소로 최초 메시지 전송 성공 | 인터넷의 시초. 초기에는 군사 목적이었으나 점차 학술, 민간으로 확대. 분산 네트워크 개념이 현대 보안 아키텍처의 기반 |
| **2** | **TCP/IP 프로토콜** | ARPANET이 일반에 공개되면서 채택된 통신 규약. 인터넷의 표준 프로토콜로 자리잡음 | 모든 인터넷 통신의 기초. 보안 취약점 분석의 출발점. 패킷 구조와 헤더 정보를 이해해야 네트워크 공격/방어 가능 |
| **3** | **한국 인터넷 역사** | 1982년 서울대-KIET 간 TCP/IP로 SDN 시작, 1994년 한국통신이 코넷(KORNET)으로 일반 개방 | 한국의 인터넷 인프라 발전 과정. 초기 학술망에서 상용 인터넷으로 전환되는 역사적 맥락 이해 |

### 인터넷 프로토콜과 표준

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| **4** | **프로토콜 3요소** | 구문(Syntax): 데이터 형식, 의미(Semantics): 오류 제어, 순서(Timing): 통신 속도/순서 | 프로토콜 분석 시 이 세 가지 관점에서 접근. 취약점은 대부분 구문 검증 미흡이나 순서 제어 오류에서 발생 |
| **5** | **RFC 문서** | IETF에서 발행하는 인터넷 기술 표준 문서. TCP는 RFC 793, HTTP/1.0은 RFC 1945에 정의 | 프로토콜 동작 원리를 정확히 이해하려면 RFC 원문 참조 필수. 보안 취약점 연구 시 표준 명세와 실제 구현의 차이 분석 |
| **6** | **TCP/IP** | 가장 널리 사용되는 프로토콜. 신뢰성 있는 연결 지향 통신 제공 | 3-way handshake, 4-way termination 과정 이해 필요. SYN Flooding 같은 TCP 기반 공격의 원리 파악에 필수 |

### 인터넷 거버넌스 기구

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| **7** | **ICANN** | 인터넷 주소 관리 기구. 도메인 이름, DNS, IP 주소, 프로토콜 번호 관리 | 도메인 하이재킹, DNS 스푸핑 등 공격 이해의 배경 지식. 도메인 보안 정책 수립 시 참조 |
| **8** | **IANA** | 인터넷 할당 번호 관리 기관. DNS Root Zone 관리가 핵심 기능 | DNS 계층 구조의 최상위. DNS 관련 보안 이슈(DNS 터널링, 캐시 포이즈닝) 분석 시 필수 |
| **9** | **IETF** | 인터넷 표준화 기구. 프로토콜과 구조적 사안 분석 및 RFC 문서 발행 | 새로운 프로토콜의 보안 메커니즘 확인. 보안 프로토콜(TLS, IPSec 등) 표준 동향 파악 |
| **10** | **W3C** | 웹 기술 표준화 기구. HTML, CSS, 웹 API 등 웹 표준 제정 | 웹 보안 표준(CSP, CORS 등) 제정 주체. XSS, CSRF 같은 웹 공격 방어 메커니즘의 표준화 |
| **11** | **ITU** | UN 산하 국제 전기통신 연합. 통신 기술 표준과 정책 수립 | 국가 간 사이버 보안 협력 체계. 통신 보안 규제 및 국제 표준 이해 |

### 웹의 탄생과 발전

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| **12** | **WWW 탄생** | 1989년 팀 버너스 리가 CERN에서 정보 공유 목적으로 제안. 1991년 일반 공개, 로열티 포기로 급속 확산 | 웹의 개방성이 보안 취약점의 근본 원인. 초기 설계 시 보안보다 접근성에 초점을 둔 역사적 배경 |
| **13** | **URL, HTTP, HTML** | 웹의 3대 핵심 기술. 1990년에 차례로 설계됨 | 웹 보안의 기본 단위. URL 조작, HTTP 헤더 변조, HTML 인젝션 등 모든 웹 공격의 대상 |
| **14** | **하이퍼텍스트** | 링크를 통해 문서 간 이동하는 비선형 텍스트 구조 | 하이퍼링크를 악용한 피싱, 오픈 리다이렉트 취약점의 기본 원리 |
| **15** | **웹 브라우저 발전** | 초기 텍스트 중심에서 멀티미디어, 동적 콘텐츠 지원으로 진화 | 브라우저 취약점(Sandbox 우회, XSS, CSRF)이 주요 공격 벡터. Same-Origin Policy 같은 브라우저 보안 모델 이해 필요 |

### HTTP 프로토콜

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| **16** | **HTTP 버전** | HTTP/0.9(읽기만), HTTP/1.0(GET/POST/HEAD), HTTP/1.1(8가지 메서드) | 버전별 보안 특성 차이. HTTP/1.1의 Keep-Alive는 성능 향상이지만 Slowloris 공격에 악용 가능 |
| **17** | **HTTP 메서드** | GET(조회), POST(전송), PUT(수정), DELETE(삭제), HEAD, OPTIONS, TRACE, CONNECT | REST API 보안 설계의 기초. TRACE 메서드는 XST 공격에 악용 가능하여 비활성화 권장 |
| **18** | **HTTP Request** | 메서드, URL, 버전, 헤더(Host, User-Agent, Cookie 등), 바디로 구성 | User-Agent 변조, Cookie 탈취, Referer 조작 등 헤더 기반 공격 이해. GET은 URL에 파라미터 노출 |
| **19** | **HTTP Response** | 상태 코드, 헤더, 바디로 구성. 200(성공), 404(Not Found), 500(서버 오류) 등 | 상태 코드 기반 정보 수집. 500 에러는 SQL Injection 탐지에 활용. 응답 헤더에서 서버 정보 노출 주의 |
| **20** | **HTTP 상태 코드** | 1xx(정보), 2xx(성공), 3xx(리다이렉션), 4xx(클라이언트 오류), 5xx(서버 오류) | 비정상 응답 패턴 분석으로 취약점 탐지. 403은 접근 제어, 401은 인증 실패 의미 |

### 웹 애플리케이션 기술

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| **21** | **서버 측 스크립트** | PHP, Node.js, Python, ASP, JSP 등. 동적 웹 페이지 생성 | 코드 인젝션, 파일 업로드 취약점 등 서버 측 공격 대상. 소스코드 노출 시 치명적 |
| **22** | **웹 서버** | Nginx, Apache, IIS. 정적 콘텐츠 제공 및 애플리케이션 서버 연동 | 웹 서버별 설정 오류(디렉터리 리스팅, 불필요한 메서드 허용) 점검 필요. 버전 정보 노출 주의 |
| **23** | **데이터베이스** | MySQL, PostgreSQL, MSSQL, Oracle 등 DBMS | SQL Injection 공격의 직접 타깃. 최소 권한 원칙, Prepared Statement 사용 필수 |
| **24** | **클라이언트 측 기술** | HTML5, JavaScript. 브라우저에서 실행되는 코드 | XSS 공격의 주요 수단. 클라이언트 측 검증은 우회 가능하므로 서버 측 재검증 필수 |
| **25** | **GET vs POST** | GET은 URL에 파라미터, POST는 바디에 데이터 전송 | GET은 로그에 남고 브라우저 히스토리에 저장되어 민감 정보 노출 위험. 중요 작업은 POST 사용 |

---

## 2. 실습 내용

### 실습 1-1: TCP/IP의 RFC 문서 살펴보기

**목표:** RFC 문서 구조 이해 및 TCP 표준 문서 확인

1. IETF RFC 목록 페이지 접속 (ietf.org/rfc)
2. rfc-index.txt 파일 확인 - RFC 문서 번호, 제목, 최종 수정일 확인 가능
3. "Transmission Control Protocol" 검색:
   - RFC 0761: DoD standard Transmission Control Protocol (비표준)
   - RFC 0793: Transmission Control Protocol (INTERNET STANDARD)
4. rfc793.txt.pdf 파일 열람 - TCP 프로토콜의 상세 명세 확인

**핵심 포인트:**
- RFC 문서는 인터넷 기술의 공식 표준 명세서
- TCP는 RFC 793에 표준으로 등록
- 프로토콜 동작 원리를 정확히 이해하려면 RFC 원문 참조 필수

---

### 실습 1-2: 초창기의 웹 사이트 살펴보기

**목표:** 인터넷 아카이브를 통해 웹의 발전 과정 확인

1. Internet Archive (archive.org) 접속
2. Wayback Machine에서 www.daum.net 검색 - 1998년 11월 11일부터 아카이빙 기록 확인
3. 특정 연도(예: 1999년 2월) 선택하여 과거 사이트 확인

**관찰 내용:**
- 초기 웹사이트는 단순한 텍스트와 링크 위주
- 그래픽이 제한적이고 레이아웃이 단순함
- 현대 웹과 비교하여 보안 기능(HTTPS, CSRF 토큰 등)이 부재

**보안 관점:**
- 과거 웹사이트 구조 분석으로 레거시 시스템 취약점 이해
- 오래된 웹 아카이브에서 노출된 정보로 인한 정보 유출 가능성

---

### 실습 1-3: 웹 프록시를 이용해 HTTP 패킷 분석하기

**목표:** Burp Suite를 사용하여 HTTP Request/Response 패킷 실시간 분석

**환경 구성:**
1. JRE (Java Runtime Environment) 설치
2. Burp Suite Community Edition 다운로드 및 설치 (portswigger.net)
3. Burp Suite 실행 - Proxy -> Intercept -> Intercept is on
4. 브라우저 프록시 설정: 주소 127.0.0.1, 포트 8080

**HTTP Request 주요 헤더:**
- Host: www.hanbit.co.kr - 요청 대상 서버
- User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) - 브라우저/OS 정보
- Accept: text/html,application/xhtml+xml,\*/\* - 허용 컨텐츠 타입
- Cookie: session=abc123 - 세션 정보
- Connection: Keep-Alive

**HTTP Response 주요 헤더:**
- HTTP/1.1 200 OK
- Server: Apache/2.4.41 - 웹 서버 정보 (노출 주의)
- Content-Type: text/html; charset=UTF-8
- Set-Cookie: PHPSESSID=xyz789; path=/ - 쿠키 설정

**분석 포인트:**
- Request 헤더: User-Agent, Cookie, Referer 등 중요 정보 확인
- Response 헤더: Server 정보, Set-Cookie, Content-Type 확인
- 상태 코드: 200(정상), 302(리다이렉트), 404(없음), 500(서버 오류)

**보안 활용:**
- 쿠키 변조로 세션 하이재킹 시도 가능 여부 확인
- 응답 헤더에서 서버 버전 정보 노출 확인
- SQL Injection 시도 시 500 에러 발생 여부로 취약점 판단

---

## 3. HTTP 메서드 및 상태 코드 정리

### HTTP 메서드

| 메서드 | 설명 | 보안 고려사항 |
|:---:|:---|:---|
| GET | 리소스 조회, URL에 파라미터 노출 | 민감 정보 노출 위험, 로그에 기록됨 |
| POST | 데이터 전송, Body에 파라미터 포함 | GET보다 안전하지만 암호화 없으면 스니핑 가능 |
| PUT | 리소스 생성/수정 | 파일 업로드 취약점, 권한 검증 필수 |
| DELETE | 리소스 삭제 | 인증/인가 철저히 검증 필요 |
| HEAD | 헤더 정보만 조회 | 정보 수집 단계에서 사용 |
| OPTIONS | 지원 메서드 확인 | CORS 설정 확인, 불필요한 메서드 노출 주의 |
| TRACE | 요청 메시지 루프백 | XST 공격 가능, 비활성화 권장 |
| CONNECT | 프록시 터널링 | SSRF 공격에 악용 가능 |

### HTTP 상태 코드

| 코드 | 의미 | 보안 관점 |
|:---:|:---|:---|
| 200 OK | 요청 성공 | 정상 응답 |
| 301 Moved Permanently | 영구 리다이렉션 | 오픈 리다이렉트 취약점 점검 |
| 302 Found | 임시 리다이렉션 | 피싱 사이트로 유도 가능 |
| 400 Bad Request | 잘못된 요청 | 입력 검증 오류 |
| 401 Unauthorized | 인증 필요 | 인증 메커니즘 확인 |
| 403 Forbidden | 접근 거부 | 권한 검증 작동, 우회 시도 필요 |
| 404 Not Found | 리소스 없음 | 디렉터리 구조 탐색에 활용 |
| 500 Internal Server Error | 서버 오류 | SQL Injection 등 공격 탐지 신호 |
| 502 Bad Gateway | 게이트웨이 오류 | 백엔드 서버 문제 |
| 503 Service Unavailable | 서비스 불가 | DoS 공격 결과일 수 있음 |

---

## 4. 실무/보안 적용

### SOC 관점 활용 시나리오

| 상황 | 적용 방법 | 기대 효과 |
|:---:|:---|:---|
| **웹 공격 탐지** | HTTP 로그 분석으로 비정상 패턴 탐지 (SQL Injection 시도는 500 에러, XSS는 특정 스크립트 패턴) | 실시간 공격 탐지 및 차단 |
| **세션 하이재킹 모니터링** | 동일 세션 ID의 IP 주소 변경, User-Agent 변경 패턴 탐지 | 계정 탈취 조기 발견 |
| **정보 수집 단계 탐지** | OPTIONS, TRACE 메서드 사용, 디렉터리 스캐닝(404 대량 발생) 패턴 | 공격 초기 단계 차단 |
| **서버 취약점 분석** | 응답 헤더의 Server, X-Powered-By 정보로 버전 파악, CVE 매칭 | 사전 패치 적용 |

### 웹 방화벽(WAF) 주요 탐지 패턴

- **SQL Injection 패턴**: union, select, insert, update, delete, drop, 세미콜론, 주석(--) 포함 요청 -> 403 차단
- **XSS 패턴**: script 태그, javascript: 프로토콜, onerror=, onload= 이벤트 -> 403 차단
- **디렉터리 탐색 차단**: ../ (Path Traversal) 패턴 -> 403 차단
- **불필요한 HTTP 메서드 차단**: GET, POST, HEAD 외 메서드 -> 405 차단

### 보안 응답 헤더 설정

- **Server: webserver** - 실제 서버 정보 숨기기
- **X-XSS-Protection: 1; mode=block** - XSS 방어
- **X-Frame-Options: DENY** - 클릭재킹 방어
- **X-Content-Type-Options: nosniff** - MIME 스니핑 방지
- **Strict-Transport-Security: max-age=31536000; includeSubDomains** - HTTPS 강제
- **Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'** - CSP 설정

---

## 5. 배운 점 및 심화 방향

- **배운 점**: 인터넷과 웹은 다른 개념이다. 인터넷은 네트워크 인프라이고, 웹은 인터넷 위에서 동작하는 하나의 서비스다. TCP/IP 같은 프로토콜이 RFC 문서로 공개 표준화되어 있다는 점이 놀라웠다. 누구나 접근 가능하기에 공격자도 표준 명세를 보고 취약점을 연구할 수 있다. HTTP는 stateless 프로토콜이기 때문에 세션 관리를 위해 쿠키가 필수적이다. 이것이 세션 하이재킹의 근본 원인이다. GET과 POST의 차이가 단순히 파라미터 위치가 아니라 보안 측면에서 중요한 의미를 갖는다는 것을 이해했다. Burp Suite 같은 프록시 도구로 HTTP 트래픽을 중간에서 가로채고 조작할 수 있다는 사실이 웹 보안의 취약성을 실감하게 했다.
- **심화 방향**: SOC 분석가는 HTTP 로그 분석이 핵심 업무다. 상태 코드 패턴, User-Agent 변조, 비정상 요청 빈도 등을 모니터링해야 한다. Burp Suite 같은 프록시 도구 사용 능력은 모의해킹팀뿐만 아니라 SOC 분석가에게도 필수다. 공격자의 관점에서 웹 애플리케이션을 볼 수 있어야 한다.

---

## 6. Quick Reference

### 자주 사용하는 HTTP 헤더

**Request 헤더:**
- **Host**: www.example.com - 요청 대상 서버
- **User-Agent**: Mozilla/5.0 ... - 브라우저/OS 정보
- **Accept**: text/html,application/json - 받을 수 있는 컨텐츠 타입
- **Cookie**: session=abc123 - 세션 정보
- **Referer**: https://google.com - 이전 페이지
- **Authorization**: Bearer token123 - 인증 토큰

**Response 헤더:**
- **Server**: Apache/2.4.41 - 웹 서버 정보 (노출 주의)
- **Content-Type**: text/html; charset=UTF-8 - 응답 컨텐츠 타입
- **Content-Length**: 1024 - 응답 바디 크기
- **Set-Cookie**: session=xyz; HttpOnly - 쿠키 설정
- **Location**: https://example.com/new - 리다이렉션 주소

### 주요 웹 서버 점유율 (2022년 4월 기준)

| 웹 서버 | 점유율 | 특징 |
|:---:|:---:|:---|
| Nginx | 31.13% | 경량, 높은 동시 접속 처리, 리버스 프록시 |
| Apache | 23.08% | 전통적 웹 서버, 모듈 방식, .htaccess |
| OpenResty | 8.01% | Nginx 기반, Lua 스크립트 내장 |
| Cloudflare | 5.49% | CDN 겸 웹 서버, DDoS 방어 |

### 보안 체크리스트

- [ ] 서버 응답 헤더에서 버전 정보 제거했는가?
- [ ] 불필요한 HTTP 메서드(TRACE, OPTIONS 등) 비활성화했는가?
- [ ] HTTPS 강제 리다이렉션 설정했는가?
- [ ] 보안 헤더(X-Frame-Options, CSP 등) 적용했는가?
- [ ] 쿠키에 HttpOnly, Secure 플래그 설정했는가?
- [ ] 민감한 작업(로그인, 결제)은 POST 메서드 사용하는가?
- [ ] 에러 메시지에서 상세 정보(스택 트레이스, DB 쿼리) 노출하지 않는가?
- [ ] 디렉터리 리스팅 비활성화했는가?

### 트러블슈팅

| 문제 | 원인 | 해결 방법 |
|:---:|:---|:---|
| Burp Suite 프록시 연결 안 됨 | 브라우저 프록시 설정 오류 | 127.0.0.1:8080 확인, Intercept is on 확인 |
| HTTPS 사이트 접속 시 인증서 오류 | Burp Suite CA 인증서 미설치 | Burp CA 인증서를 브라우저에 등록 |
| 500 에러 지속 발생 | 서버 측 스크립트 오류 또는 DB 연결 실패 | 서버 로그 확인, DB 연결 상태 점검 |
| 403 Forbidden | 접근 권한 없음 또는 WAF 차단 | 인증 여부 확인, IP 화이트리스트 등록 |

---

**Today's Insight:**

웹은 개방성과 편의성을 위해 설계되었기에 보안은 나중에 덧붙여진 것이다. HTTP는 기본적으로 암호화도, 인증도 없는 평문 프로토콜이다. 그래서 HTTPS, 쿠키 보안 플래그, CORS, CSP 같은 보안 메커니즘이 추가로 개발되었다. 웹 보안의 핵심은 이 "후천적 보안 장치"들을 제대로 이해하고 적용하는 것이다.
