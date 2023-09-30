from datetime import datetime

from src.bot.enums import LessonLevel, LessonStatus, LessonType, SuggestionStatus

from .base import BaseAdminModel


class SuggestionModel(BaseAdminModel):
    suggestion_id: str
    tg_unique_file_id: str
    edit_lesson_description: str
    edit_lesson_date: datetime
    edit_lesson_type: LessonType | None
    edit_lesson_level: LessonLevel | None
    edit_lesson_status: LessonStatus
    suggestion_status: SuggestionStatus
    suggested_by: int
    is_active: bool
    created_at: datetime
