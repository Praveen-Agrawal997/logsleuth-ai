
from ml_detector import LogAnomalyDetector


def test_detector_returns_one_result_per_message():
    messages = [
        "INFO application started successfully",
        "INFO request completed successfully",
        "INFO application health check passed",
        "ERROR database connection failed",
        "INFO request completed successfully",
    ]

    results = LogAnomalyDetector().detect(messages)

    assert len(results) == len(messages)
    assert all("is_anomaly" in result for result in results)
    assert all("anomaly_score" in result for result in results)


def test_detector_handles_insufficient_data():
    results = LogAnomalyDetector().detect(["Only one log entry"])

    assert len(results) == 1
    assert results[0]["ml_status"] == "Insufficient data"


def test_detector_handles_empty_input():
    assert LogAnomalyDetector().detect([]) == []
