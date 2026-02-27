---
title: "2025.12.29 (Day 44) - 웹 보안과 Apache 웹 서버 보안 설정"
date: 2025-12-29
draft: false
tags: ["Apache", "웹서버보안", "접근통제", "생체인증", "로그분석", "입력값검증", "ModSecurity", "SetEnvIf"]
categories: ["daily-logs"]
summary: "ROT13/47 패스워드 관리, 생체 인증 FRR/FAR/EER, DAC/Bell-LaPadula/Biba/RBAC 접근통제 모델, Apache2 설치 및 보안 설정, access.log Combined 형식 분석, SetEnvIf 로그 필터링, SQL Injection/XSS/파일 업로드 입력값 검증 비교"
---

# 📄 2025.12.29 (Day 44) - 웹 보안과 Apache 웹 서버 보안 설정

---

## 1. 핵심 개념 정리

### 사용자 인증 메커니즘

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 1 | **패스워드 보안 원칙** | 세 종류 이상 문자 조합(abc123!@), 두 종류 이상 8자 이상(angel12345), 특정 명칭 첫 글자 조합 | 안전한 패스워드 생성 규칙, 추측 어려운 조합 사용, 노래 제목/숫자 조합 활용 |
| 2 | **ROT 암호화** | ROT13(영어 13자 이동), ROT47(모든 ASCII 문자 치환) | rot13.com, webutils.pl/ROTencode 사이트 활용, 패스워드 변형 저장 |
| 3 | **패스워드 파일 관리** | 엑셀 파일 암호화 + 시트 숨기기 + USB 메모리 이중 보관 | [파일]-[정보]-[통합 문서 보호]-[암호 설정], 외부 저장장치 백업 |
| 4 | **공인인증서 구조** | ITU-T X.509 표준, PKI 공개키 기반 구조 | 일련번호, 주체, 발행자, 유효기간, 공인키, 지문 알고리즘, 지문 포함 |
| 5 | **공인인증서 저장** | C:\Users\계정\AppData\LocalLow\NPKI\발급기관\USER | signCert.der(DER 암호화 인증서), signPri.key(개인키) |

### 생체 인증 기술

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 6 | **지문 인증** | 융선과 골 구성, 지문 등록(enrollment) -> 지문 인증(verification) 프로세스 | 가장 대중적, 평생 변하지 않음, 복제 가능성 존재 |
| 7 | **손 모양 인증** | 손가락 길이와 굵기 측정, 낮은 보안 수준 | 정맥 모양 촬영 시 보안 수준 향상 가능 |
| 8 | **망막 인증** | 눈 뒷부분 모세혈관 형태 확인, 10~15초 소요 | 매우 높은 정확도, 안경 착용 시 불가, 불편함 |
| 9 | **홍채 인증** | 홍채 패턴을 수학/통계 알고리즘으로 분석, 50cm 거리 인증 | 망막보다 정확도 높음, 자동 통관 시스템 적용, Apple Face ID |
| 10 | **생체 인증 성능** | FRR(False Rejection Rate, Type I), FAR(False Acceptance Rate, Type II), EER(Error Equal Rate) | FRR: 권한자 거부, FAR: 비권한자 허용(더 치명적), EER: 교차점(낮을수록 우수) |

### 접근 통제 모델

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 11 | **보안 등급 체계** | Top Secret(최고 기밀) > Secret > Confidential > Restricted > Unclassified | 군사/정부 문서 보안 수준, 극도의 치명적 피해 방지 |
| 12 | **DAC (임의적 접근 통제)** | Discretionary Access Control, 정보 소유자가 보안 수준 결정 | 유닉스/윈도우 파일 권한(rwx rw- rw-), 중앙 집중 관리 어려움 |
| 13 | **Bell-LaPadula 모델** | 기밀성 중심, No read up(상위 정보 읽기 금지), *property(하위 정보 쓰기 금지) | 보안 수준 2 정보를 수준 1에 기록하면 기밀성 손상, 군사/정부 적용 |
| 14 | **Biba 모델** | 무결성 중심, Read up(상위 정보 읽기 허용), No write up(상위 정보 쓰기 금지) | Bell-LaPadula와 반대 개념, 금융 거래 데이터 보호 |
| 15 | **RBAC** | Role-Based Access Control, 직책 기반 권한 부여 | 사람이 아닌 역할에 권한 할당, 직책 이동 시 불필요 권한 확대 방지 |

---

## 2. 실습 내용 정리

### 실습 9-1: 나만의 방식으로 안전하게 패스워드 관리하기

**목표:** ROT 암호화 및 엑셀 파일 암호화를 활용한 안전한 패스워드 저장 방법 실습

**실습 환경:**
- ROT13 온라인 도구: rot13.com
- ROT47 온라인 도구: webutils.pl/ROTencode
- Microsoft Excel

