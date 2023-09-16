from aiogram import Router

from .dialogs import update_user_level_sub_dialog


def setup(router: Router):
    router.include_router(update_user_level_sub_dialog)
