from app.routes.v1.handlers import users
from app.routes.v1.handlers import lists
from app.routes.v1.handlers import tags
from utils.tools.routers import Router, compile_routers

routers = [
    Router(router=lists.router, tags=["Lists"], prefix="/lists"),
    Router(router=users.router, tags=["Users"], prefix="/users"),
    Router(router=tags.router, tags=["Tags"], prefix="/tags"),
]


compiled_routers = compile_routers(
    routers=routers,
    root_prefix="/api/v1",
)
