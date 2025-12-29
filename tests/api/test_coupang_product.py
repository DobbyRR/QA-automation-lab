from http import HTTPStatus

import pytest

from qa_lab import ApiClient


@pytest.mark.network
def test_coupons_endpoint_requires_auth(api_client: ApiClient):
    response = api_client.get("/np/coupons")

    assert response.status_code in {HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN}
    headers = response.headers
    assert headers.get("Strict-Transport-Security") is not None
    assert headers.get("Content-Type") is not None


@pytest.mark.network
def test_coupons_endpoint_includes_reference_error(api_client: ApiClient):
    response = api_client.get("/np/coupons")
    headers = {k.lower(): v for k, v in response.headers.items()}

    if response.status_code == HTTPStatus.FORBIDDEN:
        assert "x-reference-error" in headers
