---
title: "2025.12.02 (Day 27) - TCP/IP 네트워크 종합: 애플리케이션 계층 & 네트워크 보안 (방화벽, IDS/IPS)"
date: 2025-12-02
draft: false
tags: ["네트워크", "보안", "방화벽", "IDS", "IPS", "Suricata", "HTTP", "DNS", "DHCP", "Wireshark"]
categories: ["daily-logs"]
summary: "애플리케이션 계층 프로토콜(HTTP/HTTPS, DNS, DHCP) 분석, Untangle 방화벽 룰 설정, Suricata IDS/IPS 룰 작성 및 실습"
---

# 📄 2025.12.02 (Day 27) - TCP/IP 네트워크 종합: 애플리케이션 계층 & 네트워크 보안 (방화벽, IDS/IPS)

---

## 1. 핵심 개념 정리

| # | 핵심 개념 | 간결한 설명 | 실무/보안 관점에서의 중요성 |
|:---:|:---|:---|:---|
| **1** | **애플리케이션 계층 (Application Layer)** | OSI 7계층으로 **최종 사용자 서비스**를 제공합니다. HTTP, HTTPS, FTP, SMTP, DNS, DHCP, SSH, Telnet 등의 프로토콜이 동작하며, **포트 번호**를 통해 서비스를 식별합니다. | **대부분의 공격이 발생하는 계층**입니다. SQL Injection, XSS, CSRF, DNS Spoofing 등 다양한 애플리케이션 레벨 공격이 존재합니다. WAF(Web Application Firewall)로 방어합니다. |
| **2** | **HTTP/HTTPS** | **HTTP**(HyperText Transfer Protocol)는 **80번 포트**를 사용하며 **평문** 전송으로 도청/변조에 취약합니다. **HTTPS**는 SSL/TLS로 암호화한 HTTP로 **443번 포트**를 사용합니다. GET, POST, PUT, DELETE 등 메서드로 요청합니다. | **HTTPS는 필수**입니다. HTTP는 세션 하이재킹, 중간자 공격, 쿠키 탈취에 취약합니다. HSTS(HTTP Strict Transport Security)로 강제 HTTPS 적용이 권장됩니다. |
| **3** | **DNS (Domain Name System)** | 도메인 이름을 IP 주소로 변환하는 시스템입니다. **53번 포트**(UDP 주로 사용, TCP는 Zone Transfer). **A 레코드**(IPv4), **AAAA 레코드**(IPv6), **MX 레코드**(메일 서버), **CNAME**(별칭) 등의 레코드 타입이 존재합니다. | **DNS Spoofing/Cache Poisoning** 공격의 대상입니다. **DNSSEC**로 DNS 응답의 무결성을 검증하고, **DoH(DNS over HTTPS)** 또는 **DoT(DNS over TLS)**로 암호화합니다. |
| **4** | **DHCP (Dynamic Host Configuration Protocol)** | IP 주소를 **자동으로 할당**하는 프로토콜입니다. **67번(서버), 68번(클라이언트) 포트** 사용. **DORA 과정**: (1) **Discover** → (2) **Offer** → (3) **Request** → (4) **Acknowledge**. | **DHCP Starvation** 공격(IP 풀 고갈)과 **Rogue DHCP Server** 공격의 대상입니다. **DHCP Snooping**으로 신뢰할 수 있는 DHCP 서버만 허용합니다. |
| **5** | **방화벽 (Firewall)** | 네트워크 트래픽을 **정책(Rule)** 기반으로 **허용/차단**하는 보안 장비입니다. **패킷 필터링 방화벽**(L3/L4: IP/포트 기반), **상태 기반 방화벽**(Stateful: 세션 추적), **애플리케이션 방화벽**(L7: 프로토콜 분석), **차세대 방화벽**(NGFW: IPS 통합)으로 발전했습니다. | **네트워크 경계 방어**의 핵심입니다. 룰 순서(First Match 원칙), Default Deny, 최소 권한 허용이 기본 원칙입니다. |
| **6** | **IDS/IPS** | **IDS**는 침입을 **탐지**하여 **알림**만 제공하고, **IPS**는 침입을 **탐지 + 차단**합니다. **시그니처 기반**(알려진 공격 패턴 매칭)과 **이상 징후 기반**(정상 행위에서 벗어난 패턴 탐지)으로 나뉩니다. **Suricata**, **Snort**가 대표적인 오픈소스 IDS/IPS입니다. | **방화벽을 우회한 공격**을 탐지/차단합니다. 방화벽은 허용된 포트 내 악성 트래픽을 구별하지 못하지만, IDS/IPS는 **패킷 페이로드**를 분석하여 SQL Injection, 버퍼 오버플로우, C&C 통신 등을 탐지합니다. **오탐(False Positive)** 최소화가 중요합니다. |

