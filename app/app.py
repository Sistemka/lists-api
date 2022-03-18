from logging import getLogger

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.routes.v1.app import compiled_routers as v1_routers
from utils.tools.routers import register_routers
from settings import settings, TORTOISE_ORM


logging = getLogger(__name__)


def create_app() -> FastAPI:
    # init_logger(is_debug=settings.IS_DEBUG)
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
    )
    register_routers(
        app=app,
        routers=[*v1_routers]
    )

    register_tortoise(app=app, config=TORTOISE_ORM)
    return app


app = create_app()
