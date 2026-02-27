---
title: "2025.12.17 (Day 37) - VMware 3-Tier Architecture 구성 실습"
date: 2025-12-17
draft: false
tags: ["VMware", "3-Tier", "Nginx", "Tomcat", "MariaDB", "Linux", "systemctl", "리버스프록시", "보안"]
categories: ["daily-logs"]
summary: "VMware Workstation으로 Web(Nginx)/WAS(Tomcat)/DB(MariaDB) 3계층 아키텍처 구성, 리버스 프록시 설정, 계층별 보안 강화 실습"
---

# 📄 2025.12.17 (Day 37) - VMware 3-Tier Architecture 구성 실습

---

## 1. 핵심 개념 정리

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| **1** | **3-Tier Architecture** | 애플리케이션을 Presentation Tier(웹 서버), Application Tier(비즈니스 로직), Data Tier(데이터베이스)로 분리한 아키텍처. 각 계층이 독립적으로 동작하며 서로 다른 서버에 배치 | **보안 계층화(Defense in Depth)의 기본**. DMZ에 웹 서버 배치로 직접 공격 표면 제한, DB는 가장 안쪽에 격리. 한 계층 침투 시에도 다른 계층 보호 |
| **2** | **VMware Workstation** | 물리적 컴퓨터 위에서 여러 가상 머신(VM)을 실행하는 하이퍼바이저 소프트웨어. Type 2 하이퍼바이저로 호스트 OS 위에서 동작 | 안전한 실습 환경 구축 가능. 스냅샷으로 실수 시 즉시 복구. VM 간 네트워크 격리로 호스트 시스템 보호. 멀웨어 분석, 취약점 테스트 시 샌드박스 역할 |
| **3** | **Nginx (웹 서버)** | 고성능 HTTP 웹 서버, 리버스 프록시, 로드 밸런서. 비동기 이벤트 기반 아키텍처로 낮은 메모리로 많은 동시 연결 처리 | 리버스 프록시로 백엔드 서버 IP 숨김. Rate limiting으로 DDoS 완화. SSL/TLS 설정으로 암호화 통신. 보안 헤더(X-Frame-Options, CSP) 추가 |
| **4** | **Apache Tomcat (WAS)** | Java 기반 웹 애플리케이션 서버(WAS). Servlet과 JSP를 실행하여 동적 웹 콘텐츠 생성. 기본 포트 8080에서 실행 | Manager 앱 기본 계정 변경 필수. AJP 커넥터 비활성화(Ghostcat 취약점). 불필요한 예제 애플리케이션 삭제 |
| **5** | **MariaDB (데이터베이스)** | MySQL 기반 오픈소스 관계형 데이터베이스. 기본 포트 3306에서 실행, /etc/mysql/ 디렉토리에 설정 파일 위치 | Root 계정 원격 접속 차단(localhost만 허용). 애플리케이션별 전용 계정 생성, 최소 권한 부여. bind-address를 내부 IP로 제한 |
| **6** | **systemctl (시스템 관리)** | Systemd 기반 리눅스에서 서비스를 관리하는 명령어. 시작/중지/재시작, 자동 실행 설정, 상태 확인 기능 | enable로 부팅 시 자동 시작 보장. status로 실시간 서비스 상태 확인. 불필요한 서비스 disable로 공격 표면 축소 |
| **7** | **리버스 프록시 (Reverse Proxy)** | 클라이언트 요청을 받아 백엔드 서버로 전달하는 중계 서버. Nginx가 80포트로 요청 수신 후 Tomcat 8080포트로 프록시 | 백엔드 서버 IP/포트 숨김으로 직접 공격 차단. SSL/TLS는 Nginx에서만 처리(백엔드 부담 감소). Rate limiting, IP 필터링 중앙 적용 |
| **8** | **방화벽 포트 구성** | 네트워크 트래픽을 포트 번호로 제어하는 보안 설정. HTTP(80), HTTPS(443), SSH(22), MySQL(3306), Tomcat(8080) 등 | 웹 서버: 80/443만 외부 개방. WAS: 8080은 웹 서버에서만 접근. DB: 3306은 WAS에서만 접근. SSH: 22는 관리자 IP만 허용 |
| **9** | **원격 접속 (SSH)** | Secure Shell 프로토콜로 원격 서버를 안전하게 관리. 공개키 인증 또는 비밀번호 인증 지원. 기본 포트 22 | Root 직접 로그인 금지(PermitRootLogin no). 기본 포트 22 변경으로 자동화 공격 회피. Fail2ban으로 brute force 차단 |
| **10** | **런레벨 / Target** | 리눅스 시스템의 부팅 모드 정의. multi-user.target(CLI 모드, 런레벨 3), graphical.target(GUI 모드, 런레벨 5) | GUI 불필요 시 multi-user.target으로 메모리/CPU 절약. 공격 표면 축소(GUI 관련 서비스 미실행) |

