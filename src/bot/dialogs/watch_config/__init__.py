from aiogram import Router

from .dialogs import setup_watch_lessons_config_dialog


def setup(router: Router):
    router.include_router(setup_watch_lessons_config_dialog)
