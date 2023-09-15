from datetime import datetime

from bson.objectid import ObjectId
from pydantic import Field

from src.bot.enums import UserLevel

from .base import BaseAdminModel, PyObjectId


class _UserModel(BaseAdminModel):
    """Mongo object."""

    id: int
    chat_id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str | None
    level: UserLevel
    created_at: datetime


class UserModel(_UserModel):
    obj_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
