from enum import Enum, unique
from tortoise import fields

from db.base import BaseTortoiseModel, BaseMeta
from tortoise.fields.base import SET_NULL


@unique
class ListType(Enum):
    SIMPLE_LIST = "simple_list"
    NUMERIC_LIST = "numeric_list"
    WISH_LIST = "wish_list"
    TODO_LIST = "todo_list"


@unique
class ListStatus(Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    DELETED = "deleted"


class ListModel(BaseTortoiseModel):
    user_id = fields.ForeignKeyField("models.UserModel", null=False)
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
    is_public = fields.BooleanField(null=False, default=False)
    status = fields.CharEnumField(
        ListStatus, max_length=20, null=False, default=ListStatus.DRAFT
    )
    footer = fields.TextField(null=True, default=None)
    tags = fields.ManyToManyField("models.TagModel")
    publish_time = fields.DatetimeField(null=True, default=None)

    class Meta(BaseMeta):
        table = "lists"


class ListItemModel(BaseTortoiseModel):
    list_id = fields.ForeignKeyField("models.ListModel", null=True, on_delete=SET_NULL)
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
