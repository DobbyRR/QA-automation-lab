from qa_lab.utils.rate_limit import RequestSpikeDetector


def test_spike_detector_flags_burst(monkeypatch):
    detector = RequestSpikeDetector(window_seconds=1, threshold=3)
    timeline = iter([0.0, 0.1, 0.2, 0.3, 2.0, 2.1])

    monkeypatch.setattr("qa_lab.utils.rate_limit.monotonic", lambda: next(timeline))

    counts = [detector.record() for _ in range(4)]
    # advance time beyond window to ensure eviction works
    detector.record()

    assert counts[-1] == 4
    assert detector.is_spike() is False


def test_spike_detector_threshold(monkeypatch):
    detector = RequestSpikeDetector(window_seconds=2, threshold=2)
    timeline = (i * 0.5 for i in range(5))
    monkeypatch.setattr("qa_lab.utils.rate_limit.monotonic", lambda: next(timeline))

    for _ in range(3):
        detector.record()
    assert detector.is_spike() is True
