from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, status

from app.routes.v1.models.lists import GetList, AddList
from services.v1.lists import ListsService

router = APIRouter()
