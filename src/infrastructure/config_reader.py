from pydantic_settings import BaseSettings, SettingsConfigDict


class TgBot(BaseSettings):
    """Telegram bot envs."""

    token: str
    log_chat: int
    port: int
    use_redis: bool


class Redis(BaseSettings):
    """Redis envs."""

    db: int
    host: str
    port: int


class Mongo(BaseSettings):
    """MongoDB envs."""

    username: str
    password: str
    host: str
    port: int
    name: str


class Settings(BaseSettings):
    """To attributes sets name which correspond to prefix name (NAME__) from .env file
    and ignore prefix before add environmental variable to this config."""

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    tg_bot: TgBot
    redis: Redis
    mongo: Mongo


settings = Settings(_env_file=".env")
