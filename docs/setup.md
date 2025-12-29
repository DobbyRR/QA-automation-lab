# Python 테스트 환경 설정 가이드

아래 순서대로 실행하면 로컬에서 pytest 기반 테스트를 바로 작성/실행할 수 있다.

## 1. 가상환경 생성
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. 의존성 설치
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## 3. 테스트 실행
```bash
pytest
# HTML 리포트 (timestamp 파일명 생성)
./scripts/run_tests.sh --report
```

## 참고
- 가상환경 비활성화: `deactivate`
- 새 패키지를 추가했다면 `pip install <pkg>` 후 `pip freeze > requirements.txt` 로 버전을 고정해둔다.
- 실 서비스 호출을 제외하려면 `pytest -m "not network"` 를, 실제 호출만 실행하려면 `pytest -m network` 를 사용한다.
- HTTP 로그를 파일로 남기고 싶다면 `export QA_LAB_LOG_PATH=logs/http.log` 처럼 경로를 지정한다.
- Playwright UI 테스트만 실행하려면 `pytest -m "network and ui"` 를 사용한다.
