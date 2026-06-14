import datetime as dt

from backend.config.config import Settings
from backend.tools.code.executor import run_code_snippet


def test_run_code_snippet_success():
    code = "print('hello from test')"
    result = run_code_snippet(code, timeout=2.0)
    assert result.success is True
    assert "hello from test" in result.stdout
    assert result.timed_out is False


def test_settings_defaults():
    s = Settings()
    assert isinstance(s.code_execution_timeout, float)
    assert isinstance(s.code_execution_max_retries, int)


def test_calendar_datetime_parsing_roundtrip():
    # Sanity check that datetime isoformat/parse works as expected
    now = dt.datetime.now(dt.timezone.utc)
    iso = now.isoformat()
    parsed = dt.datetime.fromisoformat(iso)
    assert parsed.replace(microsecond=0) == now.replace(microsecond=0)

