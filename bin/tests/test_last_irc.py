import pytest

from binmodules.last_irc import parse_logs


LOGS = [
    "hi chris\nHi cpete",
    "hey cpete\nhey chris",
]


@pytest.mark.parametrize(
    "logs, queries, expected", [
        (LOGS, ["chris"], ["hi chris", "hey chris"]),
        (LOGS, ["cpete"], ["Hi cpete", "hey cpete"]),
    ])
def test_parse_logs(logs, queries, expected):
    assert expected == parse_logs(queries, logs)
