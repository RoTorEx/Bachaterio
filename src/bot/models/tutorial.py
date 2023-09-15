from datetime import datetime

from bson.objectid import ObjectId
from pydantic import Field

from src.bot.enums import BachataLessonLevel, BachataLessonStatus, BachataLessonType

from .base import BaseAdminModel, PyObjectId


class _BachataTutorialModel(BaseAdminModel):
    """Mongo object."""

    tg_unique_file_id: str
    tg_file_id: str
    original_file_name: str
    lesson_description: str
    lesson_date: datetime
    lesson_type: BachataLessonType | None
    lesson_level: BachataLessonLevel | None
    lesson_status: BachataLessonStatus
    loaded_by: int
    is_active: bool
    last_updated_at: datetime | None
    suggestion_id: str | None
    created_at: datetime


class BachataTutorialModel(_BachataTutorialModel):
    obj_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
