from aiogram import html
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format, Multi

from src.bot.enums import UserLevel
from src.bot.states import SuperintendDialog

from .getters import get_data_manage_user, get_data_update_user_level
from .handlers import (
    increment_counter,
    manage_suggestions,
    manage_users,
    other_type_handler,
    return_to_menu,
    save_level,
    set_level,
    text_message_handler,
    try_update_level,
)


superintend_dialog = Dialog(
    Window(
        Const("<b>GOD mode activated!</b>"),
        Row(
            SwitchTo(
                Const("Users 👤"), id="c_manage_users", on_click=manage_users, state=SuperintendDialog.manage_users
            ),
            SwitchTo(
                Const("Suggestions 📝"),
                id="c_manage_suggestions",
                on_click=manage_suggestions,
                state=SuperintendDialog.start,
            ),
        ),
        Button(
            Const("Back to menu ↩"),
            id="return_to_main_menu",
            on_click=return_to_menu,
        ),
        state=SuperintendDialog.start,
    ),
    Window(
        Multi(
            Format(
                "Id: <b>{user_id}</b>\n"
                + "Name: <b>{first_name} {last_name}</b>\n"
                + "Username: <b>{username}</b>\n"
                + "Level: <b>{level}</b>\n"
                + "Created: <b>{created_at}</b>\n\n"
                + f"{html.quote('=== < ~ > ===')}\n\n"
                + "User: <i>{current} <b>/</b> {count}</i>",
                when="show_user",
            ),
            Format("No one user was found", when="say_sorry"),
        ),
        SwitchTo(
            Const("Update level ✏️"),
            id="update_level",
            state=SuperintendDialog.update_user_level,
            when="is_another",
        ),
        Button(
            Const("Okay, try ✏️"),
            id="get_interdiction",
            on_click=try_update_level,
            when="is_myself",
        ),
        Select(
            Format("{item}"),
            items=["← Previos", "Next →"],
            item_id_getter=lambda x: x,
            id="c_count_stamp",
            on_click=increment_counter,
            when="show_user",
        ),
        SwitchTo(
            Const("Message ✉️"),
            id="continue_send_message",
            # on_click=send_message,
            state=SuperintendDialog.send_message,
            when="show_user",
        ),
        SwitchTo(
            Const("Back ↩"),
            id="switch_to_target",
            state=SuperintendDialog.start,
        ),
        state=SuperintendDialog.manage_users,
        getter=get_data_manage_user,
    ),
    Window(
        Const("Write message and I'll send it!"),
        SwitchTo(
            Const("Back ↩"),
            id="switch_to_users",
            state=SuperintendDialog.manage_users,
        ),
        MessageInput(text_message_handler, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),
        state=SuperintendDialog.send_message,
    ),
    Window(
        Format(
            "Id: <b>{user_id}</b>\n"
            + "Name: <b>{first_name} {last_name}</b>\n"
            + "Username: <b>@{username}</b>\n"
            + "Level: <b>{level}</b>\n"
            + "Created: <b>{created_at}</b>\n\n"
            + f"{html.quote('=== < ~ > ===')}\n\n"
            + "Update level on <b>{edit_level}</b>. Are you sure?\n"
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in UserLevel],
            item_id_getter=lambda x: x,
            id="update_level",
            on_click=set_level,
        ),
        SwitchTo(
            Const("Save ✔️"),
            id="save_and_switch_to_users",
            state=SuperintendDialog.manage_users,
            on_click=save_level,
        ),
        SwitchTo(
            Const("Revert ❌"),
            id="switch_to_users",
            state=SuperintendDialog.manage_users,
        ),
        state=SuperintendDialog.update_user_level,
        getter=get_data_update_user_level,
    ),
)
