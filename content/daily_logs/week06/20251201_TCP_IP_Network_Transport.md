---
title: "2025.12.01 (Day 26) [TCP/IP 네트워크 계층 & 트랜스포트 계층: 라우팅, ARP, ICMP, TCP]"
date: 2025-12-01
draft: false
tags: ["네트워크", "TCP/IP", "ARP", "ICMP", "Wireshark", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "네트워크 계층(ARP, ICMP, 라우팅)과 트랜스포트 계층(TCP 3-Way Handshake)을 Packet Tracer와 Wireshark로 실습"
---

# 📄 2025.12.01 (Day 26) [TCP/IP 네트워크 계층 & 트랜스포트 계층: 라우팅, ARP, ICMP, TCP]

## 1. 핵심 개념 정리 (Concepts & Theory)

| # | 핵심 개념 | 간결한 설명 |
|:---:|:---|:---|
| **1** | **네트워크 계층 (Network Layer)** | OSI 3계층으로 **라우팅**과 **논리적 주소 지정**(IP 주소)을 담당합니다. **라우터**가 핵심 장비이며, 패킷의 출발지에서 목적지까지 **최적 경로**를 결정합니다. 주요 프로토콜: IP, ICMP, ARP, RARP. |
| **2** | **ARP (Address Resolution Protocol)** | IP 주소를 **MAC 주소**로 변환하는 프로토콜입니다. 동일 네트워크 내에서 통신 시 목적지 MAC 주소를 알아내기 위해 **ARP Request**(브로드캐스트)를 보내고, 해당 IP를 가진 호스트가 **ARP Reply**(유니캐스트)로 자신의 MAC 주소를 알려줍니다. |
| **3** | **ICMP (Internet Control Message Protocol)** | 네트워크 진단 및 오류 보고를 위한 프로토콜입니다. **ping**(Echo Request/Reply), **traceroute**, **Destination Unreachable**, **Time Exceeded** 등의 메시지를 전송합니다. IP 계층에서 동작하지만 상위 계층 프로토콜로 분류됩니다. |
| **4** | **라우팅 (Routing)** | 패킷을 목적지까지 전달하기 위해 **최적 경로**를 결정하는 과정입니다. **정적 라우팅**(Static: 관리자가 수동 설정)과 **동적 라우팅**(Dynamic: RIP, OSPF, BGP 등 프로토콜이 자동 경로 학습)으로 나뉩니다. **라우팅 테이블**에 경로 정보를 저장합니다. |
| **5** | **트랜스포트 계층 (Transport Layer)** | OSI 4계층으로 **종단 간(End-to-End) 통신**을 담당합니다. **포트 번호**를 통해 애플리케이션을 식별하고, **신뢰성**(TCP) 또는 **속도**(UDP)를 제공합니다. 주요 프로토콜: TCP, UDP. |
| **6** | **TCP 3-Way Handshake** | TCP 연결 수립 과정: **(1) SYN** (클라이언트→서버: 연결 요청), **(2) SYN+ACK** (서버→클라이언트: 연결 수락), **(3) ACK** (클라이언트→서버: 연결 확립). **Sequence Number**와 **Acknowledgment Number**로 신뢰성을 보장합니다. |

---

## 2. 실습 코드 & 응용 (Practice & Code Walkthrough)

### (A) Packet Tracer 라우팅 실습

**토폴로지 구성:**
```
[PC2: 192.168.10.2] --- [Router1: Fa0/0=192.168.10.1, Fa0/1=11.0.0.1] --- [Router0: Fa0/0=11.0.0.2, Fa0/1=10.0.0.2] --- [Router2: Fa0/0=10.0.0.1, Fa0/1=192.168.20.1] --- [PC3: 192.168.20.2]
```

**Router1 설정:**
```cisco
Router> enable
Router# configure terminal
Router(config)# hostname router1

! FastEthernet 0/0 인터페이스 설정 (PC2쪽)
router1(config)# interface fa0/0
router1(config-if)# ip address 192.168.10.1 255.255.255.0
router1(config-if)# no shutdown
router1(config-if)# exit

! FastEthernet 0/1 인터페이스 설정 (Router0쪽)
router1(config)# interface fa0/1
router1(config-if)# ip address 11.0.0.1 255.0.0.0
router1(config-if)# no shutdown
router1(config-if)# exit

! 정적 라우팅 설정 (Default Gateway)
router1(config)# ip route 0.0.0.0 0.0.0.0 11.0.0.2
router1(config)# exit

! 라우팅 테이블 확인
router1# show ip route
router1# show ip interface brief
```

**Router0 설정 (중간 라우터):**
```cisco
Router> enable
Router# configure terminal
Router(config)# hostname router0

! 인터페이스 설정
router0(config)# interface fa0/0
router0(config-if)# ip address 11.0.0.2 255.0.0.0
router0(config-if)# no shutdown
router0(config-if)# exit

router0(config)# interface fa0/1
router0(config-if)# ip address 10.0.0.2 255.0.0.0
router0(config-if)# no shutdown
router0(config-if)# exit

! 정적 라우팅 설정 (양쪽 네트워크로 가는 경로)
router0(config)# ip route 192.168.10.0 255.255.255.0 11.0.0.1
router0(config)# ip route 192.168.20.0 255.255.255.0 10.0.0.1
```

**Router2 설정:**
```cisco
Router> enable
Router# configure terminal
Router(config)# hostname router2

! 인터페이스 설정
router2(config)# interface fa0/0
router2(config-if)# ip address 10.0.0.1 255.0.0.0
router2(config-if)# no shutdown
router2(config-if)# exit

router2(config)# interface fa0/1
router2(config-if)# ip address 192.168.20.1 255.255.255.0
router2(config-if)# no shutdown
router2(config-if)# exit

! 정적 라우팅 설정
router2(config)# ip route 0.0.0.0 0.0.0.0 10.0.0.2
```

**PC 설정 및 연결 테스트:**

PC2 설정:
- IP: 192.168.10.2
- Subnet Mask: 255.255.255.0
- Default Gateway: 192.168.10.1

PC3 설정:
- IP: 192.168.20.2
- Subnet Mask: 255.255.255.0
- Default Gateway: 192.168.20.1

PC2에서 연결 테스트:
C:\> ping 192.168.10.1      (Router1 확인)
C:\> ping 192.168.20.2      (PC3까지 확인)
C:\> tracert 192.168.20.2   (경로 확인: Router1 → Router0 → Router2 → PC3)


### (B) Wireshark ARP 패킷 분석

**ARP Request (브로드캐스트):**

Ethernet II
    Destination: Broadcast (ff:ff:ff:ff:ff:ff)
    Source: 00:0c:29:3a:2f:1a
    Type: ARP (0x0806)

Address Resolution Protocol (request)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: request (1)
    Sender MAC address: 00:0c:29:3a:2f:1a
    Sender IP address: 192.168.1.100
    Target MAC address: 00:00:00:00:00:00  (아직 모름)
    Target IP address: 192.168.1.1         (알고 싶은 IP)


**ARP Reply (유니캐스트):**

Ethernet II
    Destination: 00:0c:29:3a:2f:1a  (요청자에게만)
    Source: 00:50:56:c0:00:08      (자신의 MAC)
    Type: ARP (0x0806)

Address Resolution Protocol (reply)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: reply (2)
    Sender MAC address: 00:50:56:c0:00:08  (자신의 MAC)
    Sender IP address: 192.168.1.1
    Target MAC address: 00:0c:29:3a:2f:1a  (요청자 MAC)
    Target IP address: 192.168.1.100


**ARP 캐시 확인 (Linux/Windows):**
```bash
# Linux
arp -a
ip neigh show

# Windows
arp -a

# ARP 캐시 삭제
arp -d 192.168.1.1       # 특정 항목
arp -d *                 # 전체 삭제 (Windows)
ip neigh flush all       # 전체 삭제 (Linux)
```

### (C) Wireshark ICMP 패킷 분석

**ICMP Echo Request (ping 요청):**

Internet Protocol Version 4
    Source: 192.168.1.100
    Destination: 8.8.8.8

Internet Control Message Protocol
    Type: 8 (Echo (ping) request)
    Code: 0
    Checksum: 0x1234
    Identifier: 0x0001
    Sequence number: 1
    Data (48 bytes)


**ICMP Echo Reply (ping 응답):**

Internet Protocol Version 4
    Source: 8.8.8.8
    Destination: 192.168.1.100

Internet Control Message Protocol
    Type: 0 (Echo (ping) reply)
    Code: 0
    Checksum: 0x5678
    Identifier: 0x0001
    Sequence number: 1
    Data (48 bytes)


**ICMP Destination Unreachable:**
```
Internet Control Message Protocol
    Type: 3 (Destination unreachable)
    Code: 0 (Network unreachable)
    Code: 1 (Host unreachable)
    Code: 3 (Port unreachable)
    Code: 9 (Network administratively prohibited)
```

**ICMP Time Exceeded (traceroute):**

Internet Control Message Protocol
    Type: 11 (Time-to-live exceeded)
    Code: 0 (Time to live exceeded in transit)

traceroute가 TTL을 1씩 증가시키며 보내면, 각 라우터가 ICMP Time Exceeded를 회신하여 경로를 추적합니다.


### (D) TCP 3-Way Handshake 실습

**1. DNS로 IP 확인:**
```bash
nslookup dictionary.cambridge.org
# 결과: 54.251.164.119 (예시)
```

**2. Wireshark 필터 설정:**

ip.addr == 54.251.164.119 and tcp.port == 443


**3. 브라우저에서 접속:**

https://dictionary.cambridge.org


**4. Wireshark에서 확인한 3-Way Handshake:**

**패킷 #1 (SYN):**

Transmission Control Protocol
    Source Port: 54321 (클라이언트 랜덤 포트)
    Destination Port: 443 (HTTPS)
    Sequence number: 0 (relative)
    Acknowledgment number: 0
    Flags: 0x002 (SYN)
        ..0. .... .... = ACK: Not set
        ...0 .... .... = PSH: Not set
        .... 0... .... = RST: Not set
        .... .0.. .... = SYN: Set
        .... ..0. .... = FIN: Not set
    Window size: 65535


**패킷 #2 (SYN+ACK):**

Transmission Control Protocol
    Source Port: 443
    Destination Port: 54321
    Sequence number: 0 (relative)
    Acknowledgment number: 1
    Flags: 0x012 (SYN, ACK)
        ..1. .... .... = ACK: Set
        ...0 .... .... = PSH: Not set
        .... 0... .... = RST: Not set
        .... .1.. .... = SYN: Set
        .... ..0. .... = FIN: Not set
    Window size: 29200


**패킷 #3 (ACK):**

Transmission Control Protocol
    Source Port: 54321
    Destination Port: 443
    Sequence number: 1
    Acknowledgment number: 1
    Flags: 0x010 (ACK)
        ..1. .... .... = ACK: Set
        ...0 .... .... = PSH: Not set
        .... 0... .... = RST: Not set
        .... .0.. .... = SYN: Not set
        .... ..0. .... = FIN: Not set
    Window size: 65535

→ 연결 확립 완료, 이후 데이터 전송 시작


### (E) 포트 스캔 실습 (nmap)

**기본 포트 스캔:**
```bash
# 자신의 IP 확인
ipconfig  (Windows)
ifconfig  (Linux/Mac)

# nmap으로 로컬 호스트 스캔
nmap 127.0.0.1
nmap localhost

# 자신의 IP로 스캔 (모든 인터페이스)
nmap 192.168.1.100

# 특정 포트만 스캔
nmap -p 80,443,22,3389 192.168.1.100

# 서비스 버전 탐지
nmap -sV 192.168.1.100

# OS 탐지
nmap -O 192.168.1.100

# 상세 스캔 (Intense Scan)
nmap -T4 -A -v 192.168.1.100
# -T4: 속도 설정 (빠름)
# -A: OS 탐지, 버전 탐지, 스크립트 스캔, traceroute
# -v: 상세 출력
```

**TCP 스캔 방법:**
```bash
# TCP SYN Scan (Half-open, 가장 빠름)
nmap -sS 192.168.1.100

# TCP Connect Scan (Full connection)
nmap -sT 192.168.1.100

# TCP ACK Scan (방화벽 탐지)
nmap -sA 192.168.1.100

# UDP Scan (느림)
nmap -sU 192.168.1.100

# 고속 모드 (상위 100개 포트만)
nmap -F 192.168.1.100
```

**nmap 결과 해석:**

PORT     STATE    SERVICE
22/tcp   open     ssh
80/tcp   open     http
443/tcp  open     https
3389/tcp closed   ms-rdp

STATE 종류:
- open: 포트 열림, 서비스 실행 중
- closed: 포트 닫힘, 서비스 없음
- filtered: 방화벽에 의해 필터링됨
- open|filtered: 불확실 (UDP 스캔 시 흔함)


---

## 3. 실무/보안 관점 분석 (Insight & Scenario Mapping)

| 분야 | 적용 시나리오 |
|:---:|:---|
| **SOC / 관제** | **ARP Spoofing 탐지**: IDS/IPS에서 비정상적인 ARP 패킷(동일 IP에 대한 서로 다른 MAC 주소, 짧은 시간에 대량 ARP Reply)을 탐지합니다. Wireshark 필터 `arp.duplicate-address-detected`로 ARP 충돌을 확인합니다. **ICMP Flood 탐지**: 특정 출발지에서 초당 수백~수천 개의 ICMP Echo Request가 발생하면 DDoS 공격으로 판단, Rate Limiting 적용. **포트 스캔 탐지**: 짧은 시간(수초~수분) 내에 동일 출발지에서 다수의 포트로 SYN 패킷 전송 시 자동 차단. Snort 룰: `alert tcp any any -> $HOME_NET any (flags:S; threshold: type threshold, track by_src, count 20, seconds 10; msg:"Possible Port Scan";)` |
| **CERT / 사고 대응** | **MITM 공격 분석**: 침해 사고 시 ARP 캐시와 Wireshark 캡처를 분석하여 비정상 ARP 엔트리(공격자 MAC 주소가 게이트웨이 IP와 매핑)를 식별합니다. 정상 MAC 주소를 정적 ARP 엔트리로 설정하여 우회합니다. **라우팅 테이블 조작 탐지**: `show ip route` 또는 `route print`로 비인가 라우팅 엔트리 확인, BGP 로그 분석으로 BGP Hijacking 시도를 추적합니다. **TCP 세션 하이재킹 분석**: Wireshark에서 `tcp.analysis.retransmission` 및 비정상 Sequence Number를 탐지하여 세션 가로채기 시도를 확인합니다. |
| **네트워크 운영** | **라우팅 최적화**: `traceroute`로 패킷 경로를 추적하여 불필요한 홉(hop) 제거, 정적 라우팅으로 중요 트래픽의 고정 경로 보장. **서비스 포트 관리**: nmap으로 정기적으로 서버 포트 스캔을 수행하여 불필요한 서비스(Telnet 23, FTP 21 등 취약한 프로토콜) 탐지 및 종료. Windows `services.msc`에서 "Simple TCP/IP Services" 등 불필요한 서비스 중지. **네트워크 세그먼테이션**: Packet Tracer로 네트워크 토폴로지를 설계하고, 각 세그먼트 간 ACL 적용하여 불필요한 통신 차단. 예: DMZ ↔ Internal 간 특정 포트만 허용. |

---

## 4. 개인 인사이트 및 다음 단계 (Reflection & Next Steps)

* **배운 점/느낀 점:**
  - **네트워크 계층과 트랜스포트 계층의 연결**: 이론으로만 배운 OSI 7계층이 실제 패킷에서 어떻게 구현되는지 Wireshark를 통해 명확히 이해했습니다. ARP가 IP와 MAC을 연결하고, 라우팅이 네트워크 간 경로를 결정하며, TCP가 신뢰성 있는 연결을 수립하는 전체 과정이 유기적으로 연결되어 있음을 체감했습니다.
  - **Packet Tracer의 실용성**: 물리적 장비 없이 복잡한 네트워크 토폴로지를 구성하고 라우팅 설정을 실습할 수 있어 매우 유용했습니다. 특히 `show ip route`로 라우팅 테이블을 직접 확인하며 정적 라우팅의 동작 원리를 손으로 익혔습니다.
  - **3-Way Handshake의 중요성**: TCP 연결 수립 과정을 패킷 단위로 분석하니, SYN Flood 공격이 왜 위험한지(Half-Open 연결 고갈), 방화벽이 왜 SYN 패킷을 특별히 관리하는지 이해되었습니다. Sequence Number의 역할도 명확해졌습니다.
  - **ARP와 보안**: ARP가 인증 메커니즘이 없어 Spoofing에 취약하다는 것을 알았고, 동일 네트워크 내 MITM 공격의 실체를 이해했습니다. DAI, DHCP Snooping 같은 방어 기술의 필요성을 절감했습니다.
  - **포트 스캔의 양면성**: nmap이 네트워크 관리자에게는 **보안 점검 도구**이지만, 공격자에게는 **정찰 도구**라는 양면성을 깨달았습니다. 불필요한 포트를 닫고, 방화벽으로 스캔을 탐지/차단하는 것이 기본 방어입니다.

* **심화 방향:**
  - **동적 라우팅 프로토콜**: 다음 단계로 RIP, OSPF, BGP 같은 동적 라우팅 프로토콜의 동작 원리와 보안 취약점을 학습할 계획입니다. BGP Hijacking, OSPF LSA Flooding 같은 공격 시나리오를 Packet Tracer로 재현해볼 예정입니다.
  - **TCP 심화**: 3-Way Handshake 이후의 데이터 전송, 흐름 제어(Window Size), 혼잡 제어(Slow Start, Congestion Avoidance), 4-Way Handshake(연결 종료) 과정을 Wireshark로 분석합니다.
  - **UDP 학습**: TCP와 달리 연결 없는(Connectionless) UDP의 특성과 사용 사례(DNS, DHCP, VoIP), UDP Flood 공격과 방어를 학습합니다.
  - **ICMP 터널링 탐지**: 공격자가 ICMP 패킷에 데이터를 숨겨 방화벽을 우회하는 기법을 연구하고, Wireshark로 비정상 ICMP 페이로드를 탐지하는 방법을 습득합니다.
  - **IPsec VPN 심화**: Packet Tracer에서 구성한 IPsec VPN을 Wireshark로 분석하여 ESP/AH 헤더 구조와 암호화된 페이로드를 확인하고, VPN 터널링의 보안성을 검증합니다.
  - **방화벽 ACL 설정**: Cisco 라우터에서 ACL(Access Control List)을 설정하여 특정 IP/포트를 허용/차단하는 실습을 진행합니다.

---

## 5. 추가 참고사항 (Quick Reference)

### ARP 패킷 구조

```
Hardware Type: Ethernet (1)
Protocol Type: IPv4 (0x0800)
Hardware Address Length: 6 (MAC 주소 길이)
Protocol Address Length: 4 (IP 주소 길이)
Opcode:
  - 1: ARP Request
  - 2: ARP Reply
  - 3: RARP Request
  - 4: RARP Reply
Sender Hardware Address: 송신자 MAC
Sender Protocol Address: 송신자 IP
Target Hardware Address: 수신자 MAC (Request 시 00:00:00:00:00:00)
Target Protocol Address: 수신자 IP
```


### ICMP 주요 타입 & 코드

```
Type 0: Echo Reply (ping 응답)
Type 3: Destination Unreachable
  - Code 0: Network unreachable
  - Code 1: Host unreachable
  - Code 2: Protocol unreachable
  - Code 3: Port unreachable
  - Code 9: Network administratively prohibited
  - Code 10: Host administratively prohibited
Type 5: Redirect
Type 8: Echo Request (ping 요청)
Type 11: Time Exceeded
  - Code 0: Time to live exceeded in transit (traceroute)
  - Code 1: Fragment reassembly time exceeded
Type 13: Timestamp Request
Type 14: Timestamp Reply
```


### TCP 플래그

```
Flags (6비트):
  URG (Urgent): 긴급 데이터
  ACK (Acknowledgment): 확인 응답
  PSH (Push): 즉시 전달
  RST (Reset): 연결 강제 종료
  SYN (Synchronize): 연결 수립
  FIN (Finish): 연결 종료

주요 조합:
  S   : SYN (연결 요청)
  SA  : SYN+ACK (연결 수락)
  A   : ACK (데이터 확인)
  PA  : PSH+ACK (데이터 전송 및 확인)
  F   : FIN (연결 종료 요청)
  FA  : FIN+ACK (연결 종료 확인)
  R   : RST (연결 강제 종료)
  RA  : RST+ACK
```


### 잘 알려진 포트 번호 (Well-Known Ports: 0-1023)

```
20/21  : FTP (File Transfer Protocol)
22     : SSH (Secure Shell)
23     : Telnet
25     : SMTP (Simple Mail Transfer Protocol)
53     : DNS (Domain Name System)
67/68  : DHCP (Dynamic Host Configuration Protocol)
80     : HTTP (Hypertext Transfer Protocol)
110    : POP3 (Post Office Protocol v3)
143    : IMAP (Internet Message Access Protocol)
443    : HTTPS (HTTP Secure)
445    : SMB (Server Message Block)
3389   : RDP (Remote Desktop Protocol)

등록된 포트 (Registered Ports: 1024-49151):
3306   : MySQL
5432   : PostgreSQL
8080   : HTTP Alternate

동적 포트 (Dynamic Ports: 49152-65535):
클라이언트가 임시로 사용
```


### Cisco 라우터 주요 명령어

```
# 모드 전환
enable                        # User → Privileged 모드
configure terminal            # Privileged → Global Config 모드
interface fa0/0               # Interface Config 모드
exit                          # 이전 모드로
end                           # Privileged 모드로 (어디서든)

# 라우터 설정
hostname R1                   # 호스트 이름 변경
enable secret cisco           # Privileged 모드 비밀번호
no ip domain-lookup           # 오타 시 도메인 검색 방지

# 인터페이스 설정
interface fa0/0
ip address 192.168.1.1 255.255.255.0
no shutdown                   # 인터페이스 활성화

# 정적 라우팅
ip route 0.0.0.0 0.0.0.0 192.168.1.254      # Default Gateway
ip route 10.0.0.0 255.0.0.0 192.168.1.254   # 특정 네트워크

# 확인 명령어
show running-config           # 현재 구성
show ip route                 # 라우팅 테이블
show ip interface brief       # 인터페이스 요약
show arp                      # ARP 테이블
ping 192.168.1.1             # 연결 테스트
traceroute 8.8.8.8           # 경로 추적

# 설정 저장
copy running-config startup-config
write memory                  # 동일
```


### Wireshark 필터 (네트워크 & 트랜스포트 계층)

```
# ARP
arp                                      # 모든 ARP 패킷
arp.opcode == 1                          # ARP Request
arp.opcode == 2                          # ARP Reply
arp.duplicate-address-detected           # ARP 충돌

# ICMP
icmp                                     # 모든 ICMP
icmp.type == 8                           # Echo Request
icmp.type == 0                           # Echo Reply
icmp.type == 3                           # Destination Unreachable
icmp.type == 11                          # Time Exceeded

# TCP
tcp                                      # 모든 TCP
tcp.flags.syn == 1 and tcp.flags.ack == 0  # SYN 패킷
tcp.flags.syn == 1 and tcp.flags.ack == 1  # SYN+ACK
tcp.flags.reset == 1                     # RST 패킷
tcp.port == 80                           # HTTP
tcp.stream eq 0                          # 첫 번째 TCP 스트림

# 조합
ip.src == 192.168.1.100 and tcp.port == 443
arp or icmp
tcp.flags.syn == 1 and ip.dst == 192.168.1.1
```


### nmap 스캔 기법 요약

```
스캔 방식              명령어              특징
----------------      ----------------   ------------------
TCP SYN Scan          -sS                Half-open, 빠름, 로그 회피
TCP Connect Scan      -sT                Full connection, 느림
TCP ACK Scan          -sA                방화벽 룰 탐지
TCP Window Scan       -sW                윈도우 크기 분석
UDP Scan              -sU                느림, 비신뢰성
FIN Scan              -sF                은밀함
XMAS Scan             -sX                FIN+PSH+URG 플래그
NULL Scan             -sN                플래그 없음

속도 옵션:
-T0  : Paranoid (매우 느림, IDS 회피)
-T1  : Sneaky
-T2  : Polite
-T3  : Normal (기본값)
-T4  : Aggressive (빠름)
-T5  : Insane (매우 빠름)
```

