---
title: "2025.11.28 (Day 25) - TCP/IP 네트워크 보안: IPv4 프로토콜 & Wireshark 패킷 분석"
date: 2025-11-28
draft: false
tags: ["TCP/IP", "IPv4", "Wireshark", "네트워크보안", "패킷분석"]
categories: ["daily-logs"]
summary: "OSI 7계층 vs TCP/IP 모델, IPv4 헤더 구조 분석, Wireshark 캡처/디스플레이 필터 실습, 비정상 패킷 탐지"
---

# 📄 2025.11.28 (Day 25) - TCP/IP 네트워크 보안: IPv4 프로토콜 & Wireshark 패킷 분석

---

## 1. 핵심 개념 정리

| # | 핵심 개념 | 간결한 설명 | 실무/보안 관점에서의 중요성 |
|:---:|:---|:---|:---|
| **1** | **OSI 7계층 vs TCP/IP 모델** | OSI는 7계층(물리, 데이터링크, 네트워크, 전송, 세션, 표현, 응용)으로 이론적 모델이며, TCP/IP는 4계층(네트워크 접근, 인터넷, 전송, 응용)으로 실제 인터넷 프로토콜 스택입니다. 각 계층은 **캡슐화(Encapsulation)**를 통해 상위 계층 데이터를 하위 계층 헤더로 감쌉니다. | **공격 벡터 분석**의 기초입니다. 계층별로 서로 다른 공격이 존재합니다: L2(ARP Spoofing), L3(IP Spoofing), L4(SYN Flooding, Port Scanning), L7(SQL Injection, XSS). 계층별 이해는 방어 전략 수립의 출발점입니다. |
| **2** | **IPv4 주소 체계** | 32비트 주소(8비트씩 4개 옥텟)로 구성되며, 네트워크부와 호스트부로 나뉩니다. **클래스**(A, B, C, D, E)와 **서브넷 마스크**를 통해 네트워크를 구분합니다. **사설 IP**(10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)는 NAT를 통해 공인 IP로 변환됩니다. | **네트워크 세분화**와 **접근 제어**의 기반입니다. 서브넷을 통해 네트워크를 논리적으로 분리하여 **측면 이동(Lateral Movement)** 공격을 차단하고, 방화벽 정책을 효과적으로 적용할 수 있습니다. |
| **3** | **IPv4 헤더 구조** | **Version(4bit)**, **Header Length(4bit)**, **TOS(8bit)**, **Total Length(16bit)**, **Identification(16bit)**, **Flags(3bit)**, **Fragment Offset(13bit)**, **TTL(8bit)**, **Protocol(8bit)**, **Header Checksum(16bit)**, **Source IP(32bit)**, **Destination IP(32bit)**, **Options(가변)** 필드로 구성됩니다. | **패킷 분석**과 **위협 탐지**의 핵심입니다. TTL 값으로 **라우팅 루프**나 **패킷 변조** 탐지, Flags/Fragment Offset으로 **Fragmentation 공격** 탐지, Protocol 필드로 **터널링 우회** 탐지가 가능합니다. |
| **4** | **Wireshark 패킷 분석** | Wireshark는 네트워크 패킷을 실시간으로 캡처하고 분석하는 도구입니다. **캡처 필터**(BPF 문법)로 원하는 패킷만 수집하고, **디스플레이 필터**로 캡처된 패킷에서 특정 조건을 검색합니다. 각 계층별 헤더를 시각적으로 확인할 수 있습니다. | **포렌식 분석**과 **이상 트래픽 탐지**의 필수 도구입니다. 공격 패킷의 특성(비정상 플래그 조합, 악성 페이로드, C&C 통신 패턴)을 식별하고, **베이스라인 트래픽**과 비교하여 이상 징후를 발견합니다. |

---

## 2. 실습 내용

### (A) IPv4 주소 계산 실습

**예제 1 : 192.168.10.130/25 네트워크 분석**

- IP 주소 : 192.168.10.130
- 서브넷 마스크 : 255.255.255.128 (/25)

이진수 변환:
- IP : 11000000.10101000.00001010.10000010
- Mask : 11111111.11111111.11111111.10000000

