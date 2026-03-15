import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# ── Load .env early so all os.getenv() calls below see the values ────────────
_backend_dir = Path(__file__).resolve().parent          # .../agentic_ai_project/backend
_jarvis_dir  = _backend_dir.parent / "jarvis_ai"        # .../agentic_ai_project/jarvis_ai
_env_path    = _jarvis_dir / ".env"
load_dotenv(dotenv_path=_env_path, override=True)
# ─────────────────────────────────────────────────────────────────────────────


def _get_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _resolve_path(value: Optional[str]) -> Optional[str]:
    """
    If value is a bare filename (e.g. 'credentials.json'), resolve it
    relative to the jarvis_ai/ directory so it works regardless of cwd.
    If value is already absolute, return it unchanged.
    If value is None, return None.
    """
    if not value:
        return None
    p = Path(value)
    if p.is_absolute():
        return str(p)
    # Resolve relative to jarvis_ai/ where the .env and credential files live
    resolved = _jarvis_dir / p
    return str(resolved)


@dataclass
class Settings:
    """
    Central configuration for external APIs and feature flags.
    All values are loaded from environment variables to keep the
    code cloud-friendly and deployment-agnostic.
    """
    # Google Calendar — accept both _FILE and _PATH suffixes, resolve to absolute path
    google_credentials_path: Optional[str] = field(default=None)
    google_token_path: Optional[str] = field(default=None)

    # Research / Tavily
    tavily_api_key: Optional[str] = field(default=None)

    # Code execution
    code_execution_timeout: float = field(default=10.0)
    code_execution_max_retries: int = field(default=1)

    # Feature flags
    enable_google_calendar: bool = field(default=False)
    enable_advanced_code_tool: bool = field(default=False)
    enable_advanced_research_tool: bool = field(default=False)

    def __post_init__(self):
        # Credentials — support both GOOGLE_CREDENTIALS_FILE and GOOGLE_CREDENTIALS_PATH
        raw_creds = os.getenv("GOOGLE_CREDENTIALS_FILE") or os.getenv("GOOGLE_CREDENTIALS_PATH")
        self.google_credentials_path = _resolve_path(raw_creds)

        # Token — support both GOOGLE_TOKEN_FILE and GOOGLE_TOKEN_PATH
        raw_token = os.getenv("GOOGLE_TOKEN_FILE") or os.getenv("GOOGLE_TOKEN_PATH", "token.json")
        self.google_token_path = _resolve_path(raw_token)

        self.tavily_api_key = os.getenv("TAVILY_API_KEY")

        self.code_execution_timeout = float(os.getenv("CODE_EXECUTION_TIMEOUT", "10.0"))
        self.code_execution_max_retries = int(os.getenv("CODE_EXECUTION_MAX_RETRIES", "1"))

        self.enable_google_calendar      = _get_bool("ENABLE_GOOGLE_CALENDAR", False)
        self.enable_advanced_code_tool   = _get_bool("ENABLE_ADVANCED_CODE_TOOL", False)
        self.enable_advanced_research_tool = _get_bool("ENABLE_ADVANCED_RESEARCH_TOOL", False)


settings = Settings()