from datetime import datetime

from src.bot.enums import LessonLevel, LessonType

from .base import BaseAdminModel


class TutorialModel(BaseAdminModel):
    id: str
    tg_unique_file_id: str
    tg_file_id: str
    original_file_name: str
    lesson_description: str
    lesson_date: datetime
    lesson_type: LessonType | None
    lesson_level: LessonLevel | None
    loaded_by: int
    is_active: bool
    last_updated_at: datetime | None
    suggestion_id: str | None
    created_at: datetime