계산 결과:
- 네트워크 주소 : 192.168.10.128 (호스트부를 0으로)
- 브로드캐스트 : 192.168.10.255 (호스트부를 1로)
- 사용 가능 호스트 : 192.168.10.129 ~ 192.168.10.254 (126개)

**예제 2 : CIDR 표기법 정리**

| CIDR | 서브넷 마스크 | 주소 수 | 호스트 수 |
|:---:|:---|:---:|:---:|
| /24 | 255.255.255.0 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 14 |
| /30 | 255.255.255.252 | 4 | 2 (P2P 링크용) |

---

### (B) Wireshark 캡처 필터 (BPF 문법)

**호스트/네트워크 기반 필터:**
- **host 192.168.1.100** : 특정 호스트의 모든 트래픽
- **net 192.168.1.0/24** : 특정 네트워크의 모든 트래픽
- **src host 192.168.1.100** : 출발지 IP 필터
- **dst host 192.168.1.200** : 목적지 IP 필터

**포트 기반 필터:**
- **port 80** : 특정 포트의 트래픽
- **port 443** : HTTPS 트래픽
- **portrange 1000-2000** : 포트 범위

**프로토콜 필터:**
- **tcp** : TCP 트래픽만
- **udp** : UDP 트래픽만

**조합 예시:**
- **tcp and src host 192.168.1.100 and dst port 80** : 192.168.1.100에서 80포트로 가는 TCP 트래픽

---

### (C) Wireshark 디스플레이 필터

**IP 주소 필터:**
- **ip.addr == 192.168.1.100** : 출발지 또는 목적지
- **ip.src == 192.168.1.100** : 출발지만
- **ip.dst == 192.168.1.200** : 목적지만

**프로토콜 필터:**
- **tcp**, **udp**, **icmp**, **arp**, **http**, **dns**, **ssh**

**TCP 플래그 필터:**
- **tcp.flags.syn == 1** : SYN 플래그
- **tcp.flags.ack == 1** : ACK 플래그
- **tcp.flags.reset == 1** : RST 플래그
- **tcp.flags.syn == 1 and tcp.flags.ack == 0** : SYN 패킷 (3-way handshake 시작)

**포트 필터:**
- **tcp.port == 80**
- **tcp.dstport == 443**
- **tcp.srcport == 22**

**HTTP 필터:**
- **http.request** : HTTP 요청만
- **http.response** : HTTP 응답만
- **http.request.method == "POST"** : POST 요청
- **http.request.uri contains "login"** : URI에 login 포함

**DNS 필터:**
- **dns.qry.name contains "google"** : DNS 쿼리에 google 포함

**패킷 크기 필터:**
- **frame.len > 1000** : 1000바이트 초과
- **ip.len < 100** : IP 패킷 길이 100바이트 미만

**조합 예시:**
- **tcp.flags.syn == 1 and ip.src == 192.168.1.100 and tcp.dstport == 22** : 특정 IP에서 SSH로 연결 시도하는 SYN 패킷
- **http.request.method == "POST" and http.request.uri contains "admin"** : admin 경로로 가는 POST 요청

---

### (D) 리눅스 네트워크 명령어

**네트워크 인터페이스 및 라우팅 확인:**
- **ip addr show** / **ifconfig** : 네트워크 인터페이스 확인
- **ip route show** / **route -n** : 라우팅 테이블 확인
- **ip neigh show** / **arp -a** : ARP 테이블 확인

**연결 상태 확인:**
- **netstat -tunap** : 모든 TCP/UDP 연결
- **ss -tunap** : 최신 명령어 (동일 기능)
- **netstat -tunlp | grep :80** : 특정 포트 리스닝 확인

**연결성 테스트:**
- **ping 192.168.1.1** : ICMP 테스트
- **ping -c 4 google.com** : 4개 패킷만 전송
- **traceroute google.com** : 경로 추적
- **mtr google.com** : 실시간 경로 추적

**DNS 조회:**
- **dig google.com**
- **nslookup google.com**
- **host google.com**