**실습 단계:**
1. ROT13 암호화 실습 - rot13.com 접속, Password123!@# 입력 -> Cnffjbeq123!@# 결과 확인
2. ROT47 암호화 실습 - webutils.pl/ROTencode 접속, ROT47 옵션 선택 -> Password123!@# 입력
3. 엑셀 파일에 패스워드 정보 입력 - 사이트, 설명, 아이디, 인코딩된 패스워드, 가입일, 최종 변경일 컬럼 생성
4. 시트 숨기기 - 시트명 우클릭 -> [숨기기(H)] 선택
5. 엑셀 파일 암호화 - [파일] -> [정보] -> [통합 문서 보호] -> [암호를 사용하여 암호화] -> 암호 설정
6. USB 메모리에 이중 보관 - 외부 저장장치 백업

**분석 포인트:**
- ROT13은 영어 알파벳만 13자 이동 (A -> N, B -> O)
- ROT18은 문자+숫자 모두 치환
- ROT47은 모든 ASCII 문자(33~126) 치환 가능
- 엑셀 파일 암호 설정 후 외부 저장장치 백업 여부 확인

**보안 인사이트:**
- ROT 암호화는 기초적이지만 평문 저장보다 안전
- 패스워드 파일 자체 암호화로 2차 보안 레이어 구축
- 시트 숨기기 기능으로 추가 보안 레이어 제공
- USB 이중 보관으로 컴퓨터 손상/해킹 시 복구 가능

---

### 실습 9-2: 공인인증서 파일 확인하기

**목표:** Windows 시스템에서 공인인증서 파일 구조 및 X.509 인증서 정보 확인

**실습 단계:**
1. 공인인증서 폴더 탐색 - C:\Users\사용자계정\AppData\LocalLow\NPKI
2. 발급 기관별 폴더 확인 (yessign, SignKorea, CrossCert, NPKI 등)
3. USER 폴더 내 파일 확인
   - signCert.der - DER 암호화된 인증서 파일
   - signPri.key - 개인키 파일
4. signCert.der 더블클릭하여 인증서 정보 확인
   - [일반] 탭: 발급 대상, 발급자, 유효 기간
   - [자세히] 탭: 버전, 일련번호, 서명 알고리즘, 발급자, 유효 기간, 주체, 공개 키
5. 인증서 구성요소 확인
   - 버전: V3
   - 일련번호: 고유 식별자
   - 서명 알고리즘: sha256RSA
   - 발급자: yessignCA Class 1
   - 유효 기간: 2016.04.24 ~ 2017.04.24

**X.509 인증서 구조:**
1. 일련번호 - 증명서 개별 인증
2. 주체 - 사람 또는 증명자
3. 서명 알고리즘 - 서명 생성 알고리즘
4. 발행자 - 정보 검증 및 증명서 발행 주체 (CA)
5. 유효 기간 - 시작일/만료일
6. 키 이용 목적 - SSL, 전자서명 등
7. 공인키 - 공개키
8. 지문 알고리즘 - 인증서 해시 알고리즘
9. 지문 - 증명서 개봉 여부 증명

**보안 고려사항:**

탐지 패턴:
- 인증서 유효 기간 만료
- 비인가 인증서 사용 시도
- 인증서 파일 무단 복사/이동
- 취소된 인증서(CRL) 사용 시도

방어 방법:
- 주기적인 인증서 유효 기간 점검
- 인증서 파일 접근 권한 엄격 관리 (signPri.key 특히 중요)
- 인증서 갱신 알림 시스템 구축
- CRL(Certificate Revocation List) 확인 절차

---

### 실습 9-3: 아파치 웹 서버 설치하기 (Ubuntu 22.04)

**목표:** Ubuntu Linux에 Apache2 웹 서버 설치 및 기본 동작 확인

**실습 환경:**
- Ubuntu 22.04 LTS
- VMware Workstation
- root 권한 필요

**실습 단계:**
1. 패키지 목록 업데이트 - `sudo apt-get install update`
2. 루트 권한 전환 - `sudo su -`
3. DPKG 설정 파일 세팅 - `dpkg --configure -a`
4. Apache2 설치 - `apt-get install apache2`
5. 아파치 서비스 시작 - `systemctl start apache2`
6. 프로세스 확인 - `ps -ef | grep apache2`
   - root 권한 parent 프로세스 1개
   - www-data 권한 worker 프로세스 여러 개 확인
7. 포트 리스닝 확인 - `netstat -tuln | grep :80` 또는 `ss -tuln | grep :80`
8. 브라우저 접속 테스트 - http://localhost 또는 http://서버IP -> "It works!" 페이지 확인

**분석 포인트:**
- apache2 프로세스가 여러 개 실행 중 (parent + worker processes)
- root 권한으로 parent 실행, www-data 권한으로 worker 실행
- 기본 포트 80번 리스닝 상태
- /var/www/html/index.html 기본 페이지 표시
- 설정 파일 위치: /etc/apache2/ (Ubuntu 특징)

**보안 인사이트:**
- Apache는 멀티 프로세스 모델 (MPM Prefork)로 동작
- root 권한으로 시작하나 worker는 www-data 계정으로 권한 제한
- 기본 설치 상태는 보안 강화 필요 (디렉터리 리스팅, 버전 정보 노출 등)
- Ubuntu는 설정 파일이 여러 개로 분산 (apache2.conf, sites-available, mods-available 등)

