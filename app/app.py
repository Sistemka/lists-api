import json
from uuid import uuid4
from logging import getLogger

from fastapi import FastAPI, Request
from tortoise.contrib.fastapi import register_tortoise

from app.routes.v1.app import compiled_routers as v1_routers
from utils.tools.routers import register_routers
from settings import settings, TORTOISE_ORM


logger = getLogger()


async def ping():
    return "ok"


def create_app() -> FastAPI:
    # init_logger(is_debug=settings.IS_DEBUG)
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        docs_url="/docs" if settings.IS_DEBUG else None,
        redoc_url="/redoc" if settings.IS_DEBUG else None,
    )
    app.add_api_route(path="/ping", endpoint=ping, tags=["Health checks"])
    register_routers(app=app, routers=[*v1_routers])

    register_tortoise(app=app, config=TORTOISE_ORM, generate_schemas=settings.IS_DEBUG)
    return app


app = create_app()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    uid = str(uuid4())
    logger.info(
        f"""
            Request:
                From:      {request.client.host}:{request.client.port}
                URL:       {request.url.path}
                Method:    {request.method}
                Headers:
                           {json.dumps(dict(request.headers), indent=27)[28:-2]}
                QParams:
                           {json.dumps(dict(request.query_params), indent=27)[28:-2]}
                PParams:
                           {json.dumps(request.path_params, indent=27)[28:-2]}
                UUID:      {uid}
        """
    )
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(
            f"""
            Exception:
                Exception: {str(e)}
                Traceback: {str(e.with_traceback())}
                UUID:      {uid}
        """
        )
    else:
        logger.info(
            f"""
            Done:
                Status:    {response.status_code}
                UUID:      {uid}
        """
        )
    return response
