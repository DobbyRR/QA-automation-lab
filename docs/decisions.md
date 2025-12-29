# 설계 / 판단 근거

## API Client
- requests.Session을 래핑한 `ApiClient` 로 공통 헤더/timeout/User-Agent를 한 곳에서 제어.
- `QA_LAB_BASE_URL`, `QA_LAB_CDN_URL`, `QA_LAB_TIMEOUT`, `QA_LAB_USER_AGENT` 등 환경변수로 쿠팡 메인/ CDN 엔드포인트를 쉽게 조정.

## 테스트 구조
- `tests/api/` : 실제 쿠팡 도메인을 호출하는 Positive/Regression 테스트(`@pytest.mark.network` 사용).
- `tests/security/` : Negative(WAF) + 행위 기반/탐지 로직 + 로그 검증.
- 네트워크 의존도가 없는 시나리오는 `monkeypatch` 로 응답을 가짜로 만들어 속도/안정성을 확보.
- `tests/ui/` : Playwright 기반으로 브라우저 관점의 QA/보안 검증을 수행(`@pytest.mark.ui`).

## 로깅 & rate limit
- `qa_lab/utils/logging.py` 는 stdout 로그뿐 아니라 `QA_LAB_LOG_PATH` 에 지정된 JSON 로그 파일도 생성해 `tests/security/test_log_sink.py` 로 검증.
- `RequestSpikeDetector` 는 sliding window 방식으로 구현해 과도한 `/np/search` 호출 여부를 테스트 가능하게 함.
- `qa_lab/utils/detections.py` 는 Threat Hunting 관점에서 `LogEvent` → MITRE 전술/기술을 매핑해 Negative Test Case 를 구조화.

## Playwright UI
- Headless Chromium을 사용해 403 Access Denied 페이지가 올바르게 노출되는지, SQLi 검색 시 차단 메시지가 뜨는지 확인.
- API 레벨과 동일한 Negative 시나리오를 실제 브라우저에서도 재현함으로써 “행위 테스트” 메시지를 강화.

## 리포트
- `pytest-html` 플러그인으로 `./scripts/run_tests.sh --report` 를 실행하면 `reports/qa_report_<timestamp>.html` 형태의 HTML 리포트가 자동 생성된다.

## 실행 방법
1. `python3 -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `python -m playwright install chromium`
3. `./scripts/run_tests.sh` 또는 `pytest`
