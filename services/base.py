from db.db import Db


class BaseService:
    def __init__(self):
        self.db = Db
