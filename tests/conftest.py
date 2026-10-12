"""Shared pytest fixtures."""

from collections.abc import Iterator

import pytest
from litestar.testing import TestClient

from app.core.config import Settings
from app.main import create_app


@pytest.fixture
def settings() -> Settings:
    """Settings for tests, with a throwaway secret and no real database."""
    return Settings(
        secret_key="test-secret-key",
        database_url="sqlite+aiosqlite:///:memory:",
    )


@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    """A test client for an app built with the test settings."""
    with TestClient(app=create_app(settings)) as client:
        yield client
