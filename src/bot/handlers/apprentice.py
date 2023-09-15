from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram_dialog import DialogManager, StartMode

from src.bot.enums import BachataLessonLevel, BachataLessonStatus, BachataLessonType, SelectOrder
from src.bot.keyboards import finish_filter_setup
from src.bot.states import SetupLessonsSelectDialog, WatchLessonDialog


async def msg_setup_select_config(message: Message, state: FSMContext, bot: Bot, dialog_manager: DialogManager) -> None:
    await message.answer(
        "Set up filters please.\n\n"
        + "A lot of vidoes are in `<b>disable</b>` status right now, so able to play with config!\n\n"
        + "<b>Dance</b> in chat using your <i>keybutton</i> when you're done setting up the coffig to see what I have to you!",  # noqa
        reply_markup=finish_filter_setup(),
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

    await message.answer(
        "Watching mode activated.\nEnter `/menu` to get back.\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    await dialog_manager.start(
        WatchLessonDialog.watch,
        mode=StartMode.RESET_STACK,
        data={
            "skip_stamp": 0,
            "sorting_order": previous_dialog_result.get("lesson_order"),
            "lesson_type": previous_dialog_result.get("lesson_type"),
            "lesson_level": previous_dialog_result.get("lesson_level"),
            "lesson_status": previous_dialog_result.get("lesson_status"),
        },
    )
