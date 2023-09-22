from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from src.bot.states import RulesDialog

from .handlers import return_to_menu


rules_dialog = Dialog(
    Window(
        Const("It's empty in here!"),
        Button(
            Const("Back to menu ↩"),
            id="return_to_main_menu",
            on_click=return_to_menu,
        ),
        state=RulesDialog.start,
    ),
)
