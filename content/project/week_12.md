---
title: "Week 12 — E-Commerce 보안 컨설팅 시뮬레이션 1/4: 취약 시스템 구축"
date: 2026-01-18
draft: false
tags: ["보안컨설팅", "Flask", "SQLInjection", "XSS", "파일업로드", "취약점", "OWASP", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "4주 보안 컨설팅 시뮬레이션의 첫 번째 주 — 의도적 취약점을 내포한 E-Commerce Flask 앱을 직접 구축하여 진단 대상 시스템을 준비한 개인 솔로 프로젝트"
---

# Week 12 — E-Commerce 보안 컨설팅 시뮬레이션 1/4: 취약 시스템 구축

> 전체 소스코드는 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_12](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_12)

> **학습 목적으로 구성된 실습입니다.**
> 의도적으로 취약한 시스템을 구축하고, 다음 주에 이를 직접 진단하는 구조의 교육용 프로젝트입니다.
> 실제 서비스에 대한 무단 공격은 정보통신망법 위반입니다.

---

## 프로젝트 배경 — 왜 4주 시리즈인가

파이널 프로젝트 주제를 선정하는 과정에서 **관제(SOC)** 와 **보안 컨설팅** 사이에서 고민이 있었다.

Week 10~11 에서 팀 프로젝트로 취약점 진단 경험을 쌓았지만, 당시에는 팀 단위로 역할을 나누어 진행하여 전체 프로세스를 온전히 혼자 경험하지는 못했다. **취약 시스템 구축 → 진단 → 개선 → 모니터링** 까지 보안 컨설턴트의 A to Z 업무 흐름을 **솔로로 직접 수행** 해보고 싶었다.

4주 계획:

    Week 12 (1/4) : 취약한 시스템 구축          <- 이번 주
    Week 13 (2/4) : 취약점 진단 (모의해킹 + 스캔)
    Week 14 (3/4) : 보안 개선 구현
    Week 15 (4/4) : 모니터링 체계 + 최종 컨설팅 보고서

---

## 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **시나리오** | 중소기업 E-Commerce 보안 컨설팅 시뮬레이션 |
| **이번 주 목표** | 의도적 취약점 내포 쇼핑몰 구현 |
| **기술 스택** | Flask, SQLite3, Jinja2, werkzeug |
| **접속 URL** | http://localhost:5000 |
| **테스트 계정** | admin / admin123 |

---

## 시스템 구조

    ecommerce_vulnerable/
    ├── app.py             # Flask 메인 애플리케이션 (취약점 핵심 코드)
    ├── init_db.py         # DB 초기화 (테스트 계정 + 더미 상품 데이터)
    ├── database.db        # SQLite 데이터베이스
    ├── templates/         # Jinja2 HTML 템플릿
    │   ├── base.html
    │   ├── index.html     # 상품 목록 (검색 기능 포함)
    │   ├── login.html
    │   ├── register.html
    │   ├── product.html   # 상품 상세 + 댓글
    │   ├── cart.html
    │   ├── checkout.html
    │   └── profile.html   # 프로필 + 이미지 업로드
    └── static/
        └── uploads/       # 업로드 파일 저장 경로

구현 기능:

- 회원가입 / 로그인 / 로그아웃
- 상품 목록 조회 (키워드 검색 포함)
- 상품 상세 페이지 + 댓글 작성
- 장바구니 / 주문 / 결제 흐름
- 프로필 관리 (이미지 업로드 포함)

---

## 의도적으로 삽입한 취약점 4종

이번 주의 핵심 목표는 **나쁜 코드를 의도적으로 잘 쓰는 것** 이다.
다음 주 진단 단계에서 실제로 공격해볼 수 있도록 OWASP Top 10 취약점을 정교하게 심어두었다.

---

### 취약점 1 — SQL Injection (로그인)

**위치**: `/login` POST 핸들러

취약한 구현 — 사용자 입력을 f-string 으로 직접 쿼리에 삽입:

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = conn.execute(query).fetchone()

공격 예시:

    Username : admin' OR '1'='1
    Password : anything

    실행 쿼리 => SELECT * FROM users WHERE username='admin' OR '1'='1' AND password='anything'
    결과       => OR 조건으로 항상 참 => 비밀번호 검증 없이 로그인 성공

