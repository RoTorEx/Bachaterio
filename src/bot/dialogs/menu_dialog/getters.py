from aiogram.types import User
from aiogram_dialog import DialogManager

from src.bot.enums import UserLevel
from src.bot.models import UserModel
from src.infrastructure.database import cursor


async def get_menu_data(dialog_manager: DialogManager, **kwargs):
    response = {}

    event_user: User = dialog_manager.middleware_data["event_from_user"]

    document: dict = cursor.users.find_one({"user_id": event_user.id})
    user_obj = UserModel.model_validate(document)

    if user_obj.level == UserLevel.MEMBER:
        response.update({"is_member": True})

    if user_obj.level in [UserLevel.MODERATOR, UserLevel.ADMIN]:
        response.update({"is_member": True})
        response.update({"is_moder": True})

    if user_obj.level == UserLevel.SUPERUSER:
        response.update({"is_member": True})
        response.update({"is_moder": True})
        response.update({"is_superuser": True})

    return response
