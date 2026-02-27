---
title: "2025.12.01 (Day 26) - TCP/IP 네트워크 계층 & 트랜스포트 계층: 라우팅, ARP, ICMP, TCP"
date: 2025-12-01
draft: false
tags: ["네트워크", "TCP/IP", "ARP", "ICMP", "라우팅", "Wireshark", "nmap", "보안"]
categories: ["daily-logs"]
summary: "네트워크 계층(ARP, ICMP, 라우팅)과 트랜스포트 계층(TCP 3-Way Handshake) 원리 분석, Packet Tracer 정적 라우팅 실습, nmap 포트 스캔 실습"
---

# 📄 2025.12.01 (Day 26) - TCP/IP 네트워크 계층 & 트랜스포트 계층: 라우팅, ARP, ICMP, TCP

---

## 1. 핵심 개념 정리

| # | 핵심 개념 | 간결한 설명 | 실무/보안 관점에서의 중요성 |
|:---:|:---|:---|:---|
| **1** | **네트워크 계층 (Network Layer)** | OSI 3계층으로 **라우팅**과 **논리적 주소 지정**(IP 주소)을 담당합니다. **라우터**가 핵심 장비이며, 패킷의 출발지에서 목적지까지 **최적 경로**를 결정합니다. 주요 프로토콜: IP, ICMP, ARP, RARP. | **네트워크 세분화**와 **경로 제어**의 핵심입니다. 라우팅 테이블 조작 공격(Routing Table Poisoning), IP Spoofing, ICMP Flooding 등의 공격 벡터가 존재합니다. |
| **2** | **ARP (Address Resolution Protocol)** | IP 주소를 **MAC 주소**로 변환하는 프로토콜입니다. 동일 네트워크 내에서 **ARP Request**(브로드캐스트)를 보내고, 해당 IP를 가진 호스트가 **ARP Reply**(유니캐스트)로 자신의 MAC 주소를 알려줍니다. | **ARP Spoofing/Poisoning** 공격의 대상입니다. 공격자가 위조된 ARP Reply를 보내 희생자의 ARP 캐시를 오염시켜 **MITM(Man-in-the-Middle)** 공격을 수행할 수 있습니다. DAI(Dynamic ARP Inspection)로 방어 가능합니다. |
| **3** | **ICMP (Internet Control Message Protocol)** | 네트워크 진단 및 오류 보고를 위한 프로토콜입니다. **ping**(Echo Request/Reply), **traceroute**, **Destination Unreachable**, **Time Exceeded** 등의 메시지를 전송합니다. | **네트워크 정찰**과 **DoS 공격**에 악용됩니다. ICMP Flood(Ping Flood), Smurf Attack(증폭 공격), ICMP Tunneling(데이터 은닉)이 대표적입니다. |
| **4** | **라우팅 (Routing)** | 패킷을 목적지까지 전달하기 위해 **최적 경로**를 결정하는 과정입니다. **정적 라우팅**(Static: 관리자가 수동 설정)과 **동적 라우팅**(Dynamic: RIP, OSPF, BGP 등)으로 나뉩니다. | **네트워크 가용성**의 핵심입니다. 라우팅 프로토콜 취약점(BGP Hijacking, OSPF Flooding)을 통한 트래픽 우회 및 서비스 거부 공격이 가능합니다. |
| **5** | **트랜스포트 계층 (Transport Layer)** | OSI 4계층으로 **종단 간(End-to-End) 통신**을 담당합니다. **포트 번호**를 통해 애플리케이션을 식별하고, **신뢰성**(TCP) 또는 **속도**(UDP)를 제공합니다. | **방화벽 정책**과 **서비스 식별**의 기준입니다. TCP/UDP 취약점(SYN Flood, UDP Flood, TCP Hijacking)을 악용한 공격이 빈번합니다. |
| **6** | **TCP 3-Way Handshake** | TCP 연결 수립 과정: **(1) SYN** (클라이언트 → 서버: 연결 요청), **(2) SYN+ACK** (서버 → 클라이언트: 연결 수락), **(3) ACK** (클라이언트 → 서버: 연결 확립). **Sequence Number**와 **Acknowledgment Number**로 신뢰성을 보장합니다. | **SYN Flood 공격**의 대상입니다. 공격자가 대량의 SYN 패킷을 보내고 ACK를 보내지 않아 서버의 **Half-Open 연결**을 고갈시킵니다. SYN Cookie, Rate Limiting으로 방어합니다. |

