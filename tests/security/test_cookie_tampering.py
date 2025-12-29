from http import HTTPStatus

import pytest

from qa_lab import ApiClient


@pytest.mark.network
def test_fake_session_cookie_is_rejected(api_client: ApiClient):
    api_client.session.cookies.set("PCID", "fake-session", domain="coupang.com")
    response = api_client.get("/np/search", params={"q": "router"})

    assert response.status_code in {HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN}
    headers = {k.lower(): v for k, v in response.headers.items()}
    assert headers.get("strict-transport-security") is not None
    if response.status_code == HTTPStatus.FORBIDDEN:
        assert "x-reference-error" in headers
