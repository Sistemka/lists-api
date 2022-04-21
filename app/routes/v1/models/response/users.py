from tortoise.contrib.pydantic import pydantic_model_creator

from db.models.user import UserModel


GetUser = pydantic_model_creator(
    UserModel,
    name="GetUser",
)

GetUserPreview = pydantic_model_creator(
    UserModel,
    name="GetUserPreview",
    include=("id", "name", "profile_picture"),
    computed=("profile_picture", ),
)
