from uuid import uuid4

from tortoise import Model, fields
from tortoise.contrib.postgres.indexes import HashIndex


class BaseTortoiseModel(Model):
    object_id = fields.IntField(pk=True)
    id = fields.UUIDField(unique=True, default=uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

    class PydanticMeta:
        exclude = ["object_id", "updated_at", "created_at"]


class BaseMeta:
    indexes = (HashIndex(fields={"id"}),)
