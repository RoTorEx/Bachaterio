from datetime import datetime

from src.bot.enums import UserLevel

from .base import BaseAdminModel


class UserModel(BaseAdminModel):
    user_id: int
    chat_id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str | None
    level: UserLevel
    created_at: datetime
