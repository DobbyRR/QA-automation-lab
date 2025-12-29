"""Helpers for detecting abusive call patterns."""

from collections import deque
from dataclasses import dataclass
from time import monotonic


@dataclass
class RequestSpikeDetector:
    """Detects bursts of requests in a sliding time window."""

    window_seconds: float = 1.0
    threshold: int = 5

    def __post_init__(self) -> None:
        self._events: deque[float] = deque()

    def record(self) -> int:
        """Record an event timestamp and return the count in the window."""
        now = monotonic()
        self._events.append(now)
        self._evict(now)
        return len(self._events)

    def is_spike(self) -> bool:
        """Return True if current window exceeds the configured threshold."""
        now = monotonic()
        self._evict(now)
        return len(self._events) > self.threshold

    def _evict(self, now: float) -> None:
        cutoff = now - self.window_seconds
        while self._events and self._events[0] < cutoff:
            self._events.popleft()
