from tortoise.contrib.pydantic import pydantic_model_creator

from db.models import ListsModel


GetList = pydantic_model_creator(
    ListsModel,
    name='GetList',
)

AddList = pydantic_model_creator(
    ListsModel,
    name='AddList',
    exclude=('id',)
)

