
from root_cause import suggest_root_cause


def test_database_error():
    cause, action = suggest_root_cause(
        "Database connection failed"
    )
    assert cause
    assert action


def test_timeout_error():
    cause, action = suggest_root_cause(
        "Request timeout"
    )
    assert cause
    assert action


def test_memory_error():
    cause, action = suggest_root_cause(
        "Out of memory error"
    )
    assert cause
    assert action


def test_permission_error():
    cause, action = suggest_root_cause(
        "Permission denied"
    )
    assert cause
    assert action


def test_unknown_error():
    cause, action = suggest_root_cause(
        "Something unusual happened"
    )
    assert cause
    assert action
