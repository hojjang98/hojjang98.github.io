---
title: "Azure Blob Storage를 악용한 HTML Smuggling 피싱 캠페인"
date: 2025-12-28
categories: ["security-issues-analysis"]
tags: ["HTMLSmuggling", "AzureBlobStorage", "피싱캠페인", "클라우드악용", "LogoKit", "Microsoft"]
draft: false
summary: "Microsoft Azure Blob Storage를 악용한 HTML Smuggling 기법의 대규모 피싱 캠페인 분석"
---

# Azure Blob Storage를 악용한 HTML Smuggling 피싱 캠페인

## 기사 정보
- **출처**: ANY.RUN Cybersecurity Blog, Cybersecurity News
- **작성일**: 2024-12 (캠페인 발견 시기)
- **링크**: 
  - https://any.run/cybersecurity-blog/cyber-attacks-december-2024/
  - https://cybersecuritynews.com/cyber-attacks-in-december-2024/
- **카테고리**: 피싱/클라우드 악용/자격증명 탈취

---

## 핵심 요약
> 2024년 12월, 공격자들이 Microsoft Azure Blob Storage 서비스를 악용하여 HTML Smuggling 기법을 사용한 대규모 피싱 캠페인을 전개했다. *.blob.core.windows.net 서브도메인을 통해 피싱 페이지를 호스팅함으로써 Microsoft의 신뢰받는 인프라와 유효한 TLS 인증서를 활용해 보안 필터를 우회했다. 이 캠페인은 OneDrive, Microsoft Dynamics 365 등 다양한 Microsoft 서비스로 확장되었다.

---

## 사건/이슈 배경

### 무슨 일이 일어났는가?

**공격 개요:**
2024년 12월, ANY.RUN 보안 연구팀은 Microsoft의 Azure Blob Storage 서비스를 악용한 정교한 피싱 캠페인을 발견했다. 공격자들은 Microsoft의 공식 클라우드 인프라를 이용해 가짜 로그인 페이지를 호스팅하고, HTML Smuggling 기법을 사용하여 사용자 자격증명을 탈취했다.

**공격 확산:**
이 공격은 여러 Microsoft 서비스로 확장되었다:

1. **Azure Blob Storage 피싱**
   - *.blob.core.windows.net 서브도메인 악용
   - HTML Smuggling 기법 사용
   - 짧은 수명의 피싱 페이지로 탐지 회피

2. **OneDrive HTML Blob Smuggling**
   - OneDrive에 미끼 배치
   - 피해자를 악성 페이지로 리다이렉트
   - IPFS에 웹사이트 디자인 저장

3. **Microsoft Dynamics 365 웹 폼 악용**
   - *.microsoft.com 서브도메인에 악성 링크 삽입
   - 정상적인 Microsoft 서비스로 위장

4. **LogoKit 피싱 도구 사용**
   - 타겟 웹사이트의 로고 및 스크린샷 활용
   - Cloudflare Pages에 실제 피싱 페이지 호스팅

### 누가 관련되었는가?

- **공격자/위협 주체**: 
  - 신원 미상의 사이버 범죄 조직
  - 정교한 피싱 도구(LogoKit) 사용
  
- **피해자/영향 받은 대상**: 
  - Microsoft 서비스 사용자
  - Office 365, OneDrive 사용자
  - 기업 사용자 (Microsoft Dynamics 365 사용 조직)
  
- **기타 관련 당사자**: 
  - ANY.RUN 보안 연구팀 (캠페인 발견 및 분석)
  - Microsoft (악용된 인프라 제공자)

---

## 원인 분석

### 기술적 원인

**1. Azure Blob Storage의 퍼블릭 액세스 설정**

Azure Blob Storage는 기본적으로 익명 액세스를 허용하도록 설정할 수 있다. 공격자들은 이를 악용하여:
- 퍼블릭 컨테이너 생성
- HTML 피싱 페이지 업로드
- *.blob.core.windows.net 도메인을 통해 배포

**2. HTML Smuggling 기법**

