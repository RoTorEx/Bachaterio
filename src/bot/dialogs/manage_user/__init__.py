from aiogram import Router

from .dialogs import manage_user_dialog


def setup(router: Router):
    router.include_router(manage_user_dialog)
