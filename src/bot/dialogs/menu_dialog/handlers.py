from typing import Any

from aiogram_dialog import ChatEvent, DialogManager

from src.bot.states import DanceDialog, InfoDialog, RulesDialog, SuperintendDialog


async def start_info_dialog(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await manager.start(state=InfoDialog.start)


async def start_dance_dialog(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await manager.start(state=DanceDialog.start)


async def start_rules_dialog(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await manager.start(state=RulesDialog.start)


async def start_superintend_dialog(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await manager.start(state=SuperintendDialog.start)
