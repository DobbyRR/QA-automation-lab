import json

from qa_lab.utils.log_summary import summarize_log_file


def test_log_summary_counts_and_suspicious(tmp_path):
    log_path = tmp_path / "http.log"
    entries = [
        {
            "timestamp": "2025-12-30T00:00:00Z",
            "method": "GET",
            "url": "https://example.com/ok",
            "status": 200,
            "payload": None,
        },
        {
            "timestamp": "2025-12-30T00:00:01Z",
            "method": "GET",
            "url": "https://example.com/blocked",
            "status": 403,
            "payload": None,
        },
        {
            "timestamp": "2025-12-30T00:00:02Z",
            "method": "GET",
            "url": "https://example.com/search",
            "status": 200,
            "payload": {"q": "' OR 1=1 --"},
        },
    ]
    with log_path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry) + "\n")

    summary = summarize_log_file(log_path)

    assert summary["total"] == 3
    assert summary["status_counts"][200] == 2
    assert summary["status_counts"][403] == 1
    suspicious_entries = summary["suspicious"]
    assert len(suspicious_entries) == 2
    assert any(entry["status"] == 403 for entry in suspicious_entries)
    assert any("' or 1=1" in json.dumps(entry["payload"]).lower() for entry in suspicious_entries)
