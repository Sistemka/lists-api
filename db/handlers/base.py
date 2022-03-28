from abc import ABCMeta
from uuid import UUID
from types import FunctionType

from tortoise.models import Model


def validate(func):
    def wrapper(cls, *args, **kwargs):
        if cls.__base__ == ABCMeta:
            raise ValueError()
        if len(cls.__bases__) != 2:
            raise ValueError()
        if cls.__bases__[-1] == BaseDB:
            raise ValueError()
        return func(cls, *args, **kwargs)

    return wrapper


def validator(cls):
    def func_validator(func):
        def wrapper(cls, *args, **kwargs):
            if cls.__base__ == ABCMeta:
                raise ValueError()
            if len(cls.__bases__) != 2:
                raise ValueError()
            if cls.__bases__[-1] == BaseDB:
                raise ValueError()
            return func(cls, *args, **kwargs)

        return wrapper

    for attr_name in cls.__dict__:
        if isinstance(attr := getattr(cls, attr_name), FunctionType):
            setattr(cls, attr_name, classmethod(func_validator(attr)))
    return cls


class BaseDB(ABCMeta):
    def validate(func):
        def wrapper(cls, *args, **kwargs):
            if cls.__base__ == ABCMeta:
                raise ValueError()
            if len(cls.__bases__) != 2:
                raise ValueError()
            if cls.__bases__[-1] == BaseDB:
                raise ValueError()
            return func(cls, *args, **kwargs)

        return wrapper

    def __new__(cls, *args, **kwargs):
        return super(BaseDB, cls).__new__(cls, *args, **kwargs)

    @classmethod
    @validate
    async def create(cls, **kwargs) -> Model | None:
        return await cls.__bases__[-1].create(**kwargs)

    @classmethod
    @validate
    async def get_all(cls) -> list:
        return await cls.__bases__[-1].all()

    @classmethod
    @validate
    async def get(cls, id: int | UUID) -> Model | None:
        if isinstance(id, int):
            return await cls.__bases__[-1].get_or_none(object_id=id)
        elif isinstance(id, UUID):
            return await cls.__bases__[-1].get_or_none(id=id)
        else:
            raise ValueError

    @classmethod
    @validate
    async def update(cls, id: int | UUID, **kwargs) -> Model | None:
        if (instance := await cls.get(id)) is not None:
            for k, v in kwargs.items():
                setattr(instance, k, v)
            await instance.save()
            return instance

    @classmethod
    @validate
    async def delete(cls, id: UUID) -> None:
        if (instance := await cls.__bases__[-1].get_or_none(object_id=id)) is not None:
            await instance.delete()
