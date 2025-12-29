import json

from qa_lab import ApiClient


def test_http_log_written_to_file(monkeypatch, tmp_path, api_client: ApiClient, fake_response):
    log_path = tmp_path / "http.log"
    monkeypatch.setenv("QA_LAB_LOG_PATH", str(log_path))

    def fake_request(method, url, timeout=None, **kwargs):
        return fake_response(status_code=403, payload={"error": "blocked"})

    monkeypatch.setattr(api_client.session, "request", fake_request)

    api_client.get("/np/search")

    data = [json.loads(line) for line in log_path.read_text().splitlines() if line]
    assert data
    last_entry = data[-1]
    assert last_entry["method"] == "GET"
    assert last_entry["status"] == 403
