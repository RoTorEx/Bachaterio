from datetime import datetime

from aiogram.types import ContentType
from aiogram.types.user import User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from bson import ObjectId

from src.bot.enums import SuggestionStatus
from src.bot.models import BachataTutorialModel, SuggestEditTutorialModel
from src.infrastructure.database import cursor


async def get_data_edit_dialog(dialog_manager: DialogManager, **kwargs):
    unique_file_id = dialog_manager.start_data["lesson_id"]
    suggestion_id = dialog_manager.start_data["suggestion_id"]

    document: dict = cursor.tutorials.find_one({"tg_unique_file_id": unique_file_id})

    tutorial = BachataTutorialModel.model_validate(document)
    lesson_video = MediaAttachment(ContentType.VIDEO, file_id=MediaId(tutorial.tg_file_id))

    edit_document = cursor.modify_tutorials.find_one({"suggestion_id": suggestion_id})

    if not edit_document:

        event_user: User = dialog_manager.middleware_data["event_from_user"]
        suggest_obj_id = ObjectId()

        suggest_obj = SuggestEditTutorialModel(
            obj_id=suggest_obj_id,
            suggestion_id=suggestion_id,
            tg_unique_file_id=tutorial.tg_unique_file_id,
            edit_lesson_description=tutorial.lesson_description,
            edit_lesson_date=tutorial.lesson_date,
            edit_lesson_type=tutorial.lesson_type,
            edit_lesson_level=tutorial.lesson_level,
            edit_lesson_status=tutorial.lesson_status,
            suggestion_status=SuggestionStatus.PENDING,
            suggested_by=event_user.id,  # ToDo: fixit
            is_active=False,
            created_at=datetime.utcnow(),
        )

        edit_document = cursor.modify_tutorials.find_one_and_update(
            {"suggestion_id": str(suggestion_id)}, {"$set": suggest_obj.model_dump()}, upsert=True, return_document=True
        )

    edit_tutorial = SuggestEditTutorialModel.model_validate(edit_document)

    edit_lesson_dialog_response = {
        # Static
        "lesson_video": lesson_video,
        "lesson_id": tutorial.tg_unique_file_id,
        "lesson_date": tutorial.lesson_date.strftime("%d/%m/%Y"),
        "lesson_type": tutorial.lesson_type.value if tutorial.lesson_type else "null",
        "lesson_level": tutorial.lesson_level.value if tutorial.lesson_level else "null",
        "lesson_status": tutorial.lesson_status.value,
        "lesson_description": tutorial.lesson_description,
        # Dinamic
        "edit_lesson_date": edit_tutorial.edit_lesson_date.strftime("%d/%m/%Y"),
        "edit_lesson_type": edit_tutorial.edit_lesson_type.value if edit_tutorial.edit_lesson_type else "null",
        "edit_lesson_level": edit_tutorial.edit_lesson_level.value if edit_tutorial.edit_lesson_level else "null",
        "edit_lesson_status": edit_tutorial.edit_lesson_status.value,
        "edit_lesson_description": edit_tutorial.edit_lesson_description,
    }

    return edit_lesson_dialog_response
