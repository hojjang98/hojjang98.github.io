---
title: "Week 06 — TCP/IP 네트워크 프로토콜 분석 및 실무 적용"
date: 2025-12-05
draft: false
tags: ["Network", "TCP/IP", "OSI", "프로토콜", "네트워크보안", "Wireshark", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "TCP/IP 계층 모델부터 주요 프로토콜 동작 원리, 네트워크 보안 기초까지 실무 관점으로 정리한 기술 보고서"
---

# Week 06 — TCP/IP 네트워크 프로토콜 분석 및 실무 적용

> 상세 기술 보고서 (PDF) 는 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_06](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_06)

---

## 개요

Week 6 는 **TCP/IP 네트워크의 동작 원리와 보안 기초**를 학습한 주간이다.
이번 주의 산출물도 Week 5 와 마찬가지로 **기술 보고서** 형태로 정리하였다.

> "서버가 아무리 안정적으로 구축되어 있어도, 네트워크 통신이 원활하지 않으면 서비스를 제공할 수 없다."

네트워크 계층의 문제는 전체 시스템의 **가용성**에 직접 영향을 미친다.
보안 전문가가 패킷을 읽지 못하면 공격 흔적을 남겨도 알아채지 못한다.
Wireshark 로 실제 패킷을 분석하며 추상적인 개념을 구체화하는 과정이 이번 주의 핵심이었다.

---

## 1. 네트워크 계층 모델

### OSI 7계층 vs TCP/IP 4계층

    OSI 7계층 (이론 참조 모델)         TCP/IP 4계층 (실제 인터넷 표준)
    ──────────────────────────         ──────────────────────────────
    7. 응용 계층 (Application)  ─┐
    6. 표현 계층 (Presentation) ─┤ => 4. 응용 계층 (Application)
    5. 세션 계층 (Session)      ─┘         HTTP, HTTPS, DNS, FTP, SSH

    4. 전송 계층 (Transport)    ──── => 3. 전송 계층 (Transport)
                                              TCP, UDP
    3. 네트워크 계층 (Network)  ──── => 2. 인터넷 계층 (Internet)
                                              IP, ICMP, ARP
    2. 데이터링크 계층           ─┐
    1. 물리 계층 (Physical)     ─┘ => 1. 네트워크 접근 계층 (Network Access)
                                              Ethernet, Wi-Fi

**OSI 7계층** 은 이론적 참조 모델로, 프로토콜 설계와 장애 분석의 사고 틀을 제공한다.
**TCP/IP 4계층** 은 실제 인터넷에서 동작하는 프로토콜 스택으로, 실무에서 더 자주 사용한다.

### 계층화의 핵심 가치

- **모듈화** — 각 계층은 독립적으로 동작하여 한 계층의 변경이 다른 계층에 영향을 주지 않는다
- **표준화** — 제조사가 달라도 같은 계층끼리 통신 가능
- **장애 격리** — 문제 발생 시 어느 계층에서 발생했는지 범위를 좁혀 진단 가능

---

## 2. 주요 프로토콜 동작 원리

### ARP — IP 주소를 MAC 주소로 변환

같은 네트워크(LAN) 내에서 통신하려면 IP 주소만으로는 부족하다.
실제 프레임 전송에는 **MAC 주소**가 필요하기 때문에, ARP 가 이 변환을 담당한다.

    1. 송신 측: "192.168.1.10 의 MAC 주소를 알려주세요!" (브로드캐스트)
       => ARP Request: 네트워크 전체에 뿌림 (FF:FF:FF:FF:FF:FF)

    2. 수신 측 (192.168.1.10): "제 MAC 주소는 AA:BB:CC:DD:EE:FF 입니다." (유니캐스트)
       => ARP Reply: 요청자에게만 응답

    3. 송신 측: MAC 주소를 ARP 캐시에 저장 후 통신 시작
       => arp -a 명령으로 현재 캐시 확인 가능

보안 위협 — **ARP 스푸핑 (ARP Spoofing)**:
ARP 는 인증 없이 누구나 Reply 를 보낼 수 있다.
공격자가 가짜 ARP Reply 를 전송하면 피해자의 ARP 캐시가 오염되어
**중간자 공격(Man-in-the-Middle)** 이 가능해진다.

    정상:  피해자 => 게이트웨이 => 인터넷
    ARP 스푸핑: 피해자 => 공격자 => 게이트웨이 => 인터넷  (모든 트래픽 도청 가능)

---

### ICMP — 네트워크 상태 진단 프로토콜

IP 프로토콜의 보조 역할을 하며, 데이터 전송이 아닌 **네트워크 상태 진단 및 오류 보고**가 목적이다.

주요 ICMP 메시지:

| 타입 | 이름 | 용도 |
|------|------|------|
| 8 / 0 | Echo Request / Reply | ping 명령의 기반 |
| 3 | Destination Unreachable | 목적지 도달 불가 (포트 차단 포함) |
| 11 | Time Exceeded | TTL 초과 (traceroute 의 기반) |
| 5 | Redirect | 더 나은 경로 안내 |