피싱 페이지의 특징:
- HTML 문서에 "doom"이라는 ID를 가진 block input 요소 포함
- JScript를 사용하여 피해자의 시스템 정보 수집
  ```javascript
  window.navigator.platform // OS 식별
  window.navigator.userAgent // 브라우저 탐지
  ```
- 수집된 정보로 페이지의 신뢰성 증대

**3. 다단계 리다이렉션 체계**

**OneDrive 공격 사례:**
- OneDrive에 미끼 링크 배치
- 클릭 시 HTML Blob Smuggling 코드가 포함된 메인 페이지로 리다이렉트
- 자격증명 입력 후 정상 웹사이트로 재리다이렉트
- ANY.RUN의 MITM 기능으로 base.js 추출 및 디코딩

**LogoKit 공격 체계:**
- 디코더-리다이렉터 도메인 사용 (예: asiangrocers[.]store)
- 실제 피싱 콘텐츠는 Cloudflare Pages에 호스팅
- 회사 로고: logo.clearbit[.]com/<Domain>에서 가져옴
- 배경 이미지: thum[.]io/get/width/<DPI>/https://<Domain>에서 생성

**4. 데이터 탈취 메커니즘**

- 자격증명을 HTTP POST 요청으로 C2 서버에 전송
- 파라미터: `fox=&con=`
- 수집 서비스: nocodeform[.]io 활용
- 웹사이트 디자인: IPFS에 저장
- 유인 이미지: imgur.com에 호스팅

**5. 분석 회피 기술**

- 랜덤 10자 이름의 3개 스크립트 사용
  - assets/js/e0nt7h8uiw[.]js
  - assets/js/vddq2ozyod[.]js
  - assets/js/j3046eqymn[.]js
- 페이지 분석 방해 및 데이터 전송 역할

### 관리적/절차적 원인

**Microsoft 인프라의 신뢰성 악용:**
- Microsoft 소유 도메인에 대한 높은 신뢰도
- 유효한 TLS 인증서로 인한 브라우저 경고 부재
- URL 및 인증서 기반 필터링 우회

**클라우드 서비스 설정 관리 부재:**
- 퍼블릭 컨테이너에 대한 모니터링 부족
- 익명 액세스 변경 사항 추적 미흡
- Storage Account 정기 감사 부재

**짧은 페이지 수명 전략:**
- 피싱 페이지를 짧은 시간 동안만 운영
- 최소한의 악성 콘텐츠로 탐지 회피
- 탐지 후 신속한 제거로 분석 방해

### 인적 원인

**사용자의 신뢰 악용:**
- Microsoft 도메인에 대한 무조건적 신뢰
- *.microsoft.com 서브도메인의 정당성 가정
- 로고와 디자인의 진위 여부 미확인

**보안 인식 부족:**
- 정상적인 Microsoft 로그인 도메인 구별 능력 부족
  - 정상: login.microsoftonline.com, microsoft.com
  - 악성: *.blob.core.windows.net, customervoice.microsoft.com
- 테넌트별 URL 검증 습관 부재

---

## 영향 및 파급효과

### 직접적 영향

**자격증명 탈취:**
- Office 365 계정 정보
- 기업 이메일 계정
- 클라우드 서비스 접근 권한

**2차 공격 가능성:**
- 탈취한 계정을 통한 내부망 접근
- 비즈니스 이메일 침해(BEC) 공격
- 추가 피싱 이메일 발송

**데이터 유출:**
- 이메일 및 문서 접근
- 연락처 정보 유출
- 민감한 비즈니스 정보 노출

### 간접적 영향

**Microsoft 서비스 신뢰도 하락:**
- Azure Blob Storage 서비스에 대한 의구심
- Microsoft 도메인에 대한 신뢰 감소
- 클라우드 서비스 보안에 대한 우려 증가

**보안 필터링 우회:**
- 전통적인 URL 필터링 무력화
- 인증서 기반 필터링 우회
- 보안 도구의 한계 노출

**다른 클라우드 서비스로의 확산 가능성:**
- AWS S3, Google Cloud Storage 등 유사 공격 예상
- 신뢰받는 인프라 악용 트렌드 확산

