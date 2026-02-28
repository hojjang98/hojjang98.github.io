---
title: "2026.01.26 (Day 63) - Wazuh Agent 등록 및 모니터링 실습"
date: 2026-01-26
draft: false
categories: ["daily-logs"]
tags: ["Wazuh", "Agent", "Agentless", "Sysmon", "HIDS", "에이전트모니터링", "Windows", "Linux"]
summary: "Windows/Linux Wazuh Agent 설치 및 서버 등록(1514·1515 포트), Agentless SSH 키 인증 방식, Sysmon 연동으로 Windows 상세 활동 로그(프로세스 생성·네트워크 연결) 수집, Agent vs Agentless 운영 환경별 비교, Wazuh 룰 레벨 0~15 체계 및 SOC 대응 기준"
---

# 📄 2026.01.26 (Day 63) - Wazuh Agent 등록 및 모니터링 실습

---

## 1. 핵심 개념 정리

### Wazuh Agent 개요

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 1 | **Agent 방식** | 대상 시스템에 직접 프로그램을 설치하여 실시간 모니터링 수행 | 실시간 위협 탐지가 가능하여 대부분의 서버/워크스테이션 환경에서 권장되는 방식 |
| 2 | **Agentless 방식** | SSH 프로토콜을 통해 원격으로 주기적 점검 수행, 별도 설치 불필요 | 네트워크 장비나 Agent 설치가 제한된 환경에서 유용하나 기능이 제한적 |
| 3 | **에이전트 통신 포트** | 1514(등록), 1515(통신) 포트를 통해 Wazuh 서버와 양방향 통신 | 방화벽 정책 수립 시 필수 허용 포트이며, 통신 장애의 주요 원인 |
| 4 | **에이전트 상태 관리** | Active, Disconnected, Never connected 등 상태로 에이전트 연결 관리 | 정기적인 상태 점검으로 모니터링 사각지대 방지 필요 |
| 5 | **에이전트 그룹** | 에이전트를 논리적으로 그룹화하여 정책 및 설정 일괄 적용 가능 | 조직 구조나 시스템 특성에 따른 그룹 분류로 효율적 관리 가능 |

### Windows Agent 구성

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 6 | **MSI 설치 패키지** | PowerShell 명령어 또는 GUI 방식으로 설치 가능한 설치 파일 | 대규모 배포 시 GPO나 자동화 스크립트 활용 고려 |
| 7 | **WazuhSvc 서비스** | Windows 서비스로 등록되어 백그라운드에서 실행되는 에이전트 프로세스 | 서비스 자동 시작 설정으로 재부팅 후에도 모니터링 연속성 보장 |
| 8 | **ossec.conf 설정** | 에이전트의 동작 방식, 로그 수집 대상 등을 정의하는 핵심 설정 파일 | 조직 보안 정책에 맞춰 커스터마이징 필요 |
| 9 | **이벤트 채널 수집** | Windows 이벤트 로그를 실시간으로 수집하여 서버로 전송 | 로그인 실패, 권한 변경 등 주요 보안 이벤트 탐지의 기반 |
| 10 | **에이전트 로그** | ossec.log 파일에 에이전트 동작 상태 및 오류 정보 기록 | 문제 발생 시 1차 점검 대상, 연결 실패나 설정 오류 진단에 활용 |

### Linux Agent 구성

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 11 | **DEB 패키지 설치** | apt 저장소 등록 또는 직접 다운로드하여 dpkg로 설치 | Ubuntu/Debian 계열 서버에서 표준 패키지 관리 방식 활용 |
| 12 | **systemd 서비스 관리** | systemctl 명령어로 에이전트 서비스 시작/중지/상태 확인 | 자동 시작 설정(enable)으로 서버 재부팅 시에도 모니터링 유지 |
| 13 | **서버 주소 설정** | ossec.conf의 server/address 태그에 Wazuh 서버 IP 지정 | 잘못된 주소 설정은 에이전트 등록 실패의 가장 흔한 원인 |
| 14 | **로그 경로** | /var/ossec/logs/ossec.log에 에이전트 동작 로그 저장 | tail -f 명령으로 실시간 로그 확인 가능 |
| 15 | **권한 관리** | ossec 사용자 권한으로 실행되며, 시스템 로그 접근 권한 필요 | 보안을 위해 최소 권한 원칙 적용, 필요 시 sudo 권한 부여 |

