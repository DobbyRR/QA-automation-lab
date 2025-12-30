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
    first_headers = {k.lower(): v for k, v in first.headers.items()}
    second_headers = {k.lower(): v for k, v in second.headers.items()}

    assert first.status_code == second.status_code
    assert (
        ("x-reference-error" in first_headers) == ("x-reference-error" in second_headers)
    )


@pytest.mark.network
def test_session_cookie_behavior(api_client: ApiClient):
    home = api_client.get("/")
    first_cookie = api_client.session.cookies.get("PCID")

    search = api_client.get("/np/search", params={"q": "테스트"})
    second_cookie = api_client.session.cookies.get("PCID")

    assert home.status_code in {
        HTTPStatus.OK,
        HTTPStatus.MOVED_PERMANENTLY,
        HTTPStatus.FOUND,
        HTTPStatus.FORBIDDEN,
    }
    assert search.status_code in {HTTPStatus.OK, HTTPStatus.FORBIDDEN}
    if first_cookie or second_cookie:
        assert first_cookie == second_cookie