### 예상 피해 규모

기사에서는 구체적인 피해 규모가 언급되지 않음. 다만:
- 캠페인의 정교함과 다양한 변종으로 볼 때 대규모 공격으로 추정
- 여러 Microsoft 서비스에 걸쳐 진행되어 피해 범위 광범위
- ANY.RUN 연구팀이 "emerging threat"로 분류할 만큼 심각성 인정

---

## 예방 및 대응 방안

### 사전 예방 방법

1. **클라우드 Storage 설정 강화**
   - 퍼블릭 컨테이너 생성 제한
   - 익명 액세스 비활성화
   - Storage Account 정기 감사
   - 컨테이너 레벨 액세스 제어 강화

2. **네트워크 레벨 보안**
   - *.blob.core.windows.net 트래픽 검사
   - 승인된 Storage Account만 허용
   - 프록시를 통한 트래픽 검사
   - DLP(Data Loss Prevention) 적용

3. **이메일 및 URL 분석**
   - *.blob.core.windows.net로 연결되는 이메일 플래그
   - 리다이렉트 체인 상관관계 분석
   - 신뢰할 수 있는 도메인의 의심스러운 경로 탐지

4. **사용자 교육**
   - 정상적인 Microsoft 로그인 도메인 교육
   - 테넌트별 URL 확인 습관 형성
   - 로고와 디자인만으로 신뢰하지 않기
   - 의심스러운 링크 신고 절차 수립

### 사고 발생 시 대응 방안

1. **즉각적 격리**
   - 의심스러운 계정 세션 즉시 종료
   - 리프레시 토큰 폐기
   - 계정 비밀번호 강제 변경

2. **ID 텔레메트리 분석**
   - Azure AD / Entra ID 로그 분석
   - Blob 링크 클릭 후 이상 로그인 패턴 탐지
   - 불가능한 여행(Impossible Travel) 경고 확인
   - MFA 실패 후 성공 패턴 분석

3. **샌드박스 분석**
   - 의심스러운 URL을 안전한 샌드박스에서 실행
   - 정적 HTML 폼 또는 자격증명 POST 엔드포인트 식별
   - 악성 스크립트 추출 및 분석

### 재발 방지 대책

**기술적 대책:**

1. **조건부 액세스 정책**
   - MFA 강제 적용
   - 익숙하지 않은 디바이스/IP/지역 차단
   - 위치 기반 접근 제어

2. **실시간 모니터링**
   - Blob URL 클릭과 ID 텔레메트리 상관관계 분석
   - 의심스러운 활동 시 자동 세션 종료
   - 비정상 POST 요청 탐지

3. **콘텐츠 검사**
   - Azure Blob Storage의 업로드 콘텐츠 스캔
   - HTML 파일의 "doom" ID 같은 알려진 패턴 탐지
   - JScript 기반 정보 수집 코드 식별

**조직적 대책:**

1. **정기 보안 감사**
   - Storage Account 설정 검토
   - 퍼블릭 컨테이너 목록 확인
   - 익명 액세스 설정 검증

2. **위협 인텔리전스 활용**
   - ANY.RUN TI Lookup 같은 도구로 IOC 추적
   - 알려진 피싱 패턴 데이터베이스 구축
   - 업계 정보 공유 참여

3. **인시던트 대응 계획**
   - Blob 링크 기반 피싱 시나리오 준비
   - 대응 플레이북 작성
   - 정기적 모의훈련

---

## 개인 인사이트

### 배운 점

1. **신뢰받는 인프라의 양면성**
   - Microsoft의 공식 도메인과 유효한 TLS 인증서가 오히려 무기로 사용됨
   - "*.microsoft.com = 안전"이라는 고정관념이 취약점이 됨
   - 신뢰받는 인프라는 공격자에게도 가치 있는 자산
   - 도메인의 소유자가 아닌 콘텐츠의 진위를 검증해야 함

2. **HTML Smuggling의 진화**
   - 단순한 HTML 파일이지만 매우 효과적
   - "doom" ID 같은 특정 패턴으로 캠페인 추적 가능
   - JScript를 통한 시스템 정보 수집으로 신뢰성 증대
   - 최소한의 악성 콘텐츠로 탐지 회피

