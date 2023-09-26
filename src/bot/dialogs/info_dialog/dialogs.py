from aiogram import html
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from src.bot.states import InfoDialog

from .getters import get_info_data
from .handlers import return_to_menu


info_dialog = Dialog(
    Window(
        Format(
            "• Your ID: <b>{your_id}</b>\n"
            + "• Your level: <b>{your_level}</b>\n"
            + "• Your opportunities: <b>{your_opportunities}</b>\n\n"
            + f"{html.quote('=== < ~ > ===')}\n\n"
            + "• My name: <i>{my_name}</i>\n"
            + "• My version: <i>{my_version}</i>\n"
            + "• My description: <i>{my_description}</i>\n"
            + "• My instructors: <i>@RadekBachata</i> & <i>@KingaBachata</i>"
        ),
        Button(
            Const("Back to menu ↩"),
            id="return_to_main_menu",
            on_click=return_to_menu,
        ),
        state=InfoDialog.start,
        getter=get_info_data,
    ),
)
