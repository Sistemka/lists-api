from uuid import UUID

from db.models.user import UserModel
from services.exceptions import InvalidDataError


class UserService:
    @staticmethod
    async def get_user(user_id: UUID | int):
        if isinstance(user_id, UUID):
            return await UserModel.get_or_none(id=user_id)
        elif isinstance(user_id, int):
            return await UserModel.get_or_none(object_id=user_id)
        else:
            raise InvalidDataError

    @staticmethod
    async def create_user():
        return await UserModel.create()
