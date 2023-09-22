from aiogram.types import User
from aiogram_dialog import DialogManager

from src.bot.models import UserModel
from src.infrastructure.config_reader import settings
from src.infrastructure.database import cursor


# ======
# COMMON
async def get_info_data(dialog_manager: DialogManager, **kwargs):
    response = {}
    event_user: User = dialog_manager.middleware_data["event_from_user"]

    document: dict = cursor.users.find_one({"user_id": event_user.id})
    user_obj = UserModel.model_validate(document)

    response.update(
        {
            "my_name": settings.app.name,
            "my_version": settings.app.version,
            "my_description": settings.app.description,
            "your_id": user_obj.user_id,
            "your_level": user_obj.level.value,
        }
    )

    return response
