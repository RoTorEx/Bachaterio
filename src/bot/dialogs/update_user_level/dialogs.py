from aiogram import html
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.text import Const, Format

from src.bot.enums import UserLevel
from src.bot.states import SetLevelSubManageUserDialog

from .getters import get_data_update_user_level
from .handlers import revert_level, save_level, set_level


update_user_level_sub_dialog = Dialog(
    Window(
        Format(
            "Id: <b>{user_id}</b>\n"
            + "Name: <b>{first_name} {last_name}</b>\n"
            + "Username: <b>@{username}</b>\n"
            + "Level: <b>{level}</b>\n"
            + "Created: <b>{created_at}</b>\n\n"
            + f"{html.quote('=== < ~ > ===')}\n\n"
            + "Update level on <b>{edit_level}</b>. Are you sure?\n",
        ),
        Select(
            Format("{item}"),
            items=[e.value for e in UserLevel],
            item_id_getter=lambda x: x,
            id="e_lesson_type",
            on_click=set_level,
        ),
        Button(
            Const("Save"),
            id="w_save_updated_level",
            on_click=save_level,
        ),
        Button(
            Const("Revert"),
            id="w_revert_updated_level",
            on_click=revert_level,
        ),
        state=SetLevelSubManageUserDialog.set_level,
        getter=get_data_update_user_level,
    ),
)
