"""Minimal logging helpers for HTTP exchanges."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

LOG_PATH_ENV = "QA_LAB_LOG_PATH"


def log_http_exchange(method: str, url: str, status: int, payload: Optional[Any]) -> None:
    """Log HTTP call metadata to stdout and optional JSON log file."""
    timestamp = datetime.utcnow().isoformat()
    record = {
        "timestamp": timestamp,
        "method": method.upper(),
        "url": url,
        "status": status,
        "payload": payload,
    }
    print(f"[{timestamp}] {method.upper()} {url} -> {status}")
    log_path = os.getenv(LOG_PATH_ENV)
    if log_path:
        path = Path(log_path)
        if not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
