from aiogram import Router

from .dialogs import info_dialog


def setup(router: Router):
    router.include_router(info_dialog)
