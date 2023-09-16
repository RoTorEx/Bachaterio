from typing import Any
from uuid import uuid4

from aiogram.types.user import User
from aiogram_dialog import ChatEvent, Data, DialogManager

from src.bot.enums import UserLevel
from src.bot.models import UserModel
from src.bot.states import EditSubWatchLessonDialog
from src.infrastructure.database import cursor


async def watch_lessons_dialog_process_result(start_data: Data, result: Any, dialog_manager: DialogManager):
    pass


async def update_info(callback: ChatEvent, select: Any, manager: DialogManager, item_id: str) -> None:
    event_user: User = manager.middleware_data["event_from_user"]
    document = cursor.users.find_one({"user_id": event_user.id})
    user_obj = UserModel.model_validate(document)

    if user_obj.level in [UserLevel.SUPERUSER, UserLevel.ADMIN, UserLevel.MODERATOR]:
        await manager.start(
            state=EditSubWatchLessonDialog.edit,
            data={"lesson_id": manager.start_data.get("lesson_id"), "suggestion_id": str(uuid4())},
        )

    else:
        await callback.answer(text="Locked.", show_alert=True)


async def increment_counter(callback: ChatEvent, select: Any, manager: DialogManager, item_id: str):
    count = manager.start_data["count"]

    if item_id == "Next →":
        if manager.start_data["skip_stamp"] < count - 1:
            manager.start_data["skip_stamp"] += 1

        else:
            await callback.answer(text="It's the last item on the right!", show_alert=True)

    if item_id == "← Previos":
        if manager.start_data["skip_stamp"] > 0:
            manager.start_data["skip_stamp"] -= 1

        else:
            await callback.answer(text="It's the last item on the left!", show_alert=True)
