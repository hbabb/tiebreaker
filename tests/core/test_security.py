"""Tests for application security configuration."""

from litestar.testing import TestClient


def test_home_page_sets_csrf_cookie(client: TestClient) -> None:
    """The application issues a CSRF token on a GET request."""
    response = client.get("/")

    assert response.status_code == 200
    assert "csrftoken" in response.cookies
