from __future__ import annotations

import logging
from typing import Any, Dict

from backend.config import settings
from backend.tools.code.executor import run_code_snippet

logger = logging.getLogger(__name__)


def code_tool(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Advanced code execution tool.

    Expected payload:
      - language: currently only 'python' is supported
      - code: str

    Behavior:
      - Executes the code in a subprocess with a timeout.
      - Automatically retries up to CODE_EXECUTION_MAX_RETRIES times
        in case of transient failures.
      - Returns a structured result plus a human-readable explanation.
    """
    language = str(payload.get("language") or "python").lower()
    if language != "python":
        raise ValueError(f"Unsupported language: {language!r}. Only 'python' is supported.")

    code = str(payload.get("code") or "")
    if not code.strip():
        raise ValueError("code must be a non-empty string.")

    max_retries = max(1, settings.code_execution_max_retries)
    timeout = settings.code_execution_timeout

    attempts = 0
    last_result = None

    for attempt in range(1, max_retries + 1):
        attempts = attempt
        logger.info("Executing code attempt %d/%d", attempt, max_retries)
        result = run_code_snippet(code, timeout=timeout)
        result.attempts = attempt
        last_result = result

        if result.success:
            break

        # For now, retry without modification; this is mainly to handle
        # transient issues (e.g., I/O or environment flakiness).
        if attempt < max_retries:
            logger.info("Code execution failed, will retry. error=%s", result.error_message)

    assert last_result is not None

    explanation_parts = []

    if last_result.success:
        explanation_parts.append(
            f"Code executed successfully in {attempts} attempt(s)."
        )
        if last_result.stdout.strip():
            explanation_parts.append("Standard output was captured.")
        if last_result.stderr.strip():
            explanation_parts.append("There were messages on standard error, but the exit code was 0.")
    else:
        explanation_parts.append(
            f"Code failed after {attempts} attempt(s)."
        )
        if last_result.error_type or last_result.error_message:
            explanation_parts.append(
                f"Last error: {last_result.error_type or 'Error'} - {last_result.error_message or ''}".strip()
            )
        if last_result.timed_out:
            explanation_parts.append(
                "Execution timed out. Consider reducing work done or increasing the timeout."
            )

    explanation = " ".join(explanation_parts)

    return {
        "ok": last_result.success,
        "attempts": attempts,
        "timeout_seconds": timeout,
        "result": {
            "success": last_result.success,
            "stdout": last_result.stdout,
            "stderr": last_result.stderr,
            "error_type": last_result.error_type,
            "error_message": last_result.error_message,
            "timed_out": last_result.timed_out,
            "attempts": last_result.attempts,
        },
        "explanation": explanation,
    }