---

## 2. 실습 내용

### (A) Packet Tracer 라우팅 실습

**토폴로지 구성:**

- PC2 (192.168.10.2) -- Router1 (Fa0/0=192.168.10.1, Fa0/1=11.0.0.1) -- Router0 (Fa0/0=11.0.0.2, Fa0/1=10.0.0.2) -- Router2 (Fa0/0=10.0.0.1, Fa0/1=192.168.20.1) -- PC3 (192.168.20.2)

**Router1 설정 (PC2쪽 게이트웨이):**
- Router> **enable** → 특권 모드 진입
- Router# **configure terminal** → 전역 설정 모드
- router1(config)# **hostname router1** → 호스트 이름 설정
- router1(config)# **interface fa0/0** → FastEthernet 0/0 설정 (PC2쪽)
  - **ip address 192.168.10.1 255.255.255.0**
  - **no shutdown** → 인터페이스 활성화
- router1(config)# **interface fa0/1** → FastEthernet 0/1 설정 (Router0쪽)
  - **ip address 11.0.0.1 255.0.0.0**
  - **no shutdown**
- router1(config)# **ip route 0.0.0.0 0.0.0.0 11.0.0.2** → 기본 경로(Default Gateway) 설정
- router1# **show ip route** → 라우팅 테이블 확인
- router1# **show ip interface brief** → 인터페이스 요약 확인

**Router0 설정 (중간 라우터):**
- interface fa0/0: **ip address 11.0.0.2 255.0.0.0**
- interface fa0/1: **ip address 10.0.0.2 255.0.0.0**
- **ip route 192.168.10.0 255.255.255.0 11.0.0.1** → PC2 네트워크 경로
- **ip route 192.168.20.0 255.255.255.0 10.0.0.1** → PC3 네트워크 경로

**Router2 설정 (PC3쪽 게이트웨이):**
- interface fa0/0: **ip address 10.0.0.1 255.0.0.0**
- interface fa0/1: **ip address 192.168.20.1 255.255.255.0**
- **ip route 0.0.0.0 0.0.0.0 10.0.0.2** → 기본 경로

**PC 설정:**
- PC2 IP: 192.168.10.2, Subnet Mask: 255.255.255.0, Default Gateway: 192.168.10.1
- PC3 IP: 192.168.20.2, Subnet Mask: 255.255.255.0, Default Gateway: 192.168.20.1

**연결 테스트:**
- PC2에서 **ping 192.168.10.1** → Router1 확인
- PC2에서 **ping 192.168.20.2** → PC3까지 엔드-투-엔드 확인
- PC2에서 **tracert 192.168.20.2** → 경로 확인 (Router1 → Router0 → Router2 → PC3)

---

### (B) Wireshark ARP 패킷 분석

**ARP Request (브로드캐스트):**
- Ethernet II Destination: Broadcast (ff:ff:ff:ff:ff:ff)
- Ethernet II Source: 00:0c:29:3a:2f:1a
- Type: ARP (0x0806)
- Opcode: request (1)
- Sender MAC: 00:0c:29:3a:2f:1a
- Sender IP: 192.168.1.100
- Target MAC: 00:00:00:00:00:00 (아직 모름)
- Target IP: 192.168.1.1 (알고 싶은 IP)

**ARP Reply (유니캐스트):**
- Ethernet II Destination: 00:0c:29:3a:2f:1a (요청자에게만)
- Ethernet II Source: 00:50:56:c0:00:08 (자신의 MAC)
- Opcode: reply (2)
- Sender MAC: 00:50:56:c0:00:08
- Sender IP: 192.168.1.1
- Target MAC: 00:0c:29:3a:2f:1a (요청자 MAC)
- Target IP: 192.168.1.100

