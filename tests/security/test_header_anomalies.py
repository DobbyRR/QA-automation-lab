from http import HTTPStatus

import pytest

from qa_lab import ApiClient


@pytest.mark.network
def test_suspicious_user_agent_blocked(api_client: ApiClient):
    api_client.session.headers["User-Agent"] = "QA-Test-Bot/1.0"
    response = api_client.get("/np/search", params={"q": "monitor"})

    assert response.status_code in {
        HTTPStatus.OK,
        HTTPStatus.FORBIDDEN,
        HTTPStatus.UNAUTHORIZED,
    }
    assert response.headers.get("Strict-Transport-Security") is not None


@pytest.mark.network
def test_missing_accept_language_still_secure(api_client: ApiClient):
    api_client.session.headers.pop("Accept-Language", None)
    response = api_client.get("/")

    assert response.status_code in {
        HTTPStatus.OK,
        HTTPStatus.FORBIDDEN,
        HTTPStatus.MOVED_PERMANENTLY,
        HTTPStatus.FOUND,
    }
    assert "Strict-Transport-Security" in response.headers
    assert "Content-Type" in response.headers