---

### 실습 9-4: 아파치 웹 서버 보안 설정하기

**목표:** 디렉터리 리스팅 차단, FollowSymLinks 비활성화, 로그 분석

**실습 단계:**
1. Apache 메인 설정 파일 확인 - `nano /etc/apache2/apache2.conf`
2. 포트 설정 확인 - `nano /etc/apache2/ports.conf` (Listen 80 기본 HTTP)
3. 가상 호스트 설정 확인 - `nano /etc/apache2/sites-available/000-default.conf` (DocumentRoot /var/www/html)
4. 기본 문서 설정 확인 - `nano /etc/apache2/mods-available/dir.conf` (DirectoryIndex 설정)
5. 디렉터리 리스팅 차단 - apache2.conf에서 `<Directory /var/www/>` 블록의 Options에서 Indexes 제거
6. 아파치 재시작 - `systemctl restart apache2`
7. 디렉터리 리스팅 테스트 - `/var/www/html/test` 폴더 생성 후 브라우저 접속 -> Forbidden 확인
8. FollowSymLinks 테스트 - `ln -s /etc /var/www/html/etc` 후 접속 -> /etc 내용 노출 확인
9. FollowSymLinks 비활성화 - `Options -Indexes -FollowSymLinks` 설정 후 재시작
10. 접근 로그 확인 - `tail -f /var/log/apache2/access.log`

**디렉터리 리스팅 차단 원리:**

Options 지시자:
- **Indexes**: 디렉터리 내 파일 목록 자동 표시 -> 제거 시 403 Forbidden 반환
- **FollowSymLinks**: 심볼릭 링크 추적 허용 -> 활성화 시 시스템 디렉터리 접근 가능, 제거 시 차단
- **MultiViews**: 콘텐츠 협상 기능 -> 필요시에만 활성화

권장 설정: `Options -Indexes -FollowSymLinks`

**발견 가능한 취약점:**
- Indexes 설정 시 디렉터리 구조 완전 노출
- FollowSymLinks 허용 시 /etc, /var 등 시스템 디렉터리 접근 가능
- 기본 에러 페이지에 Apache 버전 정보 노출
- 상세한 에러 메시지로 웹 서버 내부 경로 정보 유출

**보안 고려사항:**

탐지 패턴:
- 403 Forbidden 대량 발생 (무작위 디렉터리 스캔)
- ../../../etc/passwd 경로 순회(Path Traversal) 시도
- access.log에서 robots.txt, .git, .env 등 민감 파일 접근 시도
- 특정 IP에서 짧은 시간 대량 요청 (디렉터리 스캔)

방어 방법:
- Options에서 Indexes, FollowSymLinks 제거
- ServerTokens Prod (버전 정보 숨김)
- ServerSignature Off (에러 페이지 시그니처 제거)
- 심볼릭 링크 사용 금지 또는 제한적 허용
- Fail2ban 설정으로 스캔 시도 IP 자동 차단

---

### 실습 9-5: Apache access_log 분석하기

**목표:** Apache 접근 로그 구조 이해 및 CustomLog/LogFormat 설정 분석

**Combined 로그 형식 분석:**

로그 구조 예시:
`127.0.0.1 - - [29/May/2022:00:41:38 +0300] "GET / HTTP/1.1" 200 3460 "-" "Mozilla/5.0"`

각 필드 설명:
- `%h` - 클라이언트 IP 주소
- `%l` - 클라이언트 사용자 이름 (identd, 대부분 -)
- `%u` - 인증된 사용자 이름 (HTTP 인증)
- `%t` - 요청 시간 [날짜:시간 타임존]
- `"%r"` - 요청 라인 (메소드 URL 프로토콜)
- `%>s` - 최종 상태 코드 (200, 404, 500 등)
- `%O` - 응답 크기 (bytes, 헤더 포함)
- `"%{Referer}i"` - 리퍼러 (이전 페이지)
- `"%{User-Agent}i"` - 브라우저 정보

**LogFormat 정의:**
- combined: `%h %l %u %t "%r" %>s %O "%{Referer}i" "%{User-Agent}i"`
- common: `%h %l %u %t "%r" %>s %O`
- referer: `%{Referer}i -> %U`
- agent: `%{User-agent}i`

**로그 인수 상세:**

| 인수 | 설명 | 예시 |
|:---|:---|:---|
| %a | 클라이언트 IP | 192.168.1.100 |
| %A | 로컬 서버 IP | 10.0.0.1 |
| %h | 클라이언트 호스트/IP | example.com |
| %l | 클라이언트 identd | - |
| %u | 인증 사용자 | john |
| %t | 요청 시간 | [29/May/2022:00:41:38] |
| %r | 요청 첫 번째 줄 | GET /index.html HTTP/1.1 |
| %>s | 최종 상태 코드 | 200, 404, 500 |
| %O | 응답 크기(헤더 포함) | 3460 |
| %{Referer}i | 리퍼러 URL | https://google.com |
| %{User-Agent}i | UA 문자열 | Mozilla/5.0 |

