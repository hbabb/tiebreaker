"""Tests for application security configuration."""

import pytest
from litestar.testing import TestClient


def test_home_page_sets_csrf_cookie(client: TestClient) -> None:
    """The application issues a CSRF token on a GET request."""
    response = client.get("/")

    assert response.status_code == 200
    assert "csrftoken" in response.cookies


def test_post_without_csrf_token_is_rejected(
    csrf_client: TestClient,
) -> None:
    """POST requests without a CSRF token are rejected."""
    csrf_client.get("/")

    response = csrf_client.post("/test-csrf")

    assert response.status_code == 403


def tests_post_with_valid_csrf_token_is_accepted(
    csrf_client: TestClient,
) -> None:
    """POST requests with a valid CSRF token are accepted."""
    response = csrf_client.get("/")
    token = response.cookies["csrftoken"]

    response = csrf_client.post(
        "/test-csrf",
        headers={"x-csrftoken": token},
    )

    assert response.status_code == 201


def test_post_with_valid_csrf_form_field_is_accepted(
    csrf_client: TestClient,
) -> None:
    """POST requests accept a valid CSRF form field."""
    response = csrf_client.get("/")
    token = response.cookies["csrftoken"]

    response = csrf_client.post("/test-csrf", data={"_csrf_token": token})

    assert response.status_code == 201


@pytest.mark.parametrize(
    "token",
    ["invalid-token", "", "malformed"],
)
def test_post_with_invalid_csrf_header_is_rejected(
    csrf_client: TestClient,
    token: str,
) -> None:
    """POST requests with invalid CSRF headers are rejected."""
    csrf_client.get("/")

    response = csrf_client.post(
        "/test-csrf",
        headers={"x-csrftoken": token},
    )

    assert response.status_code == 403


def test_post_with_invalid_csrf_form_field_is_rejected(
    csrf_client: TestClient,
) -> None:
    """POST requests with invalid CSRF form data are rejected."""
    csrf_client.get("/")

    response = csrf_client.post(
        "/test-csrf",
        data={"_csrf_token": "invalid-token"},
    )

    assert response.status_code == 403


def test_post_with_token_but_no_cookie_is_rejected(
    csrf_client: TestClient,
) -> None:
    """A valid CSRF header cannot replace the required cookie."""
    response = csrf_client.get("/")
    token = response.cookies["csrftoken"]

    csrf_client.cookies.clear()

    response = csrf_client.post(
        "/test-csrf",
        headers={"x-csrftoken": token},
    )

    assert response.status_code == 403


def test_post_with_invalid_csrf_cookie_is_rejected(
    csrf_client: TestClient,
) -> None:
    """A valid CSRF header cannot authorize a forged cookie."""
    response = csrf_client.get("/")
    token = response.cookies["csrftoken"]

    csrf_client.cookies.set(
        "csrftoken",
        "invalid-token",
        path="/",
    )

    response = csrf_client.post(
        "/test-csrf",
        headers={"x-csrftoken": token},
    )

    assert response.status_code == 403
