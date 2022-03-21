from enum import IntEnum, unique
from tortoise import fields

from db.base import BaseTortoiseModel, BaseMeta
from tortoise.fields.base import SET_NULL


@unique
class ListType(IntEnum):
    SIMPLE_LIST = 1
    NUMERIC_LIST = 2
    WISH_LIST = 3
    TODO_LIST = 4


@unique
class ListStatus(IntEnum):
    DRAFT = 0
    PUBLISHED = 1
    DELETED = -1


class ListModel(BaseTortoiseModel):
    user_id = fields.ForeignKeyField("models.UserModel")
    type = fields.IntEnumField(ListType, default=ListType.SIMPLE_LIST, null=False)
    header = fields.CharField(max_length=255)
    header_image_id = fields.ForeignKeyField("models.ImageModel")
    text = fields.TextField(null=True, default=None)
    pluses = fields.IntField(null=True, default=None)
    minuses = fields.IntField(null=True, default=None)
    views = fields.IntField(null=True, default=None)
    is_public = fields.BooleanField(null=False, default=False)
    status = fields.IntEnumField(ListStatus, null=False, default=ListStatus.DRAFT)
    footer = fields.TextField(null=True, default=None)
    tags = fields.ManyToManyField("models.TagModel")
    puplish_time = fields.DatetimeField(null=True, default=None)

    class Meta(BaseMeta):
        table = "lists"


class ListItemModel(BaseTortoiseModel):
    list_id = fields.ForeignKeyField("models.ListModel", null=True, on_delete=SET_NULL)
    header = fields.CharField(max_length=255)
    order = fields.IntField(null=False, default=0)
    text = fields.TextField(null=True, default=None)
    pluses = fields.IntField(null=True, default=None)
    minuses = fields.IntField(null=True, default=None)
    checked = fields.BooleanField(null=True, default=None)
    owned_by = fields.ForeignKeyField("models.UserModel", null=True, default=None)
    parent_item = fields.ForeignKeyField(
        "models.ListItemModel", related_name="child", null=True, default=None
    )
    images = fields.ManyToManyField("models.ImageModel")

    class Meta(BaseMeta):
        table = "items"
