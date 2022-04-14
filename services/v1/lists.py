import asyncio
from enum import Enum
from typing import List, Tuple
from uuid import UUID
from datetime import datetime

from db.models.list import (
    ListStatus,
    ListModel,
    SaveUser,
    ViewUser,
    PlusUser,
    MinusUser,
)
from db.models.user import UserModel
from services.exceptions import (
    ActionAlreadyDoneError,
    ActionCantBeDoneError,
    InvalidDataError,
    ListNotFoundError,
    PermissionDeniedError,
    UpdateError,
    UserNotFoundError,
)


class ListAction(Enum):
    UPVOTE = {"model": PlusUser, "field": "pluses"}
    DOWNVOTE = {"model": MinusUser, "field": "minuses"}
    VIEW = {"model": ViewUser, "field": "views"}
    SAVE = {"model": SaveUser, "field": "saves"}


class ListService:
    @staticmethod
    async def get_list(list_id: UUID | int):
        if isinstance(list_id, UUID):
            return await ListModel.get_or_none(id=list_id)
        elif isinstance(list_id, int):
            return await ListModel.get_or_none(object_id=list_id)
        else:
            raise InvalidDataError

    @staticmethod
    async def get_user_lists(user_id: UUID, offset: int, size: int) -> ListModel:
        if (user := await UserModel.get_or_none(id=user_id)) is None:
            raise UserNotFoundError
        return (
            await ListModel.filter(user=user)
            .offset(offset)
            .limit(size)
            .order_by("-updated_at")
        )

    @staticmethod
    async def __get_list_and_user(
        *, list_id: UUID, user_id: UUID
    ) -> Tuple[ListModel, UserModel]:

        user_instance, list_instance = await asyncio.gather(
            UserModel.get_or_none(id=user_id),
            ListModel.filter(id=list_id).select_for_update(),
        )
        if user_instance is None:
            raise UserNotFoundError
        if not list_instance:
            raise ListNotFoundError
        return list_instance[0], user_instance

    @staticmethod
    async def __is_action_done(
        *, user_instance: UserModel, list_instance: ListModel, action: ListAction
    ):
        model = action.value.get("model")
        if (
            await model.get_or_none(user=user_instance, list=list_instance)
        ) is not None:
            return True
        return False

    @staticmethod
    async def __action(
        *,
        user_instance: UserModel,
        list_instance: ListModel,
        action: ListAction,
        undo=False,
    ):
        model = action.value.get("model")
        field = action.value.get("field")
        if undo:
            if not await ListService.__is_action_done(
                user_instance=user_instance, list_instance=list_instance, action=action
            ):
                raise ActionCantBeDoneError
        else:
            if await ListService.__is_action_done(
                user_instance=user_instance, list_instance=list_instance, action=action
            ):
                raise ActionAlreadyDoneError
        setattr(
            list_instance,
            field,
            (getattr(list_instance, field) or 0) + -1 if undo else 1,
        )
        await asyncio.gather(
            list_instance.save(),
            model.get(user=user_instance, list=list_instance).delete()
            if undo
            else model.create(user=user_instance, list=list_instance),
        )
        return getattr(list_instance, field)

    @staticmethod
    async def upvote(list_id: UUID, user_id: UUID, undo: bool):
        list_instance, user_instance = await ListService.__get_list_and_user(
            list_id=list_id, user_id=user_id
        )
        if (
            minus := await MinusUser.get_or_none(user=user_instance, list=list_instance)
        ) is not None:
            list_instance.minuses -= 1
            await asyncio.gather(minus.delete(), list_instance.save())
        return await ListService.__action(
            user_instance=user_instance,
            list_instance=list_instance,
            action=ListAction.UPVOTE,
            undo=undo,
        )

    @staticmethod
    async def downvote(list_id: UUID, user_id: UUID, undo: bool):
        list_instance, user_instance = await ListService.__get_list_and_user(
            list_id=list_id, user_id=user_id
        )
        if (
            plus := await PlusUser.get_or_none(user=user_instance, list=list_instance)
        ) is not None:
            list_instance.pluses -= 1
            await asyncio.gather(plus.delete(), list_instance.save())
        return await ListService.__action(
            user_instance=user_instance,
            list_instance=list_instance,
            action=ListAction.DOWNVOTE,
            undo=undo,
        )

    @staticmethod
    async def view(list_id: UUID, user_id: UUID):
        list_instance, user_instance = await ListService.__get_list_and_user(
            list_id=list_id, user_id=user_id
        )
        return await ListService.__action(
            user_instance=user_instance,
            list_instance=list_instance,
            action=ListAction.VIEW,
        )

    @staticmethod
    async def user_save(list_id: UUID, user_id: UUID):
        list_instance, user_instance = await ListService.__get_list_and_user(
            list_id=list_id, user_id=user_id
        )
        return await ListService.__action(
            user_instance=user_instance,
            list_instance=list_instance,
            action=ListAction.SAVE,
        )

    @staticmethod
    async def create_list(user_id: UUID):
        if (user := await UserModel.get(id=user_id)) is None:
            raise UserNotFoundError
        return await ListModel.create(user=user)

    @staticmethod
    async def update_list(
        user_id: UUID, list_id: UUID, status: ListStatus = None, **kwargs
    ) -> ListModel:
        list_instance, user_instance = await ListService.__get_list_and_user(
            list_id=list_id, user_id=user_id
        )
        if list_instance.user_id != user_instance.object_id:
            raise PermissionDeniedError
        prev_status = list_instance.status
        if status == ListStatus.DELETED or prev_status == ListStatus.DELETED:
            raise UpdateError
        if status == ListStatus.PUBLISHED:
            if prev_status == ListStatus.DRAFT:
                list_instance.status = ListStatus.PUBLISHED
                list_instance.published_at = datetime.now()
        kwargs = kwargs | {"status": status} if status else kwargs
        await list_instance.update_from_dict(kwargs).save()
        return list_instance

    @staticmethod
    async def move_to_trash(user_id: UUID, list_id: UUID) -> ListModel:
        list_instance, user_instance = await ListService.__get_list_and_user(
            list_id=list_id, user_id=user_id
        )
        if list_instance.user_id != user_instance.object_id:
            raise PermissionDeniedError
        if list_instance.status == ListStatus.DELETED:
            raise UpdateError
        list_instance.status = ListStatus.DELETED
        await list_instance.save()
        return list_instance

    @staticmethod
    async def restore(user_id: UUID, list_id: UUID) -> ListModel:
        list_instance, user_instance = await ListService.__get_list_and_user(
            list_id=list_id, user_id=user_id
        )
        if list_instance.user_id != user_instance.object_id:
            raise PermissionDeniedError
        if list_instance.status != ListStatus.DELETED:
            raise UpdateError
        list_instance.status = ListStatus.DRAFT
        await list_instance.save()
        return list_instance

    @staticmethod
    async def get_old_lists(timestamp: datetime) -> ListModel:
        return await ListModel.filter(
            published_at__lte=timestamp, status=ListStatus.PUBLISHED
        )

    @staticmethod
    async def get_new_lists(timestamp: datetime) -> ListModel:
        return await ListModel.filter(
            published_at__gte=timestamp, status=ListStatus.PUBLISHED
        )

    @staticmethod
    async def get_lists(offset: int, size: int, timestamp: datetime) -> List[ListModel]:
        return (
            await ListModel.filter(
                published_at__lte=timestamp, status=ListStatus.PUBLISHED
            )
            .offset(offset)
            .limit(size)
            .prefetch_related("user")
            .order_by("-published_at")
        )
