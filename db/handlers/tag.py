from db.handlers.base import BaseDB, UUID
from db.models.tag import TagModel


class TagsDB(BaseDB, TagModel):
    async def get_full(id: UUID):
        await TagModel.get(id=id).prefetch_related("parent_tag")

    async def find(query: str) -> TagModel:
        await TagModel.filter(name__startswith=query)
