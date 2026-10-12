
import csv
import io

import json
from flask import Response

from flask import Flask, render_template, request
from analyzer import analyze_log

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB limit

@app.route("/sample-logs")
def sample_logs():
    sample_data = """2026-10-12 10:00:01 INFO Server started successfully
2026-10-12 10:01:02 WARNING High response time detected
2026-10-12 10:01:05 ERROR Database connection failed
2026-10-12 10:01:08 ERROR Database connection failed
2026-10-12 10:02:00 CRITICAL Memory usage exceeded threshold
2026-10-12 10:03:00 INFO Health check completed"""

    return Response(
        sample_data,
        mimetype="text/plain",
        headers={
            "Content-Disposition": "attachment; filename=sample_logs.log"
        }
    )


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    log_text = ""

    if request.method == "POST":
        uploaded_file = request.files.get("log_file")
        pasted_text = request.form.get("log_text", "")

        if uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename.lower()

            if not filename.endswith((".log", ".txt")):
                error = "Please upload a .log or .txt file."
            else:
                try:
                    log_text = uploaded_file.read().decode("utf-8-sig")
                except UnicodeDecodeError:
                    error = "The file must use UTF-8 text encoding."
        else:
            log_text = pasted_text

        if not error:
            if not log_text.strip():
                error = "Please upload a log file or paste some log text."
            else:
                result = analyze_log(log_text)

    return render_template(
        "index.html",
        result=result,
        error=error,
        log_text=log_text
    )


@app.route("/export", methods=["POST"])
def export_report():
    uploaded_file = request.files.get("log_file")
    pasted_text = request.form.get("log_text", "")

    if uploaded_file and uploaded_file.filename:
        filename = uploaded_file.filename.lower()

        if not filename.endswith((".log", ".txt")):
            return "Please upload a .log or .txt file.", 400

        try:
            log_text = uploaded_file.read().decode("utf-8-sig")
        except UnicodeDecodeError:
            return "The file must use UTF-8 text encoding.", 400
    else:
        log_text = pasted_text

    if not log_text.strip():
        return "Please provide log text or upload a log file.", 400

    result = analyze_log(log_text)

    
    anomaly_logs = [
        log for log in result["logs"]
        if log.get("is_anomaly", False)
    ]

    report = {
        "project": "LogSleuth AI",
        "detection_method": "TF-IDF + Isolation Forest",
        "root_cause_method": "Rule-based",
        "total_lines": result["total_lines"],
        "health_score": result["health_score"],
        "health_status": result["health_status"],
        "severity_counts": result["severity_counts"],
        "ml_summary": {
            "total_anomalies": len(anomaly_logs),
            "anomaly_detection_type": "Unsupervised ML",
            "note": (
                "Anomaly scores are relative indicators, "
                "not probabilities."
            )
        },
        "incidents": result["top_errors"],
        "timeline": result["logs"]
    }


    return Response(
        json.dumps(report, indent=2),
        mimetype="application/json",
        headers={
            "Content-Disposition":
                "attachment; filename=logsleuth-report.json"
        }
    )


@app.route("/export/csv", methods=["POST"])
def export_csv():
    uploaded_file = request.files.get("log_file")
    pasted_text = request.form.get("log_text", "")

    if uploaded_file and uploaded_file.filename:
        filename = uploaded_file.filename.lower()

        if not filename.endswith((".log", ".txt")):
            return "Please upload a .log or .txt file.", 400

        try:
            log_text = uploaded_file.read().decode("utf-8-sig")
        except UnicodeDecodeError:
            return "The file must use UTF-8 text encoding.", 400
    else:
        log_text = pasted_text

    if not log_text.strip():
        return "Please provide log text or upload a log file.", 400

    result = analyze_log(log_text)

    output = io.StringIO()
    writer = csv.writer(output)

    
    writer.writerow([
        "Incident ID",
        "Severity",
        "Risk Level",
        "Message",
        "Occurrences",
        "Possible Cause",
        "Suggested Investigation",
        "ML Anomaly Detected",
        "ML Flagged Occurrences",
        "ML Anomaly Score"
    ])


    
    for incident in result["top_errors"]:
        writer.writerow([
            incident["incident_id"],
            incident["severity"],
            incident["risk_level"],
            incident["message"],
            incident["count"],
            incident["possible_cause"],
            incident["suggested_action"],
            incident.get("ml_anomaly_detected", False),
            incident.get("ml_anomaly_count", 0),
            incident.get("ml_anomaly_score", 0.0)
        ])


    return Response(
        "\ufeff" + output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={
            "Content-Disposition":
                "attachment; filename=logsleuth-report.csv"
        }
    )


@app.errorhandler(413)
def file_too_large(error):
    return "File too large. Please upload a file smaller than 2 MB.", 413


if __name__ == "__main__":
    app.run(debug=True)
