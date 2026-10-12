
def suggest_root_cause(message):
    text = message.lower()

    rules = [
        {
            "keywords": ["database", "sql", "postgres", "mysql"],
            "cause": "Database service unavailable, incorrect connection settings, or connectivity issues.",
            "action": "Check database status, host, port, credentials, and network access."
        },
        {
            "keywords": ["timeout", "timed out"],
            "cause": "A request or operation exceeded its allowed time.",
            "action": "Inspect response times, network latency, service load, and timeout configuration."
        },
        {
            "keywords": ["memory", "out of memory", "oom"],
            "cause": "The application or system may be running low on memory.",
            "action": "Check memory usage, application memory leaks, and system resource limits."
        },
        {
            "keywords": ["permission denied", "access denied", "forbidden"],
            "cause": "The process may lack the required permissions or access rights.",
            "action": "Review user permissions, file access rights, roles, and access policies."
        },
        {
            "keywords": ["connection refused", "connection reset"],
            "cause": "The remote service may be unavailable or rejecting the connection.",
            "action": "Verify service status, host and port, firewall rules, and network connectivity."
        },
        {
            "keywords": ["file not found", "no such file"],
            "cause": "A required file or configured path may be missing or incorrect.",
            "action": "Verify the file path, file existence, deployment package, and access permissions."
        },
        {
            "keywords": ["authentication", "unauthorized", "invalid token"],
            "cause": "Authentication credentials or token validation may have failed.",
            "action": "Check credentials, token expiry, authentication configuration, and system clock."
        },
        {
            "keywords": ["rate limit", "too many requests", "429"],
            "cause": "A service may be receiving requests above its allowed rate.",
            "action": "Review request frequency, rate limits, retry policies, and backoff handling."
        }
    ]

    for rule in rules:
        if any(keyword in text for keyword in rule["keywords"]):
            return {
                "cause": rule["cause"],
                "action": rule["action"]
            }

    return {
        "cause": "No matching rule was found for this error.",
        "action": "Inspect surrounding log entries, stack traces, recent deployments, and application configuration."
    }
