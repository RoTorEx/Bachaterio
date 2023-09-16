from aiogram import Router

from src.bot.dialogs import choose_date, edit_lesson, manage_user, update_user_level, watch_config, watch_lesson


def load_dialogs() -> Router:
    router = Router(name=__name__)

    # Dance
    choose_date.setup(router)
    watch_config.setup(router)
    watch_lesson.setup(router)
    edit_lesson.setup(router)

    # Manage
    manage_user.setup(router)
    update_user_level.setup(router)

    return router