---

## 2. 실습 내용 정리

### 실습 61-1: Windows Agent 설치 및 등록

**목표:** Windows 시스템에 Wazuh Agent를 설치하고 서버에 등록하여 실시간 모니터링 환경 구축

**실습 환경:**
- Wazuh 서버: 192.168.2.10
- Windows 클라이언트 (관리자 권한 필요)
- PowerShell 5.1 이상

**실습 단계:**

1. 관리자 권한 PowerShell 실행 후 에이전트 다운로드 및 설치
   - Invoke-WebRequest로 wazuh-agent-4.7.0-1.msi 다운로드 (packages.wazuh.com)
   - msiexec.exe 로 MSI 설치, WAZUH_MANAGER=192.168.2.10, WAZUH_AGENT_GROUP=default 지정
2. 서비스 시작: NET START WazuhSvc
3. 에이전트 상태 확인: agent-control.exe -s 실행
4. 설정 파일 확인: C:\Program Files (x86)\ossec-agent\ossec.conf
5. Wazuh 대시보드 https://192.168.2.10 접속 → Agents 메뉴에서 등록 확인

**확인 항목:**
- 에이전트가 Active 상태로 표시되는지 확인
- Last keep alive 시간이 최근인지 점검
- ossec.log에서 "Connected to the server" 메시지 확인
- 방화벽에서 1514, 1515 포트 허용 상태 확인

**보안 인사이트:**
- 에이전트 설치 후 즉시 서버와 통신하므로 네트워크 세그먼트 설계 중요
- 기본 그룹보다는 시스템 역할별 그룹 분류로 차별화된 정책 적용 권장
- WazuhSvc 서비스 자동 시작 설정으로 재부팅 후에도 모니터링 연속성 확보

### 실습 61-2: Linux Agent 설치 및 서버 연동

**목표:** Ubuntu 시스템에 Wazuh Agent를 설치하고 중앙 서버와 연동

**실습 환경:**
- Ubuntu 20.04/22.04
- Wazuh 서버: 192.168.2.10
- sudo 권한 필요

**실습 단계:**

1. GPG 키 및 저장소 추가
   - curl -s packages.wazuh.com/key/GPG-KEY-WAZUH | sudo apt-key add -
   - echo 저장소 URL | sudo tee /etc/apt/sources.list.d/wazuh.list
2. 패키지 설치: sudo apt update && sudo apt install -y wazuh-agent
3. 서버 주소 설정: sudo nano /var/ossec/etc/ossec.conf → client/server/address 태그에 192.168.2.10 입력
4. 서비스 시작 및 활성화
   - sudo systemctl daemon-reload
   - sudo systemctl enable wazuh-agent
   - sudo systemctl start wazuh-agent
   - sudo systemctl status wazuh-agent

**systemd 서비스 동작 방식:**
- systemctl enable: 부팅 시 자동 시작되도록 심볼릭 링크 생성 (/etc/systemd/system/multi-user.target.wants/)
- systemctl start: 서비스 즉시 시작, PID 파일 생성 및 프로세스 포크
- daemon-reload: systemd가 유닛 파일 변경사항 인식하도록 재로드

**발견 가능한 연결 상태:**
- Active (running): 정상 동작 중
- Failed: 설정 오류 또는 서버 연결 실패
- Inactive: 서비스가 중지된 상태

**보안 고려사항:**
- systemctl status에서 "active (running)" 상태 확인
- /var/ossec/logs/ossec.log에서 연결 성공 메시지 모니터링
- 대시보드에서 Agent 상태가 "Active"로 변경되는지 확인
- 방화벽에서 Wazuh 서버 IP만 허용하도록 iptables 규칙 설정
- ossec.conf 파일 권한을 640으로 제한하여 무단 수정 방지

### 실습 61-3: Agentless 모니터링 설정

**목표:** SSH 기반 Agentless 방식으로 원격 시스템 무결성 검사 구성

**실습 환경:**
- Wazuh 서버: 192.168.2.10
- 대상 서버: 192.168.2.100 (admin 계정)
- SSH 키 인증 방식 사용

**실습 단계:**

