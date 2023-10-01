from typing import Any
from uuid import uuid4

from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.input import MessageInput

from src.bot.enums import UserLevel
from src.infrastructure.database import cursor


# ======
# COMMON
async def return_to_menu(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await manager.done()


async def return_back(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await manager.back()


# =====
# USERS
async def manage_users(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    count = cursor.users.count_documents({})

    manager.dialog_data["skip_stamp"] = 0
    manager.dialog_data["count"] = count

    await callback.answer(text=f"I have `{count}` registered users.")


async def text_message_handler(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    chat_id = manager.dialog_data["chat_id"]

    bot: Bot = manager.middleware_data["bot"]

    # ToDo: === return call back here that message has been sent ===
    await message.answer(text=f"Following message: <i>{message.text}</i> has been sent to user.")
    await bot.send_message(chat_id=chat_id, text=message.text)


async def other_type_handler(message: Message, message_input: MessageInput, manager: DialogManager):
    await message.answer(r"Unsupported type ¯\_(ツ)_/¯")


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
    chat_id = manager.dialog_data["chat_id"]
    user_id = manager.dialog_data["user_id"]

    cursor.users.update_one({"user_id": user_id}, {"$set": {"level": level}})

    bot: Bot = manager.middleware_data["bot"]

    if level == UserLevel.STRANGER:
        tip = "Sorry, you no longer have permission to view the lessons :'("

    elif level == UserLevel.MEMBER:
        tip = "Hey, you can look at the lessons now!"

    elif level == UserLevel.MODERATOR:
        tip = "You can edit and upload lessons!"

    elif level == UserLevel.ADMIN:
        tip = "Now you are able to manage!"

    else:
        tip = "You've got <b>GOD</b> mode!"

    await callback.answer(text="User has been notified of the level changes!", show_alert=True)
    await bot.send_message(chat_id=chat_id, text=tip)


# ===========
# SUGGESTIONS
async def manage_suggestions(callback: ChatEvent, select: Any, manager: DialogManager):
    await callback.answer(text="Not implemented!", show_alert=True)


# ===========
# DO ACTION
async def do_some_action(callback: ChatEvent, select: Any, manager: DialogManager):
    # await callback.answer(text="Unavailable now.", show_alert=True)
    all_tutorials = cursor.tutorials.find({"id": None}).distinct("tg_unique_file_id")

    tutorials_count = 0
    suggestions_count = 0
    for tutorial_file_id in all_tutorials:
        obj_id = str(uuid4())

        result = cursor.tutorials.update_one({"tg_unique_file_id": tutorial_file_id}, {"$set": {"id": obj_id}})
        tutorials_count += result.modified_count

        result = cursor.suggestions.update_many(
            {"tg_unique_file_id": tutorial_file_id}, {"$set": {"tutorial_id": obj_id}}
        )
        suggestions_count += result.modified_count

    await callback.answer(
        text=f"`{tutorials_count}` tutorials and `{suggestions_count}` suggestions were modified.", show_alert=True
    )
