---
title: "2025.12.09 (Day 32) - AWS 네트워크 심화 및 데이터베이스 서비스"
date: 2025-12-09
draft: false
tags: ["AWS", "Route53", "CloudFront", "RDS", "Aurora", "DynamoDB", "Redshift", "데이터베이스", "CDN"]
categories: ["daily-logs"]
summary: "Route 53 라우팅 정책, CloudFront CDN, API Gateway, RDS/Aurora Multi-AZ 고가용성, DynamoDB NoSQL, Redshift 데이터 웨어하우스 개요 및 실습"
---

# 📄 2025.12.09 (Day 32) - AWS 네트워크 심화 및 데이터베이스 서비스

---

## 1. 핵심 개념 정리

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| **1** | **Amazon Route 53** | 가용성과 확장성이 뛰어난 클라우드 DNS 웹 서비스. 도메인 등록, DNS 라우팅, 헬스 체크 기능 제공 | 단순, 가중치, 지연 시간, 장애 조치 등 다양한 라우팅 정책을 통해 DR(재해 복구) 및 트래픽 관리 구현 가능 |
| **2** | **Amazon CloudFront** | 짧은 지연 시간과 빠른 전송 속도로 데이터, 동영상, 애플리케이션을 전송하는 CDN 서비스. 엣지 로케이션에 콘텐츠 캐싱 | S3와 연동 시 **OAC(Origin Access Control)**를 사용하여 S3 직접 접근을 막고 CloudFront를 통해서만 접근하도록 보안 강화 |
| **3** | **Amazon API Gateway** | 규모에 상관없이 개발자가 API를 생성, 게시, 유지 관리, 모니터링 및 보안 설정할 수 있는 완전 관리형 서비스 | REST, HTTP, WebSocket API 지원. **스로틀링(Throttling)**으로 트래픽 급증 방지, 인증/인가(Cognito, IAM) 통합으로 보안성 확보 |
| **4** | **AWS Global Accelerator** | AWS 글로벌 네트워크를 사용하여 애플리케이션의 가용성과 성능을 개선. 고정된 Anycast IP 제공 | 클라이언트 IP 보존 가능. CloudFront와 달리 TCP/UDP 프로토콜 지원 및 비 HTTP 사용 사례(게임 등)에 적합 |
| **5** | **Amazon RDS** | 관계형 데이터베이스(RDB)의 설정, 운영, 확장을 돕는 관리형 서비스. MySQL, PostgreSQL, MariaDB, Oracle, SQL Server 엔진 지원 | **Multi-AZ 배포**로 고가용성 확보(장애 시 자동 Failover). **읽기 전용 복제본(Read Replica)**으로 읽기 부하 분산 |
| **6** | **Amazon Aurora** | MySQL 및 PostgreSQL과 호환되는 클라우드 네이티브 관계형 DB. 고성능 상용 DB 속도와 오픈 소스 DB의 비용 효율성 결합 | 3개 가용 영역에 6개의 데이터 사본 저장으로 높은 내구성 제공. 스토리지 자동 확장 및 빠른 복구 기능 |
| **7** | **Amazon DynamoDB** | 어떤 규모에서도 10밀리초 미만의 성능을 제공하는 키-값(Key-Value) 및 문서 데이터베이스. 완전 관리형, 서버리스 NoSQL | 유연한 스키마, 무제한 처리량. 트래픽에 따라 자동 확장(Auto Scaling)되며 온디맨드 및 프로비저닝 용량 모드 선택 가능 |
| **8** | **Amazon Redshift** | SQL을 사용하여 정형 및 반정형 데이터를 분석할 수 있는 클라우드 데이터 웨어하우스 서비스. 열(Columnar) 기반 스토리지 사용 | 대규모 데이터 분석 및 BI(Business Intelligence) 도구와 연동. 리더 노드와 컴퓨팅 노드로 구성되어 병렬 처리 수행 |

---

## 2. 실습 내용

### RDS 생성 실습 (MySQL)

**1. DB 서브넷 그룹 생성:**
- RDS Console → Subnet groups → Create DB subnet group
- Name: oooo-myvpc-subnet-group
- VPC: oooo-myvpc
- Availability Zones: ap-northeast-2a, ap-northeast-2c
- Subnets: Private Subnet 2개 선택

**2. RDS 생성 (MySQL):**
- Engine: MySQL, Template: Dev/Test
- DB Instance Identifier: oooo-mysqldb-test
- Master username: admin / Password: 안전한 비밀번호
- Instance Class: db.t4g.micro (Burstable)
- Storage: gp2 20GiB
- Connectivity:
  - VPC: oooo-myvpc
  - **Public access: No** (보안상 Private 배치 권장)
  - Security Group: 신규 생성 (oooo-myvpc-mysqldb-sg)

**3. 보안 그룹 설정 (Bastion Host에서의 접근 허용):**
- EC2 Console → Security Groups → oooo-myvpc-mysqldb-sg
- Inbound Rule 추가: Type MYSQL/Aurora (3306), Source: oooo-bastion-sg (Bastion 서버의 보안 그룹 ID)

**4. DB 접속 (Bastion Host를 통한 접속):**
- Bastion 서버에 SSH 접속 후 MySQL 클라이언트 설치
- **sudo yum install -y mysql**
- **mysql -h [RDS_ENDPOINT] -u admin -p** → RDS에 접속

---

### Aurora DB 클러스터 생성 실습

**1. Aurora DB 클러스터 생성 (MySQL 호환):**
- Engine: Aurora MySQL, Template: Dev/Test
- DB Cluster Identifier: oooo-aurora-mysql-test
- Instance Class: db.t3.medium
- Availability & Durability: Multi-AZ deployment (Aurora Replica/Reader 포함)

