from typing import List
from uuid import UUID

from db.models.tag import TagModel, TagType
from services.exceptions import (
    InvalidDataError,
    TagAlreadyExistsError,
    TagNotFoundError,
)


class TagService:
    @staticmethod
    async def get_tag(tag_id: UUID | int) -> TagModel:
        if isinstance(tag_id, UUID):
            return await TagModel.get_or_none(id=tag_id)
        elif isinstance(tag_id, int):
            return await TagModel.get_or_none(object_id=tag_id)
        else:
            raise InvalidDataError

    @staticmethod
    async def create_tag(
        tag_name: str,
        tag_type: TagType,
        parent_tag_id: UUID | int = None,
    ) -> TagModel:
        parent_tag = None
        tag = await TagModel.filter(name=tag_name)
        if tag:
            raise TagAlreadyExistsError
        if parent_tag_id:
            parent_tag = await TagService.get_tag(parent_tag_id)
            if parent_tag is None:
                raise TagNotFoundError
        return await TagModel.create(
            name=tag_name,
            parent_tag=parent_tag,
            tag_type=tag_type,
        )

    @staticmethod
    async def autocomplete(search_query: str, size: int) -> List[TagModel]:
        return await TagModel.filter(name__startswith=search_query).limit(size)
