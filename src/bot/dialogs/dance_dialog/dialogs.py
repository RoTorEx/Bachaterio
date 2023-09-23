import random as r

from aiogram import html
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Calendar, Select, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from src.bot.enums import BachataLessonLevel, BachataLessonStatus, BachataLessonType, SelectOrder
from src.bot.states import DanceDialog

from .getters import get_dance_data, get_edit_lesson_data, get_lesson_data, get_lesson_filter_data, get_load_lesson_data
from .handlers import (
    change_level,
    change_order,
    change_status,
    change_type,
    edit_lesson,
    enter_description,
    increment_counter,
    on_date_selected,
    other_type_handler,
    return_back,
    return_to_menu,
    save_lesson_filter,
    save_suggestion,
    setup_config,
    update_info,
    video_handler,
)


dance_dialog = Dialog(
    Window(
        Const(r"Make your choise"),
        SwitchTo(
            Const("New lesson 💡"),
            id="continue_load",
            state=DanceDialog.select_lesson_date,
            when="is_moder",
        ),
        SwitchTo(
            Const("Practice in bachata 🎯"),
            id="continue_practice",
            state=DanceDialog.create_lesson_filter,
            on_click=setup_config,
        ),
        Button(
            Const("Back to menu ↩"),
            id="return_to_main_menu",
            on_click=return_to_menu,
        ),
        state=DanceDialog.start,
        getter=get_dance_data,
    ),
    # LOAD
    Window(
        Const("Choose lesson date"),
        Calendar(id="calendar", on_click=on_date_selected),
        SwitchTo(
            Const("Back ↩"),
            id="switch_to_section",
            state=DanceDialog.start,
        ),
        state=DanceDialog.select_lesson_date,
    ),
    Window(
        Format("You can now submit videos, they will all be saved with a lesson date of <b>{lesson_date}</b>."),
        Button(
            Const("Save ✔️"),
            id="finish_dialog",
            on_click=return_to_menu,
        ),
        Button(
            Const("Back ↩"),
            id="back_to_date",
            on_click=return_back,
        ),
        MessageInput(video_handler, content_types=[ContentType.VIDEO]),
        MessageInput(other_type_handler),
        state=DanceDialog.load_lesson,
        getter=get_load_lesson_data,
    ),
    # PRACTICE
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
            id="update_lesson_order",
            on_click=change_order,
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in BachataLessonType],
            item_id_getter=lambda x: x,
            id="update_lesson_type",
            on_click=change_type,
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in BachataLessonLevel],
            item_id_getter=lambda x: x,
            id="update_lesson_level",
            on_click=change_level,
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in BachataLessonStatus],
            item_id_getter=lambda x: x,
            id="update_lesson_status",
            on_click=change_status,
        ),
        SwitchTo(
            Const(f"Let's dance {r.choice(['🕺', '💃'])}"),
            id="back_to_section",
            on_click=save_lesson_filter,
            state=DanceDialog.watch_lesson,
        ),
        SwitchTo(
            Const("Back ↩"),
            id="switch_to_section",
            state=DanceDialog.start,
        ),
        state=DanceDialog.create_lesson_filter,
        getter=get_lesson_filter_data,
    ),
    Window(
        Multi(
            Format(
                "Id: <i>{lesson_id}</i>\n\n"
                + f"{html.quote('=== < ~ > ===')}\n\n"
                + "Date: <b>{lesson_date}</b>\n"
                + "Type: <b>{lesson_type}</b>\n"
                + "Level: <b>{lesson_level}</b>\n"
                + "Status: <b>{lesson_status}</b>\n"
                + "Description: <b>{lesson_description}</b>",
                when="show_lesson",
            ),
            Format(
                f"{html.quote('=== < ~ > ===')}\n\n" + "Lesson: <i>{current} <b>/</b> {count}</i>",
                when="order",
            ),
            Const(
                "I'm sorry, but I couldn't find any lessons on the given parameters :'(",
                when="say_sorry",
            ),
            sep="\n\n",
        ),
        DynamicMedia(
            "lesson_video",
            when="show_lesson",
        ),
        SwitchTo(
            Const("Edit lesson ✏️"),
            id="edit_lesson",
            state=DanceDialog.edit_lesson,
            on_click=update_info,
            when="is_moder",
        ),
        Select(
            Format("{item}"),
            items=["← Previos", "Next →"],
            item_id_getter=lambda x: x,
            id="count_stamp",
            on_click=increment_counter,
            when="order",
        ),
        Button(
            Const("🎲"),
            id="w_random",
            when="random",
        ),
        SwitchTo(
            Const("Back ↩"),
            id="switch_to_filter",
            state=DanceDialog.create_lesson_filter,
        ),
        state=DanceDialog.watch_lesson,
        getter=get_lesson_data,
    ),
    Window(
        Format(
            "Id: <i>{lesson_id}</i>\n\n"
            + f"{html.quote('=== < ~ > ===')}\n\n"
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
            id="edit_lesson_type",
            on_click=edit_lesson,
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in BachataLessonLevel if e != BachataLessonLevel.ALL],
            item_id_getter=lambda x: x,
            id="edit_lesson_level",
            on_click=edit_lesson,
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in BachataLessonStatus],
            item_id_getter=lambda x: x,
            id="edit_lesson_status",
            on_click=edit_lesson,
        ),
        SwitchTo(
            Const("Save ✔️"),
            id="save_and_switch_to_users",
            state=DanceDialog.watch_lesson,
            on_click=save_suggestion,
        ),
        SwitchTo(
            Const("Revert ❌"),
            id="switch_to_users",
            state=DanceDialog.watch_lesson,
        ),
        MessageInput(enter_description, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),
        state=DanceDialog.edit_lesson,
        getter=get_edit_lesson_data,
    ),
)