보안 관점:

- **ICMP Flood (Ping Flood)** — 대량의 Echo Request 로 서버 자원 고갈 (DDoS)
- **ICMP Redirect 악용** — 가짜 Redirect 메시지로 트래픽 경로 조작
- 방화벽에서 **ICMP 를 완전히 차단하면** 오히려 장애 진단이 어려워짐 (적절한 허용 정책 필요)

---

### TCP 3-Way Handshake — 신뢰성 있는 연결 수립

TCP 는 데이터를 보내기 전에 반드시 3단계 핸드셰이크로 **양방향 연결을 먼저 확립**한다.

    클라이언트                            서버
         │                                   │
         │  ── SYN (seq=x) ──────────────>  │  "연결 요청합니다"
         │                                   │
         │  <── SYN-ACK (seq=y, ack=x+1) ── │  "확인했습니다, 저도 연결 요청합니다"
         │                                   │
         │  ── ACK (ack=y+1) ─────────────>  │  "확인했습니다, 연결 확립!"
         │                                   │
         │  ═══════ 데이터 전송 시작 ══════ │

연결 종료는 **4-Way Handshake** (FIN -> ACK -> FIN -> ACK) 로 이루어진다.

보안 위협 — **SYN Flood 공격**:
대량의 SYN 패킷을 보내되 ACK 를 보내지 않으면,
서버는 수많은 **반개방 연결(Half-Open Connection)** 을 유지하다 자원이 고갈된다.

    대응 방법:
    - SYN Cookie 활성화: 완전한 연결 전까지 서버 자원 미할당
    - Rate Limiting: IP당 SYN 패킷 수 제한
    - 방화벽 임계치 설정

---

### HTTPS & TLS — 안전한 통신의 기반

HTTPS 는 HTTP 에 **TLS(Transport Layer Security)** 보안 계층을 추가한 것이다.

TLS 가 제공하는 3가지 보안 속성:

- **기밀성 (Confidentiality)** — 대칭키 암호화로 데이터 내용을 보호
- **무결성 (Integrity)** — MAC(Message Authentication Code) 로 데이터 변조 탐지
- **인증 (Authentication)** — 서버 인증서(X.509) 로 신뢰할 수 있는 서버임을 확인

TLS Handshake 흐름 (TLS 1.3 기준):

    1. Client Hello  => 지원하는 암호화 방식 목록 전송
    2. Server Hello  => 선택된 암호화 방식 + 인증서 전송
    3. 인증서 검증   => 클라이언트가 CA(인증기관) 서명 확인
    4. 키 교환       => ECDHE 로 세션키 협의
    5. 데이터 전송   => 협의된 대칭키로 암호화 통신 시작

---

### DNS — 도메인을 IP 로 변환

    브라우저에서 www.google.com 입력 시:

    1. 로컬 DNS 캐시 확인 (이미 알고 있으면 바로 사용)
    2. Recursive Resolver (ISP 제공) 에 질의
    3. Root DNS => .com TLD DNS => Google 권한 DNS 순으로 위임 질의
    4. 최종 IP 주소 반환 => 브라우저가 해당 IP 로 HTTP 연결

보안 위협 — **DNS 스푸핑 / DNS 캐시 포이즈닝**:
가짜 DNS 응답을 캐시에 주입하면 피해자가 정상 도메인을 입력해도 **가짜 사이트로 유도**된다.
대응: **DNSSEC** (DNS 응답에 디지털 서명 추가)

---

## 3. 네트워크 보안 기초

### 방화벽 (Firewall)

미리 정의된 **보안 정책(ACL)** 에 따라 트래픽을 허용하거나 차단한다.

    방화벽 종류별 특성:
    - 패킷 필터링    : IP / 포트 기반 단순 차단. 빠르지만 응용 계층 탐지 불가
    - 상태 기반 (Stateful): 연결 상태(SYN/ACK/FIN)를 추적하여 비정상 패킷 차단
    - 응용 계층(WAF): HTTP 요청 내용(SQL Injection, XSS 등) 까지 검사

### IDS vs IPS — 탐지와 차단의 차이

| 구분 | IDS (Intrusion Detection System) | IPS (Intrusion Prevention System) |
|------|----------------------------------|-----------------------------------|
| 역할 | 침입 **탐지** 후 경고 | 침입 **탐지 + 실시간 차단** |
| 성격 | **수동적 (Passive)** — 트래픽 복사본 분석 | **능동적 (Inline)** — 트래픽 경로에 삽입 |
| 오탐 영향 | 경고만 발생, 서비스 영향 없음 | **오탐 시 정상 트래픽도 차단** 위험 |
| 배치 위치 | 네트워크 미러 포트 / TAP | 인라인 (방화벽과 서버 사이) |

보안관제(SOC) 에서는 IDS 와 IPS 를 **상호 보완적으로 함께 운영**하는 것이 일반적이다.

### 포트 스캔과 방어

