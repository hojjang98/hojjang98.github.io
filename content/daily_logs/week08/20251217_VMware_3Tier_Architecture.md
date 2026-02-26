---
title: "2025.12.17 (Day 37) VMware 3-Tier Architecture 구성 실습"
date: 2025-12-17
draft: false
tags: ["VMware", "3Tier", "Nginx", "Tomcat", "MariaDB", "리눅스", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "VMware로 Web(Nginx) - WAS(Tomcat) - DB(MariaDB) 3계층 아키텍처 구축 및 리버스 프록시 설정 실습"
---

# 📄 2025.12.17 (Day 37) [VMware 3-Tier Architecture 구성 실습]

> **Note**: 이 문서는 수업에서 제공된 명령어와 설정을 참고하여, 실제 환경에서 직접 구현하고 테스트한 내용을 기록한 것입니다. 수업 코드를 그대로 복사한 것이 아니라, 학습 과정에서 이해한 내용을 바탕으로 재구성하였습니다.

## 1. 핵심 개념 정리 (Concepts & Theory)

| # | 핵심 개념 | 간결한 설명 | 실무/보안 관점에서의 중요성 |
|:---:|:---|:---|:---|
| **1** | **3-Tier Architecture** | 애플리케이션을 **Presentation Tier**(웹 서버), **Application Tier**(비즈니스 로직), **Data Tier**(데이터베이스)로 분리한 아키텍처입니다. 각 계층이 독립적으로 동작하며 서로 다른 서버에 배치됩니다. 확장성, 유지보수성, 보안성이 향상되며 계층 간 통신은 정의된 인터페이스로만 이루어집니다. | **보안 계층화(Defense in Depth)의 기본**입니다. DMZ에 웹 서버 배치로 직접 공격 표면 제한, 애플리케이션 서버는 내부망에서 비즈니스 로직 처리, 데이터베이스는 가장 안쪽에 격리. 각 계층마다 방화벽 규칙 적용 가능. 한 계층 침투 시에도 다른 계층 보호. 역할 분리로 권한 관리 명확화. |
| **2** | **VMware Workstation** | 물리적 컴퓨터 위에서 **여러 가상 머신(VM)을 실행**하는 하이퍼바이저 소프트웨어입니다. 하나의 호스트 시스템에서 다양한 OS를 동시 실행 가능. VM 간 격리, 스냅샷, 복제, 네트워크 구성 기능 제공. 개발, 테스트, 교육 환경에 적합합니다. Type 2 하이퍼바이저로 호스트 OS 위에서 동작합니다. | **안전한 실습 환경 구축**이 가능합니다. 실제 인프라 구성 없이 멀티 서버 환경 구현. 스냅샷으로 실수 시 즉시 복구. VM 간 네트워크 격리로 호스트 시스템 보호. 멀웨어 분석, 취약점 테스트 시 샌드박스 역할. 클라우드 마이그레이션 전 온프레미스 시뮬레이션. |
| **3** | **Nginx (웹 서버)** | 고성능 **HTTP 웹 서버, 리버스 프록시, 로드 밸런서**입니다. 비동기 이벤트 기반 아키텍처로 낮은 메모리로 많은 동시 연결 처리. 정적 콘텐츠 서빙, SSL/TLS 종료, 요청 라우팅, 캐싱 기능 제공. Apache보다 가볍고 빠르며, 설정 파일은 `/etc/nginx/` 디렉토리에 위치합니다. | **웹 계층 보안의 최전선**입니다. 리버스 프록시로 백엔드 서버 IP 숨김. Rate limiting으로 DDoS 완화. SSL/TLS 설정으로 암호화 통신. 헤더 조작으로 서버 정보 숨김. Access log로 모든 요청 기록. 보안 헤더(X-Frame-Options, CSP) 추가. Fail2ban 연동으로 공격 IP 자동 차단. |
| **4** | **Apache Tomcat (WAS)** | Java 기반 **웹 애플리케이션 서버(WAS)**입니다. Servlet과 JSP를 실행하여 동적 웹 콘텐츠 생성. Java EE 표준 구현으로 비즈니스 로직 처리. 기본 포트 8080에서 실행되며, `/opt/tomcat` 또는 `/usr/share/tomcat` 디렉토리 구조 사용. Manager 앱으로 애플리케이션 배포/관리 가능합니다. | **애플리케이션 계층 보안**이 중요합니다. Manager 앱 기본 계정 변경 필수. AJP 커넥터 비활성화(Ghostcat 취약점). 불필요한 예제 애플리케이션 삭제. HTTPS Connector 설정으로 암호화. 접근 로그 활성화로 의심 활동 추적. JVM 보안 옵션 설정. 최신 패치 유지로 취약점 대응. |
| **5** | **MariaDB (데이터베이스)** | MySQL 기반 **오픈소스 관계형 데이터베이스**입니다. MySQL과 호환되며 성능 개선과 추가 기능 제공. SQL 쿼리로 데이터 CRUD 작업 수행. 기본 포트 3306에서 실행되며, `/etc/mysql/` 디렉토리에 설정 파일 위치. 사용자 계정 및 권한 관리 기능 제공합니다. | **데이터 보안의 핵심**입니다. Root 계정 원격 접속 차단(localhost만 허용). 애플리케이션별 전용 계정 생성, 최소 권한 부여. `bind-address`를 내부 IP로 제한. 강력한 비밀번호 정책 적용. SSL/TLS 암호화 연결 설정. 정기 백업 자동화. Slow query log로 SQL Injection 의심 쿼리 탐지. |
| **6** | **systemctl (시스템 관리)** | Systemd 기반 리눅스에서 **서비스를 관리**하는 명령어입니다. 서비스 시작/중지/재시작(`start/stop/restart`), 부팅 시 자동 실행 설정(`enable/disable`), 상태 확인(`status`) 기능 제공. Unit 파일로 서비스 정의하며, `/etc/systemd/system/` 디렉토리에 위치합니다. | **서비스 안정성과 모니터링**입니다. `enable`로 부팅 시 자동 시작 보장(서비스 중단 방지). `status`로 실시간 서비스 상태 확인. 서비스 재시작 시 설정 변경 반영. 서비스 실패 시 자동 재시작 설정(Restart=always). 로그는 `journalctl`로 확인. 불필요한 서비스 `disable`로 공격 표면 축소. |
| **7** | **리버스 프록시 (Reverse Proxy)** | 클라이언트 요청을 받아 **백엔드 서버로 전달**하는 중계 서버입니다. Nginx가 80포트로 요청 수신 후 Tomcat 8080포트로 프록시. 클라이언트는 백엔드 서버 존재를 모릅니다. 로드 밸런싱, SSL 종료, 캐싱, 압축 기능 수행. `proxy_pass` 지시문으로 설정합니다. | **보안과 성능 향상**을 동시에 달성합니다. 백엔드 서버 IP/포트 숨김으로 직접 공격 차단. SSL/TLS는 Nginx에서만 처리(백엔드 부담 감소). 정적 파일은 Nginx에서 직접 서빙(Tomcat 부하 감소). Rate limiting, IP 필터링 중앙 적용. WAF(ModSecurity) 연동 가능. 로그 중앙화. |
| **8** | **방화벽 포트 구성** | 네트워크 트래픽을 **포트 번호로 제어**하는 보안 설정입니다. **HTTP(80)**, **HTTPS(443)**, **SSH(22)**, **MySQL(3306)**, **Tomcat(8080)** 등 서비스마다 표준 포트 존재. `ufw`, `iptables`, `firewalld`로 포트 허용/차단 설정. `netstat`, `ss`로 열린 포트 확인합니다. | **최소 권한 네트워크 접근**입니다. 필요한 포트만 개방(White List 방식). 웹 서버: 80, 443만 외부 개방. WAS: 8080은 웹 서버에서만 접근 허용. DB: 3306은 WAS에서만 접근 허용. SSH: 22는 관리자 IP만 허용. 불필요한 포트 닫아 공격 표면 축소. 포트 스캔 탐지 및 차단. |
| **9** | **원격 접속 (SSH)** | **Secure Shell** 프로토콜로 원격 서버를 안전하게 관리하는 방법입니다. 암호화된 연결로 명령어 실행, 파일 전송 가능. 공개키 인증 또는 비밀번호 인증 지원. 기본 포트 22 사용. PuTTY(Windows), OpenSSH(Linux/Mac) 클라이언트 사용. `sshd` 서비스로 서버에서 실행됩니다. | **안전한 원격 관리**의 기본입니다. 비밀번호보다 SSH 키 인증 권장. Root 직접 로그인 금지(`PermitRootLogin no`). 기본 포트 22 변경으로 자동화 공격 회피. Fail2ban으로 brute force 차단. 특정 IP만 접속 허용. 세션 타임아웃 설정. 모든 세션 로그 기록(`/var/log/auth.log`). |
| **10** | **런레벨 (Runlevel) / Target** | 리눅스 시스템의 **부팅 모드**를 정의합니다. Systemd에서는 Target으로 대체. **multi-user.target**(CLI 모드, 런레벨 3), **graphical.target**(GUI 모드, 런레벨 5)가 주요 모드. `systemctl set-default`로 기본 부팅 모드 변경. 서버는 일반적으로 CLI 모드 사용합니다. | **서버 리소스 최적화**입니다. GUI 불필요 시 multi-user.target으로 메모리/CPU 절약. 공격 표면 축소(GUI 관련 서비스 미실행). 서버 안정성 향상(X Window 충돌 없음). 원격 관리 중심 환경에 적합. 필요 시 `startx`로 임시 GUI 실행 가능. |

---

## 2. 실습 코드 & 응용 (Practice & Code Walkthrough)

### 아키텍처 구성도

[사용자/클라이언트]  
        |  
        | HTTP/HTTPS (Port 80/443)  
        ↓  
+------------------+  
|   Web Server     |  ← VM1: Ubuntu 24.04  
|   (Nginx)        |     IP: 192.168.186.128  
|   Port: 80       |  
+------------------+  
        |  
        | Reverse Proxy (Port 8080)  
        ↓  
+------------------+  
|   WAS Server     |  ← VM2: Ubuntu 24.04  
|   (Tomcat)       |     IP: 192.168.186.129  
|   Port: 8080     |  
+------------------+  
        |  
        | JDBC Connection (Port 3306)  
        ↓  
+------------------+  
|   DB Server      |  ← VM3: Ubuntu 24.04  
|  (MariaDB)       |     IP: 192.168.186.130  
|   Port: 3306     |  
+------------------+  
  
보안 규칙:  
- 외부 → Web: 80, 443 허용  
- Web → WAS: 8080 허용  
- WAS → DB: 3306 허용  
- 관리자 → All: SSH 22 허용 (특정 IP만)  
- 기타 모든 포트: 차단  
```  
  
### (A) VMware 환경 준비 및 초기 설정  
  
**실습 0: VMware 및 Ubuntu 설치**  
  
```bash  
[1단계] VMware Workstation 설치  
1. VMware Workstation Pro/Player 다운로드 및 설치  
2. 라이선스 입력 (Pro) 또는 무료 버전 선택 (Player)  
  
[2단계] Ubuntu 24.04 VM 생성 (3대 반복)  
VMware → "Create a New Virtual Machine"  
  - Typical 선택  
  - ISO 이미지: Ubuntu 24.04 LTS Desktop ISO 선택  
  - Full name: webserver / wasserver / dbserver  
  - Location: 적절한 경로 지정  
  - Disk size: 20GB (기본값)  
  - Memory: 4GB (4096 MB)  
  - Processors: 2 cores  
  - Network Adapter: NAT 또는 Bridged  
  
[3단계] Ubuntu 기본 설치  
1. 언어: English 선택 (한글은 콘솔에서 깨짐)  
2. Keyboard: English (US)  
3. Installation type: Normal installation  
4. 사용자 계정:  
   - Your name: student (예시)  
   - Computer name: webserver / wasserver / dbserver  
   - Username: student  
   - Password: 본인 설정 (예: P@ssw0rd)  
5. 설치 완료 후 재부팅  
  
[4단계] 초기 시스템 설정 (3대 모두)  
# 콘솔 로그인 후  
sudo su  # root 권한 전환  
  
# 필수 패키지 설치  
apt-get update  
apt-get install -y net-tools openssh-server vim curl wget  
  
# 시스템 전체 업그레이드  
apt-get upgrade -y  
  
# IP 주소 확인  
ifconfig  
# 또는  
ip addr show  
  
# 예시 결과:  
# webserver: 192.168.186.128  
# wasserver: 192.168.186.129  
# dbserver:  192.168.186.130  
  
[5단계] GUI → CLI 모드 전환 (선택 사항, 리소스 절약)  
sudo systemctl set-default multi-user.target  
reboot  
  
# 부팅 후 CLI 화면으로 로그인  
# 다시 GUI로 돌아가려면:  
# sudo systemctl set-default graphical.target  
# reboot  
  
[6단계] SSH 접속 테스트 (PuTTY 또는 터미널)  
# Windows: PuTTY 사용  
# Linux/Mac: 터미널 사용  
ssh student@192.168.186.128  
  
# 정상 접속 확인 후 이후 작업은 SSH로 진행  
```  
  
### (B) Tier 1: Web Server (Nginx) 구성  
  
**실습 1: Nginx 웹 서버 설치 및 설정**  
  
```bash  
# ========================================  
# VM1 (webserver) - IP: 192.168.186.128  
# ========================================  
  
[1단계] Nginx 설치  
sudo su  # root 권한 전환  
apt-get install nginx -y  
  
[2단계] 설치 확인  
# Nginx 프로세스 확인  
netstat -antp | grep nginx  
# 출력 예:  
# tcp  0  0 0.0.0.0:80  0.0.0.0:*  LISTEN  1234/nginx: master  
  
# 또는 ss 명령어 사용  
ss -tlnp | grep nginx  
  
# Nginx 버전 확인  
nginx -v  
# 출력 예: nginx version: nginx/1.24.0 (Ubuntu)  
  
[3단계] 자동 실행 설정  
# 부팅 시 자동 시작 활성화  
systemctl enable nginx  
  
# 자동 시작 비활성화 (필요 시)  
# systemctl disable nginx  
  
# 현재 자동 실행 상태 확인  
systemctl is-enabled nginx  
# 출력: enabled  
  
[4단계] 서비스 관리  
# 서비스 시작  
systemctl start nginx  
  
# 서비스 중지  
systemctl stop nginx  
  
# 서비스 재시작 (설정 변경 후 반영)  
systemctl restart nginx  
  
# 서비스 상태 확인  
systemctl status nginx  
# 출력에서 "active (running)" 확인  
  
# 설정 파일 문법 검사  
nginx -t  
# 출력: nginx: configuration file /etc/nginx/nginx.conf syntax is ok  
  
[5단계] 기본 웹 페이지 수정  
# 기본 index.html 삭제  
rm -f /var/www/html/index.nginx-debian.html  
  
# 새로운 index.html 생성  
vi /var/www/html/index.html  
  
# 아래 내용 입력 (vi 에디터: i 눌러 입력 모드, ESC 후 :wq로 저장)  
<html>  
   <head>  
      <title>My Web Server</title>  
   </head>  
   <body>  
      <h1>Hello from Web Server!</h1>  
      <p>This is the Nginx web server (Tier 1)</p>  
      <p>Current time: <script>document.write(new Date().toLocaleString());</script></p>  
   </body>  
</html>  
  
[6단계] 웹 브라우저에서 접속 테스트  
# 호스트 PC의 브라우저에서 접속  
http://192.168.186.128  
  
# 또는 curl 명령어로 테스트  
curl http://192.168.186.128  
  
# 정상 응답: 위에서 작성한 HTML 내용 출력  
  
[7단계] Nginx 로그 확인  
# 접근 로그 (모든 HTTP 요청 기록)  
tail -f /var/log/nginx/access.log  
  
# 에러 로그 (오류 발생 시 기록)  
tail -f /var/log/nginx/error.log  
  
# 로그 형식 예:  
# 192.168.186.1 - - [17/Dec/2024:10:30:45 +0900] "GET / HTTP/1.1" 200 ...  
```  
  
**Nginx 주요 설정 파일 구조**  
  
```bash  
/etc/nginx/  
├── nginx.conf              # 메인 설정 파일  
├── sites-available/        # 사이트 설정 (가용)  
│   └── default             # 기본 사이트 설정  
├── sites-enabled/          # 사이트 설정 (활성화, 심볼릭 링크)  
│   └── default -> ../sites-available/default  
├── conf.d/                 # 추가 설정 파일  
└── modules-enabled/        # 활성화된 모듈  
  
/var/www/html/              # 웹 문서 루트 디렉토리  
└── index.html              # 기본 페이지  
  
/var/log/nginx/             # 로그 디렉토리  
├── access.log              # 접근 로그  
└── error.log               # 에러 로그  


### (C) Tier 2: WAS Server (Tomcat) 구성

**실습 2: Tomcat 웹 애플리케이션 서버 설치**

```bash
# ========================================
# VM2 (wasserver) - IP: 192.168.186.129
# ========================================

[1단계] Java JDK 설치 (Tomcat 실행 필수)
sudo su
apt-get update
apt-get install -y openjdk-17-jdk

# Java 설치 확인
java -version
# 출력 예: openjdk version "17.0.9" ...

# JAVA_HOME 환경 변수 설정
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# 환경 변수 확인
echo $JAVA_HOME

[2단계] Tomcat 다운로드 및 설치
# Tomcat 10.x 다운로드 (최신 버전 확인: https://tomcat.apache.org)
cd /tmp
wget https://dlcdn.apache.org/tomcat/tomcat-10/v10.1.28/bin/apache-tomcat-10.1.28.tar.gz

# 압축 해제
tar -xzf apache-tomcat-10.1.28.tar.gz

# /opt 디렉토리로 이동
mv apache-tomcat-10.1.28 /opt/tomcat

# Tomcat 사용자 생성 (보안 강화)
useradd -r -m -U -d /opt/tomcat -s /bin/false tomcat

# 소유권 변경
chown -R tomcat:tomcat /opt/tomcat/

[3단계] Systemd 서비스 등록
# Tomcat 서비스 파일 생성
vi /etc/systemd/system/tomcat.service

# 아래 내용 입력:
[Unit]
Description=Apache Tomcat Web Application Container
After=network.target

[Service]
Type=forking

User=tomcat
Group=tomcat

Environment="JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64"
Environment="CATALINA_PID=/opt/tomcat/temp/tomcat.pid"
Environment="CATALINA_HOME=/opt/tomcat"
Environment="CATALINA_BASE=/opt/tomcat"

ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/opt/tomcat/bin/shutdown.sh

RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target

[4단계] Tomcat 서비스 시작
# Systemd 데몬 리로드
systemctl daemon-reload

# Tomcat 시작
systemctl start tomcat

# 부팅 시 자동 시작 설정
systemctl enable tomcat

# 상태 확인
systemctl status tomcat
# "active (running)" 확인

# 포트 8080 리스닝 확인
netstat -antp | grep 8080
# 또는
ss -tlnp | grep 8080

[5단계] JSP 테스트 페이지 생성
# 웹 애플리케이션 디렉토리 생성
mkdir -p /opt/tomcat/webapps/ROOT

# 기존 ROOT 디렉토리가 있으면 백업
# mv /opt/tomcat/webapps/ROOT /opt/tomcat/webapps/ROOT.bak

# index.jsp 생성
vi /opt/tomcat/webapps/ROOT/index.jsp

# 아래 내용 입력:
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Tomcat JSP Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h2 { color: #4CAF50; }
        .info { background-color: #f0f0f0; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <h2>Tomcat JSP 정상 동작 확인</h2>
    <div class="info">
        <p><strong>현재 서버 시간:</strong> <%= new java.util.Date() %></p>
        <p><strong>서버 정보:</strong> <%= application.getServerInfo() %></p>
        <p><strong>Java 버전:</strong> <%= System.getProperty("java.version") %></p>
        <p><strong>서버 IP:</strong> <%= request.getLocalAddr() %></p>
        <p><strong>클라이언트 IP:</strong> <%= request.getRemoteAddr() %></p>
    </div>
    <hr>
    <p style="color:green;">✓ JSP가 정상적으로 실행되고 있습니다.</p>
    <p style="color:blue;">✓ WAS Server (Tier 2) - Tomcat 10.1.28</p>
</body>
</html>

# 소유권 변경
chown -R tomcat:tomcat /opt/tomcat/webapps/

# Tomcat 재시작
systemctl restart tomcat

[6단계] 브라우저에서 직접 접속 테스트
# 호스트 PC 브라우저에서
http://192.168.186.129:8080

# 또는 curl 명령어로
curl http://192.168.186.129:8080

# JSP 페이지 정상 출력 확인

[7단계] Tomcat 로그 확인
# Catalina 로그 (주 로그)
tail -f /opt/tomcat/logs/catalina.out

# 접근 로그
tail -f /opt/tomcat/logs/localhost_access_log.*.txt

# 애플리케이션 로그
tail -f /opt/tomcat/logs/localhost.*.log
### (D) Nginx → Tomcat 리버스 프록시 설정  
**실습 3: Nginx를 Tomcat의 리버스 프록시로 구성**  
bash
# ========================================
# VM1 (webserver) - IP: 192.168.186.128
# ========================================

[1단계] Nginx 기본 사이트 설정 백업
cd /etc/nginx/sites-available/
cp default default.bak

[2단계] 리버스 프록시 설정 추가
vi /etc/nginx/sites-available/default

# 기존 내용 삭제 후 아래 내용으로 교체:
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    # 접근 로그
    access_log /var/log/nginx/proxy_access.log;
    error_log /var/log/nginx/proxy_error.log;

    location / {
        # 인덱스 파일 우선순위
        index index.jsp index.html index.htm;

        # Tomcat으로 프록시 (WAS 서버 IP:8080)
        proxy_pass http://192.168.186.129:8080;

        # 프록시 헤더 설정 (클라이언트 정보 전달)
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 타임아웃 설정
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # 버퍼 설정
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
    }
}

[3단계] 설정 문법 검사
nginx -t
# 출력: syntax is ok, test is successful

[4단계] Nginx 재시작
systemctl restart nginx

# 상태 확인
systemctl status nginx

[5단계] 프록시 동작 테스트
# 호스트 PC 브라우저에서
http://192.168.186.128

# 이제 80 포트로 접속하면 Tomcat JSP 페이지가 표시됨!
# (내부적으로 192.168.186.129:8080으로 프록시됨)

# curl로 테스트
curl http://192.168.186.128

# 응답 헤더 확인 (프록시 정보 포함)
curl -I http://192.168.186.128

[6단계] 로그 확인
# Nginx 프록시 로그
tail -f /var/log/nginx/proxy_access.log

# Tomcat 로그 (프록시를 통한 요청 기록 확인)
# VM2에서 실행:
tail -f /opt/tomcat/logs/localhost_access_log.*.txt
# X-Forwarded-For 헤더로 실제 클라이언트 IP 확인 가능
```

**리버스 프록시 동작 흐름**

```
클라이언트 (192.168.186.1)
    |
    | ① HTTP 요청: http://192.168.186.128/
    ↓
Nginx (192.168.186.128:80)
    |
    | ② 프록시: http://192.168.186.129:8080/
    ↓
Tomcat (192.168.186.129:8080)
    |
    | ③ JSP 실행, HTML 생성
    ↓
Nginx (192.168.186.128:80)
    |
    | ④ HTTP 응답: HTML 반환
    ↓
클라이언트 (192.168.186.1)
```

### (E) Tier 3: Database Server (MariaDB) 구성

**실습 4: MariaDB 설치 및 설정**

```bash
# ========================================
# VM3 (dbserver) - IP: 192.168.186.130
# ========================================

[1단계] MariaDB 설치
sudo su
apt-get update
apt-get install -y mariadb-server

# 설치 확인
mysql --version
# 출력 예: mysql  Ver 15.1 Distrib 10.11.6-MariaDB

[2단계] 자동 실행 설정
systemctl enable mariadb
systemctl start mariadb

# 상태 확인
systemctl status mariadb
# "active (running)" 확인

# 포트 3306 리스닝 확인
netstat -antp | grep LISTEN | grep 3306
# 출력 예: tcp  0  0 127.0.0.1:3306  0.0.0.0:*  LISTEN  1234/mariadbd

[3단계] MariaDB 보안 설정 (mysql_secure_installation)
mysql_secure_installation

# 대화형 질문 응답:
# Enter current password for root: (엔터, 초기 비밀번호 없음)
# Set root password? [Y/n] Y
#   New password: Root1234! (본인 설정)
#   Re-enter new password: Root1234!
# Remove anonymous users? [Y/n] Y
# Disallow root login remotely? [Y/n] Y (보안 강화)
# Remove test database? [Y/n] Y
# Reload privilege tables now? [Y/n] Y

[4단계] 원격 접속 허용 설정 (bind-address 변경)
# MariaDB는 기본적으로 127.0.0.1만 리스닝 (로컬만 접속 가능)
# WAS 서버에서 접속하려면 모든 IP(0.0.0.0) 또는 특정 IP로 변경 필요

# 설정 파일 위치 찾기
cd /etc/mysql
grep "127.0.0.1" -r ./
# 출력 예: ./mariadb.conf.d/50-server.cnf:bind-address = 127.0.0.1

# 설정 파일 편집
vi ./mariadb.conf.d/50-server.cnf

# 아래 줄 찾기:
# bind-address = 127.0.0.1

# 다음으로 변경:
bind-address = 0.0.0.0

# 저장 후 종료 (ESC → :wq)

[5단계] MariaDB 재시작
systemctl restart mariadb

# 포트 확인 (이제 0.0.0.0:3306으로 리스닝)
netstat -antp | grep LISTEN | grep 3306
# 출력 예: tcp  0  0 0.0.0.0:3306  0.0.0.0:*  LISTEN  2345/mariadbd

[6단계] 원격 접속용 데이터베이스 사용자 생성
# MariaDB 접속 (root 계정)
mysql -u root -p
# Enter password: Root1234!

# MariaDB 프롬프트에서 실행:

-- 모든 호스트에서 접속 가능한 사용자 생성
CREATE USER 'mydb'@'%' IDENTIFIED BY 'abcd1234';

-- 모든 데이터베이스에 대한 모든 권한 부여
GRANT ALL PRIVILEGES ON *.* TO 'mydb'@'%' WITH GRANT OPTION;

-- 권한 즉시 반영
FLUSH PRIVILEGES;

-- 생성된 사용자 확인
SELECT user, host FROM mysql.user WHERE user='mydb';
# 출력 예:
# +------+------+
# | user | host |
# +------+------+
# | mydb | %    |
# +------+------+

-- 종료
EXIT;

[7단계] 방화벽 설정 (ufw 사용 시)
# Ubuntu 방화벽이 활성화된 경우 3306 포트 허용
ufw allow 3306/tcp

# 또는 특정 IP만 허용 (보안 강화)
ufw allow from 192.168.186.129 to any port 3306

[8단계] MariaDB 기본 데이터베이스 및 테이블 생성
mysql -u root -p
# Enter password: Root1234!

-- 테스트용 데이터베이스 생성
CREATE DATABASE testdb;

-- 데이터베이스 전환
USE testdb;

-- 샘플 테이블 생성
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 샘플 데이터 삽입
INSERT INTO users (username, email) VALUES
    ('admin', 'admin@example.com'),
    ('user1', 'user1@example.com'),
    ('user2', 'user2@example.com');

-- 데이터 확인
SELECT * FROM users;

-- 종료
EXIT;

[9단계] MariaDB 주요 로그 확인
# 에러 로그
tail -f /var/log/mysql/error.log

# 슬로우 쿼리 로그 (활성화 시)
tail -f /var/log/mysql/mariadb-slow.log

# 일반 쿼리 로그 (활성화 시, 성능 영향)
tail -f /var/log/mysql/query.log
```

**실습 5: WAS에서 DB 연결 테스트**

```bash
# ========================================
# VM2 (wasserver) - IP: 192.168.186.129
# ========================================

[1단계] MariaDB 클라이언트 설치
sudo su
apt-get install -y mariadb-client-core

# 또는 전체 클라이언트 패키지
# apt-get install -y mariadb-client

[2단계] DB 서버 연결 테스트
mysql -u mydb -p -h 192.168.186.130

# Enter password: abcd1234

# 연결 성공 시 MariaDB 프롬프트 표시:
# Welcome to the MariaDB monitor.
# MariaDB [(none)]>

# 데이터베이스 목록 확인
SHOW DATABASES;

# testdb 사용
USE testdb;

# 테이블 조회
SELECT * FROM users;

# 종료
EXIT;

[3단계] JDBC 연결을 위한 MySQL Connector 다운로드
# Tomcat의 lib 디렉토리에 JDBC 드라이버 배치
cd /opt/tomcat/lib/
wget https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.3.0/mysql-connector-j-8.3.0.jar

# 소유권 변경
chown tomcat:tomcat mysql-connector-j-8.3.0.jar

[4단계] DB 연결 테스트 JSP 페이지 생성
vi /opt/tomcat/webapps/ROOT/dbtest.jsp

# 아래 내용 입력:
<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DB Connection Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .success { color: green; font-weight: bold; }
        .error { color: red; font-weight: bold; }
        table { border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
    </style>
</head>
<body>
    <h2>Database Connection Test</h2>
    <%
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        String dbURL = "jdbc:mysql://192.168.186.130:3306/testdb";
        String dbUser = "mydb";
        String dbPassword = "abcd1234";

        try {
            // JDBC 드라이버 로드
            Class.forName("com.mysql.cj.jdbc.Driver");

            // 데이터베이스 연결
            conn = DriverManager.getConnection(dbURL, dbUser, dbPassword);
            out.println("<p class='success'>✓ 데이터베이스 연결 성공!</p>");
            out.println("<p>연결 정보: " + dbURL + "</p>");

            // SQL 쿼리 실행
            stmt = conn.createStatement();
            rs = stmt.executeQuery("SELECT * FROM users");

            // 결과 출력
            out.println("<h3>Users 테이블 데이터:</h3>");
            out.println("<table>");
            out.println("<tr><th>ID</th><th>Username</th><th>Email</th><th>Created At</th></tr>");

            while (rs.next()) {
                out.println("<tr>");
                out.println("<td>" + rs.getInt("id") + "</td>");
                out.println("<td>" + rs.getString("username") + "</td>");
                out.println("<td>" + rs.getString("email") + "</td>");
                out.println("<td>" + rs.getTimestamp("created_at") + "</td>");
                out.println("</tr>");
            }

            out.println("</table>");

        } catch (ClassNotFoundException e) {
            out.println("<p class='error'>✗ JDBC 드라이버를 찾을 수 없습니다.</p>");
            out.println("<p>Error: " + e.getMessage() + "</p>");
        } catch (SQLException e) {
            out.println("<p class='error'>✗ 데이터베이스 연결 실패</p>");
            out.println("<p>Error: " + e.getMessage() + "</p>");
        } finally {
            // 리소스 정리
            try {
                if (rs != null) rs.close();
                if (stmt != null) stmt.close();
                if (conn != null) conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    %>
    <hr>
    <p><a href="/">← 메인 페이지로</a></p>
</body>
</html>

# 소유권 변경
chown tomcat:tomcat /opt/tomcat/webapps/ROOT/dbtest.jsp

# Tomcat 재시작
systemctl restart tomcat

[5단계] 브라우저에서 DB 연결 테스트
# 호스트 PC 브라우저에서
http://192.168.186.128/dbtest.jsp

# 정상 동작 시:
# ✓ 데이터베이스 연결 성공!
# Users 테이블 데이터가 표로 출력됨

# curl로 테스트
curl http://192.168.186.128/dbtest.jsp
```

**3-Tier 아키텍처 전체 연동 흐름**

```
[클라이언트]
    ↓ HTTP 요청
    ↓ http://192.168.186.128/dbtest.jsp

[Tier 1: Web Server - Nginx]
192.168.186.128:80
    ↓ Reverse Proxy
    ↓ http://192.168.186.129:8080/dbtest.jsp

[Tier 2: WAS - Tomcat]
192.168.186.129:8080
    ↓ JSP 실행
    ↓ JDBC Connection
    ↓ jdbc:mysql://192.168.186.130:3306/testdb

[Tier 3: DB - MariaDB]
192.168.186.130:3306
    ↓ SQL Query: SELECT * FROM users
    ↓ Result Set 반환

[Tier 2: WAS - Tomcat]
    ↓ HTML 생성

[Tier 1: Web Server - Nginx]
    ↓ HTTP 응답

[클라이언트]
    ↓ 웹 페이지 렌더링
    ✓ Users 테이블 데이터 표시
```

---

## 3. 실무/보안 관점 분석 (Insight & Scenario Mapping)

| 분야 | 적용 시나리오 |
|:---:|:---|
| **3-Tier 보안 아키텍처** | **계층별 격리**: Web(DMZ) → WAS(내부망) → DB(최내부) 배치로 공격자가 한 계층 침투 시에도 다른 계층 보호. **방화벽 규칙**: Web은 80/443만 외부 개방, WAS는 Web에서만 8080 접근, DB는 WAS에서만 3306 접근. **최소 권한 원칙**: 각 계층은 필요한 포트/서비스만 실행, 불필요한 서비스 비활성화. **리버스 프록시**: Nginx가 Tomcat 앞단에서 SSL 종료, Rate Limiting, IP 필터링 수행. **네트워크 세분화**: VLAN 또는 서브넷으로 각 계층 물리적 격리(실무에서는 필수). |
| **Nginx 보안 강화** | **서버 정보 숨김**: `server_tokens off;`로 응답 헤더에서 Nginx 버전 제거. **Rate Limiting**: `limit_req_zone`으로 특정 IP의 요청 빈도 제한(DDoS 완화). **IP 화이트리스트**: `allow 192.168.186.0/24; deny all;`로 특정 IP 대역만 허용. **SSL/TLS 설정**: Let's Encrypt 인증서로 HTTPS 적용, TLS 1.2+ 강제. **보안 헤더**: `X-Frame-Options DENY`, `X-Content-Type-Options nosniff`, `Content-Security-Policy` 추가. **접근 로그 분석**: SQL Injection, Path Traversal 패턴 탐지. **ModSecurity WAF 연동**: OWASP CRS 룰셋 적용으로 웹 공격 차단. |
| **Tomcat 보안 강화** | **Manager 앱 보호**: 기본 admin 계정 삭제, 강력한 비밀번호 설정, 특정 IP만 접근 허용(`RemoteAddrValve`). **불필요한 앱 제거**: `/opt/tomcat/webapps/`의 예제 앱(examples, docs, host-manager) 삭제. **AJP 커넥터 비활성화**: `server.xml`에서 AJP 포트 주석 처리(Ghostcat 취약점 방지). **Error Page 커스터마이징**: 상세 에러 메시지 숨김, 커스텀 에러 페이지 사용. **HTTPS Connector**: Tomcat에 직접 SSL 설정(Nginx 프록시 없을 시). **접근 로그**: `AccessLogValve`로 모든 요청 기록, 의심 활동 모니터링. **보안 패치**: 정기적으로 최신 버전 업데이트, CVE 확인. |
| **MariaDB 보안 강화** | **Root 원격 접속 차단**: `mysql_secure_installation`에서 설정, Root는 localhost만 허용. **최소 권한 계정**: 애플리케이션별 전용 계정 생성, 필요한 DB/테이블만 권한 부여(`GRANT SELECT, INSERT ON testdb.* TO 'appuser'@'192.168.186.129'`). **bind-address 제한**: 0.0.0.0 대신 WAS 서버 IP만 허용(`bind-address = 192.168.186.129`). **강력한 비밀번호**: 대소문자, 숫자, 특수문자 조합, 12자 이상. **SSL/TLS 연결**: MariaDB SSL 인증서 설정, JDBC URL에 `useSSL=true` 추가. **감사 로그**: MariaDB Audit Plugin으로 모든 쿼리 기록. **정기 백업**: `mysqldump` 또는 `mariabackup`으로 일일 백업 자동화. **Slow Query Log**: SQL Injection 의심 쿼리 탐지. |
| **네트워크 보안** | **방화벽 규칙 세밀화**: `iptables` 또는 `ufw`로 포트별 소스 IP 제한. 예: `ufw allow from 192.168.186.128 to any port 8080`(WAS), `ufw allow from 192.168.186.129 to any port 3306`(DB). **SSH 보안**: Root 로그인 금지(`PermitRootLogin no`), SSH 키 인증 사용, 기본 포트 22 변경, Fail2ban으로 brute force 차단. **VPN/Bastion Host**: 관리자 접속은 VPN 경유 또는 Bastion Host를 통해서만 허용. **네트워크 모니터링**: tcpdump, Wireshark로 비정상 트래픽 분석. **IDS/IPS**: Suricata 또는 Snort로 침입 탐지/차단. **포트 스캔 탐지**: portsentry로 스캔 시도 자동 차단. |
| **로그 관리 및 모니터링** | **중앙 집중식 로그**: rsyslog 또는 syslog-ng로 모든 서버 로그를 중앙 로그 서버로 전송. **로그 분석**: ELK Stack(Elasticsearch, Logstash, Kibana) 구축으로 실시간 로그 분석, 대시보드 시각화. **경보 설정**: 특정 패턴(실패한 로그인 10회, SQL Injection 시도) 탐지 시 이메일/Slack 알림. **보존 기간**: 규정 준수(ISMS-P, ISO 27001)를 위해 로그 최소 1년 보관. **로그 무결성**: 로그 파일 해시 계산, 변조 방지. **성능 모니터링**: Prometheus + Grafana로 CPU, 메모리, 디스크, 네트워크 모니터링, 임계값 초과 시 알림. |
| **백업 및 복구** | **정기 백업**: Cron 작업으로 일일 자동 백업(DB dump, 애플리케이션 파일, 설정 파일). **백업 검증**: 정기적으로 복구 테스트 수행, RTO/RPO 목표 달성 확인. **오프사이트 백업**: 원격 서버 또는 클라우드 스토리지(S3)로 백업 파일 전송. **VM 스냅샷**: VMware 스냅샷 기능으로 전체 시스템 백업, 빠른 복구 가능. **버전 관리**: Git으로 애플리케이션 코드, 설정 파일 버전 관리. **재해 복구 계획**: DR(Disaster Recovery) 절차 문서화, 정기 훈련. |
| **취약점 관리** | **정기 패치**: `apt-get update && apt-get upgrade`로 OS 및 패키지 업데이트, Nginx/Tomcat/MariaDB 최신 버전 유지. **취약점 스캔**: OpenVAS, Nessus로 정기 스캔, CVE 확인. **웹 취약점 스캔**: OWASP ZAP, Burp Suite로 웹 애플리케이션 취약점 탐지. **침투 테스트**: 외부 전문가 또는 내부 레드팀이 정기적으로 모의 해킹 수행. **보안 공지 모니터링**: Nginx, Tomcat, MariaDB 공식 보안 공지 구독, 즉시 패치 적용. |

---

## 4. 개인 인사이트 및 다음 단계 (Reflection & Next Steps)

**배운 점 / 느낀 점:**

- **3-Tier 아키텍처의 실체 파악**: 책이나 강의에서만 보던 개념을 VMware로 직접 구현하니 각 계층의 역할과 상호작용이 명확해졌습니다. 특히 "왜 3개 계층으로 나누는가?"에 대한 답을 보안 관점에서 이해했습니다.

- **리버스 프록시의 가치**: Nginx를 단순 웹 서버가 아닌 리버스 프록시로 사용하면서, 백엔드 서버 보호, SSL 종료, 로드 밸런싱 등 다양한 기능을 한 곳에서 처리할 수 있다는 점이 인상 깊었습니다. 실무에서 ALB와 유사한 역할이라는 것도 이해했습니다.

- **설정 파일의 중요성**: Nginx의 `sites-available/default`, Tomcat의 `server.xml`, MariaDB의 `50-server.cnf` 등 각 서비스의 설정 파일을 직접 편집하면서, 보안 설정이 모두 이 파일들에 달려있다는 걸 깨달았습니다. 한 줄만 잘못 설정해도 전체 서비스가 노출될 수 있습니다.

- **포트와 방화벽의 핵심 역할**: 80, 8080, 3306 포트가 각각 어떤 역할을 하는지, 어떤 서버끼리 통신해야 하는지를 직접 설정하면서 네트워크 보안의 기초를 다졌습니다. 특히 `bind-address`를 0.0.0.0으로 변경하는 순간 외부에서 DB 접근 가능해지는 위험성을 체감했습니다.

- **실습의 시행착오**: 처음에는 Nginx에서 Tomcat으로 프록시가 안 되거나, DB 연결이 실패하는 등 많은 오류를 겪었습니다. 하지만 로그 파일(`access.log`, `error.log`, `catalina.out`)을 확인하면서 문제를 해결하는 과정이 실무 트러블슈팅 능력 향상에 큰 도움이 되었습니다.

- **VMware의 유용성**: 물리적 서버 3대 없이도 3-Tier 환경을 구축할 수 있다는 점이 놀라웠습니다. 스냅샷 기능 덕분에 실수해도 즉시 복구할 수 있어서 마음껏 실험할 수 있었습니다. 클라우드 이전에 온프레미스 환경을 이해하는 데 VMware가 필수 도구라는 걸 느꼈습니다.

**새로 알게 된 점:**

- **systemctl의 강력함**: Linux 서비스 관리가 이렇게 체계적일 줄 몰랐습니다. `enable`로 자동 시작, `status`로 실시간 모니터링, `journalctl`로 로그 확인까지 모두 systemd로 통합 관리되는 게 인상적이었습니다.

- **MariaDB vs MySQL**: MariaDB가 MySQL의 포크라는 것만 알았는데, 완전 호환되면서도 성능과 기능이 개선되었다는 걸 알았습니다. JDBC URL도 `jdbc:mysql://`로 그대로 사용 가능합니다.

- **JSP의 동작 원리**: JSP 파일이 Tomcat에 의해 서블릿으로 컴파일되고 실행된다는 것, 그리고 `<%= %>` 태그로 Java 코드를 HTML에 삽입할 수 있다는 걸 처음 알았습니다. 동적 웹 페이지 생성의 기초를 이해했습니다.

- **0.0.0.0 vs 127.0.0.1**: `bind-address`가 127.0.0.1이면 로컬에서만 접속 가능하고, 0.0.0.0이면 모든 IP에서 접속 가능하다는 차이를 명확히 알게 되었습니다. 보안상 가능한 한 특정 IP만 허용해야 한다는 원칙도 이해했습니다.

**이전 학습과의 연결:**

- **네트워크 기초와의 연결**: TCP/IP 학습에서 배운 포트, 프로토콜 개념이 실제로 80(HTTP), 8080(Tomcat), 3306(MySQL) 포트로 구현되었습니다. 각 계층 간 통신이 TCP 3-way handshake로 이루어진다는 것을 확인했습니다.

- **Linux 시스템 관리**: 이전에 배운 리눅스 명령어(systemctl, netstat, vi 등)가 실제 서버 구성에 모두 사용되었습니다. 특히 로그 파일 분석 능력이 트러블슈팅에 결정적이었습니다.

- **보안 계층화 원칙**: 이론으로 배웠던 Defense in Depth가 실제로 Web → WAS → DB로 구현되는 것을 확인했습니다. 각 계층마다 다른 보안 통제(방화벽, 인증, 암호화)를 적용할 수 있습니다.

- **서비스 아키텍처 이해**: 단일 서버에 모든 것을 설치하는 것과 계층별로 분리하는 것의 차이를 체감했습니다. 확장성, 유지보수성, 보안성이 모두 향상됩니다.

**어려웠던 부분:**

- **vi 에디터 사용**: Linux 초심자라 vi 에디터 사용이 처음에 너무 어려웠습니다. `i`로 입력 모드, `ESC`로 명령 모드, `:wq`로 저장 종료하는 기본 명령어를 익히는 데 시간이 걸렸습니다. 실수로 `:q!`를 눌러서 작업을 날린 적도 있습니다.

- **경로와 디렉토리 구조**: Linux 파일 시스템 구조(`/etc`, `/opt`, `/var`, `/usr`)가 익숙하지 않아서 설정 파일을 찾는 데 헤맸습니다. 특히 Nginx는 `/etc/nginx/`, Tomcat은 `/opt/tomcat/`, MariaDB는 `/etc/mysql/`로 각각 다른 위치에 있어서 혼란스러웠습니다.

- **네트워크 연결 문제**: VMware 네트워크 설정(NAT vs Bridge)에서 막혀서 VM 간 통신이 안 되는 경우가 있었습니다. `ifconfig`로 IP 주소를 확인하고, `ping`으로 연결 테스트하면서 해결했습니다.

- **JDBC 드라이버 호환성**: 처음에 오래된 JDBC 드라이버를 사용해서 "Unable to load authentication plugin 'caching_sha2_password'" 오류가 발생했습니다. 최신 버전(mysql-connector-j-8.3.0.jar)으로 교체하면서 해결했습니다.

**심화 방향:**

1. **HTTPS 적용**
   - Let's Encrypt로 SSL/TLS 인증서 발급
   - Nginx에 HTTPS 리스너 추가, HTTP → HTTPS 리다이렉션
   - Tomcat과 Nginx 간 내부 통신도 HTTPS로 암호화

2. **로드 밸런싱**
   - Tomcat 인스턴스 2개 이상 구성
   - Nginx에서 `upstream` 블록으로 로드 밸런싱 설정
   - 세션 고정(Session Affinity) 또는 세션 클러스터링 구현

3. **Docker 컨테이너화**
   - 각 계층을 Docker 컨테이너로 변환
   - Docker Compose로 3-Tier 환경 자동 구성
   - 컨테이너 간 네트워크 격리 및 보안 설정

4. **WAF (ModSecurity) 연동**
   - Nginx에 ModSecurity 모듈 설치
   - OWASP CRS 룰셋 적용
   - SQL Injection, XSS 공격 실제 차단 테스트

5. **모니터링 시스템 구축**
   - Prometheus + Grafana 설치
   - Node Exporter로 시스템 메트릭 수집
   - Nginx, Tomcat, MariaDB 메트릭 대시보드 구성

6. **로그 중앙화 (ELK Stack)**
   - Elasticsearch, Logstash, Kibana 구축
   - Filebeat로 모든 서버 로그 수집
   - Kibana 대시보드로 실시간 로그 분석

7. **자동화 (Ansible)**
   - Ansible Playbook으로 3-Tier 환경 자동 구성
   - 멱등성(Idempotency) 보장
   - 인프라 코드화(IaC) 학습

8. **고가용성 (HA) 구성**
   - Keepalived로 Nginx 이중화 (VIP 사용)
   - MariaDB Replication (Master-Slave)
   - Tomcat 세션 클러스터링 (Redis 사용)

9. **침투 테스트**
   - OWASP ZAP으로 웹 애플리케이션 취약점 스캔
   - SQL Injection, XSS, CSRF 실제 공격 시도
   - Burp Suite로 HTTP 요청/응답 조작
   - Metasploit으로 알려진 취약점 테스트

10. **Kubernetes 마이그레이션**
    - Docker 컨테이너를 Kubernetes Pod로 배포
    - Service, Ingress로 네트워크 구성
    - ConfigMap, Secret으로 설정 관리
    - Helm Chart로 전체 스택 패키징

---

## 5. 추가 참고사항 (Quick Reference)

### 주요 명령어 모음

**시스템 관리**
```bash
# Root 권한 전환
sudo su

# 패키지 업데이트
apt-get update && apt-get upgrade -y

# 시스템 정보 확인
uname -a              # 커널 정보
lsb_release -a        # Ubuntu 버전
free -h               # 메모리 사용량
df -h                 # 디스크 사용량
top                   # 실시간 프로세스 모니터링
htop                  # 향상된 프로세스 모니터링 (설치 필요)
```

**네트워크**
```bash
# IP 주소 확인
ifconfig
ip addr show

# 네트워크 연결 테스트
ping 192.168.186.129

# 포트 리스닝 확인
netstat -antp | grep LISTEN
ss -tlnp

# 특정 포트 확인
netstat -antp | grep 8080
ss -tlnp | grep 3306

# 방화벽 상태 (ufw)
ufw status
ufw allow 80/tcp
ufw allow from 192.168.186.129 to any port 8080
ufw enable
```

**서비스 관리 (systemctl)**
```bash
# 서비스 시작/중지/재시작
systemctl start nginx
systemctl stop nginx
systemctl restart nginx

# 서비스 상태 확인
systemctl status nginx

# 부팅 시 자동 시작
systemctl enable nginx
systemctl disable nginx

# 서비스 목록 확인
systemctl list-units --type=service

# 로그 확인 (journalctl)
journalctl -u nginx -f        # 실시간 로그
journalctl -u nginx --since today
```

**로그 확인**
```bash
# Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Tomcat
tail -f /opt/tomcat/logs/catalina.out
tail -f /opt/tomcat/logs/localhost_access_log.*.txt

# MariaDB
tail -f /var/log/mysql/error.log

# 시스템 로그
tail -f /var/log/syslog
tail -f /var/log/auth.log      # SSH 로그인 이력
```

**파일 편집 (vi)**
```bash
# 파일 열기
vi filename

# 명령 모드 → 입력 모드
i           # 현재 위치에서 입력
a           # 현재 위치 다음에 입력
o           # 새 줄 추가 후 입력

# 입력 모드 → 명령 모드
ESC

# 저장 및 종료 (명령 모드에서)
:wq         # 저장 후 종료
:q!         # 저장 안 하고 강제 종료
:w          # 저장만
/pattern    # 패턴 검색
:1,10d      # 1~10줄 삭제
:%s/old/new/g  # 전체 치환
### 포트 및 프로토콜 참조표  
| 서비스 | 포트 | 프로토콜 | 용도 |  
|:---:|:---:|:---:|:---|  
| HTTP | 80 | TCP | 웹 서버 (암호화 없음) |  
| HTTPS | 443 | TCP | 웹 서버 (SSL/TLS 암호화) |  
| SSH | 22 | TCP | 원격 접속 |  
| Tomcat | 8080 | TCP | WAS (HTTP Alternative) |  
| Tomcat AJP | 8009 | TCP | Nginx ↔ Tomcat 연동 (비활성화 권장) |  
| MySQL/MariaDB | 3306 | TCP | 데이터베이스 |  
| PostgreSQL | 5432 | TCP | 데이터베이스 |  
| MongoDB | 27017 | TCP | NoSQL 데이터베이스 |  
| Redis | 6379 | TCP | 인메모리 DB/캐시 |  
| DNS | 53 | UDP/TCP | 도메인 이름 해석 |  
| FTP | 21 | TCP | 파일 전송 (비보안, 사용 지양) |  
| SFTP | 22 | TCP | 안전한 파일 전송 (SSH 기반) |  
### 보안 체크리스트  
**Nginx**  
- [ ] `server_tokens off;` (버전 정보 숨김)  
- [ ] SSL/TLS 설정 (HTTPS 적용)  
- [ ] Rate Limiting 설정  
- [ ] IP 화이트리스트 적용 (필요 시)  
- [ ] 보안 헤더 추가 (X-Frame-Options, CSP 등)  
- [ ] Access Log 활성화 및 정기 분석  
- [ ] 불필요한 HTTP 메서드 차단 (TRACE, OPTIONS 등)  
**Tomcat**  
- [ ] Manager 앱 기본 계정 변경 또는 삭제  
- [ ] 불필요한 예제 앱 삭제 (examples, docs, host-manager)  
- [ ] AJP 커넥터 비활성화 (Ghostcat 취약점)  
- [ ] 에러 페이지 커스터마이징 (상세 정보 숨김)  
- [ ] HTTPS Connector 설정 (필요 시)  
- [ ] Access Log 활성화  
- [ ] 최신 버전 유지 (정기 패치)  
**MariaDB**  
- [ ] Root 원격 접속 차단 (localhost만 허용)  
- [ ] 애플리케이션별 전용 계정 생성  
- [ ] 최소 권한 부여 (필요한 DB/테이블만)  
- [ ] `bind-address`를 특정 IP로 제한  
- [ ] 강력한 비밀번호 정책 적용  
- [ ] SSL/TLS 연결 설정  
- [ ] 정기 백업 자동화  
- [ ] Slow Query Log 활성화  
**OS/네트워크**  
- [ ] 방화벽 활성화 (ufw/iptables)  
- [ ] 필요한 포트만 개방  
- [ ] SSH Root 로그인 금지  
- [ ] SSH 키 인증 사용  
- [ ] Fail2ban 설치 및 설정  
- [ ] 불필요한 서비스 비활성화  
- [ ] 정기 시스템 업데이트  
### 트러블슈팅 가이드  
**Nginx → Tomcat 프록시 실패**  
bash
# 1. Tomcat이 실행 중인지 확인
systemctl status tomcat
netstat -antp | grep 8080

# 2. 방화벽 규칙 확인
ufw status
# 8080 포트가 허용되어 있는지 확인

# 3. Nginx 에러 로그 확인
tail -f /var/log/nginx/error.log
# "connect() failed (111: Connection refused)" 오류 확인

# 4. Nginx 설정 파일 문법 검사
nginx -t

# 5. SELinux 또는 AppArmor 확인 (있는 경우)
sestatus
aa-status
```

**DB 연결 실패**
```bash
# 1. MariaDB 실행 확인
systemctl status mariadb
netstat -antp | grep 3306

# 2. bind-address 확인
grep "bind-address" /etc/mysql/mariadb.conf.d/50-server.cnf
# 0.0.0.0 또는 WAS 서버 IP로 설정되어 있는지 확인

# 3. 사용자 권한 확인
mysql -u root -p
> SELECT user, host FROM mysql.user WHERE user='mydb';
> SHOW GRANTS FOR 'mydb'@'%';

# 4. WAS 서버에서 DB 연결 테스트
mysql -u mydb -p -h 192.168.186.130

# 5. 방화벽 확인
ufw status
# 3306 포트가 WAS에서 허용되어 있는지 확인

# 6. JDBC URL 확인
# jdbc:mysql://192.168.186.130:3306/testdb
# 호스트, 포트, 데이터베이스 이름 정확한지 확인
```

**JSP 페이지 500 에러**
```bash
# 1. Tomcat 로그 확인
tail -f /opt/tomcat/logs/catalina.out
# 스택 트레이스에서 오류 원인 확인

# 2. JDBC 드라이버 확인
ls -l /opt/tomcat/lib/mysql-connector-j-*.jar
# 파일이 존재하고 소유권이 tomcat:tomcat인지 확인

# 3. JSP 파일 문법 오류 확인
# <% %> 태그가 올바르게 닫혔는지, Java 코드에 오류 없는지

# 4. Tomcat 재시작
systemctl restart tomcat
```

**VM 간 통신 안 됨**
```bash
# 1. IP 주소 확인
ifconfig
# 각 VM의 IP가 같은 네트워크 대역인지 확인 (예: 192.168.186.x)

# 2. Ping 테스트
ping 192.168.186.129
# ICMP 응답이 오는지 확인

# 3. VMware 네트워크 설정 확인
# VMware → Edit → Virtual Network Editor
# NAT 또는 Bridge 모드로 통일

# 4. 방화벽 일시 비활성화 테스트
ufw disable
# 통신 되면 방화벽 규칙 문제, 다시 활성화 후 규칙 수정
ufw enable
```

### 성능 최적화 팁

**Nginx**
```nginx
# /etc/nginx/nginx.conf

# Worker 프로세스 수 (CPU 코어 수와 동일)
worker_processes auto;

# 연결당 이벤트 수
events {
    worker_connections 1024;
}

# Gzip 압축 (대역폭 절약)
gzip on;
gzip_types text/plain text/css application/json application/javascript;

# 캐싱 설정
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

server {
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 60m;
        proxy_pass http://192.168.186.129:8080;
    }
}
```

**Tomcat**
```xml
<!-- /opt/tomcat/conf/server.xml -->

<!-- Connector 최적화 -->
<Connector port="8080" protocol="HTTP/1.1"
           connectionTimeout="20000"
           maxThreads="200"
           minSpareThreads="25"
           acceptCount="100"
           enableLookups="false"
           compression="on"
           compressionMinSize="2048"
           compressibleMimeType="text/html,text/xml,text/plain,text/css,application/javascript"/>
```

**MariaDB**
```ini
# /etc/mysql/mariadb.conf.d/50-server.cnf

[mysqld]
# InnoDB 버퍼 풀 (전체 메모리의 70~80%)
innodb_buffer_pool_size = 2G

# 쿼리 캐시 (MariaDB 10.2.4+는 기본 비활성화)
query_cache_type = 1
query_cache_size = 64M

# 최대 연결 수
max_connections = 200

# Slow Query Log (1초 이상 쿼리 기록)
slow_query_log = 1
long_query_time = 1
```