**ARP 캐시 관련 명령어:**
- **arp -a** → ARP 캐시 확인 (Linux/Windows 공통)
- **ip neigh show** → ARP 캐시 확인 (Linux)
- **arp -d 192.168.1.1** → 특정 항목 삭제
- **ip neigh flush all** → 전체 삭제 (Linux)

---

### (C) Wireshark ICMP 패킷 분석

**ICMP Echo Request (ping 요청):**
- Source: 192.168.1.100, Destination: 8.8.8.8
- Type: 8 (Echo ping request), Code: 0
- Identifier: 0x0001, Sequence number: 1

**ICMP Echo Reply (ping 응답):**
- Source: 8.8.8.8, Destination: 192.168.1.100
- Type: 0 (Echo ping reply), Code: 0

**ICMP Destination Unreachable 코드:**
- Code 0: Network unreachable
- Code 1: Host unreachable
- Code 3: Port unreachable
- Code 9: Network administratively prohibited

**ICMP Time Exceeded (traceroute):**
- Type: 11 (Time-to-live exceeded), Code: 0
- traceroute가 TTL을 1씩 증가시키며 보내면 각 라우터가 ICMP Time Exceeded를 회신하여 경로를 추적

---

### (D) TCP 3-Way Handshake 실습

**실습 절차:**
1. **nslookup dictionary.cambridge.org** → IP 주소 확인 (예: 54.251.164.119)
2. Wireshark 필터 설정: **ip.addr == 54.251.164.119 and tcp.port == 443**
3. 브라우저에서 https://dictionary.cambridge.org 접속

**패킷 #1 (SYN) - 클라이언트 → 서버:**
- Source Port: 54321 (클라이언트 랜덤 포트), Destination Port: 443 (HTTPS)
- Sequence number: 0 (relative), Acknowledgment number: 0
- Flags: 0x002 (SYN 설정, ACK 미설정)
- Window size: 65535

**패킷 #2 (SYN+ACK) - 서버 → 클라이언트:**
- Source Port: 443, Destination Port: 54321
- Sequence number: 0 (relative), Acknowledgment number: 1
- Flags: 0x012 (SYN+ACK 모두 설정)
- Window size: 29200

**패킷 #3 (ACK) - 클라이언트 → 서버:**
- Source Port: 54321, Destination Port: 443
- Sequence number: 1, Acknowledgment number: 1
- Flags: 0x010 (ACK 설정, SYN 미설정)
- → 연결 확립 완료, 이후 데이터 전송 시작

---

### (E) 포트 스캔 실습 (nmap)

**기본 포트 스캔 명령어:**
- **nmap 127.0.0.1** → 로컬 호스트 스캔
- **nmap -p 80,443,22,3389 192.168.1.100** → 특정 포트만 스캔
- **nmap -sV 192.168.1.100** → 서비스 버전 탐지
- **nmap -O 192.168.1.100** → OS 탐지
- **nmap -T4 -A -v 192.168.1.100** → 상세 스캔 (-T4: 속도, -A: 통합 탐지, -v: 상세 출력)

**TCP 스캔 방법:**
- **nmap -sS** → TCP SYN Scan (Half-open, 가장 빠름, 로그 회피)
- **nmap -sT** → TCP Connect Scan (Full connection, 느림)
- **nmap -sA** → TCP ACK Scan (방화벽 탐지)
- **nmap -sU** → UDP Scan (느림)
- **nmap -F** → 고속 모드 (상위 100개 포트만)

**nmap 결과 STATE 종류:**
- **open**: 포트 열림, 서비스 실행 중
- **closed**: 포트 닫힘, 서비스 없음
- **filtered**: 방화벽에 의해 필터링됨
- **open|filtered**: 불확실 (UDP 스캔 시 흔함)

---

## 3. 실무/보안 관점 분석

