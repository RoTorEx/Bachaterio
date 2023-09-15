from enum import Enum


class CallbackOrder(str, Enum):
    RANDOM = "🎲"
    NEWEST = "newest"
    OLDEST = "oldest"


class SelectOrder(str, Enum):
    RANDOM = "🎲"
    NEWEST = "newest"
    OLDEST = "oldest"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
