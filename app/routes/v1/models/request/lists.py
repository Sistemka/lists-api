from pydantic import BaseModel
from db.models.list import ListStatus, ListType


class UpdateList(BaseModel):
    type: ListType = None
    header: str = None
    text: str = None
    status: ListStatus = None
