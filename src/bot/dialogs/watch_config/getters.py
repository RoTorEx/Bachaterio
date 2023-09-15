from aiogram_dialog import DialogManager

from src.bot.states import PracticeState


async def get_setup_watch_data(dialog_manager: DialogManager, **kwargs) -> dict:
    response = {
        "lesson_order": dialog_manager.start_data["lesson_order"],
        "lesson_type": dialog_manager.start_data["lesson_type"],
        "lesson_level": dialog_manager.start_data["lesson_level"],
        "lesson_status": dialog_manager.start_data["lesson_status"],
    }

    state = dialog_manager.middleware_data["state"]

    await state.set_data({"setup_watch_response": response})
    await state.set_state(PracticeState.setup_filters)

    return response
