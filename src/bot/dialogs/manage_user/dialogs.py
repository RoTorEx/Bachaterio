from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.text import Const, Format, Multi

from src.bot.states import ManageUserDialog

from .getters import get_data_manage_user
from .handlers import increment_counter, update_level


manage_user_dialog = Dialog(
    Window(
        Multi(
            Format(
                "Id: <b>{user_id}</b>\n"
                + "Name: <b>{first_name} {last_name}</b>\n"
                + "Username: <b>@{username}</b>\n"
                + "Level: <b>{level}</b>\n"
                + "Created: <b>{created_at}</b>\n",
                when="show_user",
            ),
            Format("No one user was found", when="say_sorry"),
        ),
        Button(
            Const("Update level ✏️"),
            id="w_update_level",
            on_click=update_level,
            when="show_user",
        ),
        Select(
            Format("{item}"),
            items=["← Previos", "Next →"],
            item_id_getter=lambda x: x,
            id="w_count_stamp",
            on_click=increment_counter,
            when="show_user",
        ),
        state=ManageUserDialog.manage_users,
        getter=get_data_manage_user,
    ),
)
