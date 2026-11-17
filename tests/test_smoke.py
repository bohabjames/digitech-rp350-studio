"""Smoke test proving the test workflow runs.

pytest exits with an error when it collects no tests, so CI needs at least one.
Delete this file once real tests exist.
"""


def test_pytest_runs() -> None:
    assert 1 + 1 == 2
