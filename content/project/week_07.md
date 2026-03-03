---
title: "Week 07 — AWS 3-Tier 웹 서비스 인프라 완전 구축"
date: 2025-12-11
draft: false
tags: ["AWS", "VPC", "EC2", "RDS", "ALB", "AutoScaling", "3-Tier", "클라우드", "인프라", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "중소 규모 전자상거래 시나리오를 가정하여 AWS에서 프로덕션 수준의 3-Tier 웹 인프라를 약 3시간 만에 직접 구축한 실습 프로젝트"
---

# Week 07 — AWS 3-Tier 웹 서비스 인프라 완전 구축

> 상세 기술 보고서 및 스크린샷은 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_07](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_07)

---

## 개요

Week 7 는 AWS 클라우드 인프라를 주제로 학습한 주간이다.
이론에 머무르지 않고, **중소 규모 전자상거래 웹사이트**를 가상 시나리오로 설정하여
실무 수준의 완전한 3-Tier 아키텍처를 AWS 에서 처음부터 끝까지 직접 구축했다.

- **구축일** — 2025년 12월 11일
- **리전** — ap-northeast-3 (Osaka)
- **소요 시간** — 약 3시간
- **실제 발생 비용** — ~$0.5 (구축 후 즉시 삭제)

---

## 설계 목표

| 목표 | 구현 방법 |
|------|----------|
| **고가용성 (HA)** | Multi-AZ 구성으로 단일 가용 영역 장애 시에도 서비스 지속 |
| **자동 확장성** | Auto Scaling Group 으로 트래픽 변동에 자동 대응 |
| **계층별 보안** | Public / Private 서브넷 분리 + Security Group 최소 권한 |
| **트래픽 분산** | Application Load Balancer 를 통한 인스턴스 간 로드 밸런싱 |
| **데이터 격리** | RDS 를 완전한 Private Subnet 에 배치하여 외부 접근 차단 |

---

## 전체 아키텍처

    인터넷 사용자
         │
         ▼
    Application Load Balancer  (Public Subnet — ap-northeast-3a / 3b)
         │
         ▼ (트래픽 분산)
    ┌────────────────────────────────────────┐
    │           Amazon VPC (10.0.0.0/16)     │
    │                                        │
    │  [ Public Subnet — Multi-AZ ]          │
    │    - ALB (3a, 3b)                      │
    │    - NAT Gateway (3a, 3b)              │
    │    - Internet Gateway                  │
    │                 │                      │
    │                 ▼                      │
    │  [ Private App Subnet — Multi-AZ ]     │
    │    - EC2 web-server-1a  (3a)           │
    │    - EC2 web-server-1b  (3b)           │
    │    - Auto Scaling Group (Min 2, Max 4) │
    │                 │                      │
    │                 ▼                      │
    │  [ Private DB Subnet — Multi-AZ ]      │
    │    - RDS MySQL 8.0.35                  │
    │    - DB Subnet Group                   │
    │                                        │
    └────────────────────────────────────────┘

---

## 구축 리소스 상세

### 네트워크 계층

- **VPC** — 3tier-production-vpc (CIDR: 10.0.0.0/16)
- **서브넷 6개** — Public 2개 / Private App 2개 / Private DB 2개 (각 AZ 별 1개씩)
- **Internet Gateway** — VPC 와 인터넷 연결
- **NAT Gateway 2개** — Private 서브넷의 아웃바운드 인터넷 통신 허용 (Multi-AZ)
- **Route Table 5개** — Public 1개 + Private App 2개 + Private DB 2개

서브넷 CIDR 설계:

    Public-3a      :  10.0.1.0/24   (ALB, NAT)
    Public-3b      :  10.0.2.0/24   (ALB, NAT)
    PrivateApp-3a  :  10.0.11.0/24  (EC2)
    PrivateApp-3b  :  10.0.12.0/24  (EC2)
    PrivateDB-3a   :  10.0.21.0/24  (RDS)
    PrivateDB-3b   :  10.0.22.0/24  (RDS)

### 보안 계층 — Security Groups

계층별 인바운드 규칙을 철저히 분리하여 **수평 이동(Lateral Movement)** 을 차단한다.

    alb-sg (ALB 전용)
      인바운드:  80 (HTTP)  /  443 (HTTPS)  from 0.0.0.0/0
      아웃바운드: 80  to  web-server-sg

    web-server-sg (EC2 전용)
      인바운드:  80 (HTTP)  from alb-sg 만 허용
      아웃바운드: 3306 (MySQL)  to  rds-sg

    rds-sg (RDS 전용)
      인바운드:  3306 (MySQL)  from web-server-sg 만 허용
      아웃바운드: 제한 없음

### 컴퓨팅 계층

- **Application Load Balancer** — Active 상태, 헬스 체크로 비정상 인스턴스 자동 제외
- **Target Group** — 2개 인스턴스 모두 Healthy 확인
- **Launch Template** — AMI: Amazon Linux 2023 + User Data 스크립트 포함
- **Auto Scaling Group** — Min 2 / Max 4 / Desired 2, 인스턴스 장애 시 자동 교체

### 데이터베이스 계층

- **RDS MySQL 8.0.35** (db.t3.micro)
- DB Subnet Group 으로 Multi-AZ 배치
- **완전 Private Subnet 격리** — 인터넷 및 ALB 에서 직접 접근 불가

---

## 핵심 코드 — EC2 User Data 스크립트

