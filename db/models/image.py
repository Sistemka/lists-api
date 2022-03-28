from db.base import BaseTortoiseModel, BaseMeta


class ImageModel(BaseTortoiseModel):
    class Meta(BaseMeta):
        table = "images"
