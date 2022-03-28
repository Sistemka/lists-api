from __future__ import annotations
from datetime import datetime
from enum import Enum, unique
from typing import List
from tortoise import fields

from db.models.base import BaseTortoiseModel, BaseMeta
from tortoise.fields.base import SET_NULL

__all__ = [
    "ListModel",
    "ListItemModel",
]


@unique
class ListType(str, Enum):
    SIMPLE_LIST = "simple_list"
    NUMERIC_LIST = "numeric_list"
    WISH_LIST = "wish_list"
    TODO_LIST = "todo_list"


@unique
class ListStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DELETED = "deleted"


class ListModel(BaseTortoiseModel):
    user = fields.ForeignKeyField("models.UserModel", null=False)
    type = fields.CharEnumField(
        ListType, max_length=30, default=ListType.SIMPLE_LIST, null=False
    )
    header = fields.CharField(max_length=255, null=True)
    header_image_id = fields.ForeignKeyField(
        "models.ImageModel", null=True, default=None, on_delete=SET_NULL
    )
    text = fields.TextField(null=True, default=None)
    pluses = fields.IntField(null=True, default=None)
    minuses = fields.IntField(null=True, default=None)
    views = fields.IntField(null=True, default=None)
    saves = fields.IntField(null=True, default=None)
    is_public = fields.BooleanField(null=False, default=False)
    status = fields.CharEnumField(
        ListStatus, max_length=20, null=False, default=ListStatus.DRAFT
    )
    footer = fields.TextField(null=True, default=None)
    tags = fields.ManyToManyField("models.TagModel")
    published_at = fields.DatetimeField(null=True, default=None)

    class Meta(BaseMeta):
        table = "lists"

    def rating(self) -> int:
        return (self.pluses or 0) - (self.minuses or 0)

    @classmethod
    async def get_full_or_none(cls: ListModel, **kwargs):
        return await cls.get_or_none(**kwargs).prefetch_related(
            "user", "header_image_id", "tags"
        )

    @classmethod
    async def get_old_lists(cls: ListModel, timestamp: datetime) -> List[ListModel]:
        return await cls.filter(published_at__lte=timestamp)

    @classmethod
    async def get_new_lists(cls: ListModel, timestamp: datetime) -> List[ListModel]:
        return await cls.filter(published_at__gte=timestamp)

    @classmethod
    async def get_lists(
        cls: ListModel, offset: int, size: int, timestamp: datetime
    ) -> List[ListModel]:
        return (
            await cls.filter(created_at__lte=timestamp, is_public=False)
            # await cls.filter(published_at__lte=timestamp, is_public=True)
            .offset(offset)
            .limit(size)
            .prefetch_related("user")
            .order_by("-created_at")
            # .order_by("-published_at")
        )


class ListItemModel(BaseTortoiseModel):
    parent_list = fields.ForeignKeyField(
        "models.ListModel", null=True, on_delete=SET_NULL
    )
    header = fields.CharField(max_length=255, null=True)
    order = fields.IntField(null=False, default=0)
    text = fields.TextField(null=True, default=None)
    pluses = fields.IntField(null=True, default=None)
    minuses = fields.IntField(null=True, default=None)
    checked = fields.BooleanField(null=True, default=None)
    parent_item = fields.ForeignKeyField(
        "models.ListItemModel", related_name="child", null=True, default=None
    )
    images = fields.ManyToManyField("models.ImageModel")

    class Meta(BaseMeta):
        table = "list_items"

    @classmethod
    async def get_full(cls: ListItemModel, **kwargs) -> ListItemModel:
        return await cls.get_or_none(**kwargs).prefetch_related(
            "parent_list", "parent_item", "images"
        )
