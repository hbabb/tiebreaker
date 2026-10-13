"""Tests for static files served to the browser."""

from litestar.testing import TestClient


def test_htmx_script_is_served(client: TestClient) -> None:
    """The HTMX script is served as JavaScript."""
    response = client.get("/static/js/htmx.min.js")

    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]


def test_base_page_loads_htmx(client: TestClient) -> None:
    """The base page includes a script tag for HTMX."""
    response = client.get("/")

    assert '<script src="/static/js/htmx.min.js"' in response.text
