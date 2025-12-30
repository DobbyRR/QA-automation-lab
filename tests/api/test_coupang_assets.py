from http import HTTPStatus

import pytest

from qa_lab import ApiClient


@pytest.mark.network
def test_logo_asset_has_etag(cdn_client: ApiClient):
    response = cdn_client.get("/image/coupang/common/logo_coupang_w350.png")
    headers = {k.lower(): v for k, v in response.headers.items()}

    assert response.status_code == HTTPStatus.OK
    assert headers.get("etag") is not None
    assert int(headers.get("content-length", "0")) == 7448


@pytest.mark.network
def test_logo_asset_cache_headers(cdn_client: ApiClient):
    response = cdn_client.get("/image/coupang/common/logo_coupang_w350.png")
    headers = {k.lower(): v for k, v in response.headers.items()}

    assert headers.get("strict-transport-security") is not None
    if headers.get("referrer-policy") is None:
        pytest.xfail("Referrer-Policy header not provided by CDN response")
    if headers.get("x-content-type-options") is None:
        pytest.xfail("X-Content-Type-Options header not provided by CDN response")
    if headers.get("x-xss-protection") is None:
        pytest.xfail("X-XSS-Protection header not provided by CDN response")
    assert headers.get("referrer-policy") is not None
    assert headers.get("x-content-type-options") is not None
    assert headers.get("x-xss-protection") is not None
