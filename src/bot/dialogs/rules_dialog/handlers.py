from typing import Any

from aiogram_dialog import ChatEvent, DialogManager


# ====
# INFO
async def return_to_menu(callback: ChatEvent, select: Any, manager: DialogManager) -> None:
    await manager.done()
