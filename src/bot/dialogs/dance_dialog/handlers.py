import time
from datetime import date, datetime
from typing import Any
from uuid import uuid4

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from bson import ObjectId

from src.bot.enums import BachataLessonLevel, BachataLessonStatus, BachataLessonType, SelectOrder, SuggestionStatus
from src.bot.models import SuggestionModel, TutorialModel
from src.bot.utils import convert_size
from src.infrastructure.database import cursor
from src.infrastructure.logger_builder import build_logger


logger = build_logger(__name__)


# ======
# COMMON
async def return_to_menu(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await manager.done()


async def return_back(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await manager.back()


# ====
# LOAD
async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    manager.dialog_data["lesson_date"] = selected_date

    await callback.answer(text=f"{selected_date}")
    await manager.next()


async def video_handler(message: Message, message_input: MessageInput, manager: DialogManager):
    lesson_date = manager.dialog_data["lesson_date"]

    tg_file_id = message.video.file_id
    tg_unique_file_id = message.video.file_unique_id
    original_file_name = message.video.file_name
    duration = time.strftime("%M:%S", time.gmtime(message.video.duration))
    size = convert_size(message.video.file_size)

    result = cursor.tutorials.find_one({"tg_unique_file_id": tg_unique_file_id})

    if not result:
        tutorial_obj = TutorialModel(
            tg_unique_file_id=tg_unique_file_id,
            tg_file_id=tg_file_id,
            original_file_name=original_file_name,
            lesson_description="Describe me :)",
            lesson_type=None,
            lesson_date=lesson_date,
            lesson_level=None,
            lesson_status=BachataLessonStatus.DISABLE,
            loaded_by=message.from_user.id,
            is_active=True,
            last_updated_at=None,
            suggestion_id=None,
            created_at=datetime.utcnow(),
        )

        new_document: ObjectId = cursor.tutorials.insert_one(tutorial_obj.model_dump())
        document: dict = cursor.tutorials.find_one(new_document.inserted_id)
        tutorial_obj = TutorialModel.model_validate(document)

        response_message = f"{original_file_name} has been saved!\nInfo: {duration} - {size}."

        logger.info(f"Loaded new video with `{tutorial_obj.tg_unique_file_id}` ID.")

    else:
        response_message = "I alredy have this video."

    await message.answer(response_message)


async def other_type_handler(message: Message, message_input: MessageInput, manager: DialogManager):
    await message.answer(r"Unsupported type ¯\_(ツ)_/¯. Send video.")


# ========
# PRACTICE
async def setup_config(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data["lesson_order"] = SelectOrder.RANDOM.value
    manager.dialog_data["lesson_type"] = BachataLessonType.ALL.value
    manager.dialog_data["lesson_level"] = BachataLessonLevel.ALL.value
    manager.dialog_data["lesson_status"] = BachataLessonStatus.ENABLE.value


async def update_config(callback: ChatEvent, select: Any, manager: DialogManager, item_id: str) -> None:
    if SelectOrder.has_value(item_id):
        manager.dialog_data["lesson_order"] = item_id

    if BachataLessonType.has_value(item_id):
        manager.dialog_data["lesson_type"] = item_id

    if BachataLessonLevel.has_value(item_id):
        manager.dialog_data["lesson_level"] = item_id

    if BachataLessonStatus.has_value(item_id):
        # ToDo: lock this function for nonmanager users (use reauest to MongoDB)
        manager.dialog_data["lesson_status"] = item_id


async def save_lesson_filter(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    query = {}  # Update with incoming values

    sorting_order = manager.dialog_data["lesson_order"]
    lesson_type = manager.dialog_data["lesson_type"]
    lesson_level = manager.dialog_data["lesson_level"]
    lesson_status = manager.dialog_data["lesson_status"]

    if lesson_type in [BachataLessonType.COMBINATION, BachataLessonType.DANCE, BachataLessonType.ELEMENT]:
        query.update({"lesson_type": lesson_type})

    if lesson_level in [
        BachataLessonLevel.NOVICE,
        BachataLessonLevel.BEGINNER,
        BachataLessonLevel.INTERMEDIATE,
        BachataLessonLevel.ADVANCED,
        BachataLessonLevel.EXPERT,
    ]:
        query.update({"lesson_level": lesson_level})

    query.update({"lesson_status": lesson_status})

    count = cursor.tutorials.count_documents(query)

    manager.dialog_data["skip_stamp"] = 0
    manager.dialog_data["count"] = count
    manager.dialog_data["sorting_order"] = sorting_order

    await callback.answer(text=f"I found `{count}` tutorials on your configuration")


async def update_info(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    manager.dialog_data["suggestion_id"] = str(uuid4())


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


async def enter_description(message: Message, message_input: MessageInput, manager: DialogManager):
    _ = manager.dialog_data["lesson_id"]
    suggestion_id = manager.dialog_data["suggestion_id"]

    payload = {"edit_lesson_description": message.text}
    cursor.suggestions.update_one({"suggestion_id": suggestion_id}, {"$set": payload})


async def save_suggestion(callback: CallbackQuery, button: Button, manager: DialogManager):
    unique_file_id = manager.dialog_data["lesson_id"]
    suggestion_id = manager.dialog_data["suggestion_id"]

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
    edit_suggestion_lesson = SuggestionModel.model_validate(edit_suggestion_document)

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


async def edit_lesson(callback: ChatEvent, select: Any, manager: DialogManager, item_id: str):
    payload = {}

    _ = manager.dialog_data["lesson_id"]
    suggestion_id = manager.dialog_data["suggestion_id"]

    if BachataLessonType.has_value(item_id):
        payload.update({"edit_lesson_type": item_id})

    if BachataLessonLevel.has_value(item_id):
        payload.update({"edit_lesson_level": item_id})

    if BachataLessonStatus.has_value(item_id):
        payload.update({"edit_lesson_status": item_id})

    cursor.suggestions.update_one({"suggestion_id": suggestion_id}, {"$set": payload})
