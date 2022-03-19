from uuid import UUID

from services.base import BaseService
from app.routes.v1.models.lists import AddList, GetList


class ListsService(BaseService):
    async def get_list(self, list_id: UUID) -> [GetList, None]:
        return await self.db.get_list(list_id=list_id)

    async def add_list(self, payload: AddList) -> [GetList, None]:
        return await self.db.add_list(payload=payload)
