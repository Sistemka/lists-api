from uuid import UUID

from fastapi import APIRouter

from db.models.user import UserModel
from app.exceptions import UserNotFound
from app.routes.v1.models.response.users import GetUser

router = APIRouter()


@router.get("/{user_id}", response_model=GetUser)
async def get_user_handler(user_id: UUID):
    if (user := await UserModel.get_or_none(id=user_id)) is None:
        raise UserNotFound
    return await GetUser.from_tortoise_orm(user)


@router.post("", response_model=GetUser)
async def create_user_handler():
    user = await UserModel.create()
    return await GetUser.from_tortoise_orm(user)