**SetEnvIf 활용:**

SetEnvIf 인수:
- 요청 헤더: Host, User-Agent, Referer, Accept-Language
- 요청 특성: Remote_Host, Remote_Addr, Server_Addr, Request_Method, Request_Protocol, Request_URI

SetEnvIf 적용 예시:
- 특정 IP 로그 제외: `SetEnvIf Remote_Addr "127\.0\.0\.1" dontlog` + `CustomLog logs/access_log common env=!dontlog`
- 웜 공격 로그 제외: `SetEnvIf Request_URI "\.ida" worm` + `CustomLog logs/access_log common env=!worm`
- 이미지 파일 로그 제외: `SetEnvIf Request_URI "\.(gif|jpg|png)$" image` + `CustomLog logs/access_log common env=!image`
- 특정 브라우저 식별: `SetEnvIf User-Agent "MSIE" msie_browser` 또는 `SetEnvIf User-Agent "Mozilla" mozilla_browser`

---

## 3. 입력값 검증 비교표

### SQL Injection 방어 기법

| 항목 | 취약한 코드 | 안전한 코드 | 차이점 | 사용 시기/적용 방안 |
|:---:|:---|:---|:---|:---|
| **문자열 연결** | `String query = "SELECT * FROM " + tableName + " WHERE Name = " + name;` | `String query = "SELECT * FROM ? WHERE Name = ?";` | 직접 연결 vs 파라미터 바인딩 | Prepared Statement 사용 |
| **파라미터 설정** | `stmt.executeQuery(query);` | `stmt.setString(1, tableName); stmt.setString(2, name);` | 직접 실행 vs 바인딩 후 실행 | setString(), setInt() 메서드 |
| **쿼리 컴파일** | 런타임 쿼리 생성 | 쿼리 미리 컴파일 | SQL 인젝션 가능 vs 차단 | DB에 컴파일된 쿼리 전달 |
| **공격 차단** | `' OR '1'='1` 입력 시 인증 우회 | 파라미터는 문자열로 처리 | 모든 사용자 조회 vs 안전 | 사용자 입력을 코드로 해석 안 함 |

### XSS 방어 기법

| 항목 | 취약한 코드 | 안전한 코드 | 차이점 | 사용 시기/적용 방안 |
|:---:|:---|:---|:---|:---|
| **직접 출력** | `<p>NAME: <%= name %></p>` | `name = name.replaceAll("<", "&lt;"); name = name.replaceAll(">", "&gt;");` | 특수문자 그대로 vs 치환 | 출력 전 replaceAll() 사용 |
| **특수문자 치환** | 없음 | `< -> &lt, > -> &gt, & -> &amp, " -> &quot` | 스크립트 실행 vs 문자 표시 | HTML Entity 변환 |
| **검증 위치** | 클라이언트 측만 | 서버 측 필수 (JSP, PHP) | Burp Suite 우회 가능 vs 불가 | 서버 언어에서 구현 |
| **공격 차단** | `<script>alert('XSS')</script>` 실행 | `&lt;script&gt;...` 문자열로 표시 | 악성 스크립트 실행 vs 차단 | 반사형/저장형 XSS 모두 방어 |

### 파일 업로드 검증

| 항목 | 취약한 코드 | 안전한 코드 | 차이점 | 사용 시기/적용 방안 |
|:---:|:---|:---|:---|:---|
| **확장자 검증** | 확장자 체크 없음 | 화이트리스트 방식 | 모든 파일 허용 vs 특정만 허용 | .hwp, .doc, .pdf만 허용 |
| **파일명 처리** | 원본 파일명 저장 | UUID/랜덤 문자열로 변경 | 추측 가능 vs 불가능 | UUID.randomUUID() 사용 |
| **저장 경로** | 웹 루트 내 저장 | 웹 루트 외부 저장 | 직접 실행 가능 vs 불가 | /var/uploads 별도 경로 |
| **공격 차단** | shell.php 업로드 후 실행 | .php 업로드 차단 | 웹셸 설치 가능 vs 차단 | 실행 권한 제거, MIME 검증 |

### 필터링 방식 비교

| 예시 | 화이트리스트 | 블랙리스트 | 보안 영향 |
|:---|:---|:---|:---|
| **파일 업로드** | .hwp, .doc, .pdf만 허용 | .php, .jsp, .aspx 차단 | 4개만 통과 vs 수백 개 차단 필요 (우회 가능성) |
| **SQL 인젝션** | 영문자, 숫자만 허용 | `'`, `--`, `union` 차단 | 명확한 허용 vs 새로운 패턴 우회 가능 |
| **XSS** | 특정 HTML 태그만 허용 | `<script>`, `onerror` 차단 | 안전한 태그만 허용 vs 인코딩 우회 가능 |
| **권장 사항** | 파일 확장자, 입력 형식에 사용 | 알려진 공격 패턴 보완 | 화이트리스트 우선, 블랙리스트 보완 |

---

## 4. 심화 분석

### 접근 통제 모델 상세 비교

