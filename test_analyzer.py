
from analyzer import analyze_log


def test_severity_counts():
    logs = """INFO Server started
WARNING High response time
ERROR Database connection failed"""

    result = analyze_log(logs)

    assert result["severity_counts"]["INFO"] == 1
    assert result["severity_counts"]["WARNING"] == 1
    assert result["severity_counts"]["ERROR"] == 1


def test_total_lines():
    logs = """INFO Server started
ERROR Database failed
WARNING Slow response"""

    result = analyze_log(logs)

    assert result["total_lines"] == 3


def test_repeated_errors_are_grouped():
    logs = """ERROR Database connection failed
ERROR Database connection failed
ERROR Database connection failed"""

    result = analyze_log(logs)

    assert len(result["top_errors"]) == 1
    assert result["top_errors"][0]["count"] == 3


def test_health_score():
    logs = """INFO Server started
ERROR Database connection failed
WARNING High response time"""

    result = analyze_log(logs)

    assert result["health_score"] == 87
    assert result["health_status"] == "Healthy"
