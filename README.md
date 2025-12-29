# QA Automation Lab · Coupang QA

쿠팡(`https://www.coupang.com`)의 웹/정적 자원을 대상으로  
`Python + pytest + requests` 로 기본 QA 시나리오(Positive/Negative/Regression/로그 검증)를 자동화했다.

## Stack & Principles
- Python 3.9 이상 (필수)
- pytest
- requests
- Playwright + `pytest-playwright` 로 헤드리스 브라우저 QA
- 실 서비스 호출은 `pytest -m network` 로 구분하고, 그 외는 `monkeypatch` 로 빠른 단위 테스트 유지
- `QA_LAB_LOG_PATH` 환경변수를 지정하면 HTTP 로그가 JSON 파일로 쌓여 Threat Hunting 분석에 바로 활용 가능
- Threat Hunting 자료를 그대로 활용해 MITRE ATT&CK 전술/기술을 테스트 케이스에 명시
- GitHub Actions(workflow: `.github/workflows/qa.yml`)에서 `./scripts/run_tests.sh --report` 를 주기적으로 실행하고, HTML 리포트를 artifact 로 업로드해 공유할 수 있다.
- CI(예: GitHub Actions)에서 `./scripts/run_tests.sh --report` 를 주기적으로 실행하면 네트워크/API/보안/UI 전체 커버리지 리포트를 자동 수집할 수 있다.

## 현재 검증 범위
- **Positive Test**: 쿠팡 CDN 로고 자산이 200, `image/png` 로 응답하는지 확인.
- **Negative Test**: WAF가 의심스러운 검색 쿼리를 403(`x-reference-error`)로 차단하는지 확인.
- **Regression Test**: 메인 홈(`https://www.coupang.com/`)이 `Strict-Transport-Security` 헤더를 유지하는지 확인.
- **로그 기반 검증**: `ApiClient` 가 모든 HTTP 교환을 로깅하고 있는지 pytest로 캡처.
- **자동화 개념 확장**: rate-limit 기반 행위 감지(`RequestSpikeDetector`), 탐지 룰 테스트(`tests/security/test_detection.py`).
- **Security QA 업그레이드**: MITRE Discovery(T1046) / Credential Access(T1190) 행위를 Negative Test Case로 모델링하고 “이 행동 나오면 FAIL”을 코드로 표현.

## Repo Layout
```text
qa-automation-lab/
  qa_lab/                  # 앱/공통 코드 (재사용 모듈)
    __init__.py
    config.py              # BASE_URL, CDN_URL, timeout 등
    client.py              # ApiClient (requests 래퍼)
    utils/
      __init__.py
      logging.py           # 로깅 유틸
      rate_limit.py        # 스파이크 체크 헬퍼
  tests/                   # 테스트만
    __init__.py
    conftest.py            # fixtures (api client 등)
    api/
      test_coupang_public.py
    security/
      test_abuse.py        # 반복 호출/이상행위 헬퍼
      test_detection.py    # 룰/탐지 흉내
      test_coupang_waf.py  # Negative Test
      test_logging.py      # 로그 기반 검증
      ...
    ui/
      test_coupang_ui.py   # Playwright 기반 UI 테스트
  docs/                    # 문서(포트폴리오 점수 올려주는 곳)
    scenarios.md           # 보안 시나리오 설명
    decisions.md           # 설계/판단 근거
    findings.md            # 실험 결과/이슈 기록
    setup.md               # 로컬 실행 방법
  scripts/
    run_tests.sh           # pytest 실행 스크립트
  reports/                 # (gitignore) HTML 리포트 아웃풋
  requirements.txt
  pytest.ini
  README.md
```

