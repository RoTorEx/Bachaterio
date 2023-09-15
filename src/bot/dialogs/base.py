from aiogram import Router

from src.bot.dialogs import choose_date, edit_lesson, watch_config, watch_lesson


def load_dialogs() -> Router:
    router = Router(name=__name__)

    choose_date.setup(router)

    watch_config.setup(router)
    watch_lesson.setup(router)
    edit_lesson.setup(router)

    return router
