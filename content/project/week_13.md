---
title: "Week 13 — E-Commerce 보안 컨설팅 시뮬레이션 2/4: 취약점 진단"
date: 2026-01-26
draft: false
tags: ["보안컨설팅", "취약점진단", "OWASPZAP", "SQLInjection", "XSS", "파일업로드", "CSRF", "모의해킹", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "4주 보안 컨설팅 시뮬레이션 2주차 — OWASP ZAP 자동화 스캔 + Python 수동 진단으로 Critical 2 / High 2 / Medium 3 / Low 5 총 12개 취약점을 발굴하고 종합 보고서를 작성"
---

# Week 13 — E-Commerce 보안 컨설팅 시뮬레이션 2/4: 취약점 진단

> 전체 소스코드 및 진단 보고서는 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_13](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_13)

---

## 진단 개요

| 항목 | 내용 |
|------|------|
| **진단 대상** | Week 12 에서 구축한 E-Commerce 웹 애플리케이션 |
| **진단 URL** | http://localhost:5000 |
| **진단 일자** | 2026년 1월 26일 |
| **진단자** | 호짱 (개인 솔로 프로젝트) |
| **진단 방법** | OWASP ZAP (자동화) + Python 스크립트 (수동) |

이번 주는 **공격자의 시선** 으로 지난주에 내가 직접 만든 쇼핑몰을 들여다보는 시간이었다.
설계자로서 어디에 취약점을 심었는지 알고 있음에도, 도구를 실제로 돌리고 PoC 를 작성하는 과정은 새로운 관점을 제공했다.

---

## 진단 프로세스

    1단계 — 자동화 스캔
       OWASP ZAP baseline 스캔 실행
       => 전체 애플리케이션 크롤링 + 취약점 자동 탐지
       => 결과: Medium 3개, Low 5개, Info 6개 발견

    2단계 — 수동 진단
       Python 스크립트로 SQL Injection / XSS / 파일 업로드 직접 공격
       => OWASP ZAP 이 못 잡은 Critical 취약점 2개 추가 발굴

    3단계 — 보고서 작성
       심각도별 분류 (Critical / High / Medium / Low)
       공격 시연 스크린샷 첨부
       비즈니스 영향도 + 개선 권고안 도출

사용 도구:

- **OWASP ZAP** — 자동화 취약점 스캐너 (baseline 모드)
- **Python requests + BeautifulSoup** — 수동 진단 스크립트
- **브라우저 직접 테스트** — XSS / 파일 업로드 PoC 확인

---

## 진단 결과 요약

**총 발견 취약점: 12개 (+ 정보성 항목 6개)**

    심각도별 분포:
    ┌──────────┬──────┬───────────────────────────────────────┐
    │ 심각도   │  수  │ 항목                                   │
    ├──────────┼──────┼───────────────────────────────────────┤
    │ Critical │  2   │ SQL Injection (로그인 우회, 검색 필터)  │
    ├──────────┼──────┼───────────────────────────────────────┤
    │ High     │  2   │ XSS (댓글), 파일 업로드 취약점          │
    ├──────────┼──────┼───────────────────────────────────────┤
    │ Medium   │  3   │ CSRF 토큰 없음, CSP 미설정, Clickjacking│
    ├──────────┼──────┼───────────────────────────────────────┤
    │ Low      │  5   │ 쿠키 SameSite, 서버 정보 노출 등        │
    └──────────┴──────┴───────────────────────────────────────┘

**OWASP ZAP vs 수동 진단 비교**:

    OWASP ZAP (자동화) : Medium 3 / Low 5 / Info 6
    수동 진단 (직접 공격): Critical 2 / High 2 추가 발굴
    => 자동화 도구만으로는 Critical 취약점을 놓칠 수 있음
    => 반드시 수동 진단을 병행해야 함

---

## Critical 취약점 상세

### CRIT-01 — SQL Injection (로그인 우회)

**위치**: `/login` POST

**공격 시연**:

    Username : admin' OR '1'='1
    Password : anything

    실행 쿼리 => SELECT * FROM users
                 WHERE username='admin' OR '1'='1' AND password='anything'

    OR '1'='1' 조건으로 WHERE 절 항상 참
    => 비밀번호 검증 없이 관리자 계정 로그인 성공

**취약 코드** — f-string 직접 삽입:

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    user = conn.execute(query).fetchone()

