from qa_lab.utils.detections import (
    LogEvent,
    detect_discovery_enumeration,
    detect_exploit_attempts,
    detect_latency_spike,
    detect_restricted_resource_access,
)


def test_discovery_enumeration_flags_attack():
    events = [
        LogEvent(timestamp=i * 0.3, path="/np/search", status_code=200, latency_ms=80, params={"q": f"item-{i}"})
        for i in range(6)
    ]
    result = detect_discovery_enumeration(events, window_seconds=1.5, threshold=5)

    assert result.alert is True
    assert result.tactic == "Discovery"
    assert result.technique == "T1046"
    assert "search requests" in result.reason


def test_discovery_enumeration_normal_usage():
    events = [
        LogEvent(timestamp=i * 5, path="/np/search", status_code=200, latency_ms=90, params={"q": f"item-{i}"})
        for i in range(3)
    ]
    result = detect_discovery_enumeration(events)

    assert result.alert is False
    assert "No enumeration" in result.reason


def test_exploit_attempt_detection():
    events = [
        LogEvent(
            timestamp=1.0,
            path="/np/search",
            status_code=403,
            latency_ms=75,
            params={"q": "' OR 1=1 --"},
        ),
        LogEvent(
            timestamp=2.0,
            path="/np/search",
            status_code=200,
            latency_ms=60,
            params={"q": "정상검색"},
        ),
    ]
    result = detect_exploit_attempts(events)

    assert result.alert is True
    assert result.tactic == "Credential Access"
    assert result.technique == "T1190"
    assert "Suspicious payload" in result.reason


def test_exploit_attempt_detection_false_positive():
    events = [
        LogEvent(timestamp=0.5, path="/np/search", status_code=200, latency_ms=80, params={"q": "마스크"}),
    ]
    result = detect_exploit_attempts(events)

    assert result.alert is False
    assert "No exploit" in result.reason


def test_restricted_resource_detection():
    events = [
        LogEvent(timestamp=0.1, path="/np/coupons", status_code=403, latency_ms=70),
        LogEvent(timestamp=0.5, path="/np/search", status_code=200, latency_ms=80),
    ]
    result = detect_restricted_resource_access(events)

    assert result.alert is True
    assert result.tactic == "Reconnaissance"
    assert "coupons" in result.reason


def test_latency_spike_detection():
    events = [
        LogEvent(timestamp=0.0, path="/np/search", status_code=200, latency_ms=1600),
        LogEvent(timestamp=0.1, path="/np/search", status_code=200, latency_ms=1700),
        LogEvent(timestamp=0.2, path="/np/search", status_code=200, latency_ms=200),
    ]
    result = detect_latency_spike(events)

    assert result.alert is True
    assert result.tactic == "Impact"
    assert "latency" in result.reason


def test_latency_spike_normal():
    events = [
        LogEvent(timestamp=0.0, path="/np/search", status_code=200, latency_ms=200),
        LogEvent(timestamp=0.5, path="/np/search", status_code=200, latency_ms=300),
    ]
    result = detect_latency_spike(events)

    assert result.alert is False
