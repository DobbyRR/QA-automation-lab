from http import HTTPStatus

import pytest

from qa_lab import ApiClient


@pytest.mark.network
def test_css_sentinel_asset_has_etag(cdn_client: ApiClient):
    """Monitor an accessible CDN asset as a CSS sentinel."""
    response = cdn_client.get(
        "/image/coupang/common/logo_coupang_w350.png", params={"variant": "css"}
    )
    headers = {k.lower(): v for k, v in response.headers.items()}

    assert response.status_code == HTTPStatus.OK
    assert headers.get("content-type") == "image/png"
    assert headers.get("etag") is not None
    assert int(headers.get("content-length", "0")) > 0
    assert headers.get("strict-transport-security") is not None


@pytest.mark.network
def test_sprite_asset_on_mirror_has_expected_headers(cdn_mirror_client: ApiClient):
    """Validate the img1a CDN mirror asset (sprite sentinel)."""
    response = cdn_mirror_client.get("/image/coupang/common/logo_coupang_w350.png")
    headers = {k.lower(): v for k, v in response.headers.items()}

    assert response.status_code == HTTPStatus.OK
    assert headers.get("etag") is not None
    assert int(headers.get("content-length", "0")) > 0
    assert headers.get("strict-transport-security") is not None
    assert headers.get("x-content-type-options") is not None
