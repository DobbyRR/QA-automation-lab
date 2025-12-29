from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class LogEntry:
    endpoint: str
    status_code: int
    latency_ms: int


def detect_suspicious_behavior(logs: Iterable[LogEntry]) -> bool:
    """Toy detection logic: fail rate over 50% within a sample of 4."""
    entries: List[LogEntry] = list(logs)
    if not entries:
        return False
    failures = [entry for entry in entries if entry.status_code >= 400]
    if len(entries) < 4:
        return False
    failure_ratio = len(failures) / len(entries)
    return failure_ratio >= 0.5 or any(entry.latency_ms > 1500 for entry in entries)


def test_detection_flags_many_failures():
    logs = [
        LogEntry("/posts", 200, 120),
        LogEntry("/posts", 500, 80),
        LogEntry("/posts", 503, 90),
        LogEntry("/posts", 200, 100),
    ]
    assert detect_suspicious_behavior(logs) is True


def test_detection_ignores_small_sample():
    logs = [
        LogEntry("/posts", 500, 100),
        LogEntry("/posts", 200, 90),
    ]
    assert detect_suspicious_behavior(logs) is False


def test_detection_catches_high_latency():
    logs = [
        LogEntry("/users", 200, 2000),
        LogEntry("/users", 200, 2100),
        LogEntry("/users", 200, 50),
        LogEntry("/users", 200, 60),
    ]
    assert detect_suspicious_behavior(logs) is True
