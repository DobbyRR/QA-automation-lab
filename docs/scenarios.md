# 보안 시나리오

| MITRE 전술 | 기술 ID | Negative Test Case | 기대 동작 |
| --- | --- | --- | --- |
| Discovery | T1046 | `/np/search` 가 짧은 시간 안에 연속 호출 | `detect_discovery_enumeration` 이 alert=True → 테스트 FAIL |
| Credential Access (Exploit Public-Facing App) | T1190 | `"' OR 1=1 --"` 등 SQLi 패턴 쿼리 | `detect_exploit_attempts` 가 alert=True + WAF 403 |
| Reconnaissance | T1595 | `/np/coupons`, `/np/member` 등 제한 페이지 접근 | `detect_restricted_resource_access` alert=True (403 기록) |
| Impact | T1499 | 연속으로 1500ms 이상 지연 | `detect_latency_spike` alert=True |

## 반복 호출 감지
- 동일 IP/토큰에서 1초 안에 5회 이상 `/np/search` 요청 시 스파이크로 간주.
- 실제 구매 플로우에서는 연속 검색이 드물기 때문에 False Positive 위험이 낮다.

## 실패율 기반 탐지
- `/np/search`, `/vp/products` 등에 대해 4회 요청 중 2회 이상이 4xx/5xx 라면 WAF/인증 이상 가능성이 있다.
- Latency 1500ms 이상이 연속 2번 발생하면 네트워크/봇 공격 신호로 취급한다.

## 행위 기반 abuse 테스트
- 동일 검색 쿼리를 짧은 간격으로 반복 → rate limit 발동 여부 & 로그 확인.
- SQLi 스타일 파라미터(`' OR 1=1 --`) 주입 시 403 + `x-reference-error` 가 기록되는지 검증.
