---
title: "2025.11.27 (Day 24) Linux 시스템 보안: 로그 관리, 무결성 검사, 패키지 & 압축"
date: 2025-11-27
draft: false
tags: ["Linux", "로그분석", "파일무결성", "패키지관리", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "리눅스 시스템 로그 파일 분석, debsums 무결성 검사, APT 패키지 관리, gzip/tar 압축 실습"
---

# 📄 2025.11.27 (Day 24) [Linux 시스템 보안: 로그 관리, 무결성 검사, 패키지 & 압축]

## 1. 핵심 개념 정리 (Concepts & Theory)

| # | 핵심 개념 | 간결한 설명 | 실무/보안 관점에서의 중요성 |
|:---:|:---|:---|:---|
| **1** | **시스템 로그 파일** | 리눅스는 시스템 활동을 `/var/log/` 디렉터리에 자동 기록합니다. **`auth.log`**(인증 관련), **`syslog`**(전체 시스템 로그), **`wtmp`**(로그인 기록) 등이 핵심입니다. `tail -f`로 실시간 모니터링이 가능합니다. | **침해 사고 분석**의 필수 데이터 소스입니다. 로그인 시도(`lastb`), sudo 실행 이력(`auth.log`), 서비스 동작(`syslog`) 추적을 통해 **공격 타임라인 재구성**과 **비정상 활동 탐지**가 가능합니다. |
| **2** | **파일 무결성 검사** | **`debsums`**는 패키지 파일의 MD5 체크섬을 검증하고, **`dpkg -V`**는 패키지 파일의 크기, 권한, 수정 시간 등을 원본과 비교하여 변조 여부를 탐지합니다. | **루트킷 탐지**와 **시스템 바이너리 변조 확인**의 핵심입니다. `/bin/ls`, `/bin/cat` 등 자주 타겟이 되는 바이너리를 주기적으로 검사하여 백도어 설치나 악성 코드 삽입을 조기 발견할 수 있습니다. |
| **3** | **패키지 관리 시스템** | **APT**(Debian/Ubuntu)와 **YUM**(RedHat/CentOS)은 소프트웨어 설치, 업데이트, 제거를 자동화하며 **의존성 관리**를 처리합니다. `apt update`로 저장소 정보를 갱신하고, `apt upgrade`로 보안 패치를 적용합니다. | **취약점 패치 관리**의 중추입니다. 정기적인 `apt upgrade`로 알려진 취약점을 신속히 패치하고, `apt list --upgradable`로 패치 가능한 패키지를 추적하여 보안 태세를 유지합니다. |
| **4** | **파일 압축 & 아카이빙** | **gzip/bzip2**는 파일을 압축(원본 삭제)하고, **tar**는 여러 파일을 하나의 아카이브로 묶습니다. `tar zcvf`는 압축과 묶음을 동시에 수행합니다. bzip2가 gzip보다 압축률이 높지만 속도는 느립니다. | **백업 및 로그 관리**에 필수입니다. 대용량 로그를 `tar zcvf`로 압축 보관하여 저장 공간을 절약하고, 사고 조사 시 압축된 로그를 효율적으로 분석할 수 있습니다. |

---

## 2. 실습 코드 & 응용 (Practice & Code Walkthrough)

### (A) 핵심 명령어/함수 실습

**시스템 로그 모니터링:**
```bash
# 인증 로그 실시간 모니터링 (로그인, sudo 실행 등)
tail -f /var/log/auth.log

# 실패한 로그인 시도 확인
lastb

# 성공한 로그인 기록 확인
last

# 전체 시스템 로그 실시간 모니터링
tail -f /var/log/syslog

# 다른 터미널에서 서비스 재시작 테스트
systemctl stop cron
systemctl start cron
# → syslog에서 cron 재시작 로그 실시간 확인 가능

# 현재 로그인한 사용자 확인
who     # 간단한 정보
w       # 상세 정보 (현재 실행 중인 명령 포함)
```

**파일 무결성 검사:**
```bash
# debsums 유틸리티 설치
apt install -y debsums

# coreutils 패키지 무결성 검사 (ls, cat 등 핵심 바이너리)
debsums coreutils
# 정상: OK 출력
# 변조: FAILED 출력

# 전체 시스템 무결성 검사 (FAILED만 출력)
debsums -s

# 시뮬레이션: ping 바이너리 변조
cd /bin
cp ping ping.org         # 원본 백업
cp ping7 ping            # SetUID가 설정된 파일로 교체
ls -l ping*

# dpkg를 이용한 패키지 검증
dpkg -V iputils-ping
# 출력 예: ??5?????? /bin/ping
# S: 파일 크기 변경
# M: 파일 모드(권한) 변경
# 5: MD5 체크섬 불일치
# T: 생성시간 변경
# U: 소유자 변경
# G: 그룹 변경
```

**패키지 관리:**
```bash
# 패키지 저장소 정보 업데이트
apt update

# 설치된 패키지 목록 확인
apt list --installed

# 업그레이드 가능한 패키지 확인
apt list --upgradable

# 패키지 설치 예시
apt install -y xfsprogs       # XFS 파일시스템 도구
apt install -y net-tools      # ifconfig, netstat 등
apt install -y debsums        # 무결성 검사 도구

# 패키지 검색
apt search <키워드>

# 패키지 상세 정보 확인
apt show <패키지명>

# 패키지 삭제
apt remove <패키지명>
```

**파일 압축 & 아카이빙:**
```bash
# gzip 압축 (원본 삭제됨)
gzip /backup/passwd
gunzip /backup/passwd.gz

# bzip2 압축
bzip2 /backup/passwd
bunzip2 /backup/passwd.bz2

# tar 아카이빙
tar cvf /backup/bk.tar /backup/*    # 묶기
tar tvf /backup/bk.tar              # 내용 확인
tar xvf /backup/bk.tar              # 풀기

# tar + gzip 동시 실행
tar zcvf /backup/bk.tar.gz /backup/*          # 압축하며 묶기
tar zxvf /backup/bk.tar.gz                    # 압축 해제하며 풀기
tar xvfz /backup/bk.tar.gz -C /tmp/           # 특정 디렉터리에 압축 해제
```

### (B) 실습 결과 및 분석

* **로그 파일의 실시간성:** `tail -f`를 사용하면 로그가 생성되는 즉시 화면에 표시되어, 서비스 재시작이나 로그인 시도를 실시간으로 추적할 수 있습니다. 관제 환경에서 여러 로그를 동시에 모니터링하는 **멀티 터미널 설정**이 효과적입니다.

* **무결성 검사의 정확성:** `debsums`는 MD5 체크섬을 기반으로 하므로, 바이너리가 조금이라도 변경되면 즉시 탐지됩니다. `dpkg -V`의 출력 코드를 해석하면 **정확히 어떤 속성이 변경되었는지** 파악 가능합니다 (크기, 권한, 체크섬 등).

* **압축 알고리즘 비교:**
  - **gzip**: 빠른 속도, 중간 압축률 (로그 파일에 적합)
  - **bzip2**: 느린 속도, 높은 압축률 (아카이브 장기 보관에 적합)
  - 실무에서는 속도와 압축률의 트레이드오프를 고려하여 선택합니다.

* **로그인 기록 추적:**
  - `last`: `/var/log/wtmp` 기반, 성공한 로그인
  - `lastb`: `/var/log/btmp` 기반, 실패한 로그인 (무차별 대입 공격 탐지)

---

## 3. 실무/보안 관점 분석 (Insight & Scenario Mapping)

| 분야 | 적용 시나리오 |
|:---:|:---|
| **SOC / 관제** | **로그 기반 실시간 탐지**: `tail -f /var/log/auth.log \| grep "Failed password" \| awk '{print $1,$2,$3,$11}' \| tee -a /var/log/failed_logins.log`를 통해 실패한 로그인 시도를 실시간으로 추출하고 별도 파일에 누적 기록합니다. 특정 IP에서 10회 이상 실패 시 자동으로 `iptables`로 차단하는 스크립트를 `cron`에 등록하여 **자동 대응 체계** 구축이 가능합니다. |
| **CERT / 사고 대응** | **침해 사고 시 무결성 검사 프로세스**: 사고 발생 시 가장 먼저 `debsums -s`와 `dpkg -V`를 실행하여 **변조된 바이너리를 신속히 식별**합니다. 특히 `/bin`, `/usr/bin`, `/sbin` 디렉터리의 핵심 명령어(`ls`, `ps`, `netstat` 등)가 공격자에 의해 루트킷으로 교체되었는지 확인합니다. 변조가 확인되면 `apt install --reinstall <패키지>`로 패키지를 재설치하여 원본 복구합니다. |
| **시스템 운영** | **자동화된 백업 및 패치 관리**: `cron`에 `0 2 * * * tar zcvf /backup/daily_$(date +\%Y\%m\%d).tar.gz /var/www/html /etc 2>&1 \| logger -t backup`을 등록하여 매일 새벽 2시 자동 백업을 수행하고, 에러는 syslog에 기록합니다. 보안 패치: `apt update && apt list --upgradable`을 주기적으로 실행하여 패치 가능한 패키지를 확인하고, 중요 패키지는 `apt-mark hold <패키지>`로 자동 업그레이드를 막아 안정성을 보장합니다. |

---

## 4. 개인 인사이트 및 다음 단계 (Reflection & Next Steps)

* **배운 점/느낀 점:**
  - **로그는 시스템의 블랙박스**입니다. 모든 중요 활동이 기록되므로, 로그 분석 능력은 사고 대응의 핵심입니다. `tail -f`로 실시간 모니터링하면서 서비스를 재시작했을 때 로그가 즉시 반영되는 것을 보며, 로그의 **즉시성**과 **신뢰성**을 체감했습니다.
  - **무결성 검사의 중요성**: `debsums`와 `dpkg -V`를 통해 시스템 바이너리가 변조되었는지 **객관적으로 검증**할 수 있다는 점이 매우 강력합니다. 공격자가 루트킷을 설치해도, 무결성 검사로 탐지 가능하다는 것은 **방어의 마지막 보루**입니다.
  - **패키지 관리의 편리성**: APT의 의존성 자동 해결 기능 덕분에 복잡한 소프트웨어도 간단히 설치할 수 있었습니다. 하지만 **신뢰할 수 있는 저장소**에서만 설치해야 한다는 보안 원칙을 명심해야 합니다.

* **심화 방향:**
  - **로그 집중화 시스템**: `rsyslog`를 설정하여 여러 서버의 로그를 중앙 서버로 집중시키는 **로그 집중화**(Log Aggregation) 구축. ELK Stack(Elasticsearch, Logstash, Kibana)을 활용한 대규모 로그 분석 플랫폼 구축.
  - **파일 무결성 모니터링(FIM)**: `AIDE`(Advanced Intrusion Detection Environment)나 `Tripwire` 같은 전문 FIM 도구를 활용하여 **실시간 무결성 모니터링** 시스템 구축.
  - **자동화 스크립트 작성**: 로그 분석, 무결성 검사, 백업을 하나의 Shell Script로 통합하고, `cron`으로 자동 실행되도록 설정.

---

## 5. 추가 참고사항 (Quick Reference)

### 주요 로그 파일 위치
```
/var/log/auth.log       : 인증 관련 로그 (로그인, sudo, su 등)
/var/log/syslog         : 전체 시스템 로그
/var/log/kern.log       : 커널 로그
/var/log/wtmp           : 로그인 성공 기록 (last 명령)
/var/log/btmp           : 로그인 실패 기록 (lastb 명령)
/var/log/faillog        : 로그인 실패 정보
/var/log/apache2/       : Apache 웹서버 로그
/var/log/nginx/         : Nginx 웹서버 로그
```

### dpkg -V 출력 코드
```
S : 파일 크기 변경
M : 파일 모드(권한, 파일 타입) 변경
5 : MD5 체크섬 불일치
T : 생성 시간 변경
U : 사용자/소유자 변경
G : 그룹 변경
c : 설정 파일 (configuration file)
```

### 압축 & 아카이빙 명령어 요약
```bash
# gzip 압축/해제
gzip file              # 압축 (원본 삭제)
gunzip file.gz         # 압축 해제
gzip -d file.gz        # 압축 해제 (동일)
gzip -c file > new.gz  # 원본 유지하며 압축

# bzip2 압축/해제
bzip2 file             # 압축 (원본 삭제)
bunzip2 file.bz2       # 압축 해제
bzip2 -d file.bz2      # 압축 해제 (동일)

# tar 아카이빙
tar cvf archive.tar files/      # 묶기
tar xvf archive.tar             # 풀기
tar tvf archive.tar             # 내용 확인

# tar + gzip
tar zcvf archive.tar.gz files/  # 압축하며 묶기
tar zxvf archive.tar.gz         # 압축 해제하며 풀기
tar ztvf archive.tar.gz         # 내용 확인

# tar + bzip2
tar jcvf archive.tar.bz2 files/ # 압축하며 묶기
tar jxvf archive.tar.bz2        # 압축 해제하며 풀기

# 특정 디렉터리에 압축 해제
tar xvf archive.tar -C /target/dir/
```

### APT 주요 명령어
```bash
apt update                  # 패키지 저장소 정보 업데이트
apt upgrade                 # 설치된 패키지 업그레이드
apt list --installed        # 설치된 패키지 목록
apt list --upgradable       # 업그레이드 가능 패키지
apt install <pkg>           # 패키지 설치
apt remove <pkg>            # 패키지 제거
apt purge <pkg>             # 패키지 및 설정 파일 제거
apt search <keyword>        # 패키지 검색
apt show <pkg>              # 패키지 상세 정보
apt autoremove              # 불필요한 의존성 제거
apt install --reinstall <pkg>  # 패키지 재설치
```
