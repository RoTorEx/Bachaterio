from aiogram import html
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from src.bot.enums import BachataLessonLevel, BachataLessonStatus, BachataLessonType
from src.bot.states import EditSubWatchLessonDialog

from .getters import get_data_edit_dialog
from .handlers import close_subdialog, edit_lesson, enter_description, other_type_handler


edit_lesson_sub_dialog = Dialog(
    Window(
        Format(
            "Id: <i>{lesson_id}</i>\n"
            + f"{html.quote('=== < ~ > ===')}\n"
            + "Saved data:\n"
            + "Date: <b>{lesson_date}</b>\n"
            + "Type: <b>{lesson_type}</b>\n"
            + "Level: <b>{lesson_level}</b>\n"
            + "Status: <b>{lesson_status}</b>\n"
            + "Description: <b>{lesson_description}</b>\n\n"
            + f"{html.quote('=== < ~ > ===')}\n\n"
            + "Suggested changes:\n"
            + "Type: <b>{edit_lesson_type}</b>\n"
            + "Level: <b>{edit_lesson_level}</b>\n"
            + "Status: <b>{edit_lesson_status}</b>\n"
            + "Description: <b>{edit_lesson_description}</b>\n\n"
            + f"{html.quote('=== < ~ > ===')}\n\n"
            + "<i>Edit tip: to update `description` write message in the chat</i>."
        ),
        DynamicMedia("lesson_video"),
        Select(
            Format("{item}"),
            items=[e.value for e in BachataLessonType if e != BachataLessonType.ALL],
            item_id_getter=lambda x: x,
            id="e_lesson_type",
            on_click=edit_lesson,
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in BachataLessonLevel if e != BachataLessonLevel.ALL],
            item_id_getter=lambda x: x,
            id="e_lesson_level",
            on_click=edit_lesson,
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in BachataLessonStatus],
            item_id_getter=lambda x: x,
            id="e_lesson_status",
            on_click=edit_lesson,
        ),
        Button(Const("Save"), id="s_edit", on_click=close_subdialog),
        MessageInput(enter_description, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),
        state=EditSubWatchLessonDialog.edit,
        getter=get_data_edit_dialog,
    ),
)
