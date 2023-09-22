from aiogram import Router

from .dialogs import menu_dialog


def setup(router: Router):
    router.include_router(menu_dialog)
