"""Tests for loading application settings."""

import dataclasses

import pytest

from app.core.config import Settings, load_settings


def test_reads_settings_from_environment() -> None:
    """Every setting is read from its environment variable."""
    env = {
        "TIEBREAKER_SECRET_KEY": "test-secret",
        "TIEBREAKER_DATABASE_URL": "sqlite+aiosqlite:///test.db",
    }

    settings: Settings = load_settings(env)

    assert settings.secret_key == "test-secret"
    assert settings.database_url == "sqlite+aiosqlite:///test.db"


def test_database_url_has_a_development_default() -> None:
    """The database location falls back to the development SQLite file."""
    settings = load_settings({"TIEBREAKER_SECRET_KEY": "test-secret"})

    assert settings.database_url == "sqlite+aiosqlite:///data/tiebreaker.db"


def test_missing_secret_key_is_an_error() -> None:
    """Loadking fails when the secret key is not set."""
    with pytest.raises(KeyError, match="TIEBREAKER_SECRET_KEY"):
        load_settings({})


def test_settings_cannot_be_changed_after_loading() -> None:
    """Settings are read-only once loaded."""
    settings = load_settings({"TIEBREAKER_SECRET_KEY": "test-secret"})

    with pytest.raises(dataclasses.FrozenInstanceError):
        settings.secret_key = "changed"  # pyright: ignore[reportAttributeAccessIssue]