| 분야 | 적용 시나리오 |
|:---:|:---|
| **SOC / 관제** | **ARP Spoofing 탐지**: IDS/IPS에서 비정상적인 ARP 패킷(동일 IP에 대한 서로 다른 MAC 주소, 짧은 시간에 대량 ARP Reply)을 탐지합니다. Wireshark 필터 **arp.duplicate-address-detected** 로 ARP 충돌을 확인합니다. **ICMP Flood 탐지**: 특정 출발지에서 초당 수백 개의 ICMP Echo Request가 발생하면 DDoS 공격으로 판단, Rate Limiting 적용. **포트 스캔 탐지**: 짧은 시간 내에 동일 출발지에서 다수 포트로 SYN 패킷 전송 시 자동 차단. |
| **CERT / 사고 대응** | **MITM 공격 분석**: 침해 사고 시 ARP 캐시와 Wireshark 캡처를 분석하여 비정상 ARP 엔트리(공격자 MAC 주소가 게이트웨이 IP와 매핑)를 식별합니다. 정상 MAC 주소를 정적 ARP 엔트리로 설정하여 우회합니다. **TCP 세션 하이재킹 분석**: Wireshark에서 **tcp.analysis.retransmission** 및 비정상 Sequence Number를 탐지하여 세션 가로채기 시도를 확인합니다. |
| **네트워크 운영** | **라우팅 최적화**: traceroute로 패킷 경로를 추적하여 불필요한 홉(hop) 제거, 정적 라우팅으로 중요 트래픽의 고정 경로 보장. **서비스 포트 관리**: nmap으로 정기적으로 서버 포트 스캔을 수행하여 불필요한 서비스(Telnet 23, FTP 21 등)를 탐지 및 종료. |

---

## 4. 개인 인사이트 및 다음 단계

- **배운 점/느낀 점**: 이론으로만 배운 OSI 7계층이 실제 패킷에서 어떻게 구현되는지 Wireshark를 통해 명확히 이해했습니다. ARP가 IP와 MAC을 연결하고, 라우팅이 네트워크 간 경로를 결정하며, TCP가 신뢰성 있는 연결을 수립하는 전체 과정이 유기적으로 연결되어 있음을 체감했습니다. nmap이 네트워크 관리자에게는 **보안 점검 도구**이지만, 공격자에게는 **정찰 도구**라는 양면성도 깨달았습니다.
- **심화 방향**: 다음 단계로 RIP, OSPF, BGP 같은 동적 라우팅 프로토콜의 동작 원리와 보안 취약점을 학습할 계획입니다. TCP 3-Way Handshake 이후 데이터 전송, 흐름 제어(Window Size), 4-Way Handshake 과정을 Wireshark로 분석하고, ICMP 터널링 탐지 기법도 연구할 예정입니다.

---

## 5. 추가 참고사항 (Quick Reference)

### ARP 패킷 구조

| 필드 | 값 | 설명 |
|:---:|:---:|:---|
| Hardware Type | 1 | Ethernet |
| Protocol Type | 0x0800 | IPv4 |
| Hardware Address Length | 6 | MAC 주소 길이 (바이트) |
| Protocol Address Length | 4 | IP 주소 길이 (바이트) |
| Opcode | 1 | ARP Request |
| Opcode | 2 | ARP Reply |
| Sender Hardware Address | - | 송신자 MAC |
| Sender Protocol Address | - | 송신자 IP |
| Target Hardware Address | 00:00:00:00:00:00 | Request 시 미기입 |
| Target Protocol Address | - | 수신자 IP |

### ICMP 주요 타입 & 코드

| Type | 설명 | Code |
|:---:|:---|:---|
| 0 | Echo Reply (ping 응답) | - |
| 3 | Destination Unreachable | 0=Network, 1=Host, 2=Protocol, 3=Port unreachable |
| 5 | Redirect | - |
| 8 | Echo Request (ping 요청) | - |
| 11 | Time Exceeded | 0=TTL exceeded (traceroute), 1=Fragment reassembly timeout |
| 13 | Timestamp Request | - |
| 14 | Timestamp Reply | - |

### TCP 플래그

| 플래그 | 약자 | 설명 |
|:---:|:---:|:---|
| URG | U | 긴급 데이터 |
| ACK | A | 확인 응답 |
| PSH | P | 즉시 전달 |
| RST | R | 연결 강제 종료 |
| SYN | S | 연결 수립 |
| FIN | F | 연결 종료 |

