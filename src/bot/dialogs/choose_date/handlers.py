from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from src.bot.keyboards import finished_lesson_loading
from src.bot.states import LoaderState


async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    await callback.answer(text=f"{selected_date}")

    await callback.message.answer(
        text=f"You can now submit videos, they will all be saved with a lesson date of <b>{selected_date}</b>."
        + "\nPress `Done ✔️` when you're finished or `Edit ✏️` to correct the date.",
        reply_markup=finished_lesson_loading(),
        disable_notification=True,
    )

    state = manager.middleware_data["state"]

    await state.set_data({"lesson_date": selected_date})
    await state.set_state(LoaderState.start_load)

    await manager.done()
    await callback.answer(str(selected_date))