포트 스캔은 열린 포트를 탐지하여 서비스 정보를 수집하는 기법이다.
공격 전 정찰(Reconnaissance) 단계에서 필수적으로 사용된다.

    주요 스캔 기법:
    - TCP SYN Scan (Half-Open)  : 3-Way Handshake 를 완성하지 않아 로그 최소화
    - TCP Connect Scan          : 완전한 연결 후 끊음. 탐지되기 쉬움
    - UDP Scan                  : 응답 없음 = 열림, ICMP Unreachable = 닫힘
    - Null / FIN / Xmas Scan    : 비정상 플래그 조합으로 방화벽 우회 시도

방어 전략:

- 불필요한 서비스 전부 중지 (필요한 포트만 열기)
- Nmap 탐지 시 차단 또는 경보 발령 (IDS 규칙 설정)
- 포트 넘버 변경으로 자동화 스캔 일부 우회 (SSH 22 -> 비표준 포트)

---

## 4. 실무 진단 도구

### Wireshark — 패킷 분석의 표준

Wireshark 를 통해 배운 것:

- 실제 TCP 핸드셰이크 패킷에서 SYN / SYN-ACK / ACK 플래그 확인
- HTTP 요청 / 응답의 평문 노출 확인 (=> HTTPS 의 필요성 체감)
- ARP 브로드캐스트 패턴과 스푸핑 패킷 구별 방법

### 리눅스 네트워크 진단 명령어

    # 연결 상태 및 포트 확인
    ss -tulnp           -- 현재 열린 포트와 연결 상태 (netstat 대체)
    netstat -an         -- 모든 연결 목록

    # 경로 추적
    traceroute 8.8.8.8  -- 패킷 경로 상 모든 라우터 홉 표시 (ICMP TTL 활용)
    ping -c 4 host      -- 연결성 및 RTT (왕복 시간) 확인

    # 패킷 캡처
    tcpdump -i eth0 port 80   -- eth0 인터페이스에서 80번 포트 트래픽 캡처
    tcpdump -w capture.pcap   -- pcap 파일로 저장 후 Wireshark 분석

    # 네트워크 설정 확인
    ip addr                   -- IP 주소 및 인터페이스 정보
    ip route                  -- 라우팅 테이블
    nmap -sV target_ip        -- 대상 서버 열린 포트 및 서비스 버전 스캔

---

## 5. 계층별 장애 진단 접근법

실무에서 네트워크 문제가 발생하면 **하위 계층부터 상위 계층 순으로** 접근한다.

    [1계층] 물리/링크 계층 점검
       -> 케이블 연결 확인, NIC 상태 확인 (ip link show)

    [2계층] 네트워크 계층 점검
       -> ping 으로 로컬 / 원격 IP 도달 가능 여부 확인
       -> 라우팅 테이블 확인 (ip route)

    [3계층] 전송 계층 점검
       -> 목적지 포트 열려 있는지 확인 (nmap, telnet, nc)
       -> 방화벽 정책 확인

    [4계층] 응용 계층 점검
       -> 서비스 프로세스 실행 여부 (systemctl status)
       -> 로그 확인 (/var/log/nginx/error.log 등)
       -> DNS 해석 확인 (dig, nslookup)

---

## 6. 보안관제 연계 — 네트워크 이상 징후 탐지

| 이상 징후 | 원인 가능성 | 대응 |
|----------|------------|------|
| 대량 ARP Reply | ARP 스푸핑 공격 | ARP 스푸핑 탐지 도구 (arpwatch) 운영 |
| 다수 포트 스캔 시도 | 공격 전 정찰 | IDS 경보 + IP 차단 정책 |
| 대량 SYN 패킷 | SYN Flood (DDoS) | SYN Cookie 활성화, Rate Limiting |
| DNS 쿼리 급증 | DNS 터널링 / C2 통신 | DNS 로그 분석, 비정상 도메인 탐지 |
| ICMP 대용량 트래픽 | Ping Flood / 스머프 공격 | ICMP Rate Limiting |

---

## 학습 성과 정리

| 영역 | 학습 내용 |
|------|----------|
| **계층 모델** | OSI 7계층 vs TCP/IP 4계층 비교, 계층화의 목적과 가치 |
| **프로토콜 이해** | ARP / ICMP / TCP / DNS / HTTPS 의 동작 원리 |
| **보안 기초** | 방화벽 / IDS / IPS 차이, ARP 스푸핑 / SYN Flood / DNS 포이즈닝 |
| **실무 역량** | Wireshark 패킷 분석, 리눅스 네트워크 진단 명령어 활용 |
| **장애 진단** | 계층별 Top-down / Bottom-up 접근법 체득 |

---

## 향후 학습 방향

- **SSL/TLS 심화** — 인증서 체인, HSTS, Certificate Pinning
- **BGP / OSPF** — 인터넷 라우팅 프로토콜과 BGP Hijacking 위협
- **네트워크 포렌식** — pcap 파일 분석으로 침해 사고 재현 및 증거 수집
- **Zero Trust Network** — 경계 보안 모델을 넘어선 현대적 네트워크 보안 아키텍처
- **SDN (Software Defined Networking)** — 클라우드 인프라에서의 네트워크 가상화
