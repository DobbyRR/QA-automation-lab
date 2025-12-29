import json
from typing import Any, Dict, Optional

import pytest
import requests

from qa_lab import ApiClient
from qa_lab.config import Settings, get_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Session-scoped runtime settings for the Coupang endpoints."""
    return get_settings()


@pytest.fixture
def api_client(settings: Settings) -> ApiClient:
    """Provide an ApiClient instance for Coupang web requests."""
    return ApiClient(settings=settings)


@pytest.fixture
def cdn_client(settings: Settings) -> ApiClient:
    """ApiClient configured to talk to the Coupang CDN."""
    return ApiClient(settings=settings.for_cdn())


@pytest.fixture
def fake_response():
    """Factory to build ``requests.Response`` objects without HTTP calls."""

    def _factory(
        status_code: int = 200,
        payload: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        response = requests.Response()
        response.status_code = status_code
        response._content = json.dumps(payload or {}).encode("utf-8")
        response.headers["Content-Type"] = "application/json"
        return response

    return _factory
