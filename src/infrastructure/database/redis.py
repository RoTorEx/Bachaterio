from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage

from src.infrastructure.config_reader import Redis


def redis_connection(redis: Redis) -> RedisStorage:
    """Make connection to Redis."""
    storage = RedisStorage.from_url(
        url=f"redis://{redis.host}",
        connection_kwargs={
            "db": redis.db,
        },
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )

    return storage
