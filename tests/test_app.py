"""Tests for the application's top-level setup."""

from litestar.testing import TestClient


def test_home_page_returns_html(client: TestClient) -> None:
    """The home page loads and returns HTML."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
