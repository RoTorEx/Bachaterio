from typing import Any

from aiogram.types.user import User
from aiogram_dialog import ChatEvent, DialogManager

from src.bot.states import SetLevelSubManageUserDialog


async def update_level(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    event_user: User = manager.middleware_data["event_from_user"]

    if event_user.id == manager.start_data["user_id"]:
        await callback.answer(text="You can't change your status!", show_alert=True)

    else:
        await manager.start(
            state=SetLevelSubManageUserDialog.set_level,
            data={
                "user_id": manager.start_data["user_id"],
                "edit_level": manager.start_data["edit_level"],
            },
        )


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
