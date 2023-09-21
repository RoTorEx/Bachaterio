from aiogram import html
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from src.bot.states import WatchLessonDialog

from .getters import get_data_watch_dialog
from .handlers import increment_counter, update_info, watch_lessons_dialog_process_result


watch_lessons_dialog = Dialog(
    Window(
        Multi(
            Format(
                "Id: <i>{lesson_id}</i>\n"
                + f"{html.quote('=== < ~ > ===')}\n"
                + "Date: <b>{lesson_date}</b>\n"
                + "Type: <b>{lesson_type}</b>\n"
                + "Level: <b>{lesson_level}</b>\n"
                + "Status: <b>{lesson_status}</b>\n"
                + "Description: <b>{lesson_description}</b>\n",
                when="show_lesson",
            ),
            Format("I'm sorry, but I couldn't find any lessons on the given parameters :'(", when="say_sorry"),
        ),
        DynamicMedia("lesson_video", when="show_lesson"),
        Select(
            Format("{item}"),
            items=["Edit lesson ✏️"],
            item_id_getter=lambda x: x,
            id="w_edit_info",
            on_click=update_info,
            when="show_lesson",
        ),
        Select(
            Format("{item}"),
            items=["← Previos", "Next →"],
            item_id_getter=lambda x: x,
            id="w_count_stamp",
            on_click=increment_counter,
            when="order",
        ),
        Button(Const("🎲"), id="w_random", when="random"),
        state=WatchLessonDialog.watch,
        getter=get_data_watch_dialog,
    ),
    on_process_result=watch_lessons_dialog_process_result,
)
