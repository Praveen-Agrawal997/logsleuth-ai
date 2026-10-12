
import re

from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer


class LogAnomalyDetector:
    """Detect unusual log messages using unsupervised machine learning."""

    def __init__(self, contamination=0.10):
        self.contamination = contamination
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            token_pattern=r"(?u)\b[a-zA-Z_][a-zA-Z0-9_]+\b",
            max_features=1000,
        )
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42,
        )

    @staticmethod
    def _normalize(message):
        """Reduce noise from timestamps, IDs, IPs and numeric values."""
        message = message.lower()
        message = re.sub(
            r"\b\d{4}-\d{2}-\d{2}[ t]\d{2}:\d{2}:\d{2}\b",
            " <timestamp> ",
            message,
        )
        message = re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", " <ip> ", message)
        message = re.sub(r"\b0x[0-9a-f]+\b", " <hex> ", message)
        message = re.sub(r"\b\d+\b", " <number> ", message)
        return message.strip()

    def detect(self, messages):
        """
        Return one result per message.
        Anomaly score is relative to the messages supplied in this batch.
        """
        if not messages:
            return []

        normalized = [self._normalize(str(message)) for message in messages]

        # TF-IDF cannot fit a useful model on one message or an empty corpus.
        if len(normalized) < 3 or not any(normalized):
            return [
                {
                    "is_anomaly": False,
                    "anomaly_score": 0.0,
                    "ml_status": "Insufficient data",
                }
                for _ in messages
            ]

        try:
            features = self.vectorizer.fit_transform(normalized)

            # Identical messages contain no useful variation for this model.
            if features.shape[1] == 0 or features.nnz == 0:
                raise ValueError("No usable text features")

            self.model.fit(features)

            predictions = self.model.predict(features)
            raw_scores = self.model.decision_function(features)

            results = []
            for prediction, raw_score in zip(predictions, raw_scores):
                is_anomaly = int(prediction) == -1

                # Higher displayed values mean more anomalous.
                anomaly_score = round(
                    max(0.0, min(100.0, (0.5 - float(raw_score)) * 100)),
                    2,
                )

                results.append(
                    {
                        "is_anomaly": is_anomaly,
                        "anomaly_score": anomaly_score,
                        "ml_status": (
                            "Anomaly" if is_anomaly else "Normal"
                        ),
                    }
                )

            return results

        except ValueError:
            # Avoid crashing log analysis when the input has no usable text.
            return [
                {
                    "is_anomaly": False,
                    "anomaly_score": 0.0,
                    "ml_status": "Unable to analyze",
                }
                for _ in messages
            ]
