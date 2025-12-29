from http import HTTPStatus

import pytest

from qa_lab import ApiClient


@pytest.mark.network
def test_search_returns_reference_error_header(api_client: ApiClient):
    response = api_client.get("/np/search", params={"q": "마스크"})
    headers = response.headers

    assert response.status_code in {HTTPStatus.OK, HTTPStatus.FORBIDDEN}
    if response.status_code == HTTPStatus.FORBIDDEN:
        assert headers.get("X-Reference-Error") is not None


@pytest.mark.network
def test_search_response_has_hsts(api_client: ApiClient):
    response = api_client.get("/np/search", params={"q": "노트북"})
    headers = response.headers

    assert headers.get("Strict-Transport-Security") is not None
    assert int(headers.get("Content-Length", "0")) > 0


@pytest.mark.network
def test_repeated_search_has_consistent_status(api_client: ApiClient):
    first = api_client.get("/np/search", params={"q": "' OR 1=1 --"})
    second = api_client.get("/np/search", params={"q": "' OR 1=1 --"})

    assert first.status_code == second.status_code
