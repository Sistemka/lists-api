from uuid import UUID


class BaseService:
    class ItemNotFound(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)
