from uuid import UUID

from fastapi import APIRouter, Query
from app.routes.v1.models.response.tags import GetTag, GetTags, GetTagPreview
from db.models.tag import TagType
from services.v1.tags import TagService
import services.exceptions as service_exception
import app.exceptions as http_exception

router = APIRouter()


@router.get("{tag_id}", response_model=GetTag)
async def get_tags_handler(tag_id: UUID):
    return await GetTag.from_tortoise_orm(await TagService.get_tag(tag_id=tag_id))


@router.post("", response_model=GetTagPreview)
async def create_tags_handler(name: str, tag_type: TagType, parent_tag_id: UUID = None):
    try:
        return await GetTagPreview.from_tortoise_orm(
            await TagService.create_tag(name, tag_type, parent_tag_id)
        )
    except service_exception.TagAlreadyExistsError:
        raise http_exception.TagAlreadyExists
    except service_exception.TagNotFoundError:
        raise http_exception.TagNotFound


@router.get("/autocomplete", response_model=GetTags)
async def tags_autocomplete_handler(
    search_query: str,
    size: int = Query(ge=1, default=5),
):
    return GetTags(tags=await TagService.autocomplete(search_query, size))
