"""Application settings, read from environment variables.

Secrets are supplied by Doppler (`doppler run`) in development and by the
host's environment in production (ADR-0017).
"""

import os
from collections.abc import Mapping
from dataclasses import dataclass, field

DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///data/tiebreaker.db"


@dataclass(frozen=True)
class Settings:
    """Settings the application needs to run.

    Attributes:
        secret_key: secret used to sign security tokens, such as CSRF tokens.
        database_url: SQLAlchemy URL of the database.
    """

    secret_key: str = field(repr=False)
    database_url: str


def load_settings(env: Mapping[str, str] = os.environ) -> Settings:
    """Build `Settings` from environment variables.

    Args:
        env: Where to read variables from. Defaults to the process
            environment; tests pass a plain dict instead.

    Returns:
        The loaded settings.

    Raises:
        KeyError: if `TIEBREAKER_SECRET_KEY` is not set.
    """
    return Settings(
        secret_key=env["TIEBREAKER_SECRET_KEY"],
        database_url=env.get("TIEBREAKER_DATABASE_URL", DEFAULT_DATABASE_URL),
    )
