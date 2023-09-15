from datetime import datetime

from src.bot.enums import BachataLessonLevel, BachataLessonStatus, BachataLessonType, SuggestionStatus

from .base import BaseAdminModel


class SuggestionModel(BaseAdminModel):
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
