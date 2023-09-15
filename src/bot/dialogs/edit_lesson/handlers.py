from datetime import datetime
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from src.bot.enums import BachataLessonLevel, BachataLessonStatus, BachataLessonType, SuggestionStatus
from src.bot.models import SuggestEditTutorialModel
from src.infrastructure.database import cursor
from src.infrastructure.logger_builder import build_logger


logger = build_logger(__name__)


async def enter_description(message: Message, message_input: MessageInput, manager: DialogManager):
    _ = manager.start_data["lesson_id"]
    suggestion_id = manager.start_data["suggestion_id"]

    payload = {"edit_lesson_description": message.text}
    cursor.suggestions.update_one({"suggestion_id": suggestion_id}, {"$set": payload})


async def close_subdialog(callback: CallbackQuery, button: Button, manager: DialogManager):
    unique_file_id = manager.start_data["lesson_id"]
    suggestion_id = manager.start_data["suggestion_id"]

    edit_suggestion_document: dict = cursor.suggestions.find_one_and_update(
        {"suggestion_id": suggestion_id},
        {
            "$set": {
                "is_active": True,
                "suggestion_status": SuggestionStatus.ACCEPT,
            }
        },
        upsert=True,
        return_document=True,
    )
    edit_suggestion_lesson = SuggestEditTutorialModel.model_validate(edit_suggestion_document)

    _: dict = cursor.tutorials.find_one_and_update(
        {"tg_unique_file_id": unique_file_id},
        {
            "$set": {
                "lesson_description": edit_suggestion_lesson.edit_lesson_description,
                # "lesson_date": edit_suggestion_lesson.edit_lesson_date,  # !Not ready change dates!
                "lesson_type": edit_suggestion_lesson.edit_lesson_type,
                "lesson_level": edit_suggestion_lesson.edit_lesson_level,
                "lesson_status": edit_suggestion_lesson.edit_lesson_status,
                "suggestion_id": edit_suggestion_lesson.suggestion_id,
                "last_updated_at": datetime.utcnow(),
            }
        },
    )

    logger.info(
        f"New suggestion `{edit_suggestion_lesson.suggestion_id}` from `{edit_suggestion_lesson.suggested_by}`."
    )

    await manager.done()


async def edit_lesson(callback: ChatEvent, select: Any, manager: DialogManager, item_id: str):
    payload = {}

    _ = manager.start_data["lesson_id"]
    suggestion_id = manager.start_data["suggestion_id"]

    if BachataLessonType.has_value(item_id):
        payload.update({"edit_lesson_type": item_id})

    if BachataLessonLevel.has_value(item_id):
        payload.update({"edit_lesson_level": item_id})

    if BachataLessonStatus.has_value(item_id):
        payload.update({"edit_lesson_status": item_id})

    cursor.suggestions.update_one({"suggestion_id": suggestion_id}, {"$set": payload})


async def other_type_handler(message: Message, message_input: MessageInput, manager: DialogManager):
    await message.answer("Say hello!")
