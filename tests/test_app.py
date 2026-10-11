from litestar.testing import TestClient

from app.main import app


def test_home_page_returns_html() -> None:
    with TestClient(app=app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
