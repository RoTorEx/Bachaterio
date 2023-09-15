from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Calendar
from aiogram_dialog.widgets.text import Const

from src.bot.states import LoaderState

from .handlers import on_date_selected


choose_lesson_date = Dialog(
    Window(
        Const("Choose lesson date"),
        Calendar(id='calendar', on_click=on_date_selected),
        state=LoaderState.select_date,
    ),
)
