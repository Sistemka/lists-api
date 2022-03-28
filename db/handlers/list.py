from db.handlers.base import BaseDB, UUID
from db.models.list import ListModel, ListItemModel


class ListsDB(BaseDB, ListModel):
    async def get_full(id: int):
        await ListModel.get(object_id=id).prefetch_related(
            "user_id", "header_image_id", "tags"
        )

    async def get_user_lists(user_id: int):
        await ListModel.filter(user__object_id=user_id).prefetch_related(
            "user_id", "header_image_id", "tags"
        )


class ListItemsDB(BaseDB, ListItemModel):
    async def get_full(id: int) -> ListItemModel:
        await ListItemModel.get(object_id=id).prefetch_related(
            "parent_list", "parent_item", "images"
        )

    async def get_list_items(list_id: int) -> ListItemModel:
        await ListItemModel.filter(parent_list__object_id=list_id).prefetch_related(
            "parent_item", "images"
        )
