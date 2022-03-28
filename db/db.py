from uuid import UUID

from db.models.list import ListModel
from app.routes.v1.models.lists import AddList


class Db:
    @staticmethod
    async def get_list(list_id: UUID) -> ListModel | None:
        return await ListModel.get_or_none(id=list_id)

    @staticmethod
    async def add_list(payload: AddList) -> ListModel | None:
        return await ListModel.create(header=payload.header, text=payload.text)
