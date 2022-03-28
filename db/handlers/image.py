from db.handlers.base import BaseDB
from db.models.image import ImageModel


class ImageDB(BaseDB, ImageModel):
    pass