주요 조합:
- **S** → SYN (연결 요청)
- **SA** → SYN+ACK (연결 수락)
- **A** → ACK (데이터 확인)
- **PA** → PSH+ACK (데이터 전송 및 확인)
- **F** → FIN (연결 종료 요청)
- **FA** → FIN+ACK (연결 종료 확인)
- **R** → RST (연결 강제 종료)

### 잘 알려진 포트 번호 (Well-Known Ports: 0-1023)

| 포트 | 프로토콜 | 설명 |
|:---:|:---:|:---|
| 20, 21 | FTP | File Transfer Protocol |
| 22 | SSH | Secure Shell |
| 23 | Telnet | 원격 접속 (평문, 사용 금지) |
| 25 | SMTP | Simple Mail Transfer Protocol |
| 53 | DNS | Domain Name System |
| 67, 68 | DHCP | Dynamic Host Configuration Protocol |
| 80 | HTTP | Hypertext Transfer Protocol |
| 110 | POP3 | Post Office Protocol v3 |
| 143 | IMAP | Internet Message Access Protocol |
| 443 | HTTPS | HTTP Secure |
| 445 | SMB | Server Message Block |
| 3306 | MySQL | 데이터베이스 (등록 포트) |
| 3389 | RDP | Remote Desktop Protocol |
| 8080 | HTTP Alt | HTTP 대체 포트 (등록 포트) |

### Cisco 라우터 주요 명령어

| 명령어 | 설명 |
|:---|:---|
| **enable** | User → Privileged 모드 전환 |
| **configure terminal** | Privileged → Global Config 모드 전환 |
| **interface fa0/0** | Interface Config 모드 진입 |
| **no shutdown** | 인터페이스 활성화 |
| **hostname R1** | 호스트 이름 변경 |
| **ip route 0.0.0.0 0.0.0.0 192.168.1.254** | Default Gateway 설정 |
| **ip route 10.0.0.0 255.0.0.0 192.168.1.254** | 특정 네트워크 경로 |
| **show running-config** | 현재 구성 확인 |
| **show ip route** | 라우팅 테이블 확인 |
| **show ip interface brief** | 인터페이스 요약 |
| **show arp** | ARP 테이블 확인 |
| **copy running-config startup-config** | 설정 저장 |

### Wireshark 필터 (네트워크 & 트랜스포트 계층)

| 프로토콜 | 필터 | 설명 |
|:---:|:---|:---|
| **ARP** | arp | 모든 ARP 패킷 |
| | arp.opcode == 1 | ARP Request |
| | arp.opcode == 2 | ARP Reply |
| | arp.duplicate-address-detected | ARP 충돌 탐지 |
| **ICMP** | icmp | 모든 ICMP |
| | icmp.type == 8 | Echo Request |
| | icmp.type == 0 | Echo Reply |
| | icmp.type == 3 | Destination Unreachable |
| | icmp.type == 11 | Time Exceeded |
| **TCP** | tcp | 모든 TCP |
| | tcp.flags.syn == 1 and tcp.flags.ack == 0 | SYN 패킷 |
| | tcp.flags.syn == 1 and tcp.flags.ack == 1 | SYN+ACK |
| | tcp.flags.reset == 1 | RST 패킷 |
| | tcp.port == 80 | HTTP |
| | tcp.stream eq 0 | 첫 번째 TCP 스트림 |

### nmap 스캔 기법 요약

| 스캔 방식 | 명령어 | 특징 |
|:---:|:---:|:---|
| TCP SYN Scan | -sS | Half-open, 빠름, 로그 회피 |
| TCP Connect Scan | -sT | Full connection, 느림 |
| TCP ACK Scan | -sA | 방화벽 룰 탐지 |
| TCP Window Scan | -sW | 윈도우 크기 분석 |
| UDP Scan | -sU | 느림, 비신뢰성 |
| FIN Scan | -sF | 은밀함 |
| XMAS Scan | -sX | FIN+PSH+URG 플래그 |
| NULL Scan | -sN | 플래그 없음 |

속도 옵션: -T0 (매우 느림, IDS 회피) ~ -T5 (매우 빠름), 기본값 -T3
