from urllib.parse import quote_plus

import pytest
from pathlib import Path


@pytest.mark.network
@pytest.mark.ui
def test_homepage_access_denied_banner(page):
    response = page.goto("https://www.coupang.com/", wait_until="domcontentloaded")

    assert response is not None
    assert response.status in {200, 403}
    content = page.content()
    assert "Access Denied" in content
    assert "Reference" in content


@pytest.mark.network
@pytest.mark.ui
def test_sqli_query_blocked_in_browser(page):
    payload = "' OR 1=1 --"
    url = f"https://www.coupang.com/np/search?q={quote_plus(payload)}"
    response = page.goto(url, wait_until="domcontentloaded")

    assert response is not None
    assert response.status in {200, 403}
    headers = {k.lower(): v for k, v in response.headers.items()}
    if response.status == 403:
        assert "x-reference-error" in headers
    assert "Access Denied" in page.content()


@pytest.mark.network
@pytest.mark.ui
def test_access_denied_screenshot_saved(page, tmp_path):
    screenshots_dir = Path("reports/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    response = page.goto("https://www.coupang.com/", wait_until="domcontentloaded")

    assert response is not None
    screenshot_path = screenshots_dir / "access_denied.png"
    page.screenshot(path=str(screenshot_path))

    assert screenshot_path.exists()
    assert screenshot_path.stat().st_size > 0