**개선 코드** — Prepared Statement 적용:

    user = conn.execute(
        'SELECT * FROM users WHERE username=? AND password=?',
        (username, password)
    ).fetchone()

    admin' OR '1'='1 입력 시 => 문자열 전체가 하나의 파라미터로 바인딩
    => SQL 구문으로 해석 불가 => 공격 차단

**비즈니스 영향**: 관리자 계정 탈취 => 전체 고객 데이터 유출, 주문 조작 가능

---

### CRIT-02 — SQL Injection (상품 검색 필터 우회)

**위치**: `/?search=` GET 파라미터

**공격 시연**:

    검색어 : ' OR '1'='1

    실행 쿼리 => SELECT * FROM products WHERE name LIKE '%' OR '1'='1%'
    결과       => LIKE 조건 무력화 => 전체 상품 10개 일괄 노출

**취약 코드**:

    query = f"SELECT * FROM products WHERE name LIKE '%{search}%'"
    products = conn.execute(query).fetchall()

**개선 코드**:

    products = conn.execute(
        'SELECT * FROM products WHERE name LIKE ?',
        (f'%{search}%',)
    ).fetchall()

**비즈니스 영향**: 검색 필터 우회 => DB 스키마 탐색 + UNION 기반 데이터 추출로 확장 가능

---

## High 취약점 상세

### HIGH-01 — XSS (Stored XSS, 댓글)

**위치**: `/product/<id>` 댓글 출력 (`product.html`)

**공격 시연**:

    댓글 입력 : <script>alert('XSS')</script>

    저장      => DB에 그대로 저장
    출력      => |safe 필터로 HTML 이스케이프 없이 렌더링
    결과      => 페이지를 방문하는 모든 사용자에게 스크립트 실행

Stored XSS 이므로 한 번 삽입하면 모든 방문자에게 지속 실행된다.

**취약 코드**:

    <p>{{ comment.comment|safe }}</p>

**개선 코드** — `|safe` 제거:

    <p>{{ comment.comment }}</p>

    => Jinja2 기본 이스케이프 복원
    => <script> => &lt;script&gt; 로 변환 => 텍스트로만 표시

**비즈니스 영향**: 세션 쿠키 탈취 => 사용자 계정 하이재킹, 피싱 페이지 삽입

---

### HIGH-02 — 파일 업로드 취약점

**위치**: `/profile` 프로필 이미지 업로드

**공격 시연**:

    업로드 파일 : webshell.php (또는 .py .sh 등 실행 파일)
    결과        => static/uploads/ 에 그대로 저장
               => URL 직접 접근 시 서버 명령 실행 가능

**취약 코드** — 확장자 / MIME 검증 전혀 없음:

    filename = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

**개선 코드** — 화이트리스트 기반 검증:

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if not allowed_file(file.filename):
        flash('허용되지 않는 파일 형식입니다.')
        return redirect(request.url)

추가 권고: **Magic Bytes** 검증 (확장자 위조 방어) + 업로드 경로를 웹 루트 외부로 이동

**비즈니스 영향**: 웹쉘 업로드 => 서버 전체 제어권 탈취, 랜섬웨어 감염, 내부망 침투

---

## Medium 취약점 상세

### MED-01 — CSRF 토큰 부재

**위치**: `/login`, `/register`, `/profile` 등 모든 POST 폼

CSRF(Cross-Site Request Forgery) 방어 메커니즘이 전혀 없다.

**공격 시나리오**:

    악성 사이트에 숨겨진 폼 => 피해자가 페이지 열면
    => 피해자의 세션으로 의도치 않은 요청 자동 전송 (비밀번호 변경, 주문 등)

**개선 방안** — Flask-WTF CSRF 토큰 적용:

    from flask_wtf.csrf import CSRFProtect
    csrf = CSRFProtect(app)

    # 템플릿에 토큰 삽입
    <form method="POST">
        {{ form.hidden_tag() }}
        ...
    </form>

---

### MED-02 — Content Security Policy 미설정

XSS 공격에 대한 브라우저 레벨 방어층이 없다.

**개선 방안** — CSP 헤더 추가:

    @app.after_request
    def set_security_headers(response):
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        return response

    => 인라인 <script> 실행 차단
    => 외부 도메인 스크립트 로드 차단

---

### MED-03 — Clickjacking 방어 헤더 없음

악성 사이트가 iframe 으로 이 쇼핑몰을 숨겨서 사용자를 속일 수 있다.

**개선 방안**:

    response.headers['X-Frame-Options'] = 'DENY'

---

## Low 취약점 목록