---

## 2. 실습 내용

### (A) 애플리케이션 계층 프로토콜 분석

**HTTP/HTTPS 요청 분석 (Wireshark):**

HTTP 요청 (평문):
- GET / HTTP/1.1
- Host: example.com
- User-Agent: Mozilla/5.0
- Wireshark 필터: **http.request**
- → 모든 데이터(쿠키, 세션 토큰, 비밀번호)가 평문으로 노출

HTTPS 요청 (암호화):
- TLS Handshake 단계: Client Hello → Server Hello + Certificate → Key Exchange → Encrypted Application Data
- Wireshark 필터: **tls.handshake.type == 1** (Client Hello)
- → 암호화된 데이터는 Wireshark에서도 내용 확인 불가 (서버의 Private Key 없이는 복호화 불가)

**DNS 쿼리 분석:**

DNS 쿼리 관련 명령어:
- **nslookup google.com** → DNS 쿼리 (Windows/Linux)
- **dig google.com** → 상세 DNS 쿼리 (Linux)
- **dig google.com +short** → IP만 출력
- **dig google.com ANY** → 모든 레코드
- **dig google.com MX** → 메일 서버 레코드
- **dig @8.8.8.8 google.com** → 특정 DNS 서버 지정

Wireshark DNS 패킷 분석:
- 쿼리: Transaction ID 0x1234, Flags 0x0100 (Standard query), 질문 유형 A (IPv4)
- 응답: Transaction ID 0x1234, Flags 0x8180 (Standard query response, No error), 답변: google.com → 142.250.185.46

**DHCP DORA 과정 (Wireshark):**

- 패킷 1: **DHCP Discover** - 클라이언트가 브로드캐스트로 DHCP 서버 탐색 (Option 53: Discover)
- 패킷 2: **DHCP Offer** - 서버가 IP 제안 (Your IP: 192.168.1.100, Lease Time: 86400초, Option 53: Offer)
- 패킷 3: **DHCP Request** - 클라이언트가 제안된 IP 수락 요청 (Option 50: Requested IP 192.168.1.100)
- 패킷 4: **DHCP Acknowledge** - 서버가 할당 확정 (Subnet Mask, Router, DNS 정보 포함)

---

### (B) Untangle 방화벽 실습

**네트워크 토폴로지:**
- 로컬 PC -- (NAT 포트포워딩: 3030 → 80) -- Untangle Firewall (WAN=10.0.2.10, Internal=192.168.2.1, DMZ=192.168.3.1) -- Internal Server (192.168.2.80) / Web Server (192.168.3.90)

**방화벽 룰 설정 실습:**

**1. Server → Web Server HTTP 차단:**
- Description: Block HTTP from Server to Web Server
- Source Address: 192.168.2.80, Destination Address: 192.168.3.90
- Destination Port: 80, Protocol: TCP, Action: **Block**
- 결과: Server에서 http://192.168.3.90 접속 → 연결 시간 초과

**2. Server → Web Server SSH 허용, 나머지 차단 (룰 순서 중요):**
- 룰 1 (높은 우선순위): SSH 허용
  - Source: 192.168.2.80, Destination: 192.168.3.90, Port: 22, Action: **Pass**
- 룰 2: 나머지 전체 차단
  - Source: 192.168.2.80, Destination: 192.168.3.90, Protocol: Any, Action: **Block**
- 결과:
  - **ssh ubuntu@192.168.3.90** → 접속 성공
  - http://192.168.3.90 → 차단

**3. 외부 → Web Server HTTP 접속 (포트 포워딩):**
- VirtualBox NAT 포트 포워딩: Host Port 3030 → Guest IP 10.0.2.10 (Untangle WAN), Guest Port 80
- Untangle 포트 포워딩 룰: TCP, Destination Port 80, Source Interface External, New Destination 192.168.3.90:80
- 방화벽 룰: Source 0.0.0.0/0, Destination 192.168.3.90, Port 80, Action Pass
- 결과: 로컬 PC 브라우저에서 http://127.0.0.1:3030 → Web Server 접속 성공

**4. Outbound Traffic 허용:**
- Source Interface: Internal, DMZ, Destination Interface: External, Protocol: Any, Action: **Pass**
- 결과: Server/Web Server에서 외부 인터넷 접속 성공

