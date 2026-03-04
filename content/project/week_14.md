---
title: "Week 14 — E-Commerce 보안 컨설팅 시뮬레이션 3/4: 보안 개선 구현"
date: 2026-02-02
draft: false
tags: ["보안컨설팅", "Flask", "PreparedStatement", "XSS방어", "파일업로드", "CSRF", "보안헤더", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "4주 보안 컨설팅 시뮬레이션 3주차 — Week 13 진단 결과를 바탕으로 Critical/High 취약점 4개를 완전 제거하고 Before/After 비교 검증까지 완료한 보안 개선 단계"
---

# Week 14 — E-Commerce 보안 컨설팅 시뮬레이션 3/4: 보안 개선 구현

> 전체 소스코드 및 검증 결과는 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_14](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_14)

---

## 개요

Week 13 에서 발굴한 취약점 12개를 실제로 수정하는 단계다.
코드를 고치는 것 자체보다, **"어떻게 고쳐야 공격을 원천 차단할 수 있는가"** 를 설계하는 과정이 더 중요했다.

개선 목표:

    Critical (2개) : SQL Injection (로그인, 검색) => 완전 제거
    High    (2개) : XSS, 파일 업로드             => 완전 제거
    Medium  (3개) : CSRF, CSP, Clickjacking      => 1개 해결 (CSRF)
    Low     (5개) : 보안 헤더 누락 등             => 1개 해결 (X-Frame-Options)

취약 버전(Week 12)과 개선 버전(Week 14)을 동시에 실행할 수 있도록 포트를 분리했다:

    Week 12 (취약) : http://localhost:5000
    Week 14 (개선) : http://localhost:5001

---

## 핵심 개선 — app.py 전체 설계 변경

### 1. 시크릿 키 강화

**Before** — 예측 가능한 하드코딩 문자열:

    app.secret_key = 'vulnerable_secret_key_123'

**After** — 실행마다 무작위 32바이트 생성:

    app.secret_key = os.urandom(32)

Flask 세션 쿠키는 시크릿 키로 서명된다.
`os.urandom(32)` 는 암호학적으로 안전한 난수를 생성하여 세션 위조를 원천 차단한다.

---

### 2. 보안 헤더 전역 적용

모든 HTTP 응답에 자동으로 보안 헤더를 삽입한다:

    @app.after_request
    def set_security_headers(response):
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline'"
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

각 헤더의 역할:

    X-Frame-Options: DENY         => Clickjacking 차단 (iframe 삽입 불가)
    X-Content-Type-Options: nosniff => MIME 스니핑 공격 차단
    Content-Security-Policy       => 인라인 스크립트 실행 차단 (XSS 2차 방어)
    X-XSS-Protection: 1; mode=block => 브라우저 내장 XSS 필터 활성화

---

### 3. CSRF 전역 보호

Flask-WTF 라이브러리로 모든 POST 폼에 CSRF 토큰을 자동 적용한다:

    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect(app)

`CSRFProtect(app)` 한 줄로 애플리케이션 전체의 POST 요청이 보호된다.
각 템플릿에서는 `{{ form.csrf_token }}` 또는 `{{ csrf_token() }}` 으로 토큰을 삽입한다.

---

## Critical 취약점 수정 — SQL Injection

### Before / After — 로그인

**Before** (Week 12) — f-string 직접 삽입:

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = conn.execute(query).fetchone()

    공격: admin' OR '1'='1  입력 시 => 비밀번호 검증 없이 로그인 성공

**After** (Week 14) — Prepared Statement:

    user = conn.execute(
        'SELECT * FROM users WHERE username=? AND password=?',
        (username, password)
    ).fetchone()

    동일 공격 시 => admin' OR '1'='1 전체가 하나의 문자열 파라미터로 처리
                => SQL 구문으로 해석 불가 => 로그인 실패

### Before / After — 상품 검색

**Before** (Week 12):

    query = f"SELECT * FROM products WHERE name LIKE '%{search}%'"
    products = conn.execute(query).fetchall()

**After** (Week 14):

    products = conn.execute(
        'SELECT * FROM products WHERE name LIKE ?',
        (f'%{search}%',)
    ).fetchall()

검증 결과:

    공격 입력  : ' OR '1'='1
    Week 12   : 전체 상품 10개 노출 (필터 무력화)
    Week 14   : 검색 결과 없음 (파라미터로 바인딩 => 공격 차단)

---

## High 취약점 수정 — XSS

### Before / After — 댓글 출력