---

### 취약점 2 — SQL Injection (상품 검색)

**위치**: `/` GET 핸들러, `search` 파라미터

취약한 구현 — LIKE 쿼리에 검색어 직접 삽입:

    search = request.args.get('search', '')
    if search:
        query = f"SELECT * FROM products WHERE name LIKE '%{search}%'"
        products = conn.execute(query).fetchall()

공격 예시:

    검색어 : ' OR '1'='1
    실행 쿼리 => SELECT * FROM products WHERE name LIKE '%' OR '1'='1%'
    결과       => LIKE 조건 무력화 => 전체 상품 10개 노출

---

### 취약점 3 — XSS (댓글)

**위치**: `product.html` 댓글 출력 + `/product/<id>/comment` POST

취약한 구현 — `|safe` 필터로 HTML 이스케이프를 비활성화:

    # 댓글 저장 시: 필터링 없이 DB에 그대로 저장
    conn.execute(
        'INSERT INTO comments (product_id, user_id, comment) VALUES (?, ?, ?)',
        (product_id, session['user_id'], comment)
    )

    # 출력 시 (product.html): |safe 필터 사용
    <p>{{ comment.comment|safe }}</p>

공격 예시:

    댓글 입력 : <script>alert('XSS')</script>
    결과       => 페이지 로드 시 스크립트 실행
               => 쿠키 탈취 / 피싱 페이지 삽입 등으로 확장 가능

---

### 취약점 4 — 파일 업로드

**위치**: `/profile` 프로필 이미지 업로드

취약한 구현 — 파일 타입 / 확장자 / 크기 검증 전혀 없음:

    filename = file.filename   # 원본 파일명 그대로 사용
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

공격 예시:

    업로드 파일 : webshell.php  (또는 .py, .sh 등)
    결과        => 서버에 그대로 저장
               => URL 직접 접근 시 서버 명령 실행 가능 (서버 장악)

보조 취약점 — **예측 가능한 시크릿 키**:

    app.secret_key = 'vulnerable_secret_key_123'

Flask 세션 쿠키는 시크릿 키로 서명되는데, 키가 공개되면 세션 위조가 가능하다.

---

## 취약점 설계 원칙

이번 주에서 가장 어려운 부분은 **취약하게 만드는 것** 이었다.

평소에는 Prepared Statement, HTML Escape, 화이트리스트 검증을 습관적으로 적용했기 때문에,
의식적으로 이를 피해서 코드를 짜야 했다.

    취약점 설계 원칙:
    - SQL Injection  : ? 바인딩 대신 f-string 직접 삽입
    - XSS            : |safe 필터를 명시적으로 사용
    - 파일 업로드     : ALLOWED_EXTENSIONS 검증 코드 작성 안 함
    - 세션 관리       : 예측 가능한 시크릿 키 사용

역설적으로, **무엇이 위험한지 알아야 의도적으로 취약하게 만들 수 있다**.
이 과정 자체가 방어 코드를 이해하는 좋은 방법이었다.

---

## 학습 성과 정리

| 영역 | 학습 내용 |
|------|------------|
| **취약점 설계** | OWASP Top 10 취약점을 실제 코드로 구현하는 방법 체득 |
| **Flask 구조** | 라우트 설계, 세션 관리, Jinja2 템플릿 렌더링 흐름 |
| **공격 벡터 이해** | SQL Injection / XSS / 파일 업로드의 동작 원리를 코드 레벨로 확인 |
| **컨설팅 준비** | 진단 대상 시스템을 준비하는 컨설팅 전 단계 경험 |

---

## 다음 주 예고 — Week 13: 취약점 진단

Week 12 에서 구축한 이 쇼핑몰을 대상으로, 실제 보안 컨설턴트처럼 취약점 진단을 수행한다.

    진단 도구:
    - OWASP ZAP  : 자동화 스캔
    - Python 스크립트 : 수동 진단 (SQL Injection, XSS, 파일 업로드)
    - Burp Suite : HTTP 요청/응답 분석 (선택)

    예상 발견사항:
    - Critical : SQL Injection (로그인, 검색)
    - High     : XSS, 파일 업로드
    - Medium   : CSRF, CSP 미설정, Clickjacking
    - Low      : 보안 헤더 누락
