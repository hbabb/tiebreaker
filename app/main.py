"""Create and configure the Tiebreaker application.

`litestar run` finds the `app` object in this module automatically.
"""

from pathlib import Path

from litestar import Litestar, get
from litestar.plugins.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.static_files import create_static_files_router
from litestar.template.config import TemplateConfig


@get("/")
async def home() -> Template:
    """Render the home page.

    Returns:
        The rendered `base.html` template.
    """
    return Template(template_name="base.html")


app = Litestar(
    route_handlers=[
        home,
        # Serve files in app/static (CSS, JavaScript, images) under /static/.
        create_static_files_router(
            path="/static",
            directories=[Path(__file__).parent / "static"],
        ),
    ],
    template_config=TemplateConfig(
        # Resolve templates relative to this file, so the app finds them no
        # matter which directory it is started from.
        directory=Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    ),
)
