from aiogram import Router

from .dialogs import watch_lessons_dialog


def setup(router: Router):
    router.include_router(watch_lessons_dialog)
