"""Create and configure the Tiebreaker application.

`litestar run` finds the `create_app` factory in this module automatically.
"""

from pathlib import Path

from litestar import Litestar, get
from litestar.plugins.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig

from app.core.config import Settings, load_settings

APP_DIR = Path(__file__).parent


@get("/")
async def home() -> Template:
    """Render the home page.

    Returns:
        The rendered `base.html` template.
    """
    return Template(template_name="base.html")


def create_app(settings: Settings | None = None) -> Litestar:
    """Build the Litestar application.

    Args:
        settings: Settings to build the app with. When omitted, they are
            loaded from environment variables; tests pass their own.

    Returns:
        The configured application.
    """
    settings = settings or load_settings()

    return Litestar(
        route_handlers=[
            home,
            # Serve files in app/static (CSS, JavaScript, images) under /static/.
            create_static_files_router(
                path="/static",
                directories=[APP_DIR / "static"],
            ),
        ],
        template_config=TemplateConfig(
            # Resolve templates relative to this file, so the app finds them no
            # matter which directory it is started from.
            directory=APP_DIR / "templates",
            engine=JinjaTemplateEngine,
        ),
    )
