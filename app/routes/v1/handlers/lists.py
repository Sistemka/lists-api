from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Query

from app.exceptions import UserNotFound, ListNotFound
from app.routes.v1.models.response.lists import (
    GetList,
    GetLists,
    GetFullList,
    GetListPreview,
    GetUserPreview,
    GetPreviews,
    NewLists,
)
from app.routes.v1.models.request.lists import SystemUpdateList, UserUpdateList
from app.routes.v1.models.response.users import GetUser
from db.models.list import ListItemModel, ListModel
from db.models.user import UserModel

router = APIRouter()


@router.get("", response_model=GetPreviews)
async def get_lists_handler(
    offset: int = Query(..., ge=0),
    size: int = Query(..., ge=1),
    timestamp: datetime = Query(...),
):
    return GetPreviews(
        lists=[
            {
                "user": await GetUserPreview.from_tortoise_orm(list_item.user),
                "list": await GetListPreview.from_tortoise_orm(list_item),
            }
            for list_item in await ListModel.get_lists(
                offset=offset, size=size, timestamp=timestamp
            )
        ]
    )


@router.get("/", response_model=GetLists)
async def get_user_lists_handler(
    user_id: UUID,
    offset: int = Query(..., ge=0),
    size: int = Query(..., ge=1),
):
    if (user := await UserModel.get_or_none(id=user_id)) is None:
        raise UserNotFound
    return GetLists(
        lists=await ListModel.filter(user=user)
        .offset(offset)
        .limit(size)
        .order_by("-updated_at")
    )


@router.get("/{list_id}", response_model=GetFullList)
async def get_list_handler(list_id: UUID):
    if (list_instance := await ListModel.get_full_or_none(id=list_id)) is None:
        raise ListNotFound
    return GetFullList(
        user=await GetUser.from_tortoise_orm(list_instance.user),
        list=await GetList.from_tortoise_orm(list_instance),
    )


@router.post("", response_model=GetList)
async def create_list_handler(user_id: UUID):
    if (user := await UserModel.get_or_none(id=user_id)) is None:
        raise UserNotFound
    return await GetList.from_tortoise_orm(await ListModel.create(user=user))


@router.patch("/{list_id}", response_model=GetList)
async def user_update_list_handler(list_id: UUID, payload: UserUpdateList):
    if (list_instance := await ListModel.get_or_none(id=list_id)) is None:
        raise ListNotFound
    return await GetList.from_tortoise_orm(
        await list_instance.update_from_dict(payload)
    )


@router.patch("-s/{list_id}", response_model=GetList)
async def system_update_list_handler(list_id: UUID, payload: SystemUpdateList):
    if (list_instance := await ListModel.get_or_none(id=list_id)) is None:
        raise ListNotFound
    return await GetList.from_tortoise_orm(
        await list_instance.update_from_dict(payload)
    )


@router.get("-new", response_model=NewLists)
async def is_new_lists_handler(timestamp: datetime):
    lists = await ListModel.get_new_lists(timestamp)
    return NewLists(timestamp=timestamp, lists_len=len(lists), lists=lists)
