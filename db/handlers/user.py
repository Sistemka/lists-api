from db.handlers.base import BaseDB, UUID
from db.models.user import UserModel, UserSubsModel


class UserDB(BaseDB, UserModel):
    pass


class UserSubsDB(BaseDB, UserSubsModel):
    async def get_user_subs(user_id: UUID):
        await UserSubsModel.filter(user_id=user_id)
