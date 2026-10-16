"""Tests for loading application settings."""

import pytest
from pydantic import ValidationError

from app.core.config import load_settings


@pytest.fixture(autouse=True)
def clear_settings_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove any real Tiebreaker variables so each test starts clean."""
    monkeypatch.delenv("TIEBREAKER_SECRET_KEY", raising=False)
    monkeypatch.delenv("TIEBREAKER_DATABASE_URL", raising=False)


def test_reads_settings_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Every setting is read from its environment variable."""
    monkeypatch.setenv("TIEBREAKER_SECRET_KEY", "test-secret")
    monkeypatch.setenv("TIEBREAKER_DATABASE_URL", "sqlite+aiosqlite:///test.db")

    settings = load_settings()

    assert settings.secret_key.get_secret_value() == "test-secret"
    assert settings.database_url == "sqlite+aiosqlite:///test.db"


def test_database_url_has_a_development_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The database location falls back to the development SQLite file."""
    monkeypatch.setenv("TIEBREAKER_SECRET_KEY", "test-secret")

    settings = load_settings()

    assert settings.database_url == "sqlite+aiosqlite:///data/tiebreaker.db"


def test_missing_secret_key_is_an_error() -> None:
    """Loading fails when the secret key is not set."""
    with pytest.raises(ValidationError, match="secret_key"):
        load_settings()


def test_empty_secret_key_is_an_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """An empty secret key is rejected, not treated as set."""
    monkeypatch.setenv("TIEBREAKER_SECRET_KEY", "")

    with pytest.raises(ValidationError, match="secret_key"):
        load_settings()


def test_settings_cannot_be_changed_after_loading(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Settings are read-only once loaded."""
    monkeypatch.setenv("TIEBREAKER_SECRET_KEY", "test-secret")
    settings = load_settings()

    with pytest.raises(ValidationError):
        settings.database_url = "changed"  # pyright: ignore[reportAttributeAccessIssue]


def test_secret_key_is_hidden_when_printed(monkeypatch: pytest.MonkeyPatch) -> None:
    """The secret key never appears when settings are printed or logged."""
    monkeypatch.setenv("TIEBREAKER_SECRET_KEY", "test-secret")

    settings = load_settings()

    assert "test-secret" not in repr(settings)
    assert "test-secret" not in str(settings)