Auto Scaling Group 이 새 인스턴스를 시작할 때 **Launch Template 의 User Data** 가 자동 실행된다.
이 스크립트 덕분에 인스턴스가 추가될 때마다 수동 설정 없이 Nginx 가 자동 설치 및 실행된다.

스크립트 주요 흐름:

    1. 시스템 업데이트 및 Nginx 설치
       yum update -y
       yum install -y nginx

    2. Nginx 서비스 시작 및 부팅 시 자동 실행 등록
       systemctl start nginx
       systemctl enable nginx

    3. EC2 메타데이터 API 로 인스턴스 정보 수집
       INSTANCE_ID  => ec2-metadata --instance-id
       AZ           => ec2-metadata --availability-zone

    4. 인스턴스별 고유 HTML 페이지 생성
       index.html 에 INSTANCE_ID, AZ 값을 동적으로 삽입
       => 브라우저에서 새로고침 시 ALB 가 두 인스턴스를 번갈아 응답하는 것을 육안으로 확인 가능

이 구성 덕분에 ALB 에서 발급받은 DNS 로 브라우저를 새로고침할 때마다
**web-server-1a (ap-northeast-3a)** 와 **web-server-1b (ap-northeast-3b)** 가
번갈아 응답하는 로드 밸런싱을 직접 확인할 수 있었다.

---

## 트러블슈팅

### 문제 1 — Private Subnet 에서 인터넷 접근 불가

- **증상** — User Data 스크립트 실행 실패, Nginx 설치 안 됨
- **원인** — Private App Subnet 의 Route Table 에 NAT Gateway 경로가 미설정
- **해결** — Private App Subnet Route Table 에 0.0.0.0/0 => NAT Gateway 경로 추가

    수정 전:  Private App Subnet => 목적지 없음 (인터넷 불가)
    수정 후:  Private App Subnet => 0.0.0.0/0 => NAT-3a / NAT-3b

### 문제 2 — Auto Scaling 인스턴스 단일 AZ 집중

- **증상** — Auto Scaling Group 이 두 인스턴스를 모두 ap-northeast-3a 에만 배치
- **원인** — ASG 의 AZ 밸런싱 설정이 초기 배포에서 단일 AZ 로 편중
- **해결** — ap-northeast-3b 에 EC2 인스턴스를 수동 생성 후 Target Group 에 직접 등록

    결과:  web-server-1a (ap-northeast-3a) + web-server-1b (ap-northeast-3b)
           => Target Group 에서 2 Healthy 확인

---

## 비용 분석

### 실제 구축 비용 (3시간 운영)

| 리소스 | 비용 |
|--------|------|
| NAT Gateway × 2 | $0.27 |
| Application Load Balancer | $0.07 |
| EC2 t3.micro × 2 | $0 (프리티어) |
| RDS db.t3.micro | $0 (프리티어) |
| **총계** | **~$0.5** |

### 프로덕션 환경 월 예상 비용

NAT Gateway, ALB, EC2 (On-Demand), RDS 등을 상시 운영 시 **약 $325/월** 수준.
비용 절감을 위해서는 EC2 Reserved Instance, RDS Reserved Instance, Savings Plans 를 검토해야 한다.

---

## 보안 관점 연계

이번 프로젝트에서 적용한 설계 원칙은 실무 보안 아키텍처와 직접 연결된다.

- **최소 권한 원칙 (PoLP)** — Security Group 에서 필요한 포트만 열고, 출처도 특정 SG 로 제한
- **심층 방어 (Defense in Depth)** — ALB -> EC2 -> RDS 로 이어지는 3중 방어선
- **네트워크 분리** — 외부에서 DB 에 직접 접근하는 경로가 아키텍처 레벨에서 존재하지 않음
- **가용성 확보** — Multi-AZ 구성으로 단일 장애 지점(SPOF) 제거

    공격자가 ALB DNS 를 알아도:
    - EC2 내부 IP 는 외부 노출 없음 (Private Subnet)
    - RDS 는 web-server-sg 에서만 접근 가능 (VPC 내부 전용)
    - SSH 는 Security Group 규칙에 없음 (Bastion Host 별도 구성 필요)

---

## 학습 성과 정리

| 영역 | 학습 내용 |
|------|----------|
| **네트워크** | VPC 설계, 서브넷 CIDR 할당, Route Table, NAT / IGW 역할 |
| **로드 밸런싱** | ALB 동작 원리, Target Group, 헬스 체크 메커니즘 |
| **Auto Scaling** | Launch Template, ASG 정책, User Data 자동화 |
| **데이터베이스** | RDS 배치 전략, DB Subnet Group, 보안 격리 |
| **보안 설계** | Security Group 계층 분리, 최소 권한 원칙 적용 |
| **트러블슈팅** | NAT 라우팅 문제 해결, AZ 불균형 수동 교정 |

---

## 향후 확장 방향

- **HTTPS 적용** — ACM 인증서 + ALB HTTPS 리스너 추가
- **도메인 연결** — Route 53 으로 커스텀 도메인 연결
- **Bastion Host** — Private EC2 에 SSH 접근을 위한 점프 서버 구성
- **CloudWatch 모니터링** — CPU / 메모리 / 요청 수 기반 Auto Scaling 정책 설정
- **WAF 연동** — ALB 앞단에 AWS WAF 추가하여 웹 애플리케이션 공격 차단
- **IaC 전환** — 수동 구축을 Terraform 또는 CloudFormation 으로 자동화
