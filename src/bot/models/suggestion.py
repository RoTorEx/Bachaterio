from datetime import datetime

from bson.objectid import ObjectId
from pydantic import Field

from src.bot.enums import BachataLessonLevel, BachataLessonStatus, BachataLessonType, SuggestionStatus

from .base import BaseAdminModel, PyObjectId


class _SuggestEditTutorialModel(BaseAdminModel):
    """Mongo object."""

    suggestion_id: str
    tg_unique_file_id: str
    edit_lesson_description: str
    edit_lesson_date: datetime
    edit_lesson_type: BachataLessonType | None
    edit_lesson_level: BachataLessonLevel | None
    edit_lesson_status: BachataLessonStatus
    suggestion_status: SuggestionStatus
    suggested_by: int
    is_active: bool
    created_at: datetime


class SuggestEditTutorialModel(_SuggestEditTutorialModel):
    obj_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
