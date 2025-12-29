"""Detection helpers that map behaviors to MITRE ATT&CK tactics."""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

SUSPICIOUS_PATTERNS = ("' or 1=1", "union select", "sleep(", "../", "%27%20or%201%3d1")
RESTRICTED_PATHS = ("/np/coupons", "/np/member", "/membership", "/np/my/orders")


@dataclass
class LogEvent:
    timestamp: float
    path: str
    status_code: int
    latency_ms: int
    params: Optional[Dict[str, str]] = None
    user_agent: str = ""


@dataclass
class DetectionResult:
    tactic: str
    technique: str
    alert: bool
    reason: str


def detect_discovery_enumeration(
    events: Iterable[LogEvent], *, window_seconds: float = 2.0, threshold: int = 5
) -> DetectionResult:
    """Detects Discovery (MITRE tactic) enumeration spikes."""
    sorted_events: List[LogEvent] = sorted(events, key=lambda e: e.timestamp)
    suspicious = False
    for idx, event in enumerate(sorted_events):
        window_end = event.timestamp + window_seconds
        count = sum(
            1
            for candidate in sorted_events[idx:]
            if candidate.timestamp <= window_end and candidate.path.startswith("/np/search")
        )
        if count >= threshold:
            suspicious = True
            reason = (
                f"{count} search requests within {window_seconds}s "
                f"(threshold={threshold})"
            )
            break
    else:
        reason = "No enumeration spike detected"

    return DetectionResult(
        tactic="Discovery",
        technique="T1046",
        alert=suspicious,
        reason=reason,
    )


def detect_exploit_attempts(events: Iterable[LogEvent]) -> DetectionResult:
    """Detect Exploit Public-Facing Application attempts (MITRE T1190, Initial Access)."""
    matches = [
        event
        for event in events
        if event.params
        and any(
            pattern in event.params.get("q", "").lower()
            for pattern in SUSPICIOUS_PATTERNS
        )
    ]
    if matches:
        reason = f"Suspicious payload detected: {matches[0].params.get('q')}"
    else:
        reason = "No exploit payload detected"
    return DetectionResult(
        tactic="Credential Access",
        technique="T1190",
        alert=bool(matches),
        reason=reason,
    )


def detect_restricted_resource_access(events: Iterable[LogEvent]) -> DetectionResult:
    """Detect Reconnaissance / Credential Access attempts on restricted endpoints."""
    hits = [
        event
        for event in events
        if event.path in RESTRICTED_PATHS and event.status_code in (401, 403)
    ]
    if hits:
        reason = f"{hits[0].path} returned {hits[0].status_code}"
    else:
        reason = "No restricted resource access detected"
    return DetectionResult(
        tactic="Reconnaissance",
        technique="T1595",
        alert=bool(hits),
        reason=reason,
    )


def detect_latency_spike(
    events: Iterable[LogEvent], *, latency_threshold: int = 1500, consecutive: int = 2
) -> DetectionResult:
    """Detect Impact (service degradation) based on latency spikes."""
    sorted_events: List[LogEvent] = sorted(events, key=lambda e: e.timestamp)
    streak = 0
    for event in sorted_events:
        if event.latency_ms >= latency_threshold:
            streak += 1
            if streak >= consecutive:
                return DetectionResult(
                    tactic="Impact",
                    technique="T1499",
                    alert=True,
                    reason=f"{streak} consecutive latency spikes >= {latency_threshold}ms",
                )
        else:
            streak = 0
    return DetectionResult(
        tactic="Impact",
        technique="T1499",
        alert=False,
        reason="Latency within acceptable range",
    )
