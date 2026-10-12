
from root_cause import suggest_root_cause
from ml_detector import LogAnomalyDetector
from collections import Counter, defaultdict
import re


def analyze_log(text):
    lines = text.splitlines()

    severity_counts = Counter()
    error_counts = Counter()
    parsed_logs = []

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        match = re.search(
            r"\b(CRITICAL|FATAL|ERROR|WARNING|WARN|INFO|DEBUG)\b",
            line,
            re.IGNORECASE
        )

        severity = match.group(1).upper() if match else "UNKNOWN"

        if severity == "WARN":
            severity = "WARNING"

        severity_counts[severity] += 1
        message = line.strip()

        timestamp_match = re.search(
            r"\b\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}\b",
            message
        )

        timestamp = (
            timestamp_match.group(0)
            if timestamp_match else "Unknown"
        )

        # Normalize timestamped messages for grouping.
        normalized_message = re.sub(
            r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s+",
            "",
            message
        )

        if severity in ("ERROR", "CRITICAL", "FATAL"):
            error_counts[(severity, normalized_message)] += 1

        parsed_logs.append({
            "line": line_number,
            "timestamp": timestamp,
            "severity": severity,
            "message": message,
            "is_anomaly": False,
            "anomaly_score": 0.0,
            "ml_status": "Pending"
        })

    # Run ML anomaly detection on all non-empty log entries.
    detector = LogAnomalyDetector()
    ml_results = detector.detect(
        [log["message"] for log in parsed_logs]
    )

    # Attach ML results to the corresponding timeline entries.
    anomaly_counts = Counter()
    anomaly_scores = defaultdict(list)

    for log, ml_result in zip(parsed_logs, ml_results):
        log.update(ml_result)

        normalized_message = re.sub(
            r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s+",
            "",
            log["message"]
        )

        key = (log["severity"], normalized_message)

        if log["is_anomaly"]:
            anomaly_counts[key] += 1

        anomaly_scores[key].append(log["anomaly_score"])

    # Preserve existing incident grouping and risk rules.
    incidents = []

    for index, ((severity, message), count) in enumerate(
        error_counts.most_common(10), start=1
    ):
        if severity in ("CRITICAL", "FATAL") or count >= 5:
            risk_level = "HIGH"
        elif count >= 2 or severity == "ERROR":
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        cause_info = suggest_root_cause(message)
        key = (severity, message)

        scores = anomaly_scores.get(key, [])

        incidents.append({
            "incident_id": f"INC-{index:03d}",
            "severity": severity,
            "message": message,
            "count": count,
            "risk_level": risk_level,
            "possible_cause": cause_info["cause"],
            "suggested_action": cause_info["action"],

            # New ML fields.
            "ml_anomaly_detected": anomaly_counts[key] > 0,
            "ml_anomaly_count": anomaly_counts[key],
            "ml_anomaly_score": round(max(scores), 2) if scores else 0.0
        })

    error_count = (
        severity_counts.get("ERROR", 0)
        + severity_counts.get("CRITICAL", 0)
        + severity_counts.get("FATAL", 0)
    )

    warning_count = severity_counts.get("WARNING", 0)

    health_score = max(
        0,
        100 - (error_count * 10) - (warning_count * 3)
    )

    if health_score >= 80:
        health_status = "Healthy"
    elif health_score >= 50:
        health_status = "Needs Attention"
    else:
        health_status = "Critical"

    return {
        "health_status": health_status,
        "health_score": health_score,
        "total_lines": len(parsed_logs),
        "severity_counts": dict(severity_counts),
        "top_errors": incidents,
        "logs": parsed_logs
    }
