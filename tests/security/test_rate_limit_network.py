import time

import pytest

from qa_lab import ApiClient


@pytest.mark.network
@pytest.mark.slow
def test_repeated_search_triggers_consistent_block(api_client: ApiClient):
    statuses = []
    headers_seen = []

    for _ in range(5):
        response = api_client.get("/np/search", params={"q": "' OR 1=1 --"})
        statuses.append(response.status_code)
        headers_seen.append({k.lower(): v for k, v in response.headers.items()})
        time.sleep(0.2)

    assert all(status in {401, 403} for status in statuses)
    assert any("x-reference-error" in header for header in headers_seen)
