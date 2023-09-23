import random as r

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from src.bot.states import MenuDialog

from .getters import get_menu_data
from .handlers import start_dance_dialog, start_info_dialog, start_rules_dialog, start_superintend_dialog


menu_dialog = Dialog(
    Window(
        Const(r"Welcome to menu <b><i>%username%</i></b>"),
        Button(
            Const("Info ℹ️"),
            id="d_info",
            on_click=start_info_dialog,
        ),
        Row(
            Button(
                Const(f"Dance {r.choice(['🕺', '💃'])}"),
                id="dance_d",
                on_click=start_dance_dialog,
                when="is_member",
            ),
            Button(
                Const("Rules 📜"),
                id="moderation_rule_d",
                on_click=start_rules_dialog,
                when="is_moder",
            ),
        ),
        Button(
            Const("Superintend 🔱"),
            id="superintend_d",
            on_click=start_superintend_dialog,
            when="is_superuser",
        ),
        state=MenuDialog.init,
        getter=get_menu_data,
    ),
)
