from datetime import datetime

from src.bot.enums import LessonLevel, LessonType

from .base import BaseAdminModel


class SuggestionModel(BaseAdminModel):
    id: str
    tutorial_id: str
    tg_unique_file_id: str
    edit_lesson_description: str
    edit_lesson_date: datetime
    edit_lesson_type: LessonType | None
    edit_lesson_level: LessonLevel | None
    suggested_by: int
    is_active: bool
    created_at: datetime
