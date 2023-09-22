from aiogram import Router

from .dialogs import superintend_dialog


def setup(router: Router):
    router.include_router(superintend_dialog)
