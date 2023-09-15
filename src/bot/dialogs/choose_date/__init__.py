from aiogram import Router

from .dialogs import choose_lesson_date


def setup(router: Router):
    router.include_router(choose_lesson_date)
