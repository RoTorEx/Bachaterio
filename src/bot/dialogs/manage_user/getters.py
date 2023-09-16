from aiogram_dialog import DialogManager

from src.bot.models import UserModel
from src.infrastructure.database import cursor


async def get_data_manage_user(dialog_manager: DialogManager, **kwargs):
    user_obj = None
    skip_stamp = dialog_manager.start_data["skip_stamp"]

    result = list(cursor.users.find({}).sort([("created_at", -1), ("_id", 1)]).skip(skip_stamp).limit(1))

    if result:
        document: dict = result[-1]
        user_obj = UserModel.model_validate(document)

    if user_obj:
        manage_user_dialog_response = {
            "show_user": True,
            "user_id": user_obj.user_id,
            "first_name": user_obj.first_name,
            "last_name": user_obj.last_name,
            "username": user_obj.username,
            "level": user_obj.level.value,
            "created_at": user_obj.created_at.strftime("%d/%m/%Y %H:%M:%S"),
        }
        dialog_manager.start_data["user_id"] = user_obj.user_id
        dialog_manager.start_data["edit_level"] = user_obj.level.value

    else:
        manage_user_dialog_response = {
            "say_sorry": True,
        }

    return manage_user_dialog_response
