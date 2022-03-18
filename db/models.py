from datetime import datetime
from uuid import uuid4

from tortoise import Model, fields
from tortoise.contrib.postgres.indexes import HashIndex


class BaseTortoiseModel(Model):
    object_id = fields.IntField(pk=True)
    id = fields.UUIDField(unique=True, default=uuid4)
    created_at = fields.DatetimeField(default=datetime.utcnow)
    updated_at = fields.DatetimeField(default=datetime.utcnow)

    class Meta:
        abstract = True

    class PydanticMeta:
        exclude = ['object_id', 'updated_at', 'created_at']


class ListsModel(BaseTortoiseModel):
    header = fields.CharField(max_length=255)
    text = fields.TextField()

    class Meta:
        table = "lists"
        indexes = (
            HashIndex(fields={'id'}),
        )
