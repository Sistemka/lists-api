from tortoise.contrib.pydantic import pydantic_model_creator

from db.models.list import ListModel


GetList = pydantic_model_creator(
    ListModel,
    name="GetList",
)

AddList = pydantic_model_creator(
    ListModel,
    name="AddList",
    exclude=("id", "pluses", "minuses", "views"),
)
