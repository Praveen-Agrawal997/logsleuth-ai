# LogSleuth AI 🔍

**AI-Powered Log Analysis and Incident Triage Dashboard**

LogSleuth AI is a Python-based web application that analyzes application logs, identifies recurring errors, detects unusual log entries using machine learning, and provides rule-based root-cause suggestions to support incident investigation.

## 🚀 Features

- **Log Analysis:** Parse log entries and identify severity levels such as ERROR, CRITICAL, WARNING, INFO, and DEBUG.
- **Incident Grouping:** Group repeated errors and highlight frequently occurring issues.
- **ML Anomaly Detection:** Use TF-IDF text features and Isolation Forest to flag unusual log messages.
- **Root-Cause Suggestions:** Provide possible causes and suggested investigation steps using rule-based logic.
- **Risk Assessment:** Classify incidents into HIGH, MEDIUM, and LOW risk levels.
- **System Health Score:** Calculate a basic health score from error and warning counts.
- **Interactive Dashboard:** View severity distribution, incidents, and log timelines.
- **Search and Filters:** Search log messages and filter entries by severity or ML anomaly status.
- **File Upload:** Analyze `.log` and `.txt` files up to 2 MB.
- **Report Export:** Download analysis reports in JSON and CSV formats.
- **Sample Logs:** Download sample logs for testing.

## 🛠️ Technology Stack

- Python
- Flask
- scikit-learn
- TF-IDF Vectorization
- Isolation Forest
- HTML and CSS
- Bootstrap 5
- JavaScript
- Chart.js
- pytest

## 📁 Project Structure

```text
logsleuth-ai/
├── app.py
├── analyzer.py
├── ml_detector.py
├── root_cause.py
├── test_analyzer.py
├── test_root_cause.py
├── test_ml_detector.py
├── requirements.txt
├── README.md
├── .gitignore
└── templates/
    └── index.html
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd logsleuth-ai
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows Command Prompt:**

```bat
venv\Scripts\activate
```

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

Open this address in your browser:

```text
http://127.0.0.1:5000
```

## 🧪 Run Tests

Run the project's automated tests using:

```bash
python -m pytest -v
```

The current development test suite contains 12 passing tests.

## 🤖 How Anomaly Detection Works

1. Log messages are normalized to reduce variation from timestamps, IP addresses, and numeric values.
2. TF-IDF converts log text into numerical features.
3. Isolation Forest identifies messages that appear unusual within the submitted batch.
4. The dashboard displays anomaly flags and relative anomaly scores.

**Note:** Anomaly scores are relative indicators, not calibrated probabilities. Results depend on the log entries supplied in each analysis batch.

## 🔎 Root-Cause Suggestions

The application uses rule-based matching to suggest possible causes and investigation steps for recognized patterns such as database failures, timeouts, memory issues, permission errors, connection failures, and authentication problems.

These suggestions are intended to assist investigation; they do not confirm the actual root cause.

## 📊 Reports

LogSleuth AI supports:

- **JSON:** Summary metrics, incidents, ML anomaly information, and the log timeline.
- **CSV:** Structured incident details, risk levels, root-cause suggestions, and ML anomaly fields.

## 🔐 Limitations

- ML anomaly detection is unsupervised and operates on the submitted batch rather than a pretrained production model.
- Root-cause suggestions are rule-based and may not cover every error pattern.
- The health score is a simple heuristic, not a complete measure of system reliability.
- The application is a development project and should be security-reviewed before production deployment.

## 🔮 Future Improvements

- Historical log analysis and baseline learning
- More advanced log parsing
- Configurable anomaly thresholds
- Improved root-cause correlation
- Authentication and role-based access
- Deployment with production-ready configuration

## 👨‍💻 Author

**Praveen Agrawal**

---

*Built as a project in Python, web development, and machine-learning-assisted log analysis.*