---

### (C) Suricata IDS/IPS 실습

**Suricata 설치 및 기본 설정 (Web Server):**
- **sudo apt update && sudo apt install -y suricata** → 설치
- **suricata -V** → 버전 확인
- **sudo suricata-update** → 기본 룰셋(Emerging Threats Open) 다운로드
- 설정 파일: **/etc/suricata/suricata.yaml**
  - af-packet 섹션에 모니터링 인터페이스 지정: **interface: enp0s3**
  - rule-files 섹션에 사용자 정의 룰 파일 추가: **local.rules**
- **sudo systemctl restart suricata** → 서비스 재시작

**Suricata 룰 문법:**

Action Protocol Source_IP Source_Port Direction Dest_IP Dest_Port (Rule_Options)

Action 종류:
- **alert**: 탐지 시 로그 기록
- **drop**: 패킷 차단 (IPS 모드)
- **reject**: 패킷 차단 + RST 전송
- **pass**: 허용

Direction:
- **->** : 단방향
- **<>** : 양방향

Rule_Options 주요 키워드:
- **msg:"경고 메시지"** → 로그에 기록될 메시지
- **sid:100001** → 룰 고유 ID
- **rev:1** → 룰 버전
- **classtype:trojan-activity** → 위협 분류
- **content:"GET /admin"** → 페이로드 검색
- **nocase** → 대소문자 구분 안 함
- **flow:to_server, established** → 트래픽 방향 및 세션 상태

**실습 룰 작성:**

**1. ICMP 연결 시도 탐지:**
- 룰 파일 경로: /etc/suricata/rules/local.rules
- 내용: alert icmp any any -> $HOME_NET any (msg:"ICMP connecting test"; sid:100001; rev:1;)
- 테스트: ping 192.168.3.90
- 로그 확인 (fast.log): [**] [1:100001:1] ICMP connecting test [**] {ICMP} 192.168.2.80:8 -> 192.168.3.90:0

**2. 특정 도메인 접속 탐지 (tistory.com):**
- alert tcp any any -> any 80 (msg:"tistory.com access detected"; content:"GET /"; content:"Host: "; content:"tistory.com"; nocase; sid:100002; rev:1;)
- Firefox에서 http://tistory.com 접속 시 탐지

**3. SQL Injection 공격 탐지:**
- alert tcp any any -> any 80 (msg:"Possible SQL Injection attack"; content:"' OR '1'='1"; nocase; flow:to_server, established; classtype:web-application-attack; sid:100003; rev:1;)
- alert tcp any any -> any 80 (msg:"SQL Injection - UNION SELECT"; content:"UNION"; nocase; content:"SELECT"; nocase; distance:0; within:20; flow:to_server, established; sid:100004; rev:1;)

**4. Port Scanning 탐지:**
- alert tcp any any -> $HOME_NET any (msg:"Possible Port Scan detected"; flags:S; threshold:type both, track by_src, count 20, seconds 10; classtype:attempted-recon; sid:100005; rev:1;)
- 10초 내 동일 출발지에서 20개 이상 SYN 패킷 전송 시 탐지

**5. C&C 통신 탐지 (DGA 도메인):**
- alert dns any any -> any 53 (msg:"Possible DGA domain - Random string pattern"; dns_query; content:".com"; pcre:"/[a-z]{10,}\.com/i"; threshold:type both, track by_src, count 5, seconds 60; classtype:trojan-activity; sid:100006; rev:1;)

**Suricata 로그 분석 명령어:**
- **sudo tail -f /var/log/suricata/fast.log** → 실시간 간단 로그
- **sudo tail -f /var/log/suricata/eve.json | jq '.'** → 상세 JSON 로그
- **sudo grep "sid:100002" /var/log/suricata/fast.log** → 특정 SID 필터링
- **sudo grep "192.168.2.80" /var/log/suricata/fast.log** → 특정 IP 이벤트

---

## 3. 실무/보안 관점 분석

