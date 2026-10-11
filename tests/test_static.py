"""Tests for static files served to the browser."""

from litestar.testing import TestClient

from app.main import app


def test_htmx_script_is_served() -> None:
    """The HTMX script is served as JavaScript."""
    with TestClient(app=app) as client:
        response = client.get("/static/js/htmx.min.js")

    assert response.status_code == 200
    assert "javascript" in response.headers["content-type"]


def test_base_page_loads_htmx() -> None:
    """The base page includes a script tag for HTMX."""
    with TestClient(app=app) as client:
        response = client.get("/")

    assert '<script src="/static/js/htmx.min.js"' in response.text