| 구분 | DAC | Bell-LaPadula | Biba | RBAC | 분석/인사이트 |
|:---:|:---|:---|:---|:---|:---|
| **목적** | 소유자 재량 | 기밀성 보호 | 무결성 보호 | 역할 기반 관리 | 상황에 따른 모델 선택 |
| **읽기 규칙** | 소유자 결정 | No read up | Read up 허용 | 역할별 설정 | B-L: 상위 정보 읽기 금지 |
| **쓰기 규칙** | 소유자 결정 | No write down (*property) | No write up | 역할별 설정 | 기밀성 vs 무결성 우선순위 |
| **적용 사례** | Unix rwx 권한 | 군사/정부 기밀 | 금융 거래 데이터 | 기업 ERP/그룹웨어 | 목적에 따라 혼합 사용 가능 |
| **장단점** | 유연하나 관리 어려움 | 기밀 보호 강력 | 데이터 변조 방지 | 권한 확대 자동 방지 | RBAC이 실무에서 가장 널리 사용 |

### Apache 로그 공격 패턴 분석

**공격 시나리오 1: SQL Injection 탐지**

로그 예시:
`192.168.1.100 - - [30/Dec/2024:10:15:32 +0900] "GET /login.php?user=' OR '1'='1 HTTP/1.1" 200 5432 "-" "sqlmap/1.6"`

탐지 포인트:
- Request_URI에 SQL 구문 (`' OR '1'='1`, `UNION SELECT`, `--`)
- User-Agent에 공격 도구명 (sqlmap, havij)
- 단시간 대량 요청 (초당 100+)

**공격 시나리오 2: Directory Traversal**

로그 예시:
`192.168.1.200 - - [30/Dec/2024:10:20:15 +0900] "GET /../../../etc/passwd HTTP/1.1" 403 298 "-" "Mozilla/5.0"`

탐지 포인트:
- Request_URI에 `../` 패턴 반복
- 403 Forbidden (차단 성공)
- /etc/passwd, /etc/shadow 경로 시도

**공격 시나리오 3: 웹셸 업로드**

로그 예시:
`192.168.1.150 - - [30/Dec/2024:10:25:40 +0900] "POST /upload.php HTTP/1.1" 200 89`

탐지 포인트:
- POST /upload.php 요청
- error.log에 "invalid extension"
- .php, .jsp, .aspx 확장자 시도

**공격 시나리오 4: Brute Force**

로그 예시:
`192.168.1.180 - - [30/Dec/2024:10:30:01 +0900] "POST /login.php HTTP/1.1" 401 345 "-" "Python-requests/2.28.1"` (동일 IP에서 100+ 반복)

탐지 포인트:
- 동일 IP에서 POST /login.php 대량
- 401 Unauthorized 반복
- User-Agent: Python-requests, curl

### 생체 인증 FRR/FAR 분석

**임계값에 따른 성능 트레이드오프:**
- 임계값 높임: FRR 증가, FAR 감소 (보안↑, 불편↑)
- 임계값 낮춤: FRR 감소, FAR 증가 (편의↑, 보안↓)
- EER 지점: FRR == FAR (최적 설정점)

**테스트 시나리오:**
- threshold 0.85 (일반): FRR/FAR 균형
- threshold 0.90 (엄격): FRR 증가, FAR 감소
- threshold 0.80 (느슨): FRR 감소, FAR 증가

---

## 5. 실무/보안 적용

### SOC 분석가 관점 - 웹 공격 탐지/대응