1. Wazuh 서버에서 SSH 키 생성: sudo -u ossec ssh-keygen -t rsa -N "" -f /var/ossec/.ssh/id_rsa
2. 대상 서버에 공개키 복사: sudo -u ossec ssh-copy-id admin@192.168.2.100
3. 비밀번호 없이 접속 테스트: sudo -u ossec ssh admin@192.168.2.100
4. Agentless 호스트 등록: sudo /var/ossec/agentless/register_host.sh add admin@192.168.2.100 NOPASS
5. ossec.conf에 설정 추가 (agentless 섹션)

**ossec.conf Agentless 설정 항목:**
- type: ssh_integrity_check_linux
- frequency: 36000 (초 단위, 약 10시간)
- host: admin@192.168.2.100
- state: periodic

**Agentless 점검 항목:**
- 파일 무결성 검사 (중요 시스템 파일 변경 탐지)
- 주기적 시스템 설정 점검
- 사용자 계정 및 권한 변경 모니터링

**제약 사항:**
- 실시간 모니터링 불가 (frequency 설정에 따른 주기적 점검)
- Agent 방식 대비 제한적인 로그 수집
- 네트워크 장비나 특수 환경에 적합

### 실습 61-4: Windows Sysmon 연동

**목표:** Sysmon을 통해 Windows 시스템의 상세한 활동 로그를 Wazuh로 수집

**실습 환경:**
- Windows 10/11 또는 Windows Server
- Sysmon 다운로드 필요 (Microsoft Sysinternals)
- Wazuh Agent 설치 완료 상태

**실습 단계:**

1. Sysmon 다운로드 및 설치: Sysmon64.exe -accepteula -i
2. Wazuh Agent 설정 파일 수정: notepad C:\Program Files (x86)\ossec-agent\ossec.conf
3. ossec.conf에 Sysmon 로그 수집 설정 추가
   - localfile 섹션 추가
   - location: Microsoft-Windows-Sysmon/Operational
   - log_format: eventchannel
4. Wazuh Agent 서비스 재시작: NET STOP WazuhSvc -> NET START WazuhSvc
5. 대시보드에서 Sysmon 이벤트 확인
   - Agents -> Security Events -> 필터: data.win.system.channel:Microsoft-Windows-Sysmon/Operational

**Sysmon 수집 이벤트:**
- Event ID 1: 프로세스 생성 (프로세스명, 명령줄, 해시값 등)
- Event ID 3: 네트워크 연결 (출발지/목적지 IP, 포트)
- Event ID 7: 이미지 로드 (DLL 로딩)
- Event ID 11: 파일 생성
- Event ID 13: 레지스트리 값 설정

**보안 활용도:**

APT 공격 탐지:
- 비정상적인 프로세스 실행 패턴 분석
- 악성 DLL 인젝션 탐지
- C&C 통신 네트워크 연결 식별

침해사고 분석:
- 공격자 실행 명령어 타임라인 재구성
- 악성코드 파일 생성 이력 추적
- 레지스트리 변조 흔적 발견

---

## 3. Agent vs Agentless 비교 분석

### 모니터링 방식 비교

| 항목 | Agent 방식 | Agentless 방식 | 사용 시기/적용 방안 |
|:---:|:---|:---|:---|
| **설치** | 대상 시스템에 프로그램 설치 필요 | SSH 연결만으로 모니터링 가능 | Agent: 일반 서버/PC, Agentless: 네트워크 장비 |
| **모니터링 주기** | 실시간 이벤트 수집 및 전송 | 스케줄 기반 주기적 점검 (예: 10시간) | Agent: 즉각 대응 필요한 시스템, Agentless: 보조적 점검 |
| **수집 범위** | 전체 로그, 레지스트리, 프로세스 등 | 파일 무결성, 기본 설정 점검 위주 | Agent: 포괄적 모니터링, Agentless: 특정 무결성 점검 |
| **시스템 부하** | 에이전트 프로세스가 지속 실행 | 점검 시점에만 SSH 연결 발생 | Agent: 리소스 여유 환경, Agentless: 최소 부하 요구 환경 |
| **관리 복잡도** | 각 시스템별 설치 및 업데이트 필요 | 서버 측 설정만으로 관리 | Agent: 중앙 관리 도구 활용, Agentless: 소규모 환경 |

### 운영 환경별 권장 방식

