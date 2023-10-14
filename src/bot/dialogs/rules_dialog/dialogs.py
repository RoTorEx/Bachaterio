from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from src.bot.states import RulesDialog

from .handlers import return_to_menu


rules_dialog = Dialog(
    Window(
        Const(
            "1. The first rule of Bachata Club is: You do not talk about Bachata Club.\n"
            "2. The second rule of Bachata Club is: You DO NOT talk about Bachata Club.\n"
            "3. If someone says `Stop` or signals to end the dance, the dance is over.\n"
            "4. Only two dancers in a couple at a time.\n"
            "5. One dance at a time.\n"
            "6. No restrictive clothing, and show respect for your dance partner.\n"
            "7. Dances can go on as long as they have to, even if it lasts all night.\n"
            "8. If this is your first time at Bachata Club, you have to dance.\n"
        ),
        Button(
            Const("Back to menu ↩"),
            id="return_to_main_menu",
            on_click=return_to_menu,
        ),
        state=RulesDialog.start,
    ),
)
