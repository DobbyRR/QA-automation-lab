from http import HTTPStatus

import pytest

from qa_lab import ApiClient


@pytest.mark.network
def test_logo_asset_has_etag(cdn_client: ApiClient):
    response = cdn_client.get("/image/coupang/common/logo_coupang_w350.png")

    assert response.status_code == HTTPStatus.OK
    assert response.headers.get("ETag") is not None
    assert int(response.headers.get("Content-Length", "0")) == 7448


@pytest.mark.network
def test_logo_asset_cache_headers(cdn_client: ApiClient):
    response = cdn_client.get("/image/coupang/common/logo_coupang_w350.png")
    headers = {k.lower(): v for k, v in response.headers.items()}

    assert headers.get("strict-transport-security") is not None
    assert headers.get("referrer-policy") == "strict-origin-when-cross-origin"
    assert headers.get("x-content-type-options") == "nosniff"
    assert headers.get("x-xss-protection") is not None