3. **다층 리다이렉션의 효과성**
   - 디코더-리다이렉터 → 실제 피싱 페이지 → 정상 사이트
   - 각 단계가 분석을 방해하고 탐지를 지연
   - Cloudflare Pages, IPFS 등 합법적 서비스를 각 단계에서 활용
   - 공격 인프라의 분산으로 차단 어려움

4. **LogoKit의 정교함**
   - 실시간으로 타겟 회사의 로고 가져오기
   - 웹사이트 스크린샷을 배경으로 사용
   - 랜덤 이름의 스크립트로 분석 방해
   - 기업별 맞춤형 피싱 페이지 자동 생성

5. **클라우드 서비스 설정의 중요성**
   - 퍼블릭 컨테이너 하나가 대규모 피싱의 시작점
   - 익명 액세스 설정의 비즈니스 필요성 재검토 필요
   - 클라우드 보안은 설정 관리에서 시작
   - 정기적인 감사와 모니터링 필수

### 느낀 점

**클라우드 시대의 피싱 진화:**
- 전통적인 피싱은 의심스러운 도메인 사용
- 현대 피싱은 신뢰받는 클라우드 인프라 악용
- 보안 도구들이 "신뢰받는 도메인"을 우회하도록 설계되지 않음
- 방어 패러다임의 근본적 전환 필요

**Microsoft 서비스의 광범위한 악용:**
- Azure Blob Storage, OneDrive, Dynamics 365까지
- 하나의 캠페인이 여러 Microsoft 서비스로 확장
- Microsoft 생태계의 복잡성이 공격 표면 증가
- 각 서비스별 보안 설정 통합 관리 필요

**자동화된 피싱 도구의 위협:**
- LogoKit 같은 도구로 누구나 정교한 피싱 가능
- 타겟별 맞춤형 페이지 자동 생성
- 기술적 진입장벽 낮아짐
- 공격의 규모와 빈도 증가 예상

**보안 도구의 한계:**
- URL 필터링, 인증서 검증만으로는 불충분
- 콘텐츠 기반 분석의 중요성
- 행위 기반 탐지 필요
- 사용자 교육이 마지막 방어선

**정상 서비스와 악용의 경계 모호:**
- Azure Blob Storage는 합법적 서비스
- 사용자의 설정에 따라 악용 가능
- 서비스 제공자의 책임 범위는?
- 사용자의 보안 설정 이해도 향상 필요

**학습해야 할 기술 영역:**
- Azure Blob Storage 아키텍처 및 액세스 제어
- HTML Smuggling 기법의 작동 원리
- MITM(Man-in-the-Middle) 분석 기술
- IPFS(InterPlanetary File System) 이해
- Cloudflare Pages 및 CDN 서비스
- ANY.RUN 샌드박스 및 TI Lookup 활용법
- Azure AD / Entra ID 로그 분석

**샌드박스 분석의 가치:**
- ANY.RUN 같은 도구로 실시간 분석 가능
- MITM 기능으로 암호화된 트래픽 복호화
- 리다이렉션 체인 시각화
- IOC 자동 추출
- 커뮤니티와 정보 공유

## 관련 자료
- [ANY.RUN Interactive Sandbox](https://app.any.run/)
- [ANY.RUN TI Lookup 쿼리](https://intelligence.any.run/analysis/lookup/)
  - Azure Blob Storage 탐지: `domainName:".blob.core.windows.net"`
  - HTML 페이지 탐지: `commandLine:"https:/*.blob.core.windows.net/*.html"`
- [Microsoft: Azure Blob Storage 보안 가이드](https://docs.microsoft.com/azure/storage/blobs/security-recommendations)
- LogoKit 피싱 도구 분석 리포트
- HTML Smuggling 기법 상세 분석

---

**분석일**: 2024-12-28  
**키워드**: `#HTMLSmuggling` `#AzureBlobStorage` `#피싱캠페인` `#클라우드악용` `#LogoKit` `#Microsoft`