**패킷 캡처 (tcpdump):**
- **tcpdump -i eth0** : eth0 인터페이스 모니터링
- **tcpdump -i eth0 port 80** : 80번 포트만
- **tcpdump -i eth0 -w capture.pcap** : 파일로 저장
- **tcpdump -r capture.pcap** : 캡처 파일 읽기
- **tcpdump -i eth0 'tcp\[tcpflags\] & (tcp-syn) != 0'** : SYN 패킷만

---

### (E) 실습 결과 및 분석

**IPv4 헤더 분석 (Wireshark에서 확인한 주요 내용):**

- **버전** : 4 (IPv4)
- **헤더 길이** : 20 bytes (5 * 4)
- **Total Length** : 60
- **Identification** : 0x1a2b
- **Flags** : 0x4000 (Don't Fragment 설정됨)
- **Fragment Offset** : 0
- **Time to Live** : 64
- **Protocol** : TCP (6)
- **출발지** : 192.168.1.100
- **목적지** : 192.168.1.200

**주요 필드 분석:**
- **TTL (Time to Live)** : 64 -> 일반적으로 Linux/Unix는 64, Windows는 128로 설정. 패킷이 라우터를 거칠 때마다 1씩 감소하며, 0이 되면 폐기됩니다. 비정상적으로 낮은 TTL 값은 루프나 변조를 의심할 수 있습니다.
- **Flags - Don't Fragment** : 설정 시 패킷이 MTU보다 크면 ICMP "Fragmentation Needed" 메시지를 받습니다. **Path MTU Discovery**에 사용됩니다.
- **Protocol** : 6 = TCP, 17 = UDP, 1 = ICMP. 상위 계층 프로토콜을 식별합니다.
- **Identification** : 패킷 단편화 시 동일한 원본 패킷을 식별하는 데 사용됩니다.

**Wireshark로 3-Way Handshake 분석:**

패킷 1 (SYN) : 클라이언트 -> 서버 연결 요청
- Flags : SYN / Seq : 0 / Ack : 0

패킷 2 (SYN-ACK) : 서버 -> 클라이언트 연결 수락
- Flags : SYN, ACK / Seq : 0 / Ack : 1

패킷 3 (ACK) : 클라이언트 -> 서버 연결 확립
- Flags : ACK / Seq : 1 / Ack : 1

-> 정상적인 TCP 연결 수립 과정

**비정상 패킷 탐지 예시:**

SYN Flood 공격 탐지:
- 대량의 SYN 패킷이 다양한 출발지 IP에서 발생
- SYN-ACK에 대한 ACK 응답이 없음
- Wireshark 필터 : **tcp.flags.syn == 1 and tcp.flags.ack == 0**

IP Spoofing 탐지:
- TTL 값이 비정상적으로 낮거나 일관성 없음
- 내부 네트워크 IP가 외부에서 유입
- 출발지 IP가 브로드캐스트/멀티캐스트 주소

Port Scanning 탐지:
- 짧은 시간에 동일 출발지에서 다양한 포트로 연결 시도
- 대량의 RST 패킷 (포트가 닫혀있음)
- Wireshark 필터 : **tcp.flags.reset == 1**

---

## 3. 실무/보안 관점 분석

| 분야 | 적용 시나리오 |
|:---:|:---|
| **SOC / 관제** | **실시간 트래픽 모니터링** : IDS/IPS에서 Wireshark와 유사한 패킷 분석 엔진(Suricata, Snort)을 사용하여 비정상 패턴을 탐지합니다. **베이스라인 트래픽**을 설정하고, 통계적 이상(급증하는 SYN 패킷, 비정상 TTL, 알려지지 않은 프로토콜)을 자동 알림합니다. Snort 룰 예시: **alert tcp any any -> $HOME_NET any (flags:S; threshold: type both, track by_src, count 100, seconds 10; msg:"Possible SYN Flood";)** Wireshark를 통해 알림의 실제 패킷을 확인하여 **오탐(False Positive)** 여부를 판단합니다. |
| **CERT / 사고 대응** | **포렌식 패킷 분석** : 침해 사고 시 네트워크 탭(SPAN/Mirror Port)이나 방화벽에서 수집한 PCAP 파일을 Wireshark로 분석합니다. **공격 타임라인 재구성** : (1) 초기 침투 패킷 식별 -> (2) C&C 통신 추적 (특정 IP/도메인으로의 주기적 통신) -> (3) 데이터 유출 탐지 (대용량 파일 전송). **tcp.stream eq 123** 으로 특정 TCP 세션의 모든 패킷을 추적하여 공격자의 명령어와 데이터 유출 내용을 복원. **dns.qry.name** 으로 DGA(Domain Generation Algorithm) 기반 멀웨어 탐지. |
| **네트워크 운영** | **성능 최적화 및 문제 해결** : Wireshark로 **패킷 손실**, **재전송**, **레이턴시** 문제를 진단합니다. **tcp.analysis.retransmission** 필터로 재전송 패킷을 찾아 네트워크 품질 문제를 식별하고, **tcp.analysis.zero_window** 로 수신 버퍼 고갈 상태를 확인합니다. **서브넷 설계** : 부서별/보안 등급별로 서브넷을 분리하여 VLAN과 결합, 방화벽 규칙으로 **Micro-Segmentation** 구현. |

---

## 4. 개인 인사이트 및 다음 단계

- **배운 점/느낀 점:**
  - **네트워크는 보안의 기초 중 기초**입니다. 모든 통신은 네트워크를 통해 이루어지므로, IP 헤더와 TCP/UDP 헤더를 읽을 수 있는 능력은 **공격과 방어 모두의 필수 역량**입니다.
  - **Wireshark의 강력함** : 교재에서 배운 이론적 개념(OSI 7계층, IPv4 헤더)을 실제 패킷으로 직접 확인하니 훨씬 명확하게 이해되었습니다. 특히 3-Way Handshake를 패킷 단위로 보면서 TCP의 연결 지향적 특성을 체감했습니다.
  - **서브넷의 중요성** : 단순히 IP 주소를 나누는 것이 아니라, **보안 경계**를 만드는 것임을 깨달았습니다. 잘못된 서브넷 설계는 공격자에게 전체 네트워크를 노출시킬 수 있습니다.
  - **패킷 분석의 예술** : Wireshark 필터를 잘 활용하면 수만 개의 패킷 속에서 핵심 정보만 추출할 수 있습니다. 필터 문법을 익히는 것이 효율적인 분석의 핵심입니다.

- **심화 방향:**
  - **TCP/UDP 심화** : TCP의 흐름 제어, 혼잡 제어, UDP의 특성과 활용 사례 학습
  - **고급 Wireshark 기법** : Follow TCP Stream, Statistics 메뉴 활용, Lua 스크립트를 통한 커스텀 분석, PCAP 파일 자동 분석 스크립트 작성
  - **공격 시나리오 재현** : 실습 환경에서 SYN Flood, ARP Spoofing, DNS Spoofing 등의 공격을 직접 재현하고 Wireshark로 패킷을 분석하여 탐지 시그니처 개발
  - **IDS/IPS 룰 작성** : Suricata나 Snort 룰을 작성하여 특정 공격 패턴을 자동 탐지하는 시스템 구축
  - **IPv6 학습** : IPv4 고갈과 IPv6 전환에 대비하여 IPv6 주소 체계, 헤더 구조, 보안 고려사항 학습

---

## 5. 빠른 참고 (Quick Reference)

### IPv4 주소 클래스

| 클래스 | 범위 | 서브넷 | 특이사항 |
|:---:|:---|:---:|:---|
| **A** | 0.0.0.0 ~ 127.255.255.255 | /8 | 네트워크 126개, 호스트 16,777,214개 |
| **B** | 128.0.0.0 ~ 191.255.255.255 | /16 | 네트워크 16,384개, 호스트 65,534개 |
| **C** | 192.0.0.0 ~ 223.255.255.255 | /24 | 네트워크 2,097,152개, 호스트 254개 |
| **D** | 224.0.0.0 ~ 239.255.255.255 | - | 멀티캐스트 |
| **E** | 240.0.0.0 ~ 255.255.255.255 | - | 실험용/예약 |

**사설 IP (RFC 1918):**
- 10.0.0.0 ~ 10.255.255.255 (10.0.0.0/8)
- 172.16.0.0 ~ 172.31.255.255 (172.16.0.0/12)
- 192.168.0.0 ~ 192.168.255.255 (192.168.0.0/16)

**특수 주소:**
- 127.0.0.0/8 : 루프백 (localhost)
- 0.0.0.0/8 : 현재 네트워크
- 255.255.255.255 : 제한된 브로드캐스트
- 169.254.0.0/16 : Link-local (APIPA)

### IPv4 헤더 필드 요약

| 필드 | 크기 | 설명 |
|:---|:---:|:---|
| **Version** | 4bit | IP 버전 (4) |
| **IHL** | 4bit | 헤더 길이 (5 = 20바이트, 옵션 없음) |
| **DSCP** | 6bit | 서비스 품질 (QoS) |
| **ECN** | 2bit | 명시적 혼잡 알림 |
| **Total Length** | 16bit | 전체 패킷 크기 (헤더 + 데이터) |
| **Identification** | 16bit | 단편화 시 원본 패킷 식별 |
| **Flags** | 3bit | Reserved, DF (Don't Fragment), MF (More Fragments) |
| **Fragment Offset** | 13bit | 단편화된 데이터의 오프셋 |
| **TTL** | 8bit | 패킷 생존 시간 (라우터마다 -1) |
| **Protocol** | 8bit | 상위 프로토콜 (1=ICMP, 6=TCP, 17=UDP) |
| **Header Checksum** | 16bit | 헤더 무결성 검증 |
| **Source IP** | 32bit | 출발지 주소 |
| **Destination IP** | 32bit | 목적지 주소 |
| **Options** | 가변 | 추가 옵션 (선택 사항) |

### 주요 프로토콜 번호

| 번호 | 프로토콜 |
|:---:|:---|
| 1 | ICMP (Internet Control Message Protocol) |
| 2 | IGMP (Internet Group Management Protocol) |
| 6 | TCP (Transmission Control Protocol) |
| 17 | UDP (User Datagram Protocol) |
| 41 | IPv6 (IPv6 encapsulation) |
| 47 | GRE (Generic Routing Encapsulation) |
| 50 | ESP (Encap Security Payload - IPsec) |
| 51 | AH (Authentication Header - IPsec) |
| 89 | OSPF (Open Shortest Path First) |

### Wireshark 단축키

| 단축키 | 기능 |
|:---:|:---|
| **Ctrl + K** | 캡처 시작 |
| **Ctrl + E** | 캡처 중지 |
| **Ctrl + F** | 패킷 찾기 |
| **Ctrl + G** | 특정 패킷 번호로 이동 |
| **Ctrl + N** | 다음 패킷 |
| **Ctrl + B** | 이전 패킷 |
| **Ctrl + ->** | 다음 대화 (conversation) |
| **Ctrl + <-** | 이전 대화 |
| **Ctrl + Alt + Shift + T** | TCP Stream 따라가기 |

### tcpdump 주요 옵션

| 옵션 | 설명 |
|:---:|:---|
| **-i \<interface\>** | 캡처할 인터페이스 지정 |
| **-c \<count\>** | 지정된 개수만큼만 캡처 |
| **-w \<file\>** | PCAP 파일로 저장 |
| **-r \<file\>** | PCAP 파일 읽기 |
| **-n** | DNS 이름 해석 안 함 (빠름) |
| **-v / -vv / -vvv** | 상세 출력 (레벨 증가) |
| **-A** | ASCII로 패킷 내용 출력 |
| **-X** | 16진수 + ASCII로 출력 |
| **-s \<snaplen\>** | 캡처할 패킷 크기 (0 = 전체) |

**tcpdump 사용 예시:**
- **tcpdump -i eth0 -w capture.pcap 'tcp port 80'** : HTTP 트래픽 저장
- **tcpdump -i any -c 100 -n 'src host 192.168.1.100'** : 특정 IP 100개 캡처
- **tcpdump -i eth0 -A 'tcp port 80 and (tcp\[13\] & 2 != 0)'** : SYN 플래그 패킷
