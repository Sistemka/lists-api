from dataclasses import dataclass
from typing import List

from fastapi import APIRouter, FastAPI

_PREFIX_VALIDATION_ERROR = ValueError('root_prefix must start with /')


@dataclass
class Router:
    router: APIRouter
    tags: List[str]
    prefix: str = ''


def compile_routers(routers: List[Router], root_prefix: str = ''):
    if root_prefix and not root_prefix.startswith('/'):
        raise _PREFIX_VALIDATION_ERROR

    for router in routers:
        router.prefix = root_prefix + router.prefix

    return routers


def register_routers(app: FastAPI, routers: List[Router]):
    for router in routers:
        app.include_router(
            router=router.router,
            tags=router.tags,
            prefix=router.prefix
        )
