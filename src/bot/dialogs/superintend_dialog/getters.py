from aiogram.types import User
from aiogram_dialog import DialogManager

from src.bot.models import UserModel
from src.infrastructure.database import cursor


# ======
# COMMON
async def get_superintend_menu_data(dialog_manager: DialogManager, **kwargs):
    response = {}

    count = cursor.users.count_documents({})
    response.update({"count": count})

    return response


# =====
# USERS
async def get_data_manage_user(dialog_manager: DialogManager, **kwargs):
    response = {}
    user_obj = None

    skip_stamp = dialog_manager.dialog_data["skip_stamp"]
    user_count = dialog_manager.dialog_data["count"]

    result = list(cursor.users.find({}).sort([("created_at", -1), ("_id", 1)]).skip(skip_stamp).limit(1))

    event_user: User = dialog_manager.middleware_data["event_from_user"]

    if result:
        document: dict = result[-1]
        user_obj = UserModel.model_validate(document)

    if event_user.id == user_obj.user_id:
        response.update({"is_myself": True})

    else:
        response.update({"is_another": True})

    if user_obj:
        response.update(
            {
                "current": skip_stamp + 1,
                "count": user_count,
                "user_id": user_obj.user_id,
                "first_name": user_obj.first_name if user_obj.first_name else "",
                "last_name": user_obj.last_name if user_obj.last_name else "",
                "username": f"@{user_obj.username}" if user_obj.username else "",
                "level": user_obj.level.value,
                "created_at": user_obj.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                "show_user": True,
            }
        )
        dialog_manager.dialog_data["user_id"] = user_obj.user_id
        dialog_manager.dialog_data["edit_level"] = user_obj.level.value

    else:
        response.update({"say_sorry": True})

    return response


async def get_data_update_user_level(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.dialog_data["user_id"]
    edit_level = dialog_manager.dialog_data["edit_level"]

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
