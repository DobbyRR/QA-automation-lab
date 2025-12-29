from http import HTTPStatus

import pytest

from qa_lab import ApiClient


@pytest.mark.network
def test_cdn_logo_asset_returns_png(cdn_client: ApiClient):
    response = cdn_client.get("/image/coupang/common/logo_coupang_w350.png")

    assert response.status_code == HTTPStatus.OK
    assert "image/png" in response.headers.get("Content-Type", "")
    assert int(response.headers.get("Content-Length", "0")) > 0


@pytest.mark.network
def test_homepage_enforces_hsts_header(api_client: ApiClient):
    response = api_client.get("/")

    assert response.status_code in {
        HTTPStatus.OK,
        HTTPStatus.FORBIDDEN,
        HTTPStatus.MOVED_PERMANENTLY,
        HTTPStatus.FOUND,
    }
    hsts = response.headers.get("Strict-Transport-Security")
    assert hsts is not None and "max-age" in hsts
