from typing import List
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from db.models.tag import TagModel


GetTag = pydantic_model_creator(
    TagModel,
    name="GetTag",
    exclude=["created_at", "updated_at"],
)

GetTagPreview = pydantic_model_creator(
    TagModel,
    name="GetTagPreview",
    include=["name", "tag_type"],
)


class GetTags(BaseModel):
    tags: List[GetTagPreview]
