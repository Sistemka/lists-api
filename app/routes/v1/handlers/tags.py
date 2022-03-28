from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, status

from services.v1.lists import ListsService

router = APIRouter()


@router.get("")
async def get_tags_handler():
    pass


@router.get("/autocomplete")
async def tags_autocomplete_handler(search_query: str):
    pass
