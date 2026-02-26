---
title: "2025.12.10 (Day 33) AWS 보안 서비스: Shield, WAF, GuardDuty, Config"
date: 2025-12-10
draft: false
tags: ["AWS", "보안", "WAF", "GuardDuty", "CloudTrail", "Shield", "Config", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "AWS Shield, WAF, GuardDuty, Config, CloudTrail, VPC Flow Logs를 활용한 클라우드 보안 실습"
---

# 📄 2025.12.10 (Day 33) - AWS 보안 서비스: Shield, WAF, GuardDuty, Config

---

## 1. 핵심 개념 정리

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 1 | AWS 공동 책임 모델 | AWS는 클라우드 자체의 보안(물리적 인프라, 하이퍼바이저 등)을 담당하고, 고객은 클라우드 내부의 보안(데이터, IAM, OS 패치 등)을 담당하는 보안 책임 분담 모델 | 서비스별로 책임 범위가 다름. EC2는 OS 패치까지 고객 책임, Lambda는 코드만 고객 책임. 책임 범위를 명확히 이해해야 보안 사각지대 방지 |
| 2 | AWS CloudTrail | AWS 계정의 모든 API 호출을 기록하는 감사 로깅 서비스. 누가, 언제, 어떤 작업을 수행했는지 추적 가능. 기본 90일 보관, S3로 장기 보관 가능 | SOC 운영의 핵심 데이터 소스. 보안 사고 조사, 규정 준수 감사에 필수. 모든 리전에서 Trail 활성화하고 S3에 중앙 집중 저장 권장 |
| 3 | VPC Flow Logs | VPC 내 네트워크 인터페이스(ENI)를 오가는 IP 트래픽 정보를 캡처하는 로그. 소스/목적지 IP, 포트, 프로토콜, 허용/거부 여부 기록 | 네트워크 이상 탐지, 보안 그룹 규칙 검증에 활용. CloudWatch Logs나 S3에 저장. 침해 사고 시 네트워크 포렌식의 핵심 자료 |
| 4 | AWS WAF | 웹 애플리케이션 방화벽. SQL Injection, XSS 등 웹 공격으로부터 ALB, CloudFront, API Gateway 보호. 사용자 정의 규칙 및 AWS 관리형 규칙 제공 | OWASP Top 10 공격 방어에 필수. IP 기반 차단/허용(Black/White List), Rate Limiting, Geo Blocking 가능. CloudWatch로 공격 패턴 모니터링 |
| 5 | AWS Shield | DDoS 공격으로부터 AWS 리소스를 보호하는 서비스. Standard는 무료로 기본 제공, Advanced는 유료로 고급 보호 및 24/7 DDoS 대응팀 지원 | Shield Standard는 모든 AWS 고객에게 자동 적용(L3/L4 공격 방어). Advanced는 대규모 서비스, 금융권에서 사용. WAF와 함께 사용 권장 |
| 6 | AWS GuardDuty | 머신러닝 기반 위협 탐지 서비스. CloudTrail, VPC Flow Logs, DNS 로그를 분석하여 악성 활동, 무단 접근, 암호화폐 채굴 등 탐지 | 에이전트 설치 없이 클릭 한 번으로 활성화. 탐지된 위협을 심각도(Low/Medium/High)로 분류. EventBridge로 자동 대응 구성 가능 |
| 7 | AWS Config | AWS 리소스 구성 변경을 지속적으로 기록하고 평가하는 서비스. 규정 준수 규칙(Config Rules)으로 구성 상태 자동 점검 | S3 퍼블릭 접근 여부, 암호화 활성화 여부 등 보안 기준 준수 자동 검사. 비준수 리소스 자동 알림 또는 자동 수정(Remediation) 가능 |
| 8 | AWS Security Hub | 여러 AWS 보안 서비스(GuardDuty, Inspector, Config 등)의 결과를 중앙에서 집계하고 우선순위화. CIS, PCI DSS 등 보안 표준 기반 점검 | SOC 대시보드로 활용. 멀티 계정 환경에서 보안 현황 통합 관리. 자동화된 보안 점검 및 규정 준수 보고서 생성 |

---

## 2. 실습 코드 정리

### 실습 19: AWS 로그 수집 (VPC Flow Logs + CloudTrail)

VPC Flow Logs 설정:

```bash
# 1. CloudWatch Log Group 생성
aws logs create-log-group \
  --log-group-name oooo-myvpc-flowlogs

# 2. Flow Logs용 IAM Role 생성 (Trust Policy: vpc-flow-logs.amazonaws.com)
# CloudWatchLogsFullAccess 정책 연결 필요

# 3. VPC Flow Logs 활성화
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-0abcdef1234567890 \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name oooo-myvpc-flowlogs \
  --deliver-logs-permission-arn arn:aws:iam::123456789012:role/oooo-CloudWatchLogs-Role

# 4. Flow Logs 조회 (특정 ENI 또는 IP로 필터링)
aws logs filter-log-events \
  --log-group-name oooo-myvpc-flowlogs \
  --filter-pattern "eni-0abcdef"
```

VPC Flow Log 레코드 형식:

```
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status
```

CloudTrail 조회:

```bash
# 최근 API 이벤트 조회
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=PutBucketPolicy \
  --max-results 10

# S3로 Trail 로그 장기 보관 설정
aws cloudtrail create-trail \
  --name oooo-security-trail \
  --s3-bucket-name oooo-cloudtrail-logs \
  --is-multi-region-trail \
  --enable-log-file-validation
```

### 실습 20: WAF를 이용한 웹서비스 보호

IP Set 생성 및 WebACL 구성:

```bash
# 1. IP Set 생성 (Black List)
aws wafv2 create-ip-set \
  --name oooo-BlackList \
  --scope REGIONAL \
  --ip-address-version IPV4 \
  --addresses "203.0.113.0/32" "198.51.100.0/24"

# 2. IP Set 생성 (White List)
aws wafv2 create-ip-set \
  --name oooo-WhiteList \
  --scope REGIONAL \
  --ip-address-version IPV4 \
  --addresses "내PC공인IP/32"

# 3. WebACL 생성 및 ALB 연결
aws wafv2 create-web-acl \
  --name oooo-waf-webACL \
  --scope REGIONAL \
  --default-action Allow={} \
  --rules '[
    {
      "Name": "BlockBlackListIPs",
      "Priority": 1,
      "Statement": {
        "IPSetReferenceStatement": {
          "ARN": "arn:aws:wafv2:region:account:regional/ipset/oooo-BlackList/id"
        }
      },
      "Action": { "Block": {} },
      "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "BlockBlackListIPs"
      }
    }
  ]'

# 4. WebACL을 ALB에 연결
aws wafv2 associate-web-acl \
  --web-acl-arn arn:aws:wafv2:region:account:regional/webacl/oooo-waf-webACL/id \
  --resource-arn arn:aws:elasticloadbalancing:region:account:loadbalancer/app/oooo-web-alb/id
```

WAF 규칙 우선순위:

- 숫자가 낮을수록 먼저 평가
- White List를 Black List보다 높은 우선순위로 설정하면 허용 목록 우선 적용

### 실습 21: CloudWatch 경보 만들기

SNS Topic 및 CloudWatch Alarm 설정:

```bash
# 1. SNS Topic 생성
aws sns create-topic --name oooo-SecurityNotices

# 2. 이메일 구독 추가
aws sns subscribe \
  --topic-arn arn:aws:sns:ap-northeast-2:123456789012:oooo-SecurityNotices \
  --protocol email \
  --notification-endpoint your-email@example.com

# 3. CloudWatch Alarm 생성 (CPU 사용률 기반)
aws cloudwatch put-metric-alarm \
  --alarm-name oooo-bastion-cpu-util \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 60 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=InstanceId,Value=i-0instanceid \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:ap-northeast-2:123456789012:oooo-SecurityNotices

# 4. CPU 부하 테스트 (EC2 내부에서)
sudo yum -y install stress
sudo stress --timeout 600 --cpu 1
```

---

## 3. AWS 보안 서비스 비교

### 탐지 및 모니터링 서비스

| 서비스 | 주요 기능 | 데이터 소스 | 사용 사례 |
|:---:|:---|:---|:---|
| CloudTrail | API 호출 감사 로깅 | AWS API 호출 | 누가 S3 버킷 삭제했는지 추적 |
| VPC Flow Logs | 네트워크 트래픽 로깅 | ENI 트래픽 | 비정상 아웃바운드 트래픽 탐지 |
| GuardDuty | 위협 탐지(ML 기반) | CloudTrail, Flow Logs, DNS | 암호화폐 채굴, 무단 API 호출 탐지 |
| CloudWatch | 메트릭 모니터링, 알람 | AWS 리소스 메트릭 | CPU 급증 시 알림 발송 |
| Security Hub | 보안 결과 통합 대시보드 | GuardDuty, Config, Inspector | 전체 보안 현황 한눈에 파악 |

### 방어 서비스

| 서비스 | 방어 대상 | 계층 | 비용 |
|:---:|:---|:---|:---|
| Shield Standard | L3/L4 DDoS | 네트워크/전송 | 무료 (기본 제공) |
| Shield Advanced | L3/L4/L7 DDoS | 전 계층 | 월 $3,000 + 데이터 전송 |
| WAF | 웹 공격 (SQLi, XSS) | 애플리케이션(L7) | 규칙당 과금 |
| Network Firewall | VPC 트래픽 필터링 | 네트워크(L3/L4) | 시간당 + 데이터 처리량 |
| Firewall Manager | 다중 계정 방화벽 정책 관리 | 관리 계층 | WAF/Shield 정책당 과금 |

### 규정 준수 서비스

| 서비스 | 주요 기능 | 점검 대상 |
|:---:|:---|:---|
| Config | 리소스 구성 변경 추적, 규칙 기반 평가 | S3 암호화, 보안 그룹 설정 등 |
| Config Rules | 리소스가 규정 준수하는지 자동 점검 | CIS Benchmark, 사용자 정의 규칙 |
| Audit Manager | 감사 증거 자동 수집 | SOC 2, PCI DSS, GDPR |
| Artifact | AWS 규정 준수 보고서 다운로드 | ISO, SOC, PCI 인증서 |

---

## 4. 실무/보안 관점 분석

| 분야 | 시나리오 |
|:---:|:---|
| 로그 수집 전략 | CloudTrail은 모든 리전에서 활성화하고 S3에 중앙 집중 저장. VPC Flow Logs는 주요 VPC에 활성화. 로그 보관 기간은 규정 준수 요건에 따라 설정(최소 1년 권장) |
| 위협 탐지 구성 | GuardDuty를 모든 리전에서 활성화. 탐지된 위협은 EventBridge로 Lambda 트리거하여 자동 대응(예: 보안 그룹 차단). Security Hub로 결과 통합 |
| 웹 보안 구성 | ALB 앞에 WAF 배치. AWS 관리형 규칙(AWSManagedRulesCommonRuleSet) 적용. Rate Limiting으로 DDoS 완화. CloudFront 사용 시 Shield Advanced 고려 |
| 규정 준수 자동화 | Config Rules로 보안 기준 자동 점검. 비준수 리소스는 SNS로 알림 또는 SSM Automation으로 자동 수정. Security Hub에서 CIS Benchmark 점수 모니터링 |
| 사고 대응 프로세스 | GuardDuty 알림 수신 → CloudTrail에서 관련 API 조회 → VPC Flow Logs에서 네트워크 활동 확인 → 영향 받은 리소스 격리 → 포렌식 분석 |

---

## 5. 배운 점 및 심화 방향

### 배운 점

- AWS 보안은 단일 서비스가 아닌 여러 서비스의 조합으로 구성됨. 로깅(CloudTrail, Flow Logs), 탐지(GuardDuty), 방어(WAF, Shield), 규정 준수(Config)를 계층적으로 적용해야 함
- GuardDuty는 에이전트 설치 없이 기존 로그를 분석하여 위협을 탐지하므로 도입 장벽이 낮음. SOC 운영 시 1차 위협 탐지 도구로 활용 가능
- WAF의 IP Set을 활용한 Black/White List 관리는 간단하지만 효과적. 규칙 우선순위 설정이 중요하며, White List를 먼저 평가하도록 구성해야 함
- VPC Flow Logs는 네트워크 포렌식의 핵심. 침해 사고 시 어떤 IP와 통신했는지, 어떤 포트가 사용됐는지 추적 가능

### 심화 방향

- GuardDuty 자동 대응: EventBridge + Lambda로 High Severity 탐지 시 자동으로 보안 그룹 차단하는 파이프라인 구축
- WAF 로그 분석: WAF 로그를 S3에 저장하고 Athena로 쿼리하여 공격 패턴 분석
- Config 자동 수정: 비준수 S3 버킷 발견 시 자동으로 퍼블릭 접근 차단하는 Remediation 구성
- SIEM 연동: CloudTrail, GuardDuty 로그를 OpenSearch(Elasticsearch)로 전송하여 통합 보안 모니터링

---

## 6. Quick Reference

### CloudTrail 주요 모니터링 이벤트

| 이벤트 | 의미 | 위험도 |
|:---:|:---|:---:|
| ConsoleLogin | 콘솔 로그인 (특히 Root 계정) | 높음 |
| CreateUser / CreateAccessKey | IAM 사용자/키 생성 | 높음 |
| StopLogging | CloudTrail 로깅 중지 | 높음 |
| AuthorizeSecurityGroupIngress | 보안 그룹 인바운드 규칙 추가 | 중간 |
| PutBucketPolicy | S3 버킷 정책 변경 | 높음 |
| DeleteTrail | CloudTrail 삭제 | 높음 |

### GuardDuty 주요 탐지 유형

| Finding Type | 설명 | 심각도 |
|:---:|:---|:---:|
| UnauthorizedAccess:IAMUser/ConsoleLoginSuccess.B | 비정상 위치에서 콘솔 로그인 | Medium |
| Recon:EC2/PortProbeUnprotectedPort | EC2 포트 스캔 탐지 | Low |
| CryptoCurrency:EC2/BitcoinTool.B | 암호화폐 채굴 활동 탐지 | High |
| Trojan:EC2/DNSDataExfiltration | DNS를 통한 데이터 유출 | High |
| UnauthorizedAccess:EC2/SSHBruteForce | SSH 무차별 대입 공격 | Low/Medium |

### WAF 관리형 규칙 그룹

| 규칙 그룹 | 방어 대상 |
|:---:|:---|
| AWSManagedRulesCommonRuleSet | OWASP Top 10 일반 공격 |
| AWSManagedRulesSQLiRuleSet | SQL Injection |
| AWSManagedRulesKnownBadInputsRuleSet | 알려진 악성 입력 패턴 |
| AWSManagedRulesAmazonIpReputationList | AWS 위협 인텔리전스 기반 IP 차단 |
| AWSManagedRulesBotControlRuleSet | 봇 트래픽 제어 |

### Config 주요 관리형 규칙

| 규칙 | 점검 내용 |
|:---:|:---|
| s3-bucket-public-read-prohibited | S3 퍼블릭 읽기 접근 금지 |
| s3-bucket-ssl-requests-only | S3 HTTPS 전용 접근 |
| encrypted-volumes | EBS 볼륨 암호화 여부 |
| iam-root-access-key-check | Root 계정 액세스 키 존재 여부 |
| vpc-flow-logs-enabled | VPC Flow Logs 활성화 여부 |
| cloudtrail-enabled | CloudTrail 활성화 여부 |

### 보안 서비스 활성화 우선순위

| 순위 | 서비스 | 이유 |
|:---:|:---|:---|
| 1 | CloudTrail | 모든 보안 조사의 기본 데이터 |
| 2 | GuardDuty | 원클릭 활성화, 즉시 위협 탐지 시작 |
| 3 | Config | 리소스 구성 변경 추적 및 규정 준수 |
| 4 | Security Hub | 보안 결과 통합 및 대시보드 |
| 5 | WAF | 웹 애플리케이션 보호 (ALB 사용 시) |
