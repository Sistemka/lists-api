from uuid import UUID

from db.handlers.base import BaseCRUD
from db.models.image import ImageModel


class Image(BaseCRUD, ImageModel):
    async def createio() -> ImageModel | None:
        return await ImageModel.create()


class Testo:
    async def createio() -> ImageModel | None:
        return await ImageModel.create()


import asyncio

asyncio.run(Testo.createio())
