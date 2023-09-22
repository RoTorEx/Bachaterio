from aiogram import Router

from src.bot.dialogs import dance_dialog, info_dialog, menu_dialog, rules_dialog, superintend_dialog


def load_dialogs() -> Router:
    router = Router(name=__name__)

    # Menu
    menu_dialog.setup(router)
    # Info
    info_dialog.setup(router)
    # Dance
    dance_dialog.setup(router)
    # Rules
    rules_dialog.setup(router)
    # Superinted
    superintend_dialog.setup(router)

    return router
