from aiogram import Router

from .dialogs import dance_dialog


def setup(router: Router):
    router.include_router(dance_dialog)
