from aiogram import Router

from .dialogs import edit_lesson_sub_dialog


def setup(router: Router):
    router.include_router(edit_lesson_sub_dialog)
