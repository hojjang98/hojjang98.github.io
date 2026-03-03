---
title: "Project 01 — Mini Security Log Monitor"
date: 2025-10-31
draft: false
tags: ["Python", "보안관제", "SOC", "로그분석", "SK쉴더스루키즈"]
categories: ["projects"]
series: ["SK쉴더스 루키즈 28기"]
summary: "파이썬 기초 문법을 보안 관점으로 재구성한 입문형 보안 로그 탐지 시스템"
---

# Project 01 — Mini Security Log Monitor

> 전체 소스코드는 GitHub에서 확인할 수 있습니다.
> [hojjang98 / skshielders-rookies-28 — projects/week_01](https://github.com/hojjang98/skshielders-rookies-28/tree/main/projects/week_01)

---

## 개요

**Mini Security Log Monitor**는 1주차 파이썬 기초 학습 내용을 종합하여 구현한 보안 이벤트 감지 및 기록 시스템이다.

단순한 문법 연습에 그치지 않고, **입력 검증 -> 이벤트 탐지 -> 예외 처리 -> 감사 로깅**으로 이어지는 보안 시스템의 핵심 흐름을 코드 레벨로 구현하는 것을 목표로 삼았다.

---

## 주간 학습 요약

- **Day 1 (10.27)** — 파이썬 기본 타입과 자료구조
  - 딕셔너리 `.get()` 안전 접근, 불변성(Immutable) 개념

- **Day 2 (10.28)** — 클래스 · 제어문 · 딕셔너리
  - 객체지향 탐지 구조 설계, JSON 기반 데이터 모델링

- **Day 3 (10.29)** — 조건문 · 반복문 · 문자열 처리
  - 문자열 파싱(split), 조건 기반 탐지, 날짜 반복 처리

- **Day 4 (10.30)** — 함수 · 람다 · 클로저 · 데코레이터
  - 함수 모듈화, 전역 변수 없는 상태 관리, 권한 체크 로직

- **Day 5 (10.31)** — 예외 처리 · 로깅 · 파일 입출력
  - try-except 기반 예외 대응, 로깅 및 JSON 로그 기록

---

## 주요 기능

- **사용자 인증 검증** — 인증되지 않은 사용자의 접근 차단
- **이벤트 탐지 및 기록** — 로그 파일 내 ERROR, UNAUTHORIZED 등 이벤트 감지 및 저장
- **사용자 마스킹 처리** — 개인정보 보호를 위한 이름 비식별화 (ad** 형태)
- **예외 처리 및 경고** — 오류 발생 시 try-except 로 중단 없이 로깅 지속
- **데코레이터 기반 구조** — 공통 보안 로직(로깅, 권한 체크)을 함수 외부에서 관리

---

## 핵심 코드 설명

### 1. User 클래스 — 인증 상태 관리

사용자 정보와 인증 여부를 하나의 객체로 캡슐화한다.
인증 여부는 **authenticated** 필드로 관리하며, 기본값은 False 로 설정해 안전한 기본 상태를 유지한다.

    class User:
        def __init__(self, name: str, authenticated: bool = False):
            self.name = name
            self.authenticated = authenticated

---

### 2. access_logger 데코레이터 — 공통 로깅 자동화

핵심 설계 원칙은 **공통 보안 로직의 분리**다.
접근 성공 / 실패 여부를 함수 외부에서 일괄 처리하므로, 개별 함수마다 로깅 코드를 반복할 필요가 없다.

- 사용자 이름 앞 두 글자만 남기고 나머지는 * 로 마스킹
  - ex) admin => ad***,  carol => ca***
- 접근 성공 시 => result: "SUCCESS" 로 JSON 기록
- 예외 발생 시 => result: "FAIL" + 예외 타입 + 메시지 로 JSON 기록

실제 데코레이터 구조 (축약):

    def access_logger(func):
        def wrapper(user):
            masked = user.name[:2] + "*" * (len(user.name) - 2)
            try:
                result = func(user)
                log_entry = {"user": masked, "result": "SUCCESS"}
                # access.log 에 JSON 형태로 append
            except Exception as e:
                log_entry = {"user": masked, "result": "FAIL", "error": type(e).__name__}
                # 실패 내역도 동일하게 기록
        return wrapper

---

### 3. read_secure_log — 권한 기반 로그 열람

**@access_logger** 데코레이터가 부착된 핵심 함수.
함수 진입 시 가장 먼저 인증 여부를 확인하며, 미인증 사용자는 **PermissionError** 를 발생시켜 차단한다.
인증 통과 후에는 system.log 에서 ERROR 포함 라인만 필터링해 최근 5건을 반환한다.

    @access_logger
    def read_secure_log(user):
        if not user.authenticated:
            raise PermissionError("인증되지 않은 사용자입니다.")
        with open("system.log", "r", encoding="utf-8") as f:
            logs = f.readlines()
        filtered = [line.strip() for line in logs if "ERROR" in line]
        return filtered[-5:]

---

### 4. JSON 감사 로그 형식

탐지 결과는 아래와 같은 구조로 **access.log** 에 한 줄씩 기록된다.
JSON 형태를 유지하므로 SIEM 연동이나 추가 분석 파이프라인으로 확장하기 용이하다.

성공 케이스:

    {"user": "ad***", "result": "SUCCESS", "message": "로그 접근 성공"}

실패 케이스:

    {"user": "ca***", "result": "FAIL", "error": "PermissionError", "message": "인증되지 않은 사용자입니다."}

---

## SOC 관점 연계

이 프로젝트는 보안관제(SOC) 의 4단계 흐름을 코드 레벨로 축약한 구조다.

- **로그 수집 (Collection)** — system.log 파일을 읽어 이벤트 수집
- **이벤트 탐지 (Detection)** — 문자열 탐색과 조건문으로 ERROR 이벤트 감지
- **이벤트 기록 (Logging)** — JSON 기반 access.log 에 탐지 결과 저장
- **감사 및 분석 (Audit)** — 마스킹된 사용자 로그로 접근 내역 추적

---

## 학습 연결 포인트

- **dict.get()** => KeyError 방지 및 안전한 데이터 접근
- **if / for 문** => 로그 이벤트 탐지 조건 구성
- **@decorator** => 접근 감사 로직의 공통화
- **try-except** => 예외 발생 시 안정적 흐름 유지
- **with open()** => 파일 입출력 자원 안정성 확보
- **문자열 슬라이싱** => 사용자 마스킹(ab***) 처리

---

## 확장 아이디어

- **로그 누락 탐지** — 파일 유무 확인 및 누락 이벤트 기록
- **데이터 무결성 강화** — deepcopy() 와 .get() 기반 안전한 파서 구현
- **시각화 연계** — Week 2 Streamlit 대시보드로 로그 분석 결과 시각화

---

> 이 프로젝트는 Week 1 학습 내용을 모두 아우르며,
> **데이터 구조화 -> 조건 탐지 -> 로깅 -> 감사** 로 이어지는
> 보안 시스템 로직의 핵심 뼈대를 완성하는 입문형 프로젝트다.