---

## 2. 아키텍처 구성도

3-Tier 아키텍처 네트워크 구성:

- 사용자/클라이언트
  - HTTP/HTTPS (Port 80/443)
  - **VM1: Web Server (Nginx)** - IP: 192.168.186.128, Port 80
    - Reverse Proxy (Port 8080)
    - **VM2: WAS Server (Tomcat)** - IP: 192.168.186.129, Port 8080
      - JDBC Connection (Port 3306)
      - **VM3: DB Server (MariaDB)** - IP: 192.168.186.130, Port 3306

보안 규칙:
- 외부 -> Web: 80, 443 허용
- Web -> WAS: 8080 허용
- WAS -> DB: 3306 허용
- 관리자 -> All: SSH 22 허용 (특정 IP만)
- 기타 모든 포트: 차단

---

## 3. 실습 내용

### (A) VMware 환경 준비 및 초기 설정

**VMware Workstation 설치 및 Ubuntu VM 생성 (3대):**
- VMware -> "Create a New Virtual Machine" -> Typical 선택
- ISO 이미지: Ubuntu 24.04 LTS Desktop ISO
- Computer name: webserver / wasserver / dbserver
- Disk size: 20GB, Memory: 4GB, Processors: 2 cores
- Network Adapter: NAT 또는 Bridged

**Ubuntu 초기 설정 (3대 모두):**
- **sudo su** - root 권한 전환
- **apt-get update** - 패키지 목록 갱신
- **apt-get install -y net-tools openssh-server vim curl wget** - 필수 패키지 설치
- **apt-get upgrade -y** - 시스템 업그레이드
- **ifconfig** 또는 **ip addr show** - IP 주소 확인
  - webserver: 192.168.186.128
  - wasserver: 192.168.186.129
  - dbserver: 192.168.186.130

**GUI -> CLI 모드 전환 (리소스 절약):**
- **sudo systemctl set-default multi-user.target** - CLI 모드로 기본 설정 변경
- **reboot** - 재부팅 후 CLI 화면으로 로그인

**SSH 접속:**
- **ssh student@192.168.186.128** - 이후 작업은 SSH로 진행

---

### (B) Tier 1: Web Server (Nginx) 구성

**Nginx 설치 및 설정 (VM1: 192.168.186.128):**

1. 설치:
   - **apt-get install nginx -y**

2. 설치 확인:
   - **netstat -antp | grep nginx** 또는 **ss -tlnp | grep nginx** - 80포트 리스닝 확인
   - **nginx -v** - 버전 확인

3. 자동 실행 설정:
   - **systemctl enable nginx** - 부팅 시 자동 시작
   - **systemctl start nginx** - 서비스 시작
   - **systemctl status nginx** - "active (running)" 확인
   - **nginx -t** - 설정 파일 문법 검사

4. 기본 웹 페이지 수정:
   - **rm -f /var/www/html/index.nginx-debian.html** - 기본 페이지 삭제
   - **vi /var/www/html/index.html** - 새 페이지 작성

5. 접속 테스트:
   - **curl http://192.168.186.128** - curl로 테스트
   - **tail -f /var/log/nginx/access.log** - 접근 로그 확인
   - **tail -f /var/log/nginx/error.log** - 에러 로그 확인

