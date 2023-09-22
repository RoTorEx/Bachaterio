from typing import Any

from aiogram_dialog import ChatEvent, DialogManager

from src.infrastructure.database import cursor


# ======
# COMMON
async def return_to_menu(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await manager.done()


async def return_back(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await manager.back()


# =====
# USERS
async def manage_users(callback: ChatEvent, select: Any, manager: DialogManager):
    count = cursor.users.count_documents({})

    manager.dialog_data["skip_stamp"] = 0
    manager.dialog_data["count"] = count

    await callback.answer(text=f"I have `{count}` registered users.")


async def send_message(callback: ChatEvent, select: Any, manager: DialogManager):
    await callback.answer(text="Some message has gone.", show_alert=True)


async def try_update_level(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await callback.answer(text="You can't change your status!", show_alert=True)


async def increment_counter(callback: ChatEvent, select: Any, manager: DialogManager, item_id: str):
    count = manager.dialog_data["count"]

    if item_id == "Next →":
        if manager.dialog_data["skip_stamp"] < count - 1:
            manager.dialog_data["skip_stamp"] += 1

        else:
            await callback.answer(text="It's the last item on the right!", show_alert=True)

    if item_id == "← Previos":
        if manager.dialog_data["skip_stamp"] > 0:
            manager.dialog_data["skip_stamp"] -= 1

        else:
            await callback.answer(text="It's the last item on the left!", show_alert=True)


async def set_level(callback: ChatEvent, select: Any, manager: DialogManager, item_id: str):
    manager.dialog_data["edit_level"] = item_id


async def save_level(callback: ChatEvent, select: Any, manager: DialogManager):
    level = manager.dialog_data["edit_level"]
    user_id = manager.dialog_data["user_id"]

    cursor.users.update_one({"user_id": user_id}, {"$set": {"level": level}})


# ===========
# SUGGESTIONS
async def manage_suggestions(callback: ChatEvent, select: Any, manager: DialogManager):
    await callback.answer(text="Not implemented!", show_alert=True)