## 실행 방법
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium   # UI 테스트용
./scripts/run_tests.sh
# UI 테스트만 실행하려면
pytest -m "network and ui"
# HTML 리포트 생성 (timestamp 파일명)
./scripts/run_tests.sh --report
```

## 현재 포함된 테스트
- `tests/api/test_coupang_public.py`: CDN 로고 자산 200(Positive), HSTS 헤더 보장(Regression).
- `tests/api/test_coupang_assets.py`: 로고 자산의 `ETag`, `Content-Length`, 캐시 관련 헤더 Regression.
- `tests/api/test_coupang_headers.py`: 검색 응답의 세션 쿠키, 보안 헤더, 쿠키 지속성 확인.
- `tests/api/test_coupang_product.py`: 인증이 필요한 `/np/coupons` 호출 시 401/403과 보안 헤더 노출 여부 확인.
- `tests/security/test_coupang_waf.py`: SQLi 스타일 검색어가 403으로 차단되는지 확인(Negative).
- `tests/security/test_logging.py`: HTTP 호출 시 stdout 로그가 남는지 확인(로그 기반 검증).
- `tests/security/test_abuse.py`: `RequestSpikeDetector` 로 과도한 호출을 탐지.
- `tests/security/test_detection.py`: 실패율/지연 조합으로 suspicious 동작 플래그.
- `tests/security/test_mitre_behaviors.py`: MITRE Discovery/ Credential Access 행위가 탐지 로직에 의해 차단되는지 검증.
- `tests/security/test_header_anomalies.py`: 비정상 헤더(User-Agent 제거 등)에도 보안 헤더가 유지되는지 확인.
- `tests/security/test_rate_limit_network.py`: 동일 의심 쿼리를 반복 호출했을 때 일관되게 차단되는지 확인.
- `tests/security/test_cookie_tampering.py`: 잘못된 세션 쿠키를 주입해도 401/403 차단이 유지되는지 확인.
- `tests/security/test_log_sink.py`: `QA_LAB_LOG_PATH` 기반 JSON 로그 파일 생성 + 다중 요청 기록 테스트.
- `tests/ui/test_coupang_ui.py`: Playwright로 Access Denied 배너/SQLi 차단을 검증하고 스크린샷 증거를 남김.
- Playwright 시나리오 요약:
  - Access Denied 페이지가 “Reference #” 보안 메시지를 노출하는지 확인.
  - SQLi 스타일 검색 쿼리로 403 + `x-reference-error` 가 발생하는지 브라우저 상에서 검증.
  - 헤드리스 Chromium으로 API Negative 시나리오를 UI 계층에서도 재현.

> 네트워크 실 테스트는 한국 외 지역에서 403이 날 수 있으므로, 상태코드 집합을 허용 범위로 두고 보안 헤더/응답 특징 위주로 검증한다.

## 환경 변수 / 커스터마이즈

| 변수 | 기본값 | 설명 |
| --- | --- | --- |
| `QA_LAB_BASE_URL` | `https://www.coupang.com` | 메인 도메인 (API 테스트) |
| `QA_LAB_CDN_URL` | `https://static.coupangcdn.com` | 정적 자산 검증용 |
| `QA_LAB_TIMEOUT` | `5` | `requests` 타임아웃(초) |
| `QA_LAB_USER_AGENT` | `QA-Automation-Lab/0.1 (+pytest requests)` | 공통 User-Agent |
| `QA_LAB_LOG_PATH` | (빈 값) | 설정 시 HTTP 로그를 JSON 라인 파일로 저장 |

환경변수를 조정하면 프록시/지역 제한 등의 환경에서도 동일한 테스트 스위트를 쉽게 재현할 수 있다.

## 다음 확장 아이디어
- 실제 계정 인증이 가능한 환경이라면 Positive 테스트를 홈/검색 성공 케이스로 확장.
- CDN 외 다른 정적 리소스(이미지 sprite, CSS)도 모니터링해 Regression 커버리지 증대.
- `log_http_exchange` 를 파일 로깅으로 전환하고, pytest에서 로그 파일을 fixtures로 검증.
- `docs/findings.md` 에 실험 결과/장애 케이스를 주기적으로 추가해 히스토리 확보.
