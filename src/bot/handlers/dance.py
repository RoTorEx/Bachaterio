import time
from datetime import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, StartMode
from bson import ObjectId

from src.bot.enums import BachataLessonLevel, BachataLessonStatus, BachataLessonType, SelectOrder
from src.bot.keyboards import choosen_dance_module, finished_filter_setup
from src.bot.models import TutorialModel
from src.bot.states import LoaderState, MenuState, SetupLessonsSelectDialog, WatchLessonDialog
from src.bot.utils import convert_size
from src.infrastructure.database import cursor
from src.infrastructure.logger_builder import build_logger


logger = build_logger(__name__)


# ======
# Common
async def msg_select_dance(message: Message, state: FSMContext, bot: Bot, dialog_manager: DialogManager) -> None:
    await state.set_state(MenuState.start_dance)
    await message.answer(
        "Let's make some bachata!",
        reply_markup=choosen_dance_module(),
    )


# ==========
# Apprentice
async def msg_setup_select_config(message: Message, state: FSMContext, bot: Bot, dialog_manager: DialogManager) -> None:
    await message.answer(
        "Set up filters please.\n\n"
        + "A lot of vidoes are in `<b>disable</b>` status right now, so able to play with config!\n\n"
        + "<b>Dance</b> in chat using your <i>keybutton</i> when you're done setting up the coffig to see what I have to you!",  # noqa
        reply_markup=finished_filter_setup(),
    )

    await dialog_manager.start(
        SetupLessonsSelectDialog.setup,
        mode=StartMode.RESET_STACK,
        data={
            "lesson_order": SelectOrder.RANDOM.value,
            "lesson_type": BachataLessonType.ALL.value,
            "lesson_level": BachataLessonLevel.ALL.value,
            "lesson_status": BachataLessonStatus.ENABLE.value,  # Set as Enable as default for users
        },
    )


async def msg_start_show_lessons(message: Message, state: FSMContext, bot: Bot, dialog_manager: DialogManager) -> None:
    state_data = await state.get_data()
    previous_dialog_result = state_data.get("setup_watch_response")

    query = {}  # Update with incoming values

    sorting_order = previous_dialog_result.get("lesson_order")
    lesson_type = previous_dialog_result.get("lesson_type")
    lesson_level = previous_dialog_result.get("lesson_level")
    lesson_status = previous_dialog_result.get("lesson_status")

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

    print(f"{query = }")
    count = cursor.tutorials.count_documents(query)

    await message.answer(
        f"I found `{count}` tutorials on your configuration",
        reply_markup=ReplyKeyboardRemove(),
    )

    await dialog_manager.start(
        WatchLessonDialog.watch,
        mode=StartMode.RESET_STACK,
        data={
            "skip_stamp": 0,
            "sorting_order": sorting_order,
            "lesson_type": lesson_type,
            "lesson_level": lesson_level,
            "lesson_status": lesson_status,
            "count": count
        },
    )


# ======
# Loader
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
    await state.set_state(MenuState.start_dance)
    await message.answer("👌", reply_markup=choosen_dance_module())


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
    else:
        await message.answer(r"Unsupported type ¯\_(ツ)_/¯. Send video.")
