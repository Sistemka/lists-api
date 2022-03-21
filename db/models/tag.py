from enum import IntEnum, unique
from tortoise import fields

from db.base import BaseTortoiseModel, BaseMeta


@unique
class TagType(IntEnum):
    SIMPLE_TAG = 0
    GEO_TAG = 1


class TagModel(BaseTortoiseModel):
    name = fields.CharField(max_length=30, null=False)
    parent_tag = fields.ForeignKeyField(
        "models.TagModel", related_name="child", null=True, default=None
    )
    tag_type = fields.IntEnumField(TagType, null=False, default=TagType.SIMPLE_TAG)

    class Meta(BaseMeta):
        table = "tags"