**Nginx 주요 파일 구조:**
- /etc/nginx/nginx.conf - 메인 설정 파일
- /etc/nginx/sites-available/default - 기본 사이트 설정
- /etc/nginx/sites-enabled/default - 활성화된 설정 (심볼릭 링크)
- /var/www/html/ - 웹 문서 루트 디렉토리
- /var/log/nginx/access.log - 접근 로그
- /var/log/nginx/error.log - 에러 로그

---

### (C) Tier 2: WAS Server (Tomcat) 구성

**Tomcat 설치 및 설정 (VM2: 192.168.186.129):**

1. Java JDK 설치 (Tomcat 실행 필수):
   - **apt-get install -y openjdk-17-jdk**
   - **java -version** - 설치 확인

2. Tomcat 다운로드 및 설치:
   - **cd /tmp** -> **wget** [Tomcat 10.x 다운로드 URL]
   - **tar -xzf apache-tomcat-10.1.28.tar.gz**
   - **mv apache-tomcat-10.1.28 /opt/tomcat**
   - **useradd -r -m -U -d /opt/tomcat -s /bin/false tomcat** - 전용 계정 생성
   - **chown -R tomcat:tomcat /opt/tomcat/** - 소유권 변경

3. Systemd 서비스 등록 (/etc/systemd/system/tomcat.service):
   - Unit: After=network.target
   - Service: Type=forking, User=tomcat, Group=tomcat
   - Environment: JAVA_HOME, CATALINA_HOME=/opt/tomcat
   - ExecStart=/opt/tomcat/bin/startup.sh
   - Restart=always

4. Tomcat 서비스 시작:
   - **systemctl daemon-reload** - Systemd 데몬 리로드
   - **systemctl start tomcat** - 시작
   - **systemctl enable tomcat** - 자동 시작 설정
   - **netstat -antp | grep 8080** - 포트 8080 리스닝 확인

5. JSP 테스트 페이지 생성:
   - **vi /opt/tomcat/webapps/ROOT/index.jsp** - JSP 테스트 페이지 작성
   - **chown -R tomcat:tomcat /opt/tomcat/webapps/**
   - **systemctl restart tomcat**
   - 브라우저: http://192.168.186.129:8080 접속 확인

6. 로그 확인:
   - **tail -f /opt/tomcat/logs/catalina.out** - 주 로그
   - **tail -f /opt/tomcat/logs/localhost_access_log.*.txt** - 접근 로그

---

### (D) Nginx -> Tomcat 리버스 프록시 설정

**Nginx 리버스 프록시 설정 (VM1):**

1. 설정 파일 백업:
   - **cd /etc/nginx/sites-available/** -> **cp default default.bak**

2. /etc/nginx/sites-available/default 주요 설정:
   - listen 80 default_server
   - access_log /var/log/nginx/proxy_access.log
   - location / 블록:
     - **proxy_pass http://192.168.186.129:8080** - Tomcat으로 프록시
     - proxy_set_header Host $host
     - proxy_set_header X-Real-IP $remote_addr
     - proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for
     - proxy_connect_timeout 60s

3. 설정 적용:
   - **nginx -t** - 문법 검사
   - **systemctl restart nginx**

4. 프록시 동작 확인:
   - 브라우저: http://192.168.186.128 -> Tomcat JSP 페이지가 표시됨
   - **curl -I http://192.168.186.128** - 응답 헤더 확인

**리버스 프록시 동작 흐름:**

클라이언트 (192.168.186.1)
-> ① HTTP 요청: http://192.168.186.128/
-> Nginx (192.168.186.128:80)
-> ② 프록시: http://192.168.186.129:8080/
-> Tomcat (192.168.186.129:8080)
-> ③ JSP 실행, HTML 생성
-> ④ HTTP 응답 반환
-> 클라이언트

---

### (E) Tier 3: Database Server (MariaDB) 구성

**MariaDB 설치 및 설정 (VM3: 192.168.186.130):**

1. 설치:
   - **apt-get install -y mariadb-server**
   - **systemctl enable mariadb** -> **systemctl start mariadb**
   - **netstat -antp | grep LISTEN | grep 3306** - 포트 확인

2. 보안 설정 (mysql_secure_installation):
   - Root 비밀번호 설정
   - 익명 사용자 제거 (Remove anonymous users: Y)
   - Root 원격 로그인 비허용 (Disallow root login remotely: Y)
   - 테스트 DB 삭제 (Remove test database: Y)

3. 원격 접속 허용 (bind-address 변경):
   - **vi /etc/mysql/mariadb.conf.d/50-server.cnf**
   - bind-address = 127.0.0.1 -> **bind-address = 0.0.0.0** 으로 변경
   - **systemctl restart mariadb**

4. 원격 접속용 사용자 생성 (MariaDB 프롬프트):
   - **mysql -u root -p** -> 접속
   - CREATE USER 'mydb'@'%' IDENTIFIED BY 'abcd1234'
   - GRANT ALL PRIVILEGES ON *.* TO 'mydb'@'%' WITH GRANT OPTION
   - FLUSH PRIVILEGES
   - SELECT user, host FROM mysql.user WHERE user='mydb' - 확인

5. 방화벽 설정:
   - **ufw allow from 192.168.186.129 to any port 3306** - WAS에서만 허용

6. 테스트 DB 및 테이블 생성:
   - CREATE DATABASE testdb
   - USE testdb
   - CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), email VARCHAR(100), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
   - INSERT INTO users (username, email) VALUES ('admin', 'admin@example.com'), ('user1', 'user1@example.com')
   - SELECT * FROM users - 데이터 확인

**WAS에서 DB 연결 테스트 (VM2):**
- **apt-get install -y mariadb-client-core**
- **mysql -u mydb -p -h 192.168.186.130** - DB 서버 접속
- **wget** [JDBC Connector JAR] -> **/opt/tomcat/lib/** 에 배치
- dbtest.jsp 생성 후 http://192.168.186.128/dbtest.jsp 로 전체 연동 확인

**3-Tier 전체 연동 흐름:**

클라이언트 -> http://192.168.186.128/dbtest.jsp
-> Nginx (Tier 1, 리버스 프록시)
-> Tomcat (Tier 2, JSP 실행)
-> MariaDB (Tier 3, SELECT * FROM users)
-> 결과 반환 -> HTML 생성 -> 클라이언트에 응답

---

## 4. 실무/보안 관점 분석

| 분야 | 적용 시나리오 |
|:---:|:---|
| **3-Tier 보안 아키텍처** | 계층별 격리: Web(DMZ) -> WAS(내부망) -> DB(최내부) 배치로 공격자가 한 계층 침투 시에도 다른 계층 보호. 최소 권한 원칙: 각 계층은 필요한 포트/서비스만 실행. 리버스 프록시: Nginx가 Tomcat 앞단에서 SSL 종료, Rate Limiting, IP 필터링 수행 |
| **Nginx 보안 강화** | server_tokens off로 버전 정보 숨김. limit_req_zone으로 Rate Limiting. allow/deny로 IP 화이트리스트. X-Frame-Options, X-Content-Type-Options, CSP 보안 헤더 추가. Access log로 모든 요청 기록 |
| **Tomcat 보안 강화** | Manager 앱 기본 계정 삭제, 강력한 비밀번호, 특정 IP만 접근 허용. 불필요한 예제 앱(examples, docs, host-manager) 삭제. AJP 포트 주석 처리(Ghostcat 취약점 방지). 상세 에러 메시지 숨김 |
| **MariaDB 보안 강화** | Root 원격 접속 차단(localhost만). 애플리케이션별 전용 계정: GRANT SELECT, INSERT ON testdb.* TO 'appuser'@'192.168.186.129'. bind-address를 WAS IP로 제한. Slow Query Log로 SQL Injection 의심 쿼리 탐지 |
| **네트워크 보안** | ufw allow from 192.168.186.128 to any port 8080 (WAS). ufw allow from 192.168.186.129 to any port 3306 (DB). SSH 키 인증 사용, PermitRootLogin no. Fail2ban으로 brute force 차단 |
| **로그 관리 및 모니터링** | ELK Stack(Elasticsearch, Logstash, Kibana)으로 실시간 로그 분석. 실패한 로그인 10회, SQL Injection 시도 탐지 시 알림. 로그 최소 1년 보관 |

---

## 5. 배운 점 및 심화 방향

- **배운 점**: 3-Tier 아키텍처를 VMware로 직접 구현하니 각 계층의 역할과 상호작용이 명확해졌다. 리버스 프록시를 통해 백엔드 서버 보호, SSL 종료, 로드 밸런싱 등 다양한 기능을 한 곳에서 처리할 수 있다는 점이 인상 깊었다. bind-address를 0.0.0.0으로 변경하는 순간 외부에서 DB 접근 가능해지는 위험성을 체감했다. MariaDB JDBC URL이 jdbc:mysql://로 동일하게 사용 가능하다는 점도 알게 됐다.
- **심화 방향**: HTTPS 적용(Let's Encrypt), Nginx upstream 블록으로 로드 밸런싱 구성, Docker 컨테이너화 후 Docker Compose로 자동 구성, Nginx에 ModSecurity WAF 연동(OWASP CRS 룰셋), Prometheus + Grafana 모니터링, ELK Stack 로그 중앙화, Ansible Playbook으로 3-Tier 환경 자동 구성.

---

## 6. Quick Reference

### 주요 명령어 모음

**시스템 관리:**
- **sudo su** - root 권한 전환
- **apt-get update && apt-get upgrade -y** - 패키지 업데이트
- **uname -a** - 커널 정보
- **free -h** - 메모리 사용량
- **df -h** - 디스크 사용량

**네트워크:**
- **ifconfig** / **ip addr show** - IP 주소 확인
- **ping 192.168.186.129** - 연결 테스트
- **netstat -antp | grep LISTEN** - 포트 리스닝 확인
- **ss -tlnp** - 소켓 상태 확인
- **ufw status** - 방화벽 상태 확인

**서비스 관리:**
- **systemctl start|stop|restart nginx** - 서비스 제어
- **systemctl status nginx** - 상태 확인
- **systemctl enable|disable nginx** - 자동 시작 설정
- **journalctl -u nginx -f** - 실시간 로그

**로그 확인:**
- **tail -f /var/log/nginx/access.log** - Nginx 접근 로그
- **tail -f /opt/tomcat/logs/catalina.out** - Tomcat 주 로그
- **tail -f /var/log/mysql/error.log** - MariaDB 에러 로그
- **tail -f /var/log/auth.log** - SSH 로그인 이력

### 포트 및 프로토콜 참조표

| 서비스 | 포트 | 프로토콜 | 용도 |
|:---:|:---:|:---:|:---|
| HTTP | 80 | TCP | 웹 서버 (암호화 없음) |
| HTTPS | 443 | TCP | 웹 서버 (SSL/TLS 암호화) |
| SSH | 22 | TCP | 원격 접속 |
| Tomcat | 8080 | TCP | WAS (HTTP Alternative) |
| Tomcat AJP | 8009 | TCP | Nginx 연동 (비활성화 권장) |
| MySQL/MariaDB | 3306 | TCP | 데이터베이스 |
| Redis | 6379 | TCP | 인메모리 DB/캐시 |

### 보안 체크리스트

**Nginx:**
- [ ] server_tokens off (버전 정보 숨김)
- [ ] SSL/TLS 설정 (HTTPS 적용)
- [ ] Rate Limiting 설정
- [ ] 보안 헤더 추가 (X-Frame-Options, CSP 등)
- [ ] 불필요한 HTTP 메서드 차단 (TRACE, OPTIONS 등)

**Tomcat:**
- [ ] Manager 앱 기본 계정 변경 또는 삭제
- [ ] 불필요한 예제 앱 삭제 (examples, docs, host-manager)
- [ ] AJP 커넥터 비활성화 (Ghostcat 취약점)
- [ ] 에러 페이지 커스터마이징 (상세 정보 숨김)

**MariaDB:**
- [ ] Root 원격 접속 차단 (localhost만 허용)
- [ ] 애플리케이션별 전용 계정 생성
- [ ] 최소 권한 부여 (필요한 DB/테이블만)
- [ ] bind-address를 특정 IP로 제한
- [ ] 강력한 비밀번호 정책 적용