| 환경 유형 | 권장 방식 | 사용 이유 |
|:---|:---|:---|
| Windows/Linux 서버 | Agent | 실시간 위협 탐지, 전체 로그 수집 가능 |
| 네트워크 장비 (스위치, 라우터) | Agentless | Agent 설치 불가능한 펌웨어 기반 시스템 |
| IoT 디바이스 | Agentless | 제한된 리소스, 별도 프로그램 설치 어려움 |
| 보안 정책상 Agent 설치 불가 | Agentless | 시스템 변경 최소화 요구사항 충족 |
| 임시 시스템 (테스트 서버 등) | Agentless | 짧은 운영 기간, 설치 오버헤드 불필요 |

---

## 4. 심화 분석

### 에이전트 통신 프로토콜 상세 분석

| 구분 | 포트 번호 | 프로토콜 | 용도 | 분석/인사이트 |
|:---:|:---|:---|:---|:---|
| **등록** | 1514 | TCP | 에이전트 최초 등록 및 인증 키 교환 | 등록 과정에서 고유 ID와 공유 키 생성, 중간자 공격 방지 위해 암호화 |
| **통신** | 1515 | TCP | 로그 데이터 실시간 전송 및 명령 수신 | AES 256 암호화로 데이터 기밀성 보장, 압축으로 대역폭 최적화 |
| **Syslog** | 514 | UDP | 레거시 시스템 로그 수신 (선택적) | Syslog 포워딩 환경에서 활용, 신뢰성은 TCP 대비 낮음 |
| **API** | 55000 | HTTPS | RESTful API 통한 관리 작업 | 자동화 스크립트나 외부 시스템 연동에 활용 |

### 에이전트 인증 메커니즘

에이전트 등록 시 인증 키 생성 과정:

1. 에이전트가 서버에 등록 요청 (1514 포트) → 호스트명, OS 정보 전송
2. 서버가 고유 에이전트 ID 할당 (예: 001, 002) → /var/ossec/etc/client.keys에 기록
3. 공유 인증 키 생성 및 배포 → 양방향 암호화 통신을 위한 대칭키, 에이전트 측에도 동일 키 저장
4. 이후 모든 통신은 인증 키로 암호화/검증 → 키 불일치 시 통신 거부

### Wazuh 룰 레벨 체계

레벨 체계 (0~15):
- 0~3: 정보성 이벤트 (일반 로그, 시스템 정보)
- 4~5: 낮은 우선순위 (보안과 무관한 일반 경고)
- 6~7: 중간 우선순위 (주의가 필요한 의심 활동)
- 8~11: 높은 우선순위 (확실한 보안 위협)
- 12~15: 심각 (즉각 대응 필요한 공격 탐지)

SOC 대응 기준:
- Level 7 이상: 보안 담당자 리뷰 필요
- Level 10 이상: 즉각 조사 및 격리 고려
- Level 12 이상: 긴급 대응 프로세스 가동

---

## 5. 실무/보안 적용

### 보안 전문가 관점 - 에이전트 모니터링 포인트

| 단계/유형 | 탐지 포인트 | 로그 예시 | 대응 방안 |
|:---:|:---|:---|:---|
| **에이전트 연결** | Agent 등록 이벤트, 최초 연결 시각, 인증 키 교환 성공 여부 | INFO: New connection from 192.168.2.100 | 승인되지 않은 IP의 등록 시도 차단, 등록 이벤트 로깅 및 검토, 정기적 에이전트 목록 감사 |
| **비정상 연결 해제** | 예기치 않은 Disconnect, Keep-alive 실패, 인증 오류 반복 | WARNING: Agent disconnected: 001 | 네트워크 장애 vs 악의적 차단 구분, 에이전트 무응답 알림 설정, 자동 재연결 시도 모니터링 |
| **설정 변경 탐지** | ossec.conf 수정, 서비스 중지 시도, 에이전트 삭제 시도 | CRITICAL: Configuration file modified | 파일 무결성 모니터링 활성화, 변경 이력 추적 및 승인 프로세스, 백업 설정 자동 복원 |

### Sysmon 룰셋 예시

