"""Creates a cache instance w/ redis as a backend.

Use `cache` to interact with the cache.

Objects are pickled before getting sent into redis.
"""
from aiocache import caches
from guid import settings


redis_config = {
    'default': {
        'cache': "aiocache.RedisCache",
        'endpoint': settings.REDIS_ENDPOINT,
        'port': settings.REDIS_PORT,
        'db': settings.REDIS_DB,
        'serializer': {
            'class': "aiocache.serializers.PickleSerializer"
        }
    },
}

if settings.REDIS_PASSWORD:
    redis_config['default']['password'] = str(settings.REDIS_PASSWORD)

caches.set_config(redis_config)

cache = caches.get('default')
