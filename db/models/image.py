from db.models.base import BaseTortoiseModel, BaseMeta


class ImageModel(BaseTortoiseModel):
    class Meta(BaseMeta):
        table = "images"
