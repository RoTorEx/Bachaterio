from enum import Enum


class UserLevel(str, Enum):
    STRANGER = "stranger"
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPERUSER = "superuser"
