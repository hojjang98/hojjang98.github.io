---
title: "2025.12.02 (Day 27) [TCP/IP 네트워크 종합: 애플리케이션 계층 & 네트워크 보안 (방화벽, IDS/IPS)]"
date: 2025-12-02
draft: false
tags: ["네트워크", "방화벽", "IDS", "IPS", "Suricata", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "애플리케이션 계층 프로토콜(HTTP/DNS/DHCP), Untangle 방화벽, Suricata IDS/IPS 실습"
---

# 📄 2025.12.02 (Day 27) [TCP/IP 네트워크 종합: 애플리케이션 계층 & 네트워크 보안 (방화벽, IDS/IPS)]

## 1. 핵심 개념 정리 (Concepts & Theory)

| # | 핵심 개념 | 간결한 설명 |
|:---:|:---|:---|
| **1** | **애플리케이션 계층 (Application Layer)** | OSI 7계층으로 **최종 사용자 서비스**를 제공합니다. HTTP, HTTPS, FTP, SMTP, DNS, DHCP, SSH, Telnet 등의 프로토콜이 동작하며, **포트 번호**를 통해 서비스를 식별합니다. 사용자와 직접 상호작용하는 계층입니다. |
| **2** | **HTTP/HTTPS** | **HTTP**(HyperText Transfer Protocol)는 웹 브라우저와 웹 서버 간 통신 프로토콜입니다. **80번 포트** 사용. **평문** 전송으로 도청/변조 취약. **HTTPS**는 SSL/TLS로 암호화한 HTTP로 **443번 포트** 사용. GET, POST, PUT, DELETE 등 메서드로 요청합니다. |
| **3** | **DNS (Domain Name System)** | 도메인 이름을 IP 주소로 변환하는 시스템입니다. **53번 포트**(UDP 주로 사용, TCP는 Zone Transfer). 계층적 구조: 루트 DNS → TLD DNS → 권한 있는 DNS → 재귀 DNS. **A 레코드**(IPv4), **AAAA 레코드**(IPv6), **MX 레코드**(메일 서버), **CNAME**(별칭) 등의 레코드 타입이 존재합니다. |
| **4** | **DHCP (Dynamic Host Configuration Protocol)** | IP 주소를 **자동으로 할당**하는 프로토콜입니다. **67번(서버), 68번(클라이언트) 포트** 사용. **DORA 과정**: (1) **Discover** (클라이언트 브로드캐스트), (2) **Offer** (서버가 IP 제안), (3) **Request** (클라이언트 IP 요청), (4) **Acknowledge** (서버 확인). |
| **5** | **방화벽 (Firewall)** | 네트워크 트래픽을 **정책(Rule)** 기반으로 **허용/차단**하는 보안 장비입니다. **패킷 필터링 방화벽**(L3/L4: IP/포트 기반), **상태 기반 방화벽**(Stateful: 세션 추적), **애플리케이션 방화벽**(L7: 프로토콜 분석), **차세대 방화벽**(NGFW: IPS, 애플리케이션 인식, 사용자 인증 통합)으로 발전했습니다. |
| **6** | **IDS/IPS (Intrusion Detection/Prevention System)** | **IDS**는 침입을 **탐지**하여 **알림**만 제공하고, **IPS**는 침입을 **탐지 + 차단**합니다. **시그니처 기반**(알려진 공격 패턴 매칭)과 **이상 징후 기반**(정상 행위에서 벗어난 패턴 탐지)으로 나뉩니다. **Suricata**, **Snort**가 대표적인 오픈소스 IDS/IPS입니다. |

---

## 2. 실습 코드 & 응용 (Practice & Code Walkthrough)

### (A) 애플리케이션 계층 프로토콜 실습

**HTTP/HTTPS 요청 분석 (Wireshark):**

```
# HTTP 요청 (평문)
GET / HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html
Accept-Language: en-US
Connection: keep-alive

Wireshark 필터: http.request
→ 모든 데이터(쿠키, 세션 토큰, 비밀번호)가 평문으로 노출

# HTTPS 요청 (암호화)
Client Hello (TLS Handshake)
Server Hello, Certificate
Key Exchange
Encrypted Application Data

Wireshark 필터: tls.handshake.type == 1  (Client Hello)
→ 암호화된 데이터는 Wireshark에서도 내용 확인 불가
   (서버의 Private Key 없이는 복호화 불가)
```


**DNS 쿼리 분석:**
```bash
# Linux에서 DNS 쿼리
nslookup google.com
dig google.com
dig google.com +short        # IP만 출력
dig google.com ANY           # 모든 레코드
dig google.com MX            # 메일 서버
dig @8.8.8.8 google.com      # 특정 DNS 서버 지정

# Windows
nslookup google.com
nslookup google.com 8.8.8.8  # 특정 DNS 서버 지정

# Wireshark에서 DNS 패킷 분석
Domain Name System (query)
    Transaction ID: 0x1234
    Flags: 0x0100 (Standard query)
    Questions: 1
    Answer RRs: 0
    Queries:
        google.com: type A, class IN

Domain Name System (response)
    Transaction ID: 0x1234
    Flags: 0x8180 (Standard query response, No error)
    Questions: 1
    Answer RRs: 1
    Answers:
        google.com: type A, class IN, addr 142.250.185.46
```

**DHCP DORA 과정 (Wireshark):**

패킷 1: DHCP Discover
    Bootstrap Protocol (Discover)
    Client MAC address: 00:0c:29:3a:2f:1a
    DHCP: Discover
    Option: (53) DHCP Message Type = Discover

패킷 2: DHCP Offer
    Bootstrap Protocol (Offer)
    Your (client) IP address: 192.168.1.100
    Next server IP address: 192.168.1.1
    DHCP: Offer
    Option: (53) DHCP Message Type = Offer
    Option: (54) DHCP Server Identifier = 192.168.1.1
    Option: (51) IP Address Lease Time = 86400 sec

패킷 3: DHCP Request
    Bootstrap Protocol (Request)
    DHCP: Request
    Option: (53) DHCP Message Type = Request
    Option: (50) Requested IP Address = 192.168.1.100
    Option: (54) DHCP Server Identifier = 192.168.1.1

패킷 4: DHCP Acknowledge
    Bootstrap Protocol (ACK)
    Your (client) IP address: 192.168.1.100
    DHCP: ACK
    Option: (53) DHCP Message Type = ACK
    Option: (51) IP Address Lease Time = 86400 sec
    Option: (1) Subnet Mask = 255.255.255.0
    Option: (3) Router = 192.168.1.1
    Option: (6) Domain Name Server = 8.8.8.8, 8.8.4.4


### (B) Untangle 방화벽 실습

**네트워크 토폴로지:**

[로컬 PC] ←(NAT 포트포워딩: 3030→80)→ [Untangle Firewall: WAN=10.0.2.10, Internal=192.168.2.1, DMZ=192.168.3.1] ←→ [Internal Server: 192.168.2.80] / [Web Server: 192.168.3.90]


**방화벽 룰 설정 실습:**

**1. Server → Web Server HTTP 차단:**

Description: Block HTTP from Server to Web Server
Source Address: 192.168.2.80
Destination Address: 192.168.3.90
Destination Port: 80
Protocol: TCP
Action: Block
Flag: Enabled

결과:
Server에서 http://192.168.3.90 접속 → 연결 시간 초과


**2. Server → Web Server SSH 허용, 나머지 차단:**

룰 1 (우선순위 높음):
Description: Allow SSH from Server to Web Server
Source Address: 192.168.2.80
Destination Address: 192.168.3.90
Destination Port: 22
Protocol: TCP
Action: Pass
Flag: Enabled

룰 2:
Description: Block all services from Server to Web Server
Source Address: 192.168.2.80
Destination Address: 192.168.3.90
Protocol: Any
Action: Block
Flag: Enabled

결과:
Server에서 ssh ubuntu@192.168.3.90 → 접속 성공
Server에서 http://192.168.3.90 → 차단


**3. 외부 → Web Server HTTP 접속 (포트 포워딩):**

# VirtualBox NAT 포트 포워딩 설정
Name: http_port_forward
Protocol: TCP
Host Port: 3030
Guest IP: 10.0.2.10 (방화벽 WAN IP)
Guest Port: 80

# Untangle 포트 포워딩 룰
Enable: Checked
Description: HTTP port forward to Web Server
Protocol: TCP
Destination Port: 80
Source Interface: External
New Destination: 192.168.3.90 (Web Server IP)
New Port: 80

# 방화벽 룰 (외부 → Web Server HTTP 허용)
Description: Allow external HTTP to Web Server
Source Address: 0.0.0.0/0 (Any)
Destination Address: 192.168.3.90
Destination Port: 80
Protocol: TCP
Action: Pass
Flag: Enabled

결과:
로컬 PC 브라우저에서 http://127.0.0.1:3030 → Web Server 접속 성공


**4. Outbound Traffic 허용:**

Description: Allow outbound traffic
Source Interface: Internal, Interface3 (DMZ)
Destination Interface: External
Protocol: Any
Action: Pass
Flag: Enabled

결과:
Server/Web Server에서 외부 인터넷(www.wikipedia.org 등) 접속 성공


### (C) Suricata IDS/IPS 실습

**Suricata 설치 및 설정 (Web Server):**
```bash
# Suricata 설치
sudo apt update
sudo apt install -y suricata

# 버전 확인
suricata -V

# 기본 룰셋 다운로드 (Emerging Threats Open)
sudo suricata-update

# 설정 파일 편집
sudo vi /etc/suricata/suricata.yaml

# 네트워크 인터페이스 지정
af-packet:
  - interface: enp0s3   # 모니터링할 인터페이스

# 사용자 정의 룰 파일 추가
rule-files:
  - suricata.rules      # 기본 룰셋
  - local.rules         # 사용자 정의 룰

# Suricata 재시작
sudo systemctl restart suricata
sudo systemctl status suricata
```

**Suricata 룰 문법:**

Action Protocol Source_IP Source_Port Direction Dest_IP Dest_Port (Rule_Options)

Action:
- alert: 탐지 시 로그 기록
- drop: 패킷 차단 (IPS 모드)
- reject: 패킷 차단 + RST 전송
- pass: 허용

Direction:
- ->  : 단방향
- <>  : 양방향

Rule_Options:
- msg: "경고 메시지";           # 로그에 기록될 메시지
- sid: 100001;                   # 룰 고유 ID
- rev: 1;                        # 룰 버전
- classtype: trojan-activity;    # 위협 분류
- content: "GET /admin";         # 페이로드 검색
- nocase;                        # 대소문자 구분 안 함
- flow: to_server, established;  # 트래픽 방향 및 세션 상태


**실습 룰 작성:**

**1. ICMP 연결 시도 탐지:**
```bash
sudo vi /etc/suricata/rules/local.rules

alert icmp any any -> $HOME_NET any (msg:"ICMP connecting test"; sid:100001; rev:1;)

sudo systemctl reload suricata

# 다른 터미널에서 로그 실시간 모니터링
sudo tail -f /var/log/suricata/fast.log

# Server에서 Web Server로 ping
ping 192.168.3.90

# 로그 확인
# [**] [1:100001:1] ICMP connecting test [**] [Priority: 3] {ICMP} 192.168.2.80:8 -> 192.168.3.90:0
```

**2. 특정 도메인 접속 탐지 (tistory.com):**
```bash
sudo vi /etc/suricata/rules/local.rules

alert tcp any any -> any 80 (msg:"tistory.com access detected"; content:"GET /"; content:"Host: "; content:"tistory.com"; nocase; sid:100002; rev:1;)

sudo systemctl reload suricata

# Firefox에서 http://tistory.com 접속

# 로그 확인
# [**] [1:100002:1] tistory.com access detected [**] [Priority: 3] {TCP} 192.168.3.90:59068 -> 211.183.210.24:80
```

**3. SQL Injection 공격 탐지:**
```bash
alert tcp any any -> any 80 (msg:"Possible SQL Injection attack"; content:"' OR '1'='1"; nocase; flow:to_server, established; classtype:web-application-attack; sid:100003; rev:1;)

alert tcp any any -> any 80 (msg:"SQL Injection - UNION SELECT"; content:"UNION"; nocase; content:"SELECT"; nocase; distance:0; within:20; flow:to_server, established; classtype:web-application-attack; sid:100004; rev:1;)
```

**4. Port Scanning 탐지:**
```bash
alert tcp any any -> $HOME_NET any (msg:"Possible Port Scan detected"; flags:S; threshold:type both, track by_src, count 20, seconds 10; classtype:attempted-recon; sid:100005; rev:1;)

# 짧은 시간(10초) 내 동일 출발지에서 20개 이상 SYN 패킷 전송 시 탐지
```

**5. C&C 통신 탐지 (DGA 도메인):**
```bash
alert dns any any -> any 53 (msg:"Possible DGA domain - Random string pattern"; dns_query; content:".com"; pcre:"/[a-z]{10,}\.com/i"; threshold:type both, track by_src, count 5, seconds 60; classtype:trojan-activity; sid:100006; rev:1;)

# 10글자 이상의 무작위 문자열 도메인을 1분 내 5회 이상 조회 시 의심
```

**Suricata 로그 분석:**
```bash
# 실시간 로그 (간단)
sudo tail -f /var/log/suricata/fast.log

# 상세 로그 (EVE JSON)
sudo tail -f /var/log/suricata/eve.json | jq '.'

# 특정 SID만 필터링
sudo grep "sid:100002" /var/log/suricata/fast.log

# 특정 IP에서 발생한 이벤트
sudo grep "192.168.2.80" /var/log/suricata/fast.log
```

---

## 3. 실무/보안 관점 분석 (Insight & Scenario Mapping)

| 분야 | 적용 시나리오 |
|:---:|:---|
| **SOC / 관제** | **계층별 방어 전략**: 방화벽(L3/L4)으로 불필요한 포트 차단 → IPS(L7)로 허용된 포트 내 악성 트래픽 탐지 → WAF로 웹 애플리케이션 공격 차단 → SIEM에서 로그 통합 분석. **실시간 모니터링**: Suricata/Snort 이벤트를 SIEM(Splunk, ELK)으로 전송하여 대시보드 구성. 임계값 기반 알림(예: 1분 내 동일 출발지에서 100개 이상 차단 이벤트 → 자동 IP 차단). **오탐 튜닝**: 정상 트래픽이 오탐되면 룰 수정 또는 화이트리스트 추가. 예: 내부 개발 서버의 정상적인 SQL 쿼리가 SQL Injection으로 오탐 → `suppress` 사용하여 해당 IP 예외 처리. |
| **CERT / 사고 대응** | **침해 사고 분석**: 방화벽/IPS 로그에서 공격 타임라인 재구성. (1) 포트 스캔 로그 → (2) 취약점 익스플로잇 시도 → (3) 초기 침투 성공 → (4) 권한 상승 → (5) C&C 통신 → (6) 데이터 유출. **차단 규칙 긴급 배포**: 공격 패턴 식별 후 Suricata 룰 긴급 작성 및 배포. 예: 특정 악성 도메인으로의 DNS 쿼리 차단 `alert dns any any -> any 53 (msg:"Block malicious C&C"; dns_query; content:"evil.com"; nocase; drop; sid:999001; rev:1;)`. **포렌식 패킷 분석**: PCAP 파일에서 Wireshark와 Suricata를 결합하여 공격 페이로드 추출. |
| **네트워크 운영** | **방화벽 정책 최적화**: 불필요한 룰 제거, 룰 순서 최적화(자주 매칭되는 룰을 상단으로), 로그 레벨 조정. **DMZ 설계**: 공개 서비스(웹, 메일)는 DMZ에 배치하고, 내부 네트워크와 분리. 방화벽 룰: (1) 외부 → DMZ: 필요 포트만 허용, (2) DMZ → 내부: 최소 권한(DB 쿼리 포트만), (3) 내부 → DMZ: 관리 포트(SSH)만. **IDS/IPS 성능 튜닝**: 네트워크 대역폭이 높으면 패킷 드롭 발생 가능. 불필요한 룰 비활성화, 하드웨어 성능 향상(멀티코어, NIC 오프로드), AF_PACKET 모드 사용. |

---

## 4. 개인 인사이트 및 다음 단계 (Reflection & Next Steps)

* **배운 점/느낀 점:**
  - **계층별 방어의 중요성**: 방화벽만으로는 부족하고, IDS/IPS, WAF, SIEM을 결합한 **다층 방어(Defense in Depth)**가 필수임을 깨달았습니다. 방화벽은 "문지기"이고, IPS는 "내부 경비원"인 셈입니다.
  - **룰 작성의 예술**: Suricata 룰을 직접 작성하며, 시그니처 기반 탐지의 강력함과 한계를 동시에 느꼈습니다. **너무 엄격하면 오탐**, **너무 느슨하면 미탐**. 정교한 룰 작성과 지속적인 튜닝이 핵심입니다.
  - **방화벽 룰 순서의 중요성**: First Match 원칙 때문에 룰 순서가 틀리면 의도와 다르게 동작합니다. "허용 → 차단" 순서를 명확히 하고, 가장 구체적인 룰을 상단에 배치해야 합니다.
  - **포트 포워딩의 위험성**: 내부 서버를 외부에 노출할 때 단순 포트 포워딩은 공격 표면을 넓힙니다. Reverse Proxy나 VPN을 통한 접근이 안전합니다.
  - **DNS의 중요성**: 모든 통신이 DNS로 시작되므로, DNS 로그 분석으로 C&C 통신, DGA 멀웨어, DNS Tunneling을 조기 탐지할 수 있습니다.

* **심화 방향:**
  - **SIEM 통합**: Suricata 로그를 ELK Stack(Elasticsearch, Logstash, Kibana)으로 전송하여 대시보드 구축. 실시간 알림 설정 및 통계 분석.
  - **WAF 실습**: ModSecurity를 설치하여 웹 애플리케이션 방화벽 룰(OWASP CRS) 적용. SQL Injection, XSS 차단 실습.
  - **Zeek(Bro) 학습**: 네트워크 트래픽을 메타데이터로 변환하여 분석하는 도구. Suricata와 결합하여 더 깊은 네트워크 가시성 확보.
  - **Threat Hunting**: MITRE ATT&CK 프레임워크 기반으로 능동적 위협 사냥. 특정 TTP(Tactics, Techniques, Procedures)를 Suricata 룰로 구현.
  - **고급 공격 시나리오 재현**: Metasploit으로 취약점 익스플로잇 → Suricata로 탐지 → 룰 최적화. 실제 공격-방어 사이클 경험.

---

## 5. 추가 참고사항 (Quick Reference)

### 주요 애플리케이션 계층 프로토콜 & 포트

| 프로토콜 | 포트 | 설명 | 보안 고려사항 |
|:---:|:---:|:---|:---|
| **HTTP** | 80 | 웹 브라우징 (평문) | 평문 전송, 중간자 공격 취약. HTTPS 사용 필수 |
| **HTTPS** | 443 | 암호화된 웹 브라우징 (SSL/TLS) | 인증서 검증, TLS 1.2+ 사용, 약한 암호화 금지 |
| **FTP** | 20, 21 | 파일 전송 (평문) | 평문 전송, 익명 로그인. SFTP/FTPS 사용 권장 |
| **SFTP** | 22 | SSH 기반 암호화 파일 전송 | SSH 키 관리, 강력한 비밀번호 |
| **SSH** | 22 | 원격 접속 (암호화) | 키 기반 인증, root 직접 로그인 금지, 포트 변경 |
| **Telnet** | 23 | 원격 접속 (평문) | 절대 사용 금지, SSH로 대체 |
| **SMTP** | 25 | 메일 전송 | SMTP Relay 방지, SPF/DKIM/DMARC 설정 |
| **DNS** | 53 | 도메인 이름 해석 | DNSSEC, DNS Spoofing 방어, 재귀 쿼리 제한 |
| **DHCP** | 67, 68 | IP 자동 할당 | DHCP Snooping, Rogue DHCP 방어 |
| **SNMP** | 161, 162 | 네트워크 장비 관리 | SNMPv3 사용(암호화 및 인증), v1/v2c 금지 |
| **RDP** | 3389 | Windows 원격 데스크톱 | NLA 활성화, 강력한 비밀번호, VPN 통해서만 접근 |
| **SMB** | 445 | Windows 파일 공유 | SMBv1 비활성화, 방화벽으로 외부 차단 |
| **MySQL** | 3306 | MySQL 데이터베이스 | 외부 접근 차단, 강력한 비밀번호, 최소 권한 |

### Suricata 룰 키워드 정리

| 카테고리 | 키워드 | 설명 | 예시 |
|:---:|:---:|:---|:---|
| **메타정보** | msg | 로그에 표시될 메시지 | `msg:"SQL Injection detected";` |
| | sid | 룰 고유 ID (사용자 정의는 1000000부터) | `sid:100001;` |
| | rev | 룰 버전 | `rev:1;` |
| | classtype | 위협 분류 | `classtype:web-application-attack;` |
| **페이로드** | content | 페이로드 내용 검색 | `content:"password";` |
| | nocase | 대소문자 구분 안 함 | `content:"admin"; nocase;` |
| | distance | 이전 매칭 후 N바이트 이동 | `content:"OR"; distance:0; within:10;` |
| | pcre | 정규표현식 | `pcre:"/[0-9]{4}-[0-9]{4}/";` |
| **DNS** | dns_query | DNS 쿼리 | `dns_query; content:".tk";` |
| **Flow** | flow | 트래픽 방향 및 세션 상태 | `flow:to_server,established;` |
| **Threshold** | threshold | 임계값 기반 탐지 | `threshold:type both, track by_src, count 10, seconds 60;` |

### 방화벽 정책 설계 원칙


1. Default Deny (기본 차단)
   - 모든 트래픽을 차단한 후, 필요한 것만 허용
   - 마지막 룰: "모두 차단"

2. Least Privilege (최소 권한)
   - 필요한 최소한의 포트/프로토콜만 허용
   - 특정 출발지/목적지로 제한 (Any → Any 지양)

3. 계층별 분리
   - DMZ: 외부에 노출되는 서비스 (웹, 메일)
   - Internal: 내부 업무 네트워크
   - Management: 관리 네트워크 (별도 분리)

4. 룰 순서 최적화
   - 구체적인 룰 → 일반적인 룰
   - 자주 매칭되는 룰을 상단으로
   - 예: (1) 특정 IP 차단, (2) SSH 허용, (3) HTTP/HTTPS 허용, (4) 모두 차단

5. 로깅 전략
   - 허용 룰: 필요시만 로깅 (트래픽 과다)
   - 차단 룰: 모두 로깅 (공격 시도 분석)

6. 정기 검토
   - 분기별 불필요한 룰 제거
   - 로그 분석 후 정책 최적화


### Wireshark 필터 (애플리케이션 계층)

```
# HTTP
http
http.request
http.request.method == "POST"
http.request.uri contains "admin"
http.response.code == 200
http.cookie contains "session"

# HTTPS/TLS
tls.handshake.type == 1        # Client Hello
tls.handshake.type == 2        # Server Hello
tls.handshake.type == 11       # Certificate

# DNS
dns
dns.qry.name contains "google"
dns.flags.response == 0        # 쿼리만
dns.flags.response == 1        # 응답만
dns.qry.type == 1              # A 레코드
dns.qry.type == 28             # AAAA 레코드

# DHCP
dhcp
bootp.option.dhcp == 1         # Discover
bootp.option.dhcp == 2         # Offer
bootp.option.dhcp == 3         # Request
bootp.option.dhcp == 5         # ACK

# FTP
ftp
ftp.request.command == "USER"
ftp.request.command == "PASS"

# SSH
ssh
ssh.protocol contains "2.0"

# Telnet (매우 위험!)
telnet
tcp.port == 23
```


### 보안 체크리스트

**웹 서버:**

☑ HTTPS 적용 (인증서 유효성 확인)
☑ HTTP → HTTPS 리다이렉션
☑ HSTS 헤더 설정
☑ 불필요한 HTTP 메서드 비활성화 (OPTIONS, TRACE)
☑ Directory Listing 비활성화
☑ 에러 메시지에서 버전 정보 숨김
☑ 최신 보안 패치 적용


**방화벽:**

☑ Default Deny 정책
☑ 관리 인터페이스 내부망에서만 접근
☑ 불필요한 포트 모두 차단
☑ 로그 레벨 적절히 설정
☑ 룰 순서 검증
☑ 변경 이력 관리


**IDS/IPS:**

☑ 최신 룰셋 업데이트
☑ 오탐 룰 튜닝
☑ 임계값 설정
☑ 로그 정기 검토
☑ SIEM 연동
☑ 성능 모니터링 (패킷 드롭 확인)