| 단계/유형 | 탐지 포인트 | 로그 예시 | 대응 방안 |
|:---:|:---|:---|:---|
| **SQL Injection** | Request_URI에 SQL 키워드(`union`, `select`, `'`, `--`), 비정상 파라미터 값 | `GET /login?id=admin' OR '1'='1` | WAF 규칙 적용, 해당 IP 차단, 애플리케이션 코드 검토 |
| **XSS** | `<script>`, `javascript:`, `onerror`, 인코딩 스크립트 (%3Cscript%3E) | `GET /search?q=<script>alert(1)</script>` | CSP 헤더 적용, 입력값 필터링 강화, 저장형 XSS 시 DB 정화 |
| **Path Traversal** | `../`, `..\` 패턴, 403 Forbidden 대량, /etc/passwd 접근 시도 | `GET /../../../etc/passwd` | 경로 정규화 검증, chroot 환경, 파일 접근 로그 모니터링 |
| **File Upload** | .php, .jsp, .aspx 업로드, MIME 타입 불일치, 이중 확장자 (file.php.jpg) | `POST /upload.php (shell.php)` | 화이트리스트 검증, 파일 실행 권한 제거, 업로드 디렉터리 격리 |
| **Brute Force** | 단시간 로그인 실패 반복, 401/403 대량 발생, 자동화 도구 UA | `POST /login (401) x 100회` | 계정 잠금 정책, CAPTCHA 적용, IP 속도 제한 |
| **DDoS/Scanning** | 초당 100+ 요청, robots.txt 접근, Nikto/Nmap UA | `GET /admin (404) x 1000회` | Rate Limiting, Fail2ban 설정, CDN/WAF 활용 |

### Apache 보안 설정 핵심 항목

**서버 정보 숨기기:**
- `ServerTokens Prod` - 버전 정보 최소화
- `ServerSignature Off` - 에러 페이지 시그니처 제거

**디렉터리 보안:**
- `Options -Indexes -FollowSymLinks` - 디렉터리 리스팅 및 심볼릭 링크 차단
- FilesMatch로 .htaccess, .htpasswd, .log, .sql 파일 접근 차단

**HTTP 메서드 제한:**
- GET, POST, HEAD만 허용
- TRACE, PUT, DELETE 차단

**타임아웃 및 요청 크기 제한:**
- Timeout 60
- KeepAliveTimeout 5
- LimitRequestBody 10MB

**SetEnvIf 로그 필터링:**
- 내부 IP(10.0.0.0/8) env=internal 설정 -> `CustomLog combined env=!internal`
- 정적 파일(.gif, .jpg, .png, .css, .js) env=static 설정 -> `CustomLog combined env=!static`

**보안 헤더 (mod_headers):**
- X-Frame-Options: SAMEORIGIN
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

**SSL/TLS 설정:**
- SSLv2, SSLv3, TLSv1, TLSv1.1 비활성화
- TLS 1.2 이상만 허용
- HIGH:!aNULL:!MD5 Cipher Suite

**ModSecurity (WAF):**
- SecRuleEngine On
- OWASP CRS(Core Rule Set) 포함
- 오탐 시 SecRuleRemoveById로 특정 룰 비활성화 가능

---

## 6. 배운 점 및 인사이트

### 새로 알게 된 점

- **ROT 암호화 실무 활용:** ROT13/ROT47 같은 단순 치환 암호도 평문 저장보다 훨씬 안전. 특히 ROT47은 모든 ASCII 문자(33~126)를 치환하여 특수문자 포함 복잡한 패스워드도 변형 가능. 엑셀 파일 암호화와 결합하면 실용적인 개인 패스워드 관리 방안

- **생체 인증 성능 지표:** FRR과 FAR의 트레이드오프 관계가 명확함. 임계값을 높이면 FRR 증가(사용자 불편), 낮추면 FAR 증가(보안 위험). EER 지점이 이론적 최적 설정이나, 실무에서는 보안 수준에 따라 FAR을 0.01% 이하로 낮추는 방향으로 조정

- **Apache 로그 필터링 기법:** SetEnvIf로 내부 IP나 정적 파일 요청을 `env=!dontlog` 방식으로 로그에서 제외하여 로그 파일 크기를 50% 이상 절감 가능. SIEM 연동 전 1차 필터링으로 분석 효율 향상

- **접근 통제 모델의 실제 적용:** Bell-LaPadula(기밀성)는 군사/정부, Biba(무결성)는 금융, RBAC은 기업 ERP/그룹웨어에 주로 사용. 현대 클라우드 환경에서는 RBAC + ABAC(Attribute-Based) 하이브리드 모델이 트렌드

- **서버 측 입력값 검증의 중요성:** 클라이언트 측 JavaScript 검증은 Burp Suite로 쉽게 우회 가능. JSP, PHP 등 서버 언어에서 Prepared Statement, replaceAll(), 화이트리스트 검증을 필수로 구현해야 SQL Injection/XSS 방어 가능

### 이전 학습과의 연결고리

- **개인정보보호법과 연계:** 개인정보보호법 시행령의 "접근 기록 최소 6개월 보관" 의무는 Apache access.log가 바로 충족하는 수단. 로그에는 IP 주소(개인정보)가 포함되므로 로그 파일 자체도 암호화 저장 권장. SetEnvIf로 필요한 로그만 수집하면 개인정보 최소 수집 원칙 준수

- **웹 해킹 실습 확장:** WebGoat에서 실습한 SQL Injection, XSS 공격이 실제 Apache 로그에 `union select`, `<script>` 패턴으로 기록됨을 확인. 공격자 관점에서 공격 기법 학습 -> SOC 분석가 관점에서 로그 탐지 패턴 이해

- **네트워크 보안과 연계:** Apache 로그의 클라이언트 IP 분석은 방화벽, IDS/IPS 로그와 상관분석 필수. 동일 IP에서 SQL Injection 시도 -> 방화벽 차단 -> IDS 알람 -> Apache 403 로그를 종합하여 공격 전체 타임라인 재구성

### 실무 적용 아이디어

**SOC 분석가 관점:**
- **Apache 로그 실시간 분석 자동화:** Python 스크립트로 실시간 로그 읽기. SQL Injection(`union`, `select`, `--`), XSS(`<script>`, `javascript:`), Path Traversal(`../`) 패턴을 정규표현식으로 탐지. 임계값 초과 시 Slack/Email 알림. SIEM 연동 전 1차 필터링 도구로 활용
- **SetEnvIf 기반 로그 최적화:** 내부 네트워크 대역(10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)을 SetEnvIf로 "internal" 환경변수 설정 -> `CustomLog env=!internal`로 외부 IP만 수집. 로그 볼륨 50% 절감
- **생체 인증 FAR/FRR 모니터링:** 출입통제 시스템의 인증 성공/실패 로그를 일별로 수집하여 FRR/FAR 지표 계산. FAR이 임계값(0.01%) 초과 시 인증 시스템 오작동이나 위변조 공격 가능성 의심

**보안 아키텍처 설계 - 3-Tier 웹 보안:**
- Tier 1 (Web): Apache + ModSecurity (WAF)로 SQL Injection/XSS 1차 차단
- Tier 2 (App): Prepared Statement + 입력값 검증 (replaceAll, 화이트리스트)로 2차 방어
- Tier 3 (DB): 최소 권한 DB 계정 + 저장 프로시저로 3차 방어
- 각 계층마다 로그를 SIEM으로 중앙 수집 -> 공격 경로 전체 추적 가능

---

## 7. Quick Reference

### Apache 명령어 모음

**서비스 관리:**
- `systemctl start apache2` - 시작
- `systemctl stop apache2` - 중지
- `systemctl restart apache2` - 재시작
- `systemctl reload apache2` - 설정 다시 로드 (연결 유지)
- `systemctl status apache2` - 상태 확인
- `systemctl enable apache2` - 부팅 시 자동 시작

**설정 검증:**
- `apache2ctl configtest` - 설정 파일 문법 검사
- `apache2ctl -M` - 로드된 모듈 목록
- `apache2ctl -S` - VirtualHost 설정 요약
- `apache2 -v` - Apache 버전

**로그 관리:**
- `tail -f /var/log/apache2/access.log` - 접근 로그 실시간
- `tail -f /var/log/apache2/error.log` - 에러 로그 실시간
- `grep "404" /var/log/apache2/access.log` - 404 에러 검색
- `grep "192.168.1.100" /var/log/apache2/access.log` - 특정 IP 검색

**모듈 관리:**
- `a2enmod ssl` - SSL 모듈 활성화
- `a2dismod autoindex` - 디렉터리 인덱싱 비활성화
- `a2enmod headers` - 헤더 모듈 활성화
- `a2enmod rewrite` - URL 재작성 모듈 활성화

**로그 분석 명령어:**
- 가장 많이 접속한 IP 상위 10개: `awk '{print $1}' /var/log/apache2/access.log | sort | uniq -c | sort -rn | head -10`
- 가장 많이 요청된 URL 상위 10개: `awk '{print $7}' /var/log/apache2/access.log | sort | uniq -c | sort -rn | head -10`
- SQL Injection 시도 패턴: `grep -E "(union|select|'|--)" /var/log/apache2/access.log`
- XSS 시도 패턴: `grep -E "(<script|javascript:|onerror)" /var/log/apache2/access.log`

### 보안 개념 핵심 요약표

| 구분 | 항목 | 핵심 키워드 | 주요 내용 | 적용 방법 |
|:---:|:---|:---|:---|:---|
| **인증** | 패스워드 | ROT13/47, 암호화 | 세 종류 이상 문자 조합, 변형 저장 | rot13.com, 엑셀 암호화 |
| **인증** | 공인인증서 | PKI, X.509 | 공개키 기반, 전자 신분증 | signCert.der, signPri.key |
| **인증** | 생체 인증 | FRR, FAR, EER | 지문/홍채/얼굴, 성능 지표 | FAR < 0.01%, EER 최소화 |
| **접근통제** | DAC | 임의적, rwx | 소유자가 권한 결정 | chmod 755, chown |
| **접근통제** | Bell-LaPadula | 기밀성, No read up | 상위 정보 읽기 금지 | 군사/정부 기밀 |
| **접근통제** | Biba | 무결성, No write up | 상위 정보 쓰기 금지 | 금융 거래 데이터 |
| **접근통제** | RBAC | 역할 기반 | 직책에 권한 할당 | 기업 ERP/그룹웨어 |
| **입력검증** | SQL Injection | Prepared Statement | 파라미터 바인딩 | setString(), setInt() |
| **입력검증** | XSS | HTML Entity | `<` -> `&lt`, `>` -> `&gt` | replaceAll() 메서드 |
| **입력검증** | File Upload | 화이트리스트 | 허용 확장자만 업로드 | .hwp, .doc, .pdf만 허용 |
| **웹서버** | Options | Indexes, FollowSymLinks | 디렉터리 리스팅 차단 | Options -Indexes |
| **웹서버** | ServerTokens | Prod | 서버 버전 정보 숨김 | ServerTokens Prod |
| **웹서버** | CustomLog | combined, common | 접근 로그 형식 | %h %l %u %t "%r" %>s %O |
| **웹서버** | SetEnvIf | dontlog, internal | 로그 필터링 | env=!dontlog |
| **웹서버** | ModSecurity | WAF, CRS | 웹 방화벽 | SecRuleEngine On |

### 웹 보안 점검 체크리스트

**사용자 인증:**
- [ ] 패스워드 정책 수립 (8자 이상, 3종 조합)
- [ ] 패스워드 변형 저장 (ROT 암호화 등)
- [ ] 공인인증서 유효기간 점검 (만료 전 갱신)
- [ ] 2FA/MFA 적용 여부 확인
- [ ] 생체 인증 FAR < 0.01% 유지

**접근 통제:**
- [ ] 역할 기반 권한 관리(RBAC) 적용
- [ ] 최소 권한 원칙 준수
- [ ] 관리자 계정 활동 감사 로그
- [ ] 주기적 권한 검토 (분기별)
- [ ] 직무 분리 및 직무 교대

**입력값 검증:**
- [ ] Prepared Statement 사용 (SQL Injection 방어)
- [ ] HTML Entity 치환 (XSS 방어)
- [ ] 파일 업로드 화이트리스트 검증
- [ ] 서버 측 필터링 필수 적용
- [ ] CSRF 토큰 검증

**Apache 웹 서버:**
- [ ] Options -Indexes -FollowSymLinks 설정
- [ ] ServerTokens Prod, ServerSignature Off
- [ ] 민감 파일 접근 차단 (.htaccess, .git, .env)
- [ ] SSL/TLS 1.2 이상만 허용
- [ ] 보안 헤더 적용 (X-Frame-Options, CSP)
- [ ] ModSecurity (WAF) 설치 및 활성화
- [ ] 로그 파일 권한 640 이하
- [ ] 로그 6개월 이상 보관
- [ ] Fail2ban 설정 (Brute Force 방어)

---

## 8. 트러블슈팅

| 문제 | 원인 | 해결 방법 |
|:---|:---|:---|
| **Apache 시작 실패** | 포트 80 이미 사용 중 | `netstat -tuln | grep :80`으로 프로세스 확인, `kill -9 PID`로 기존 프로세스 종료, 또는 ports.conf에서 Listen 8080으로 변경 |
| **Forbidden (403) 지속** | 디렉터리 권한 부족 | `chmod 755 /var/www/html`, `chown www-data:www-data /var/www/html`, apache2.conf에서 Require all granted 확인 |
| **디렉터리 리스팅 차단 안 됨** | Indexes 옵션 여전히 존재 | apache2.conf의 모든 Directory 블록 확인, `Options -Indexes` 설정 (하이픈 필수), `systemctl restart apache2` |
| **ModSecurity 오탐** | 정상 요청을 공격으로 판단 | /var/log/apache2/modsec_audit.log 확인, 특정 룰 ID 비활성화: SecRuleRemoveById 950901, 화이트리스트 추가 |
| **로그 파일 급격히 증가** | 정적 파일, 내부 IP 로그 과다 | SetEnvIf 활용하여 정적 파일 및 내부 IP 제외, logrotate 설정: /etc/logrotate.d/apache2 |
| **SSL 인증서 오류** | 인증서 만료 또는 경로 오류 | `openssl x509 -in cert.pem -text -noout` 유효기간 확인, SSLCertificateFile/SSLCertificateKeyFile 경로 확인, Let's Encrypt: `certbot renew` |
| **SetEnvIf 동작 안 함** | 정규표현식 오류 | 역슬래시 이스케이프: `"127\.0\.0\.1"`, 대소문자 구분 주의, `apache2ctl -M | grep setenvif` 모듈 확인 |
| **access.log에 IP 대신 -** | 역방향 DNS 조회 실패 | `HostnameLookups Off` 설정 (성능 향상), 또는 HostnameLookups On + DNS 서버 확인 |

---

**Today's Insight:**

웹 보안의 핵심은 3단계 방어 체계다. 1단계 인증(Authentication)은 패스워드부터 생체 인증까지 진화하며, 생체 인증의 FAR과 FRR 균형이 중요하다. 2단계 접근 통제(Access Control)는 DAC의 유연성, Bell-LaPadula의 기밀성, Biba의 무결성, RBAC의 실용성을 상황에 맞게 적용한다. 3단계 입력값 검증(Input Validation)은 서버 측 필터링과 화이트리스트 방식이 필수다.

Apache 웹 서버 실습을 통해 이론이 실무로 연결되는 과정을 체감했다. `Options -Indexes` 하나로 디렉터리 리스팅을 차단하고, `SetEnvIf`로 로그를 필터링하며, `CustomLog`로 SOC 분석에 필요한 정보만 수집하는 기법은 즉시 적용 가능하다. 로그 분석 시 `union select`, `<script>`, `../` 같은 패턴을 정규표현식으로 탐지하는 것은 SOC 분석가의 기본기이며, 이를 Python으로 자동화하면 침해사고 대응 속도를 크게 높일 수 있다.

앞으로는 ModSecurity(WAF) 룰셋 커스터마이징, SIEM과 Apache 로그 연동, Burp Suite를 활용한 웹 애플리케이션 취약점 진단으로 학습이 이어져야 한다. 웹 보안은 "방어자가 모든 문을 잠가야 하지만, 공격자는 하나의 문만 열면 된다"는 비대칭 게임이므로, 다층 방어(Defense in Depth) 전략이 필수다.
