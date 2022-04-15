from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Query

import app.exceptions as http_exceptions
import services.exceptions as service_exceptions

from app.routes.v1.models.response.lists import (
    GetList,
    GetLists,
    GetFullList,
    GetListPreview,
    GetUserPreview,
    GetPreviews,
    NewLists,
)
from app.routes.v1.models.request.lists import UpdateList
from services.v1.lists import ListService
from services.v1.user import UserService

router = APIRouter()


@router.get("", response_model=GetPreviews)
async def get_lists_handler(
    offset: int = Query(..., ge=0),
    size: int = Query(..., ge=1),
    timestamp: datetime = Query(...),
):
    return GetPreviews(
        __root__=[
            {
                "user": await GetUserPreview.from_tortoise_orm(list_item.user),
                "list": await GetListPreview.from_tortoise_orm(list_item),
            }
            for list_item in await ListService.get_lists(
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
    try:
        return GetLists(lists=await ListService.get_user_lists(user_id, offset, size))
    except service_exceptions.UserNotFound:
        raise http_exceptions.UserNotFound


@router.get("/{list_id}", response_model=GetFullList)
async def get_list_handler(list_id: UUID):
    if (list_instance := await ListService.get_list(list_id)) is None:
        raise http_exceptions.ListNotFound
    return GetFullList(
        user=await GetUserPreview.from_tortoise_orm(
            await UserService.get_user(list_instance.user_id)
        ),
        list=await GetList.from_tortoise_orm(list_instance),
    )


@router.post("", response_model=GetList)
async def create_list_handler(user_id: UUID):
    try:
        return await GetList.from_tortoise_orm(await ListService.create_list(user_id))
    except service_exceptions.UserNotFound:
        raise http_exceptions.UserNotFound


@router.patch("/{list_id}", response_model=GetList)
async def user_update_list_handler(user_id: UUID, list_id: UUID, payload: UpdateList):
    try:
        return await GetList.from_tortoise_orm(
            await ListService.update_list(
                user_id,
                list_id,
                **payload.dict(exclude_none=True),
            )
        )
    except service_exceptions.ListNotFoundError:
        raise http_exceptions.ListNotFound
    except service_exceptions.UserNotFoundError:
        raise http_exceptions.UserNotFound
    except service_exceptions.PermissionDeniedError:
        raise http_exceptions.PermissionDenied
    except service_exceptions.UpdateError:
        raise http_exceptions.UpdateError


@router.get("-new", response_model=NewLists)
async def is_new_lists_handler(timestamp: datetime):
    lists = await ListService.get_new_lists(timestamp)
    return NewLists(timestamp=timestamp, lists_len=len(lists), lists=lists)


@router.post("-upvote")
async def upvote_handler(list_id: UUID, user_id: UUID, undo: bool = False):
    try:
        return await ListService.upvote(list_id=list_id, user_id=user_id, undo=undo)
    except service_exceptions.UserNotFoundError:
        raise http_exceptions.UserNotFound
    except service_exceptions.ListNotFoundError:
        raise http_exceptions.ListNotFound
    except service_exceptions.ActionAlreadyDoneError:
        raise http_exceptions.ActionAlreadyDone
    except service_exceptions.ActionCantBeDoneError:
        raise http_exceptions.ActionCantBeDone


@router.post("-downvote")
async def downvote_handler(list_id: UUID, user_id: UUID, undo: bool = False):
    try:
        return await ListService.downvote(list_id=list_id, user_id=user_id, undo=undo)
    except service_exceptions.UserNotFoundError:
        raise http_exceptions.UserNotFound
    except service_exceptions.ListNotFoundError:
        raise http_exceptions.ListNotFound
    except service_exceptions.ActionAlreadyDoneError:
        raise http_exceptions.ActionAlreadyDone
    except service_exceptions.ActionCantBeDoneError:
        raise http_exceptions.ActionCantBeDone


@router.post("-view")
async def view_handler(list_id: UUID, user_id: UUID):
    try:
        return await ListService.view(list_id=list_id, user_id=user_id)
    except service_exceptions.UserNotFoundError:
        raise http_exceptions.UserNotFound
    except service_exceptions.ListNotFoundError:
        raise http_exceptions.ListNotFound
    except service_exceptions.ActionAlreadyDoneError:
        raise http_exceptions.ActionAlreadyDone
