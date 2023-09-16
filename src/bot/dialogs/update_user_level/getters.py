from aiogram_dialog import DialogManager

from src.bot.models import UserModel
from src.infrastructure.database import cursor


async def get_data_update_user_level(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.start_data["user_id"]
    edit_level = dialog_manager.start_data["edit_level"]

    document: dict = cursor.users.find_one({"user_id": user_id})

    user_obj = UserModel.model_validate(document)

    update_user_level_resposen_dialog = {
        "user_id": user_obj.user_id,
        "first_name": user_obj.first_name,
        "last_name": user_obj.last_name,
        "username": user_obj.username,
        "level": user_obj.level.value,
        "created_at": user_obj.created_at.strftime("%d/%m/%Y %H:%M:%S"),
        "edit_level": edit_level,
    }

    return update_user_level_resposen_dialog
