from typing import Any

from aiogram_dialog import ChatEvent, DialogManager
from src.infrastructure.database import cursor


async def set_level(callback: ChatEvent, select: Any, manager: DialogManager, item_id: str):
    manager.start_data["edit_level"] = item_id


async def save_level(callback: ChatEvent, select: Any, manager: DialogManager):
    level = manager.start_data["edit_level"]
    user_id = manager.start_data["user_id"]

    cursor.users.update_one({"user_id": user_id}, {"$set": {"level": level}})
    await manager.done()


async def revert_level(callback: ChatEvent, select: Any, manager: DialogManager):
    await manager.done()
