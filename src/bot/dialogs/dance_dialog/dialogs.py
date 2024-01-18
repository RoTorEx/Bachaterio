from aiogram import html
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Calendar, Row, Select, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from src.bot.enums import (
    LessonLevel,
    LessonType,
    SelectLessonLevelFilter,
    SelectLessonOrderFilter,
    SelectLessonTypeFilter,
)
from src.bot.states import DanceDialog

from .getters import get_dance_data, get_edit_lesson_data, get_lesson_data, get_lesson_filter_data, get_load_lesson_data
from .handlers import (
    change_level,
    change_order,
    change_type,
    edit_lesson,
    enter_description,
    increment_counter,
    on_date_selected,
    other_type_handler,
    remove_lesson,
    return_back,
    return_to_menu,
    save_lesson_filter,
    save_suggestion,
    setup_config,
    tutorial_id_handler,
    update_info,
    video_handler,
)


dance_dialog = Dialog(
    Window(
        Const(r"Make your choise"),
        Row(
            SwitchTo(
                Const("Add lessons 🎬"),
                id="continue_load",
                state=DanceDialog.select_lesson_date,
                when="is_moder",
            ),
            SwitchTo(
                Const("Watch lessons 🚀"),
                id="continue_practice",
                state=DanceDialog.create_lesson_filter,
                on_click=setup_config,
            ),
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
            "Here is default searching config:\n"
            + "🔗 Sort order: <b>{lesson_order}</b>\n"
            + "📷 Lesson type: <b>{lesson_type}</b>\n"
            + "📈 Lesson level: <b>{lesson_level}</b>\n\n"
            + "<i>💡 Tip: Use buttons below to adjust the current config and start dancing to continue</i>."
        ),
        SwitchTo(
            Const("Find by id 🔎"),
            id="switch_to_specific_lesson",
            state=DanceDialog.watch_specific_lesson,
        ),
        Row(
            SwitchTo(
                Const("Order 🔗"),
                id="switch_to_filter_order",
                state=DanceDialog.filter_order,
            ),
            SwitchTo(
                Const("Type 📷"),
                id="switch_to_filter_type",
                state=DanceDialog.filter_type,
            ),
            SwitchTo(
                Const("Level 📈"),
                id="switch_to_filter_level",
                state=DanceDialog.filter_level,
            ),
        ),
        SwitchTo(
            Const("Let's dance 🕺🪩💃"),
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
        Const("Please send specific lesson id 🔎"),
        SwitchTo(
            Const("Back ↩"),
            id="switch_to_filter",
            state=DanceDialog.create_lesson_filter,
        ),
        MessageInput(tutorial_id_handler, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),
        state=DanceDialog.watch_specific_lesson,
    ),
    # # Filter lesson selection
    Window(
        Const("Chose lesson order 🔗"),
        Select(
            Format("{item}"),
            items=[SelectLessonOrderFilter.NEWEST.value, SelectLessonOrderFilter.OLDEST.value],
            item_id_getter=lambda x: x,
            id="config_lesson_order",
            on_click=change_order,
        ),
        Select(
            Format("{item}"),
            items=[SelectLessonOrderFilter.RANDOM.value],
            item_id_getter=lambda x: x,
            id="config_lesson_order",
            on_click=change_order,
        ),
        Select(
            Format("{item}"),
            items=[SelectLessonOrderFilter.LAST_LOADED.value, SelectLessonOrderFilter.FIRST_LOADED.value],
            item_id_getter=lambda x: x,
            id="config_lesson_order",
            on_click=change_order,
        ),
        state=DanceDialog.filter_order,
    ),
    Window(
        Const("Chose lesson type 📷"),
        Select(
            Format("{item}"),
            items=[SelectLessonTypeFilter.ALL.value],
            item_id_getter=lambda x: x,
            id="config_lesson_type",
            on_click=change_type,
        ),
        Select(
            Format("{item}"),
            items=[
                SelectLessonTypeFilter.ELEMENT.value,
                SelectLessonTypeFilter.COMBINATION.value,
                SelectLessonTypeFilter.DANCE.value,
            ],
            item_id_getter=lambda x: x,
            id="config_lesson_type",
            on_click=change_type,
        ),
        state=DanceDialog.filter_type,
    ),
    Window(
        Const("Chose lesson level 📈"),
        Select(
            Format("{item}"),
            items=[SelectLessonLevelFilter.ALL.value],
            item_id_getter=lambda x: x,
            id="config_lesson_level",
            on_click=change_level,
        ),
        Select(
            Format("{item}"),
            items=[
                SelectLessonLevelFilter.NOVICE.value,
                SelectLessonLevelFilter.BEGINNER.value,
                SelectLessonLevelFilter.INTERMEDIATE.value,
            ],
            item_id_getter=lambda x: x,
            id="config_lesson_level",
            on_click=change_level,
        ),
        Select(
            Format("{item}"),
            items=[
                SelectLessonLevelFilter.ADVANCED.value,
                SelectLessonLevelFilter.EXPERT.value,
            ],
            item_id_getter=lambda x: x,
            id="config_lesson_level",
            on_click=change_level,
        ),
        state=DanceDialog.filter_level,
    ),
    # # Show lessons
    Window(
        Multi(
            Format(
                "🔎 Id: <i>{lesson_id}</i>\n"
                + "🗓 Date: <b>{lesson_date}</b>\n"
                + "📷 Type: <b>{lesson_type}</b>\n"
                + "📈 Level: <b>{lesson_level}</b>\n"
                + "📝 Description: <b>{lesson_description}</b>\n\n"
                + f"{html.quote('=== < ~ > ===')}\n\n",
                when="show_lesson",
            ),
            Format(
                "⛓ Series: <i>{current} / {count}</i>",
                when="order",
            ),
            Const(
                "I'm sorry, but I couldn't find any lessons on the given parameters :'(",
                when="say_sorry",
            ),
            sep="\n",
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
            "<u>Current lesson info</u>:\n"
            + "🔎 Id: <i>{lesson_id}</i>\n\n"
            + "🗓 Date: <i>{lesson_date}</i>\n"
            + "📷 Type: <i>{lesson_type}</i>\n"
            + "📈 Level: <i>{lesson_level}</i>\n"
            + "📝 Description: <i>{lesson_description}</i>\n\n"
            + f"{html.quote('=== < ~ > ===')}\n\n"
            + "<u>Suggested changes</u>:\n"
            + "📷 Type: <b>{edit_lesson_type}</b>\n"
            + "📈 Level: <b>{edit_lesson_level}</b>\n"
            + "📝 Description: <b>{edit_lesson_description}</b>\n\n"
            + "💡 <i>Edit tip: to update `description` write message in the chat</i>."
        ),
        DynamicMedia("lesson_video"),
        SwitchTo(
            Const("Remove 🗑"), id="switch_to_remove_lesson", state=DanceDialog.edit_remove_lesson, when="is_admin"
        ),
        Row(
            SwitchTo(
                Const("Type 📷"),
                id="switch_to_filter_type",
                state=DanceDialog.edit_lesson_type,
            ),
            SwitchTo(
                Const("Level 📈"),
                id="switch_to_filter_level",
                state=DanceDialog.edit_lesson_level,
            ),
        ),
        SwitchTo(
            Const("Save ✔️"),
            id="save_and_switch_to_lessons",
            state=DanceDialog.watch_lesson,
            on_click=save_suggestion,
        ),
        SwitchTo(
            Const("Reset and back 🔄"),
            id="switch_to_lessons",
            state=DanceDialog.watch_lesson,
        ),
        MessageInput(enter_description, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),
        state=DanceDialog.edit_lesson,
        getter=get_edit_lesson_data,
    ),
    Window(
        Const("Lesson type to update 📷"),
        Select(
            Format("{item}"),
            items=[
                LessonType.ELEMENT.value,
                LessonType.COMBINATION.value,
                LessonType.DANCE.value,
            ],
            item_id_getter=lambda x: x,
            id="edit_lesson_type",
            on_click=edit_lesson,
        ),
        state=DanceDialog.edit_lesson_type,
    ),
    Window(
        Const("Lesson level to update 📈"),
        Select(
            Format("{item}"),
            items=[
                LessonLevel.NOVICE.value,
                LessonLevel.BEGINNER.value,
                LessonLevel.INTERMEDIATE.value,
            ],
            item_id_getter=lambda x: x,
            id="edit_lesson_level",
            on_click=edit_lesson,
        ),
        Select(
            Format("{item}"),
            items=[
                LessonLevel.ADVANCED.value,
                LessonLevel.EXPERT.value,
            ],
            item_id_getter=lambda x: x,
            id="edit_lesson_level",
            on_click=edit_lesson,
        ),
        state=DanceDialog.edit_lesson_level,
    ),
    Window(
        Format(
            "🔎 Id: <i>{lesson_id}</i>\n\n"
            + f"{html.quote('=== < ~ > ===')}\n\n"
            + "🗓 Date: <b>{lesson_date}</b>\n"
            + "📷 Type: <b>{lesson_type}</b>\n"
            + "📈 Level: <b>{lesson_level}</b>\n"
            # + "💡 Status: <b>{lesson_status}</b>\n"
            + "📝 Description: <b>{lesson_description}</b>" + "Are you sure you want to remove this lesson?",
            when="show_lesson",
        ),
        SwitchTo(
            Const("Yes, remove 🧹"),
            id="remove_and_switch_to_lessons",
            state=DanceDialog.watch_lesson,
            on_click=remove_lesson,
        ),
        SwitchTo(
            Const("Reset and back 🔄"),
            id="switch_to_edit_lessons",
            state=DanceDialog.edit_lesson,
        ),
        DynamicMedia(
            "lesson_video",
            when="show_lesson",
        ),
        state=DanceDialog.edit_remove_lesson,
        getter=get_lesson_data,
    ),
)
