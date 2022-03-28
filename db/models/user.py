from tortoise import fields
from enum import IntEnum, unique

from db.models.base import BaseTortoiseModel, BaseMeta
from settings import settings


@unique
class SubType(IntEnum):
    USER = 0
    TAG = 1


class UserModel(BaseTortoiseModel):
    name = fields.CharField(max_length=30, null=True, default=None)
    e_mail = fields.CharField(max_length=50, null=True, default=None)
    phone_number = fields.CharField(max_length=15, null=True, default=None)
    hash_pass = fields.CharField(max_length=255, default=None, null=True)
    profile_pic = fields.ForeignKeyField("models.ImageModel", null=True)

    class Meta(BaseMeta):
        table = "users"

    def profile_picture(self) -> str:
        return (
            f"{settings.IMAGE_SERVICE}/{self.profile_pic_id}/small"
            if self.profile_pic_id is not None
            else f"{settings.CAT_IMAGE_SERVICE}/{self.id}/small"
        )


class UserSubsModel(BaseTortoiseModel):
    user_id = fields.ForeignKeyField("models.UserModel", null=False)
    sub_id = fields.IntField(null=False)
    sub_type = fields.IntEnumField(SubType, null=False)

    class Meta(BaseMeta):
        table = "user_subscriptions"
