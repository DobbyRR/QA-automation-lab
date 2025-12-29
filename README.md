# QA Automation Lab (Security-focused)

Python 기반의 QA 자동화 포트폴리오 프로젝트입니다.  
공개 REST API를 대상으로 **기능 테스트 + 보안 관점(행위 기반) 테스트**를 작성하고,  
테스트 구조/로그/탐지 룰을 점진적으로 확장합니다.

## Highlights
- `pytest + requests` 기반 API 테스트 자동화
- Positive/Negative 시나리오 포함 (실패 케이스를 명시적으로 테스트)
- 공통 API Client + pytest fixture로 테스트 구조화
- (확장) 짧은 시간 반복 호출 등 **행위 기반 이상징후 테스트** 추가 예정
- (확장) 로그 기반 판별 + 간단 탐지 룰(시그널 조합) 실험 예정

## What this project tests

### API Functional Tests
- Posts
  - `GET /posts/1` → 200 + 응답 필드 검증
  - `GET /posts?userId=1` → 200 + 필터링 결과 검증
- Users
  - `GET /users/1` → 200 + 주요 필드 검증
- Negative
  - `GET /posts/101` → 404 (존재하지 않는 리소스)

### Security-minded Tests (WIP → Week 4~)
- 짧은 시간에 반복 호출(스파이크) 발생 시 FAIL 처리
- 요청/응답 로그 기록 및 이상 징후 판별 실험
- 단순 탐지 룰: “A + B 조합이면 suspicious” 형태로 False Positive 고려

## Tech Stack
- Python
- pytest
- requests

## Project Structure
```text
qa-automation-lab/
  qa_lab/                # 공통 코드 (API Client, 설정 등)
    config.py
    client.py
  tests/                 # pytest 테스트
    conftest.py          # fixture
    test_posts.py
    test_users.py
    test_negative.py
  requirements.txt
  pytest.ini
  README.md
```
## Why this matters 
(QA + Security)
일반적인 QA 테스트가 “기능이 맞게 동작하나?”를 본다면, 
이 프로젝트는 거기에 더해 “이 행동이 정상적인가?”라는 관점을 추가합니다.
예: 동일 엔드포인트에 대한 과도한 반복 호출, 비정상적인 실패 패턴 등은
장애/오용/공격 신호가 될 수 있으므로 테스트로 검증 가능하게 만드는 것을 목표로 합니다.
Roadmap
 로깅 추가 (요청/응답 메타데이터)
 반복 호출/속도 제한 시나리오 테스트
 로그 파일 기반 이상 판별 테스트
 단순 탐지 룰 + False Positive 케이스 정리
 보안 시나리오 문서화 (docs/)
Notes
이 프로젝트는 학습/포트폴리오 목적이며,
공개 API(JSONPlaceholder 등)를 활용해 재현 가능한 테스트 환경을 구성합니다.