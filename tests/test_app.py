"""Tests for the application's top-level setup."""

from litestar.testing import TestClient

from app.main import app


def test_home_page_returns_html() -> None:
    """The home page loads and returns HTML."""
    with TestClient(app=app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
