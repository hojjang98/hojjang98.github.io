---
title: "2025.12.11 (Day 34) AWS 기타 서비스: 데이터 분석, 기계 학습, 시스템 관리"
date: 2025-12-11
draft: false
tags: ["AWS", "CloudWatch", "SystemsManager", "CloudFormation", "Athena", "데이터분석", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "AWS CloudWatch, Systems Manager, CloudFormation, Organizations, Kinesis, Athena 등 운영/분석 서비스 실습"
---

# 📄 2025.12.11 (Day 34) - AWS 기타 서비스: 데이터 분석, 기계 학습, 시스템 관리

---

## 1. 핵심 개념 정리

### 데이터 수집 및 분석 서비스

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 1 | Amazon Kinesis | 실시간 스트리밍 데이터 수집 및 처리 서비스. Data Streams(데이터 수집), Firehose(전송), Analytics(분석) 세 가지 구성요소 제공 | 실시간 로그 분석, 클릭스트림 분석에 활용. 보안 로그를 실시간으로 S3/OpenSearch로 전송하여 SIEM 구축 가능 |
| 2 | Amazon Athena | S3에 저장된 데이터를 표준 SQL로 직접 쿼리하는 서버리스 서비스. 별도 인프라 구축 없이 즉시 분석 가능 | CloudTrail, VPC Flow Logs를 S3에 저장 후 Athena로 쿼리하여 보안 분석. 스캔한 데이터량 기준 과금 |
| 3 | Amazon OpenSearch | Elasticsearch 기반 검색 및 분석 서비스. 로그 분석, 실시간 모니터링 대시보드 구축에 활용 | SIEM 구축의 핵심. CloudWatch Logs, Kinesis에서 로그를 수집하여 보안 이벤트 검색 및 시각화 |
| 4 | AWS Glue | 서버리스 ETL(추출, 변환, 적재) 서비스. 데이터 카탈로그 기능으로 데이터 레이크의 메타데이터 관리 | 여러 소스의 보안 로그를 표준 형식으로 변환하여 분석 용이하게 함. Athena와 연동하여 스키마 자동 검색 |
| 5 | Amazon QuickSight | 클라우드 기반 BI(Business Intelligence) 서비스. 대시보드 및 시각화 보고서 생성 | 보안 메트릭 대시보드 구축. 경영진 보고용 보안 현황 리포트 자동 생성 |

### 기계 학습 서비스

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 6 | Amazon SageMaker | 머신러닝 모델을 구축, 학습, 배포하는 완전 관리형 플랫폼. Jupyter 노트북 환경 제공 | 이상 탐지 모델 학습, 악성코드 분류 모델 개발에 활용. 보안 분석가도 AutoML 기능으로 ML 모델 구축 가능 |
| 7 | Amazon Rekognition | 이미지 및 비디오 분석 서비스. 얼굴 인식, 객체 탐지, 텍스트 추출 기능 제공 | 출입 통제 시스템, CCTV 영상 분석에 활용. 부적절한 콘텐츠 자동 탐지 |
| 8 | Amazon Comprehend | 자연어 처리(NLP) 서비스. 텍스트에서 감정, 핵심 구문, 개체 추출 | 피싱 이메일 탐지, 고객 피드백 분석, 문서 분류 자동화에 활용 |
| 9 | Amazon Lex | 챗봇 구축 서비스. 음성 및 텍스트 기반 대화형 인터페이스 생성 | IT 헬프데스크 챗봇, 보안 인시던트 접수 자동화에 활용 |
| 10 | Amazon Polly | 텍스트를 자연스러운 음성으로 변환하는 서비스. 다양한 언어 및 음성 지원 | 접근성 향상, 알림 음성 안내 시스템 구축 |
| 11 | Amazon Transcribe | 음성을 텍스트로 변환하는 서비스. 실시간 및 배치 변환 지원 | 콜센터 통화 녹음 분석, 회의록 자동 생성 |
| 12 | Amazon Translate | 기계 번역 서비스. 다국어 콘텐츠 실시간 번역 | 글로벌 서비스 다국어 지원, 외국어 위협 인텔리전스 분석 |
| 13 | Amazon Fraud Detector | 머신러닝 기반 사기 탐지 서비스. 온라인 결제, 계정 탈취 등 부정 행위 탐지 | 이상 로그인 탐지, 결제 사기 방지에 활용 |

### AWS 시스템 관리 서비스

| # | 핵심 개념 | 설명 | 실무/보안 관점 |
|:---:|:---|:---|:---|
| 14 | AWS Systems Manager | EC2 및 온프레미스 서버를 통합 관리하는 서비스. Session Manager, Patch Manager, Parameter Store 등 다양한 기능 제공 | SSH 키 없이 EC2 접속(Session Manager), 패치 자동화, 민감 정보 안전한 저장(Parameter Store) |
| 15 | Amazon CloudWatch | AWS 리소스 모니터링 및 로그 관리 서비스. 메트릭 수집, 알람 설정, 대시보드 생성 기능 제공 | 보안 메트릭 모니터링, 임계치 초과 시 SNS 알림. 로그 기반 메트릭 필터로 보안 이벤트 탐지 |
| 16 | AWS CloudFormation | 인프라를 코드로 관리(IaC)하는 서비스. YAML/JSON 템플릿으로 AWS 리소스 프로비저닝 자동화 | 보안 구성을 코드로 표준화. 드리프트 탐지로 수동 변경 감지. 변경 세트로 배포 전 영향 분석 |
| 17 | AWS Organizations | 여러 AWS 계정을 중앙에서 관리. OU(조직 단위) 구성, SCP(서비스 제어 정책)로 권한 제한 | 멀티 계정 보안 거버넌스. SCP로 특정 서비스/리전 사용 금지. 통합 결제로 비용 관리 |
| 18 | AWS Trusted Advisor | AWS 환경을 자동으로 점검하여 비용 최적화, 성능, 보안, 내결함성 권장사항 제공 | 보안 그룹 오픈 포트, 미사용 IAM 키, MFA 미설정 등 보안 취약점 자동 탐지 |

---

## 2. 실습 코드 정리

### 실습 21: CloudWatch 경보 만들기

SNS Topic 생성 및 이메일 구독:

```bash
# 1. SNS Topic 생성
aws sns create-topic --name oooo-SecurityNotices

# 2. 이메일 구독 추가 (이메일로 확인 링크 발송됨)
aws sns subscribe \
  --topic-arn arn:aws:sns:ap-northeast-2:123456789012:oooo-SecurityNotices \
  --protocol email \
  --notification-endpoint your-email@example.com

# 3. 구독 확인 (이메일에서 Confirm subscription 클릭 후)
aws sns list-subscriptions-by-topic \
  --topic-arn arn:aws:sns:ap-northeast-2:123456789012:oooo-SecurityNotices
```

CloudWatch Alarm 생성:

```bash
# EC2 CPU 사용률 기반 경보 생성
aws cloudwatch put-metric-alarm \
  --alarm-name oooo-bastion-cpu-util \
  --alarm-description "Bastion server CPU utilization exceeds 60%" \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 60 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=InstanceId,Value=i-0instanceid \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:ap-northeast-2:123456789012:oooo-SecurityNotices \
  --treat-missing-data notBreaching

# 경보 상태 확인
aws cloudwatch describe-alarms --alarm-names oooo-bastion-cpu-util
```

CPU 부하 테스트:

```bash
# EC2 인스턴스에 접속 후 stress 패키지 설치
sudo yum -y install stress

# 600초(10분) 동안 CPU 부하 발생
sudo stress --timeout 600 --cpu 1

# 더 높은 부하가 필요한 경우
sudo stress --timeout 60 --cpu 4 --vm 4 --vm-bytes 1024m --hdd 1 --hdd-bytes 1024m
```

### CloudWatch 로그 기반 메트릭 필터 (보안 활용)

```bash
# Root 로그인 탐지 메트릭 필터 생성
aws logs put-metric-filter \
  --log-group-name CloudTrail/logs \
  --filter-name RootAccountUsage \
  --filter-pattern '{ $.userIdentity.type = "Root" && $.userIdentity.invokedBy NOT EXISTS && $.eventType != "AwsServiceEvent" }' \
  --metric-transformations \
    metricName=RootAccountUsageCount,metricNamespace=SecurityMetrics,metricValue=1

# 메트릭 기반 경보 생성
aws cloudwatch put-metric-alarm \
  --alarm-name RootAccountUsageAlarm \
  --metric-name RootAccountUsageCount \
  --namespace SecurityMetrics \
  --statistic Sum \
  --period 300 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 1 \
  --alarm-actions arn:aws:sns:ap-northeast-2:123456789012:oooo-SecurityNotices
```

### Systems Manager Session Manager 활용

```bash
# Session Manager로 EC2 접속 (SSH 키 불필요)
aws ssm start-session --target i-0instanceid

# 명령 실행 (Run Command)
aws ssm send-command \
  --instance-ids i-0instanceid \
  --document-name "AWS-RunShellScript" \
  --parameters 'commands=["df -h","free -m"]'

# Parameter Store에 민감 정보 저장
aws ssm put-parameter \
  --name "/myapp/database/password" \
  --value "MySecurePassword123" \
  --type SecureString

# Parameter Store에서 값 조회
aws ssm get-parameter \
  --name "/myapp/database/password" \
  --with-decryption
---  
## 3. 서비스 분류 및 비교  
### 데이터 분석 파이프라인 구성  
| 단계 | 서비스 | 역할 |  
|:---:|:---|:---|  
| 수집 | Kinesis Data Streams, Kinesis Firehose | 실시간 스트리밍 데이터 수집 |  
| 저장 | S3, OpenSearch | 원본 데이터 저장 및 인덱싱 |  
| 변환 | Glue, Lambda | ETL 처리, 데이터 정규화 |  
| 분석 | Athena, OpenSearch | SQL 쿼리, 전문 검색 |  
| 시각화 | QuickSight, OpenSearch Dashboards | 대시보드, 리포트 생성 |  
### ML 서비스 선택 가이드  
| 요구사항 | 추천 서비스 | 비고 |  
|:---:|:---|:---|  
| 커스텀 모델 학습 필요 | SageMaker | 전체 ML 파이프라인 지원 |  
| 이미지/비디오 분석 | Rekognition | 사전 학습된 모델 즉시 사용 |  
| 텍스트 분석 | Comprehend | 감정 분석, 개체 인식 |  
| 음성 → 텍스트 | Transcribe | 실시간/배치 변환 |  
| 텍스트 → 음성 | Polly | 다국어 음성 합성 |  
| 챗봇 구축 | Lex | Alexa와 동일 기술 |  
| 사기 탐지 | Fraud Detector | 결제/계정 부정 행위 탐지 |  
### 시스템 관리 서비스 활용  
| 서비스 | 주요 기능 | 보안 활용 사례 |  
|:---:|:---|:---|  
| Systems Manager | 통합 관리 플랫폼 | Session Manager로 SSH 키 없이 접속, Patch Manager로 보안 패치 자동화 |  
| CloudWatch | 모니터링 및 알람 | 비정상 메트릭 탐지 시 SNS 알림, 로그 기반 보안 이벤트 탐지 |  
| CloudFormation | IaC | 보안 구성 표준화, 드리프트 탐지로 수동 변경 감지 |  
| Organizations | 멀티 계정 관리 | SCP로 보안 정책 강제, 통합 CloudTrail 설정 |  
| Trusted Advisor | 자동 점검 | 보안 그룹 오픈 포트, IAM 취약점 자동 탐지 |  
---  
## 4. 실무/보안 관점 분석  
| 분야 | 시나리오 |  
|:---:|:---|  
| 보안 로그 분석 파이프라인 | CloudTrail/VPC Flow Logs → S3 저장 → Athena로 SQL 쿼리 또는 Kinesis Firehose → OpenSearch로 실시간 분석. QuickSight로 보안 대시보드 구축 |  
| 실시간 위협 탐지 | Kinesis Data Streams로 로그 실시간 수집 → Lambda로 패턴 매칭 → 의심 이벤트 SNS 알림. 또는 OpenSearch에서 실시간 쿼리 |  
| ML 기반 이상 탐지 | CloudWatch 메트릭을 SageMaker로 학습하여 이상 패턴 탐지 모델 구축. 또는 GuardDuty의 ML 기반 탐지 활용 |  
| 시스템 보안 강화 | Session Manager로 SSH 포트(22) 닫기, Patch Manager로 보안 패치 자동 적용, Parameter Store로 비밀번호 안전 관리 |  
| 멀티 계정 보안 거버넌스 | Organizations + SCP로 전 계정에 보안 정책 강제. Security Hub로 모든 계정의 보안 현황 통합 모니터링 |  
---  
## 5. 배운 점 및 심화 방향  
### 배운 점  
- AWS는 데이터 수집부터 분석, 시각화까지 전체 파이프라인을 서버리스로 구축 가능. Kinesis + S3 + Athena 조합으로 비용 효율적인 로그 분석 환경 구성  
- ML 서비스는 사전 학습된 모델을 API로 호출하는 방식이라 ML 전문 지식 없이도 활용 가능. Rekognition, Comprehend 등은 즉시 사용 가능  
- Systems Manager의 Session Manager는 SSH 키 관리 부담을 없애고 CloudTrail에 세션 로그를 남겨 감사 추적 용이. 보안 관점에서 SSH 포트를 열지 않아도 됨  
- CloudWatch는 단순 모니터링을 넘어 로그 기반 메트릭 필터로 보안 이벤트 탐지 가능. Root 로그인, 보안 그룹 변경 등 중요 이벤트 실시간 알림 구성  
### 심화 방향  
- SIEM 구축: CloudTrail + VPC Flow Logs + GuardDuty → Kinesis Firehose → OpenSearch로 통합 보안 모니터링 대시보드 구축  
- 자동 대응: CloudWatch Alarm → SNS → Lambda → 보안 그룹 자동 차단 또는 인스턴스 격리 파이프라인  
- IaC 보안: CloudFormation 템플릿에 보안 모범 사례 적용, cfn-lint로 템플릿 검증, StackSets로 멀티 계정 배포  
- Athena 보안 쿼리: CloudTrail 로그에서 비정상 API 호출 패턴 쿼리 라이브러리 구축  
---  
## 6. Quick Reference  
### CloudWatch 주요 메트릭  
| 네임스페이스 | 메트릭 | 설명 |  
|:---:|:---|:---|  
| AWS/EC2 | CPUUtilization | CPU 사용률(%) |  
| AWS/EC2 | NetworkIn/Out | 네트워크 트래픽(바이트) |  
| AWS/EBS | VolumeReadOps | 볼륨 읽기 작업 수 |  
| AWS/RDS | DatabaseConnections | DB 연결 수 |  
| AWS/Lambda | Invocations | 함수 호출 수 |  
| AWS/Lambda | Errors | 함수 오류 수 |  
| AWS/ALB | RequestCount | 요청 수 |  
| AWS/ALB | TargetResponseTime | 응답 시간 |  
### Systems Manager 주요 기능  
| 기능 | 설명 | 보안 활용 |  
|:---:|:---|:---|  
| Session Manager | 브라우저/CLI로 EC2 접속 | SSH 포트 닫기, 세션 로깅 |  
| Run Command | 원격 명령 실행 | 대규모 서버 점검 스크립트 |  
| Patch Manager | OS 패치 자동화 | 보안 패치 일괄 적용 |  
| Parameter Store | 설정값/비밀 저장 | DB 비밀번호 안전 관리 |  
| Inventory | 소프트웨어 인벤토리 | 설치된 SW 현황 파악 |  
| State Manager | 원하는 상태 유지 | 보안 설정 강제 적용 |  
### Athena CloudTrail 쿼리 예제  
sql
-- 최근 24시간 Root 계정 활동 조회
SELECT eventTime, eventName, sourceIPAddress, userAgent
FROM cloudtrail_logs
WHERE userIdentity.type = 'Root'
  AND eventTime > date_add('hour', -24, now())
ORDER BY eventTime DESC;

-- 특정 S3 버킷 접근 기록 조회
SELECT eventTime, userIdentity.userName, eventName, requestParameters
FROM cloudtrail_logs
WHERE eventSource = 's3.amazonaws.com'
  AND requestParameters LIKE '%bucket-name%'
ORDER BY eventTime DESC
LIMIT 100;

-- 실패한 API 호출 조회
SELECT eventTime, eventName, errorCode, errorMessage, userIdentity.userName
FROM cloudtrail_logs
WHERE errorCode IS NOT NULL
ORDER BY eventTime DESC
LIMIT 50;
```

### 비용 최적화 팁

| 서비스 | 비용 최적화 방법 |
|:---:|:---|
| Athena | 파티셔닝 적용, 컬럼 기반 형식(Parquet) 사용으로 스캔량 감소 |
| CloudWatch | 불필요한 상세 모니터링 비활성화, 로그 보관 기간 설정 |
| Kinesis | 샤드 수 적절히 조절, 필요시 Firehose 버퍼링 활용 |
| OpenSearch | 인스턴스 크기 최적화, UltraWarm으로 오래된 데이터 이동 |
| SageMaker | 스팟 인스턴스 활용, 사용 안 할 때 노트북 중지 |

### AWS 서비스 약어 정리

| 약어 | 전체 명칭 | 설명 |
|:---:|:---|:---|
| SSM | Systems Manager | 시스템 통합 관리 |
| SNS | Simple Notification Service | 알림 서비스 |
| SQS | Simple Queue Service | 메시지 큐 |
| SES | Simple Email Service | 이메일 서비스 |
| ETL | Extract, Transform, Load | 데이터 추출/변환/적재 |
| IaC | Infrastructure as Code | 코드형 인프라 |
| BI | Business Intelligence | 비즈니스 인텔리전스 |
| NLP | Natural Language Processing | 자연어 처리 |
