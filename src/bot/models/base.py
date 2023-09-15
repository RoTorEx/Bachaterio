from datetime import datetime

from pydantic import BaseModel, Extra


def iso_8601_datetime_with_z_suffix(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


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
        json_encoders = {datetime: iso_8601_datetime_with_z_suffix}
