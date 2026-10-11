from pathlib import Path

from litestar import Litestar, get
from litestar.plugins.jinja import JinjaTemplateEngine
from litestar.response import Template
from litestar.template.config import TemplateConfig


@get("/")
async def home() -> Template:
    return Template(template_name="base.html")


app = Litestar(
    route_handlers=[home],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    ),
)
