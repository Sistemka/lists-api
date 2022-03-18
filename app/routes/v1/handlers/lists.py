from uuid import UUID

from fastapi import APIRouter, status

from app.routes.v1.models.lists import GetList, AddList
from services.v1.lists import ListsService

router = APIRouter()


@router.get(
    '/{list_id}',
    response_model=GetList,
    response_model_exclude_none=True
)
async def get_list(list_id: UUID):
    service = ListsService()
    return await service.get_list(list_id=list_id)


@router.post(
    '',
    response_model=GetList,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True
)
async def add_list(
    payload: AddList
):
    service = ListsService()
    return await service.add_list(payload=payload)
