from typing import List
from uuid import UUID
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator

from db.models.list import ListModel


UserUpdateList = pydantic_model_creator(
    ListModel,
    name="UserUpdateList",
    exclude=("id", "pluses", "minuses", "views", "saves", "created_at", "updated_at"),
)

SystemUpdateList = pydantic_model_creator(
    ListModel,
    name="SystemUpdateList",
    include=("views", "pluses", "minuses", "saves"),
)
