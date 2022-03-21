from app.routes.v1.handlers import lists
from utils.tools.routers import Router, compile_routers

routers = [
    Router(router=lists.router, tags=["Lists"], prefix="/lists"),
]


compiled_routers = compile_routers(
    routers=routers,
    root_prefix="/api/v1",
)