**Before** (Week 12) — `|safe` 필터로 이스케이프 비활성화:

    <p>{{ comment.comment|safe }}</p>

    공격: <script>alert('XSS')</script>
    결과: 페이지 로드 시 스크립트 실행

**After** (Week 14) — `|safe` 제거:

    <p>{{ comment.comment }}</p>

    동일 입력 시: &lt;script&gt;alert('XSS')&lt;/script&gt; 로 이스케이프
    결과: 텍스트로만 표시 => 실행되지 않음

Jinja2 는 **기본적으로 이스케이프를 켜놓는다**.
`|safe` 를 제거하는 것만으로 보호가 복원된다.

---

## High 취약점 수정 — 파일 업로드

### 화이트리스트 기반 검증 추가

**Before** (Week 12) — 검증 전무:

    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    결과: 모든 파일 형식 업로드 가능 => 웹쉘 업로드 가능

**After** (Week 14) — 화이트리스트 + secure_filename:

    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    # 업로드 처리 시
    if not allowed_file(file.filename):
        flash('허용되지 않는 파일 형식입니다.')
        return redirect(request.url)

    filename = secure_filename(file.filename)  # 경로 조작 방지
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    결과: txt, php, py, sh 등 모든 비허용 파일 업로드 차단

`secure_filename()` 의 역할 — `../../../etc/passwd` 같은 경로 조작 공격도 함께 차단한다.

---

## Before / After 비교 검증 결과

### 수동 공격 테스트

| 공격 유형 | Week 12 (취약) | Week 14 (개선) |
|-----------|----------------|----------------|
| SQL Injection (로그인) | 성공 | **차단** |
| SQL Injection (검색) | 성공 | **차단** |
| XSS (댓글) | 성공 | **차단** |
| 파일 업로드 (.txt) | 성공 | **차단** |

### OWASP ZAP 자동 스캔 비교

| 심각도 | Week 12 | Week 14 | 변화 |
|--------|---------|---------|------|
| Critical | 2 | **0** | -2 |
| High | 2 | **0** | -2 |
| Medium | 3 | 2 | -1 |
| Low | 5 | 4 | -1 |

**총 6개 취약점 해결 (Critical + High 100% 제거)**

주목할 점 — ZAP 은 여전히 Critical / High 를 0개로 표시한다.
이는 Week 13 에서 확인했듯이 자동화 스캐너가 인증 기반 취약점을 탐지하지 못하는 한계를 그대로 보여준다.
**Critical 차단 여부는 오직 수동 테스트로만 검증 가능하다.**

---

## 남은 취약점 현황

### Medium (2개 잔존)

**CSP 정책 강화** — 현재 `style-src 'unsafe-inline'` 허용 상태로, 인라인 스타일 XSS 가능성 잔존.
추가 조치 필요: Nonce 기반 CSP 적용 또는 외부 CSS 파일 분리

**Clickjacking** — `X-Frame-Options: DENY` 설정으로 1차 방어했지만,
오래된 브라우저에서 추가 검증이 필요하다.

### Low (4개 잔존)

보안 헤더 추가(`X-Content-Type-Options`, `X-XSS-Protection`)로 1개 감소했으나,
다음 항목이 남아있다:

    - 쿠키 SameSite 속성 미설정
    - 서버 버전 정보 노출 (Werkzeug 헤더)
    - Permissions-Policy 미설정
    - Cross-Origin 헤더 없음

---

## 학습 성과 정리

| 영역 | 학습 내용 |
|------|------------|
| **Prepared Statement** | ? 바인딩이 SQL Injection 을 원천 차단하는 이유를 코드로 직접 확인 |
| **Jinja2 보안** | `|safe` 필터의 위험성과 기본 이스케이프의 중요성 체득 |
| **파일 업로드 보안** | 화이트리스트 + secure_filename() 이중 방어의 구현 방법 |
| **보안 헤더** | `@app.after_request` 로 전역 보안 헤더를 적용하는 패턴 |
| **Before/After 검증** | 방어 구현 후 실제 공격으로 차단 여부를 직접 확인하는 습관 |

---

## 다음 주 예고 — Week 15: 모니터링 + 최종 보고서

4주 시리즈의 마지막 주.
로그 분석 시스템을 구축하고, 4주 전체를 하나의 **보안 컨설팅 최종 보고서** 로 정리한다.

    구현 예정:
    - log_analyzer.py    : 보안 이벤트 탐지 스크립트
    - dashboard.html     : 보안 이벤트 대시보드
    - consulting_report  : Executive Summary + 전체 결과 종합
