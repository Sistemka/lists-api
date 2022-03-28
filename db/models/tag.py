from enum import Enum, unique
from tortoise import fields

from db.models.base import BaseTortoiseModel, BaseMeta


@unique
class TagType(Enum):
    SIMPLE_TAG = "tag"
    GEO_TAG = "geo_tag"


class TagModel(BaseTortoiseModel):
    name = fields.CharField(max_length=30, null=False)
    parent_tag = fields.ForeignKeyField(
        "models.TagModel", related_name="child", null=True, default=None
    )
    tag_type = fields.CharEnumField(
        TagType, max_length=15, null=False, default=TagType.SIMPLE_TAG
    )

    class Meta(BaseMeta):
        table = "tags"
