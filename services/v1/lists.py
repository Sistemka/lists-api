from uuid import UUID
from datetime import datetime

from tortoise.queryset import QuerySet

from services.base import BaseService
from db.handlers.list import ListsDB
from db.handlers.user import UserDB
from db.handlers.tag import TagsDB


class ListsService(BaseService):
    @staticmethod
    async def get_list(list_id: UUID):
        if (list_instance := await ListsDB.get_or_none(id=list_id)) is None:
            raise ListsService.ItemNotFound()
        return await list_instance.prefetch_related(
            "user_id", "header_image_id", "tags"
        )

    @staticmethod
    async def create_list(user_id: UUID):
        if (user := await UserDB.get(id=user_id)) is None:
            raise ListsService.ItemNotFound()
        return await ListsDB.create(user=user)

    @staticmethod
    async def update_list(list_id: UUID, **kwargs):
        if (list_instance := ListsDB.get(id=list_id)) is None:
            raise ListsService.ItemNotFound()
        return await ListsDB.update(object_id=list_instance.object_id, **kwargs)

    @staticmethod
    async def get_user_lists(user_id: UUID) -> QuerySet:
        if (user := UserDB.get(id=user_id)) is None:
            raise ListsService.ItemNotFound()
        return await ListsDB.get_user_lists(user.object_id)

    @staticmethod
    async def get_old_lists(timestamp: datetime) -> QuerySet:
        return await ListsDB.filter(publish_time__lte=timestamp)

    @staticmethod
    async def get_new_lists(timestamp: datetime) -> QuerySet:
        return await ListsDB.filter(publish_time__gte=timestamp)

    @staticmethod
    async def get_lists(offset: int, size: int, timestamp: datetime) -> QuerySet:
        return (await ListsService.get_old_lists(timestamp)).offset(offset).limit(size)
