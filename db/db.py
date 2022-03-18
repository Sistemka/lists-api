from uuid import UUID

from db.models import ListsModel
from app.routes.v1.models.lists import AddList


class Db:

    @staticmethod
    async def get_list(list_id: UUID) -> [ListsModel, None]:
        return await ListsModel.get_or_none(id=list_id)

    @staticmethod
    async def add_list(payload: AddList) -> [ListsModel, None]:
        return await ListsModel.create(header=payload.header, text=payload.text)
