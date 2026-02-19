---
title: "2025.10.30 (Day 4) 파이썬 함수·클로저·스코프와 보안 게이트웨이 설계"
date: 2025-10-30
draft: false
tags: ["Python", "함수", "클로저", "보안게이트웨이", "SK쉴더스루키즈"]
categories: ["daily-logs"]
summary: "파이썬 함수, 클로저, 스코프 개념 학습 및 보안 게이트웨이 설계 실습"
---

# 2025.10.30 (Day 4) 함수, 람다, 클로저, 스코프 활용

## 1. 주요 개념 요약

* **함수 (Function)**: 코드의 재사용성과 유지보수 용이성을 확보하는 기본 단위이다. 탐지 로직이나 데이터 전처리 과정을 모듈화하여 관리할 수 있게 한다.
* **람다 함수 (Lambda)**: 내장 함수와 결합하여 로그 데이터의 간결한 조건 필터링 및 변환 로직을 구현할 때 사용한다.
* **스코프 (Scope)**: LEGB 규칙에 따른 변수 접근 범위를 명확히 하여 전역 변수의 오용을 방지하고 데이터의 안전한 관리를 보장한다.
* **클로저 (Closure)**: 외부 함수의 변수를 기억하여 전역 변수 없이 함수 내부에서 상태를 안전하게 유지하는 로직 구현에 활용한다.
* **데코레이터 (Decorator)**: 함수 로직의 변경 없이 권한 체크, 로깅 등 공통 보안 로직을 간결하게 추가할 수 있는 기법이다.

---

## 2. 실습 코드 및 응용

### A. 보안 함수 작성 (입력값 검증 및 인코딩)

* API 요청 생성 시 입력값에 악성 문자열이 포함되는 것을 URL 인코딩하여 XSS 취약점을 방어한다.

```python
from urllib.parse import quote

def safe_makeUrl(lst: list) -> list:
    if not isinstance(lst, list): raise TypeError("입력 타입 오류")
    return list(map(lambda x: 'www.'+quote(x)+'.com', lst))

```

### B. 클로저를 이용한 상태 유지 (로그 카운터)

* 특정 이벤트 발생 횟수를 전역 변수 노출 없이 안전하게 카운트하여 임계치 기반 탐지 로직의 기반으로 활용한다.

```python
def log_counter():
    count = 0 
    def increase():
        nonlocal count
        count += 1
        return count
    return increase 

```

### C. 가변 인자를 이용한 화이트리스트 검증

* API 통신 시 허용된 파라미터만 필터링하여 불필요한 정보 노출이나 잘못된 인자 주입을 방지한다.

```python
from urllib.parse import urlencode

def makeApiRequest(endpoint, **params):
    white_lst = {'q', 'page', 'lang'}
    safeParams = { k: v for k, v in params.items() if k in white_lst} 
    return endpoint +'?'+urlencode(safeParams)

```

---

## 3. 보안 관점 분석

* **보안 게이트웨이 역할**: 모든 외부 입력 데이터가 처리되는 지점에 함수를 정의하고 타입 검사 및 인코딩을 강제하여 주입 공격을 방지한다.
* **상태 관리의 폐쇄성**: 전역 변수 대신 클로저를 활용하여 특정 기능에만 접근 가능한 상태를 유지함으로써 탐지 로직의 안전성을 높인다.
* **통제 일관성 확보**: 데코레이터를 적용하여 민감 정보 처리 함수에 권한 체크나 마스킹 로깅 기능을 일괄적으로 부여한다.
* **파라미터 제어**: 가변 인자 사용 시 화이트리스트 기반 필터링을 통해 숨겨진 설정값 변경 시도 등의 공격을 차단한다.