| # | 항목 | 영향 | 개선 방안 |
|---|------|------|----------|
| L-01 | 쿠키 SameSite 속성 없음 | CSRF 공격 경로 제공 | `SameSite=Strict` 설정 |
| L-02 | 서버 버전 정보 노출 | 공격자 정보 수집 | `SERVER_NAME` 헤더 제거 또는 변경 |
| L-03 | X-Content-Type-Options 없음 | MIME 스니핑 공격 가능 | `nosniff` 헤더 추가 |
| L-04 | Permissions-Policy 미설정 | 브라우저 기능 제한 없음 | 필요 기능만 허용하는 정책 설정 |
| L-05 | Cross-Origin 헤더 없음 | Spectre 공격에 취약 | COEP / COOP 헤더 설정 |

---

## 종합 개선 권고안

**즉시 조치 (Critical / High) — 1주 이내**:

    1. Prepared Statement 적용 — 모든 DB 쿼리를 ? 바인딩으로 전환
    2. |safe 필터 제거 — Jinja2 기본 이스케이프 복원
    3. 파일 업로드 화이트리스트 검증 — 확장자 + Magic Bytes 이중 검증

**단기 조치 (Medium) — 1개월 이내**:

    4. Flask-WTF CSRF 토큰 전역 적용
    5. CSP 헤더 설정 (default-src 'self' 부터 시작)
    6. X-Frame-Options: DENY 추가

**장기 조치 (Low) — 1~3개월**:

    7. 보안 헤더 종합 적용 (SecurityHeaders.com 체크리스트 활용)
    8. 서버 정보 은닉 (Werkzeug 버전 헤더 제거)
    9. 쿠키 보안 속성 강화 (SameSite, HttpOnly, Secure)

---

## 진단 산출물

| 파일 | 설명 |
|------|------|
| `reports/vulnerability_report.md` | 종합 취약점 진단 보고서 (취약 코드 + 개선 코드 포함) |
| `reports/screenshots/` | 공격 성공 증거 스크린샷 6장 |
| `tools/sql_injection_test.py` | 로그인 우회 자동 테스트 스크립트 |
| `tools/sql_data_extraction.py` | UNION 기반 데이터 추출 테스트 스크립트 |
| `scan_results/zap_scan_result.html` | OWASP ZAP 자동 스캔 결과 HTML |

---

## 진단을 마치며 — 자동화 도구의 한계

이번 진단에서 가장 인상적이었던 점은 **OWASP ZAP 이 Critical 취약점 2개를 전혀 잡지 못했다**는 것이다.

    OWASP ZAP 발견 : Medium 3 + Low 5 (보안 헤더 누락 위주)
    수동 진단 발견  : Critical 2 (SQL Injection) + High 2 (XSS, 파일 업로드)

SQL Injection 이나 인증 우회는 **맥락을 이해하고 입력값을 직접 조작** 해야 탐지된다.
자동화 스캐너는 응답 코드와 패턴을 비교하지만, 로그인 성공/실패의 의미를 해석하지는 못한다.

    결론:
    - 보안 진단에서 자동화 도구는 필수지만 충분하지 않다
    - Critical 취약점은 도메인 지식을 가진 사람이 직접 찾아야 한다
    - 자동화 (OWASP ZAP) + 수동 진단 (전문가) 의 조합이 실무 표준인 이유

---

## 학습 성과 정리

| 영역 | 학습 내용 |
|------|------------|
| **진단 프로세스** | 자동화 스캔 → 수동 점검 → PoC → 보고서 작성 전체 흐름 |
| **도구 활용** | OWASP ZAP baseline 스캔 설정 및 결과 해석 |
| **자동화 한계** | 도구가 놓친 Critical 취약점을 수동으로 발굴하는 경험 |
| **보고서 작성** | 심각도 분류 + 개선 코드 + 비즈니스 영향도 포함 실무 보고서 |
| **공격자 시각** | 내가 만든 시스템을 공격자 입장에서 바라보는 관점 전환 |

---

## 다음 주 예고 — Week 14: 보안 개선 구현

Week 13 에서 발굴한 12개 취약점을 실제로 수정한다.

    개선 대상:
    - Prepared Statement 전면 적용 (SQL Injection 4개 지점)
    - |safe 필터 제거 + CSP 헤더 설정 (XSS 방어)
    - 파일 업로드 화이트리스트 + Magic Bytes 검증
    - Flask-WTF CSRF 토큰 전역 적용
    - 보안 헤더 종합 설정 (Low 5개 일괄 처리)

    목표: 취약 버전 vs 개선 버전 Before / After 비교 분석
