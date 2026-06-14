from __future__ import annotations

import logging
import subprocess
import sys
import tempfile
from typing import Optional

from backend.config.config import settings
from backend.tools.types import CodeExecutionResult

logger = logging.getLogger(__name__)


def run_code_snippet(code: str, timeout: Optional[float] = None) -> CodeExecutionResult:
    """
    Execute a Python code snippet in a separate process with a timeout.

    This avoids running arbitrary code in the current process and makes
    it easier to enforce execution limits.
    """
    timeout = timeout or settings.code_execution_timeout

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    cmd = [sys.executable, tmp_path]

    logger.info("Executing code snippet via subprocess with timeout=%s", timeout)

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        success = proc.returncode == 0
        stderr = proc.stderr or ""
        stdout = proc.stdout or ""
        error_type = None
        error_message = None

        if not success and stderr:
            # Take the last line of stderr as the main error summary
            last_line = stderr.strip().splitlines()[-1]
            error_message = last_line
            if ":" in last_line:
                error_type = last_line.split(":", 1)[0].strip()

        return CodeExecutionResult(
            success=success,
            stdout=stdout,
            stderr=stderr,
            error_type=error_type,
            error_message=error_message,
            timed_out=False,
            attempts=1,
        )
    except subprocess.TimeoutExpired as exc:
        logger.warning("Code execution timed out after %s seconds", timeout)
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        return CodeExecutionResult(
            success=False,
            stdout=stdout,
            stderr=stderr,
            error_type="TimeoutExpired",
            error_message=str(exc),
            timed_out=True,
            attempts=1,
        )