| 분야 | 적용 시나리오 |
|:---:|:---|
| **SOC / 관제** | **계층별 방어 전략**: 방화벽(L3/L4)으로 불필요한 포트 차단 → IPS(L7)로 허용된 포트 내 악성 트래픽 탐지 → WAF로 웹 애플리케이션 공격 차단 → SIEM에서 로그 통합 분석. **실시간 모니터링**: Suricata/Snort 이벤트를 SIEM(Splunk, ELK)으로 전송하여 대시보드 구성. **오탐 튜닝**: 정상 트래픽이 오탐되면 룰 수정 또는 화이트리스트 추가. |
| **CERT / 사고 대응** | **침해 사고 분석**: 방화벽/IPS 로그에서 공격 타임라인 재구성 (포트 스캔 → 익스플로잇 시도 → 초기 침투 → 권한 상승 → C&C 통신 → 데이터 유출). **차단 규칙 긴급 배포**: 공격 패턴 식별 후 Suricata 룰 긴급 작성 및 배포. **포렌식 패킷 분석**: PCAP 파일에서 Wireshark와 Suricata를 결합하여 공격 페이로드 추출. |
| **네트워크 운영** | **방화벽 정책 최적화**: 불필요한 룰 제거, 룰 순서 최적화(자주 매칭되는 룰을 상단으로), 로그 레벨 조정. **DMZ 설계**: 공개 서비스(웹, 메일)는 DMZ에 배치, (1) 외부 → DMZ: 필요 포트만 허용, (2) DMZ → 내부: 최소 권한, (3) 내부 → DMZ: 관리 포트(SSH)만. |

---

## 4. 개인 인사이트 및 다음 단계

- **배운 점/느낀 점**: 방화벽만으로는 부족하고, IDS/IPS, WAF, SIEM을 결합한 **다층 방어(Defense in Depth)**가 필수임을 깨달았습니다. 방화벽은 "문지기"이고, IPS는 "내부 경비원"인 셈입니다. Suricata 룰을 직접 작성하며 **너무 엄격하면 오탐**, **너무 느슨하면 미탐**이라는 균형의 어려움을 체감했습니다. DNS 로그 분석으로 C&C 통신, DGA 멀웨어, DNS Tunneling을 조기 탐지할 수 있다는 점도 인상적이었습니다.
- **심화 방향**: SIEM 통합(Suricata 로그를 ELK Stack으로 전송하여 대시보드 구축), WAF 실습(ModSecurity + OWASP CRS), Zeek(Bro) 학습, MITRE ATT&CK 프레임워크 기반 Threat Hunting, Metasploit으로 취약점 익스플로잇 → Suricata 탐지 → 룰 최적화 사이클 경험을 목표로 합니다.

---

## 5. 추가 참고사항 (Quick Reference)

### 주요 애플리케이션 계층 프로토콜 & 포트

| 프로토콜 | 포트 | 설명 | 보안 고려사항 |
|:---:|:---:|:---|:---|
| **HTTP** | 80 | 웹 브라우징 (평문) | 평문 전송, HTTPS 사용 필수 |
| **HTTPS** | 443 | 암호화된 웹 브라우징 (SSL/TLS) | 인증서 검증, TLS 1.2+ 사용 |
| **FTP** | 20, 21 | 파일 전송 (평문) | SFTP/FTPS 사용 권장 |
| **SFTP/SSH** | 22 | 암호화 파일 전송 / 원격 접속 | 키 기반 인증, root 직접 로그인 금지 |
| **Telnet** | 23 | 원격 접속 (평문) | 절대 사용 금지, SSH로 대체 |
| **SMTP** | 25 | 메일 전송 | SMTP Relay 방지, SPF/DKIM/DMARC 설정 |
| **DNS** | 53 | 도메인 이름 해석 | DNSSEC, DNS Spoofing 방어 |
| **DHCP** | 67, 68 | IP 자동 할당 | DHCP Snooping, Rogue DHCP 방어 |
| **POP3** | 110 | 메일 수신 (평문) | POP3S(995) 사용 권장 |
| **IMAP** | 143 | 메일 수신 (서버 보관) | IMAPS(993) 사용 |
| **SNMP** | 161, 162 | 네트워크 장비 관리 | SNMPv3 사용(암호화 및 인증), v1/v2c 금지 |
| **LDAP** | 389 | 디렉터리 서비스 | LDAPS(636) 사용 |
| **RDP** | 3389 | Windows 원격 데스크톱 | NLA 활성화, VPN 통해서만 접근 |
| **SMB** | 445 | Windows 파일 공유 | SMBv1 비활성화, 방화벽으로 외부 차단 |
| **MySQL** | 3306 | MySQL 데이터베이스 | 외부 접근 차단, 최소 권한 |

### Suricata 룰 키워드 정리