의심스러운 PowerShell 실행 탐지를 위한 Sysmon 설정 항목:
- ProcessCreate 이벤트에서 powershell.exe 이미지 포함, -encodedcommand 명령줄 포함인 경우 탐지
- NetworkConnect 이벤트에서 목적지 포트 4444, 5555 연결 탐지

### Wazuh 커스텀 룰 예시

Windows 방화벽 비활성화 탐지 (rule id: 100010, level: 12):
- 조건: EventID 60103이면서 commandLine에 .ps1 또는 netsh firewall disable 포함
- MITRE ATT&CK: T1562.004 매핑

---

## 6. 배운 점 및 인사이트

### 새로 알게 된 점

- **Agent vs Agentless 선택 기준:** 실시간성이 중요한 환경에서는 Agent 방식이 필수이며, Agentless는 보조적 수단이나 제한 환경에서 활용하는 것이 적절함을 이해했다.
- **Sysmon의 강력한 탐지 능력:** Windows 기본 이벤트 로그만으로는 파악하기 어려운 프로세스 생성, DLL 로딩, 네트워크 연결까지 상세하게 추적할 수 있어 APT 공격 분석에 핵심적임을 확인했다.
- **에이전트 통신 암호화:** 1515 포트를 통한 데이터 전송이 AES 256으로 암호화되어 있어 네트워크 스니핑 공격에도 안전하다는 점을 배웠다.
- **룰 레벨의 실무적 의미:** Level 7 이상을 주요 검토 대상으로 하고, Level 12 이상은 즉각 대응하는 구조가 SOC 운영의 효율성을 크게 높인다는 것을 이해했다.
- **Agentless SSH 키 인증 방식:** 비밀번호 없는 키 기반 인증으로 자동화된 점검이 가능하며, ossec 사용자 권한으로 실행되어 보안성도 확보된다는 점이 인상적이었다.

### 이전 학습과의 연결고리

- **Splunk SIEM 연계:** Wazuh에서 수집한 로그를 Splunk로 포워딩하면 더욱 강력한 상관분석과 시각화가 가능할 것으로 예상된다. 특히 Sysmon 이벤트를 Splunk에서 분석하면 공격 타임라인 재구성에 유용할 것이다.
- **Security Onion & Suricata 통합:** 네트워크 레벨(Suricata)과 호스트 레벨(Wazuh) 탐지를 결합하면 내부 측면 이동과 외부 C&C 통신을 동시에 포착하는 다층 방어가 구현된다.
- **웹 취약점 진단 -> 침해 탐지:** 이전에 학습한 XSS, CSRF 공격을 Wazuh로 탐지한다면 웹 서버 로그에서 비정상 패턴을 룰로 정의하여 실시간 차단이 가능하다.

### 실무 적용 아이디어

**보안 전문가 관점:**
- **계층별 모니터링 체계 구축:** 일반 서버는 Agent로 실시간 모니터링, 네트워크 장비는 Agentless로 보조 점검하여 사각지대 없는 관제 환경 구현
- **Sysmon + MITRE ATT&CK 매핑:** Sysmon 이벤트를 MITRE 공격 기법과 연결하는 커스텀 룰을 작성하여 공격 단계별 탐지 정확도 향상
- **에이전트 상태 자동 점검:** 주기적으로 Disconnected 에이전트를 확인하고 알림을 발송하는 Python 스크립트를 작성하여 관제 공백 최소화

**인프라 엔지니어 관점:**
- **대규모 배포 자동화:** Ansible이나 GPO를 활용한 Wazuh Agent 일괄 설치 및 설정 배포로 수백 대 서버 관리 효율화
- **로그 보관 정책 수립:** 법적 요구사항과 저장 용량을 고려하여 Wazuh 로그 보관 기간 및 압축 정책 설정

---

## 7. Quick Reference

### 에이전트 관리 명령어 모음

**Wazuh 서버 측:**
- 전체 에이전트 목록 조회: sudo /var/ossec/bin/agent_control -l
- 특정 에이전트 상세 정보: sudo /var/ossec/bin/agent_control -i 001
- 에이전트 삭제: sudo /var/ossec/bin/manage_agents -r 001
- Agentless 호스트 등록: sudo /var/ossec/agentless/register_host.sh add user@host NOPASS
- Wazuh 매니저 재시작: sudo systemctl restart wazuh-manager

