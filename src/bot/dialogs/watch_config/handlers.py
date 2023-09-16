from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram.types.update import Update
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.bot.enums import BachataLessonLevel, BachataLessonStatus, BachataLessonType, SelectOrder


async def update_config(callback: ChatEvent, select: Any, manager: DialogManager, item_id: str) -> None:
    if SelectOrder.has_value(item_id):
        manager.start_data["lesson_order"] = item_id

    if BachataLessonType.has_value(item_id):
        manager.start_data["lesson_type"] = item_id

    if BachataLessonLevel.has_value(item_id):
        manager.start_data["lesson_level"] = item_id

    if BachataLessonStatus.has_value(item_id):
        # ToDo: lock this function for nonmanager users (use reauest to MongoDB)
        manager.start_data["lesson_status"] = item_id


async def other_type_handler(message: Message, message_input: MessageInput, manager: DialogManager):
    await message.answer("Only `🕺` or `💃` are expected.", disable_notification=True,)


async def time_to_dance_handler(callback: CallbackQuery, button: Button, manager: DialogManager) -> None:
    update: Update = manager.middleware_data["event_update"]

    if update.message.text in {"🕺", "💃"}:
        if manager.is_preview():
            await manager.done()
            return

        await manager.done()
