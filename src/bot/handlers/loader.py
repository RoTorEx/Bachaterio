import time
from datetime import datetime

from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, StartMode
from bson import ObjectId

from src.bot.enums import BachataLessonStatus
from src.bot.keyboards import buttons_menu
from src.bot.models import BachataTutorialModel
from src.bot.states import LoaderState, MenuState
from src.bot.utils import convert_size
from src.infrastructure.database import cursor
from src.infrastructure.logger_builder import build_logger


logger = build_logger(__name__)
loader_router = Router()


async def msg_save_lessons(message: Message, state: FSMContext, dialog_manager: DialogManager) -> None:
    await message.answer(
        "Before load your videos select lesson (record) date.",
        reply_markup=ReplyKeyboardRemove(),
    )

    await dialog_manager.start(
        LoaderState.select_date,
        mode=StartMode.RESET_STACK,
    )


async def msg_finish_load(message: Message, state: FSMContext) -> None:
    await state.set_state(MenuState.start_menu)
    await message.answer("👌", reply_markup=buttons_menu())


async def msg_edit_date(message: Message, state: FSMContext, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        LoaderState.select_date,
        mode=StartMode.RESET_STACK,
    )


async def msg_save_lesson_videos(message: Message, state: FSMContext, bot: Bot) -> None:
    if message.video:
        state_data = await state.get_data()
        lesson_date = state_data.get("lesson_date")

        tg_file_id = message.video.file_id
        tg_unique_file_id = message.video.file_unique_id
        original_file_name = message.video.file_name
        duration = time.strftime("%M:%S", time.gmtime(message.video.duration))
        size = convert_size(message.video.file_size)

        result = cursor.tutorials.find_one({"tg_unique_file_id": tg_unique_file_id})

        if not result:
            tutorial_obj_id = ObjectId()

            tutorial_obj = BachataTutorialModel(
                obj_id=tutorial_obj_id,
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
            tutorial_obj = BachataTutorialModel.model_validate(document)

            response_message = f"{original_file_name} has been saved!\nInfo: {duration} - {size}."

            logger.info(f"Loaded new video with `{tutorial_obj.tg_unique_file_id}` ID.")

        else:
            response_message = "I alredy have this video."

        await message.answer(response_message)
    else:
        await message.answer(r"Unsupported type ¯\_(ツ)_/¯. Send video.")