| 카테고리 | 키워드 | 설명 | 예시 |
|:---:|:---:|:---|:---|
| **메타정보** | msg | 로그에 표시될 메시지 | msg:"SQL Injection detected"; |
| | sid | 룰 고유 ID (사용자 정의는 1000000부터) | sid:100001; |
| | rev | 룰 버전 | rev:1; |
| | classtype | 위협 분류 | classtype:web-application-attack; |
| **TCP** | tcp.flags | TCP 플래그 | flags:S; (SYN 플래그) |
| | window | TCP 윈도우 크기 | window:0; |
| **HTTP** | http.method | HTTP 메서드 | http.method; content:"POST"; |
| | http.uri | 요청 URI | http.uri; content:"/admin"; |
| | http.host | Host 헤더 | http.host; content:"evil.com"; |
| | http.user_agent | User-Agent 헤더 | http.user_agent; content:"sqlmap"; |
| **페이로드** | content | 페이로드 내용 검색 | content:"password"; |
| | nocase | 대소문자 구분 안 함 | content:"admin"; nocase; |
| | depth | 시작부터 N바이트 내 검색 | content:"GET"; depth:10; |
| | distance | 이전 매칭 후 N바이트 이동 | content:"OR"; distance:0; within:10; |
| | pcre | 정규표현식 | pcre:"/[0-9]{4}-[0-9]{4}/"; |
| **DNS** | dns_query | DNS 쿼리 | dns_query; content:".tk"; |
| **Flow** | flow | 트래픽 방향 및 세션 상태 | flow:to_server,established; |
| **Threshold** | threshold | 임계값 기반 탐지 | threshold:type both, track by_src, count 10, seconds 60; |

### 방화벽 정책 설계 원칙

1. **Default Deny (기본 차단)**: 모든 트래픽을 차단한 후 필요한 것만 허용. 마지막 룰: "모두 차단"
2. **Least Privilege (최소 권한)**: 필요한 최소한의 포트/프로토콜만 허용. Any → Any 지양
3. **계층별 분리**: DMZ(외부 노출 서비스), Internal(내부 업무), Management(관리 네트워크 별도 분리)
4. **룰 순서 최적화**: 구체적인 룰 → 일반적인 룰 순서. 자주 매칭되는 룰을 상단으로
5. **로깅 전략**: 허용 룰은 필요시만 로깅, 차단 룰은 모두 로깅 (공격 시도 분석)
6. **정기 검토**: 분기별 불필요한 룰 제거, 로그 분석 후 정책 최적화

### Wireshark 필터 (애플리케이션 계층)

| 프로토콜 | 필터 | 설명 |
|:---:|:---|:---|
| **HTTP** | http | 모든 HTTP 패킷 |
| | http.request | HTTP 요청 |
| | http.request.method == "POST" | POST 요청만 |
| | http.request.uri contains "admin" | URI에 admin 포함 |
| | http.response.code == 200 | 응답 코드 200 |
| **HTTPS/TLS** | tls.handshake.type == 1 | Client Hello |
| | tls.handshake.type == 2 | Server Hello |
| | tls.handshake.type == 11 | Certificate |
| **DNS** | dns | 모든 DNS 패킷 |
| | dns.qry.name contains "google" | google 포함 쿼리 |
| | dns.flags.response == 0 | 쿼리만 |
| | dns.flags.response == 1 | 응답만 |
| | dns.qry.type == 1 | A 레코드 |
| **DHCP** | dhcp | 모든 DHCP 패킷 |
| | bootp.option.dhcp == 1 | Discover |
| | bootp.option.dhcp == 2 | Offer |
| | bootp.option.dhcp == 3 | Request |
| | bootp.option.dhcp == 5 | ACK |
| **FTP** | ftp | 모든 FTP |
| | ftp.request.command == "USER" | FTP 사용자 로그인 |
| | ftp.request.command == "PASS" | FTP 비밀번호 (평문 노출!) |

### 보안 체크리스트

**웹 서버:**
- HTTPS 적용 (인증서 유효성 확인)
- HTTP → HTTPS 리다이렉션
- HSTS 헤더 설정
- 불필요한 HTTP 메서드 비활성화 (OPTIONS, TRACE)
- Directory Listing 비활성화
- 에러 메시지에서 버전 정보 숨김
- 최신 보안 패치 적용

**방화벽:**
- Default Deny 정책
- 관리 인터페이스 내부망에서만 접근
- 불필요한 포트 모두 차단
- 로그 레벨 적절히 설정
- 룰 순서 검증
- 변경 이력 관리

**IDS/IPS:**
- 최신 룰셋 업데이트
- 오탐 룰 튜닝
- 임계값 설정
- 로그 정기 검토
- SIEM 연동
- 성능 모니터링 (패킷 드롭 확인)
