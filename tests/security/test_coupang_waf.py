from http import HTTPStatus

import pytest

from qa_lab import ApiClient


@pytest.mark.network
def test_suspicious_search_query_is_blocked(api_client: ApiClient):
    response = api_client.get("/np/search", params={"q": "' OR 1=1 --"})

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert "x-reference-error" in {k.lower(): v for k, v in response.headers.items()}
