from uuid import UUID
from datetime import datetime

from tortoise.queryset import QuerySet

from services.base import BaseService
from db.handlers.list import ListsDB
from db.handlers.user import UserDB, UserModel
from db.handlers.tag import TagsDB


class UserService(BaseService):
    @staticmethod
    async def get_user(user_id: UUID):
        if (user := await UserModel.get_or_none(id=user_id)) is None:
            raise UserService.ItemNotFound
        return user

    @staticmethod
    async def create_user():
        return await UserDB.create()
