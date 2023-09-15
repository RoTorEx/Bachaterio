from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select
from aiogram_dialog.widgets.text import Format

from src.bot.enums import BachataLessonLevel, BachataLessonStatus, BachataLessonType, SelectOrder
from src.bot.states import SetupLessonsSelectDialog

from .getters import get_setup_watch_data
from .handlers import other_type_handler, time_to_dance_handler, update_config


setup_watch_lessons_config_dialog = Dialog(
    Window(
        Format(
            "This is the current config for lesson selection:\n"
            + "1. Sort order: <b>{lesson_order}</b>\n"
            + "2. Lesson type: <b>{lesson_type}</b>\n"
            + "3. Lesson level: <b>{lesson_level}</b>\n"
            + "4. Lesson status: <b>{lesson_status}</b>\n"
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in SelectOrder],
            item_id_getter=lambda x: x,
            id="w_lesson_order",
            on_click=update_config,
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in BachataLessonType],
            item_id_getter=lambda x: x,
            id="w_lesson_type",
            on_click=update_config,
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in BachataLessonLevel],
            item_id_getter=lambda x: x,
            id="w_lesson_level",
            on_click=update_config,
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in BachataLessonStatus],
            item_id_getter=lambda x: x,
            id="w_lesson_status",
            on_click=update_config,
        ),
        MessageInput(time_to_dance_handler, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),
        state=SetupLessonsSelectDialog.setup,
        getter=get_setup_watch_data,
    )
)