**Windows Agent 관리:**
- 서비스 시작: NET START WazuhSvc
- 서비스 중지: NET STOP WazuhSvc
- 상태 확인: C:\Program Files (x86)\ossec-agent\agent-control.exe -s
- 로그 확인: Get-Content ossec.log -Tail 50

**Linux Agent 관리:**
- 서비스 제어: sudo systemctl start/stop/restart/status wazuh-agent
- 실시간 로그 모니터링: sudo tail -f /var/ossec/logs/ossec.log
- 서버 연결 테스트: sudo /var/ossec/bin/agent-auth -m 192.168.2.10

### 핵심 파일 경로 요약표

| 구분 | 항목 | 경로 | 주요 내용 | 적용 방법 |
|:---:|:---|:---|:---|:---|
| **Windows** | 설정 파일 | C:\Program Files (x86)\ossec-agent\ossec.conf | 서버 주소, 로그 수집 대상 | notepad로 편집 후 서비스 재시작 |
| **Windows** | 로그 파일 | C:\Program Files (x86)\ossec-agent\ossec.log | 에이전트 동작 로그 | 문제 발생 시 확인 |
| **Linux** | 설정 파일 | /var/ossec/etc/ossec.conf | 서버 주소, 로그 수집 대상 | nano/vi로 편집 후 systemctl restart |
| **Linux** | 로그 파일 | /var/ossec/logs/ossec.log | 에이전트 동작 로그 | tail -f로 실시간 모니터링 |
| **서버** | 클라이언트 키 | /var/ossec/etc/client.keys | 등록된 에이전트 인증 키 | 백업 필수, 무단 수정 방지 |

### 대시보드 필터링 체크리스트

**기본 필터:**
- 룰 레벨 7 이상만 표시: rule.level:>=7
- 특정 에이전트 이벤트: agent.name:"DESKTOP-ABC123"
- Sysmon 이벤트: data.win.system.channel:Microsoft-Windows-Sysmon/Operational
- 인증 실패 이벤트: rule.groups:authentication_failed

**고급 쿼리:**
- PowerShell 실행: data.win.eventdata.commandLine:*powershell*
- 외부 IP 연결: data.srcip:!192.168.*
- 실패한 로그인 5회 이상: rule.id:5710 AND rule.level:>=7

---

## 8. 트러블슈팅

| 문제 | 원인 | 해결 방법 |
|:---|:---|:---|
| **Agent가 Never connected 상태** | 방화벽에서 1514/1515 포트 차단 | ufw allow 1514/tcp, ufw allow 1515/tcp 실행, Windows 방화벽에서 포트 허용 규칙 추가, 클라우드 환경이면 보안그룹 설정 확인 |
| **Agent가 Disconnected로 변경됨** | 네트워크 단절 또는 에이전트 서비스 중지 | systemctl status wazuh-agent 또는 NET START WazuhSvc 확인, 네트워크 연결 및 DNS 해석 점검, ossec.log에서 "Connection refused" 메시지 확인 |
| **Sysmon 로그가 수집되지 않음** | ossec.conf 설정 누락 또는 Sysmon 미설치 | 이벤트 뷰어에서 Sysmon 로그 생성 확인, ossec.conf에 location 태그 추가, WazuhSvc 재시작 |
| **Agentless 연결 실패** | SSH 키 인증 설정 오류 | sudo -u ossec ssh user@host 명령으로 비밀번호 없이 접속 테스트, authorized_keys 파일 권한 600 확인, /var/ossec/.ssh/id_rsa 키 파일 존재 여부 점검 |

---

**Today's Insight:**

Wazuh Agent 실습을 통해 호스트 기반 보안 모니터링의 핵심을 체득했다. Agent 방식은 실시간 위협 탐지에 필수적이며, Sysmon과 결합하면 Windows 환경에서도 공격자의 미세한 흔적까지 추적할 수 있다는 것을 확인했다. 특히 에이전트 통신이 암호화되어 있고, 인증 키 기반으로 동작하여 무단 접근이 원천 차단되는 구조가 인상적이었다. 앞으로 Splunk와 통합하여 네트워크 탐지(Suricata)와 호스트 탐지(Wazuh)를 융합한 다층 방어 체계를 구현하면, 내외부 위협을 효과적으로 대응하는 실전 SOC 환경을 완성할 수 있을 것이다.
