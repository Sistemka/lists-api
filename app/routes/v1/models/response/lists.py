from typing import List
from uuid import UUID
from datetime import datetime
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, Field

from db.models.list import ListModel
from app.routes.v1.models.response.users import GetUserPreview


GetListPreview = pydantic_model_creator(
    ListModel,
    name="GetListPreview",
    include=["id", "type", "header", "views", "published_at"],
    computed=["rating"],
)


class GetPreview(BaseModel):
    user: GetUserPreview
    list: GetListPreview


class GetPreviews(BaseModel):
    lists: List[GetPreview]


GetList = pydantic_model_creator(
    ListModel,
    name="GetList",
)


class GetLists(BaseModel):
    lists: List[GetList] = Field(...)


class GetFullList(BaseModel):
    user: GetUserPreview
    list: GetList


class GetUserLists(BaseModel):
    user_id: UUID = Field(...)
    lists: List[GetList] = Field(...)


class NewLists(BaseModel):
    timestamp: datetime
    lists_len: int
    lists: List[GetListPreview]
