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
    referrer_policy = headers.get("referrer-policy")
    if referrer_policy is not None:
        assert referrer_policy == "strict-origin-when-cross-origin"
    xcto = headers.get("x-content-type-options")
    if xcto is not None:
        assert xcto == "nosniff"
    x_xss = headers.get("x-xss-protection")
    if x_xss is not None:
        assert "mode=block" in x_xss or x_xss == "1"
