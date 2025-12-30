"""Helpers for summarizing QA_LAB_LOG_PATH HTTP logs."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

SUSPICIOUS_PATTERNS = ("' or 1=1", "union select", "../")


def load_http_log(path: Path) -> List[Dict[str, Any]]:
    """Load newline-delimited JSON log entries."""
    entries: List[Dict[str, Any]] = []
    if not path.exists():
        return entries
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def summarize_entries(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Return counts and suspicious entries derived from log entries."""
    status_counts = Counter(entry.get("status") for entry in entries)
    suspicious = [entry for entry in entries if _is_suspicious(entry)]
    return {
        "total": len(entries),
        "status_counts": {k: v for k, v in status_counts.items() if k is not None},
        "suspicious": suspicious,
    }


def summarize_log_file(path_or_str: str | Path) -> Dict[str, Any]:
    """Convenience helper that loads the log and summarizes it."""
    path = Path(path_or_str)
    return summarize_entries(load_http_log(path))


def _is_suspicious(entry: Dict[str, Any]) -> bool:
    status = entry.get("status")
    if isinstance(status, int) and status >= 400:
        return True
    payload = entry.get("payload")
    payload_text = ""
    if isinstance(payload, str):
        payload_text = payload.lower()
    elif isinstance(payload, dict):
        payload_text = json.dumps(payload).lower()
    return any(pattern in payload_text for pattern in SUSPICIOUS_PATTERNS)


if __name__ == "__main__":
    import argparse
    from pprint import pprint

    parser = argparse.ArgumentParser(description="Summarize QA_LAB HTTP logs.")
    parser.add_argument("log_path", help="Path to QA_LAB_LOG_PATH JSONL file")
    args = parser.parse_args()
    pprint(summarize_log_file(args.log_path))
