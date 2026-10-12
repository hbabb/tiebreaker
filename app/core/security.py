"""Shared application security configuration."""

from litestar.config.csrf import CSRFConfig

from app.core.config import Settings


def create_csrf_config(settings: Settings) -> CSRFConfig:
    """Configure CSRF protection using the application secret.

    Args:
        settings: Application settings containing the secret key.

    Returns:
        The Litestar CSRF configuration.
    """
    return CSRFConfig(secret=settings.secret_key)
