from qa_lab import ApiClient


def test_api_client_logs_http_exchange(api_client: ApiClient, fake_response, monkeypatch, capsys):
    def fake_request(method, url, timeout=None, **kwargs):
        return fake_response(status_code=403, payload={"error": "blocked"})

    monkeypatch.setattr(api_client.session, "request", fake_request)

    api_client.get("/np/search")

    captured = capsys.readouterr()
    assert "GET" in captured.out
    assert "/np/search" in captured.out
    assert "403" in captured.out