**2. 읽기 전용 복제본 확인:**
- 생성 완료 후 Console에서 **Writer** 인스턴스와 **Reader** 인스턴스 확인
- Writer Endpoint와 Reader Endpoint가 분리되어 있음 확인

**3. 장애 조치(Failover) 테스트:**
- Writer 인스턴스 선택 → Actions → Failover
- 결과: 기존 Reader가 Writer로 승격되고, 기존 Writer는 재부팅 후 Reader가 됨
- 애플리케이션은 Cluster Endpoint를 사용하므로 설정 변경 없이 자동 복구됨

---

### DynamoDB 실습

**1. 테이블 생성:**
- DynamoDB Console → Create table
- Table name: t-oooo-userinfo
- Partition key: id (String)
- Settings: Default settings (Provisioned mode)

**2. 아이템 생성 (Create Item):**
- Console → Tables → t-oooo-userinfo → Explore items → Create item
- 속성(Attributes) 추가:
  - id: "user01" (String)
  - name: "Hong" (String)
  - email: "hong@example.com" (String)

**3. 아이템 검색 방법 비교:**
- **Scan**: 테이블 전체를 스캔 (Filter로 조건 적용 가능하나 비용 높음)
- **Query**: Partition Key ("user01")를 지정하여 특정 데이터 직접 조회 (효율적)

---

## 3. 실무/보안 관점 분석

| 분야 | 시나리오 |
|:---:|:---|
| **DB 선택 전략** | **RDS**: 정형 데이터, 복잡한 조인 연산, 트랜잭션 관리가 필요한 기존 레거시 앱 마이그레이션. **Aurora**: 높은 처리량과 가용성이 요구되는 엔터프라이즈급 앱, 관리 포인트 최소화 필요 시. **DynamoDB**: 쇼핑몰 장바구니, 모바일 백엔드 등 대규모 트래픽과 유연한 스키마가 필요한 경우. |
| **콘텐츠 전송 최적화** | **CloudFront**: 정적 콘텐츠(이미지, CSS, JS) 캐싱으로 오리진 부하 감소 및 글로벌 전송 속도 향상. **Global Accelerator**: 게임, VoIP 등 비 HTTP 트래픽 가속화 및 고정 IP(Anycast IP)가 필요한 경우. |
| **보안 아키텍처** | **DB 보안**: RDS/Aurora는 반드시 Private Subnet에 배치, Bastion Host나 VPN/Direct Connect를 통해서만 관리 접근. Security Group으로 최소 권한(Port 3306)만 허용. **API 보안**: API Gateway와 WAF를 연동하여 DDoS 방어 및 SQL 인젝션 차단. API Key로 사용량 제어. |
| **데이터 마이그레이션** | **DMS (Database Migration Service)**: 무중단 DB 이관 지원. **SCT (Schema Conversion Tool)**: 이기종 DB(Oracle -> Aurora PostgreSQL 등) 마이그레이션 시 스키마 변환 자동화. |

---

## 4. 배운 점 및 심화 방향

- **배운 점**: Route 53은 단순 도메인 등록뿐 아니라 GSLB(Global Server Load Balancing) 역할을 수행하여 트래픽 관리의 핵심임. CloudFront와 S3 연동 시 OAC 설정은 필수적인 보안 모범 사례. RDS는 관리형이지만 인스턴스 타입 관리가 필요하고, Aurora는 클라우드 네이티브로 스토리지 자동 확장 및 고속 Failover를 지원. DynamoDB는 스키마리스(Schema-less) 구조로 개발 유연성을 제공하며, 서버리스로 운영 부담이 적음.
- **심화 방향**: Aurora Global Database(리전 간 복제 지연 시간 1초 미만, DR 아키텍처 구성), DynamoDB 모델링(파티션 키 및 정렬 키 설계 패턴, Single Table Design), Transit Gateway를 활용한 중앙 집중식 네트워크 구성, API Gateway + Lambda + DynamoDB를 연동한 완전한 서버리스 백엔드 구축.

---

## 5. Quick Reference

### RDS vs Aurora vs DynamoDB 비교

| 특성 | Amazon RDS | Amazon Aurora | Amazon DynamoDB |
|:---:|:---:|:---:|:---:|
| **유형** | 관계형 (RDBMS) | 관계형 (RDBMS) | 키-값 (NoSQL) |
| **호환성** | MySQL, PG, MariaDB, Oracle, SQL Server | MySQL, PostgreSQL | - |
| **스토리지** | EBS 볼륨 (용량 지정 필요) | 클러스터 볼륨 (자동 확장, 최대 128TB) | 무제한 |
| **가용성** | Multi-AZ (Standby 인스턴스) | 3 AZ에 6개 사본 저장 | 3 AZ 자동 복제 |
| **주요 용도** | 전통적 ERP, CRM, 웹 게시판 | 고성능 웹, SaaS, 엔터프라이즈 앱 | 모바일, 게임, IoT, 대규모 트래픽 |

### Route 53 라우팅 정책

| 정책 | 설명 | 사용 사례 |
|:---:|:---|:---|
| **단순 (Simple)** | 단일 리소스로 라우팅 | 단일 웹 서버 |
| **가중치 (Weighted)** | 지정 비율(%)로 분산 | A/B 테스트, 블루/그린 배포 |
| **지연 시간 (Latency)** | 지연 시간이 짧은 리전으로 라우팅 | 글로벌 서비스 성능 최적화 |
| **장애 조치 (Failover)** | 헬스 체크 기반 주/예비 전환 | DR (Active-Passive) 구성 |
| **지리적 위치 (Geolocation)** | 사용자 위치 기반 라우팅 | 지역별 콘텐츠 제한, 언어 설정 |
