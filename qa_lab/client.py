"""Simple API client wrapper used across tests."""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from .config import Settings, get_settings
from .utils.logging import log_http_exchange


class ApiClient:
    """Thin wrapper around ``requests.Session`` with project defaults."""

    def __init__(
        self,
        settings: Optional[Settings] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.session = session or requests.Session()
        self.session.headers["User-Agent"] = self.settings.user_agent

    def build_url(self, path: str) -> str:
        path = path.lstrip("/")
        return f"{self.settings.base_url}/{path}"

    def request(
        self,
        method: str,
        path: str,
        *,
        timeout: Optional[float] = None,
        **kwargs: Any,
    ) -> requests.Response:
        url = self.build_url(path)
        timeout = timeout or self.settings.timeout
        response = self.session.request(method, url, timeout=timeout, **kwargs)
        log_http_exchange(method, url, response.status_code, kwargs.get("json"))
        return response

    def get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self.request("GET", path, params=params)

    def post(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self.request("POST", path, json=json)
