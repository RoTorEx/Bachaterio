from aiogram import Router

from .dialogs import rules_dialog


def setup(router: Router):
    router.include_router(rules_dialog)
