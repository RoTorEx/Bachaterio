import json
from datetime import datetime, time
from typing import Any

from bson import ObjectId
from pydantic import BaseModel, Extra


def iso_8601_datetime_with_z_suffix(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def custom_serializer(obj: Any):
    def _default(val):
        if isinstance(val, BaseModel):
            return val.model_dump()

        elif isinstance(val, time):
            return val.isoformat()

        raise TypeError()

    res = json.dumps(obj, default=_default)
    return res


class _BaseAdminModel:
    def init_subclass(cls, **kwargs):
        for name, model_field in cls.fields.items():  # type: ignore
            if name == "root":
                continue

            if model_field.field_info.extra.get("example") is None:
                raise RuntimeError(f"Setup example to {cls.name}.{name}!")

            if model_field.field_info.alias is None:
                raise RuntimeError(f"Setup alias to {cls.name}.{name}!")

        super().init_subclass(**kwargs)


class BaseAdminModel(BaseModel, _BaseAdminModel):
    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 0
        extra = Extra.ignore
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {datetime: iso_8601_datetime_with_z_suffix, ObjectId: str}


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')

        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
