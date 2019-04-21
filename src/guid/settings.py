"""Gathers environment settings and loads them into global attributes."""
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret


config = Config('.env')

# Main Configs
DEBUG = config('DEBUG', cast=bool, default=False)
TESTING = config('TESTING', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', cast=Secret)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)

# Redis
REDIS_ENDPOINT = config('REDIS_ENDPOINT', default='127.0.0.1')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)
REDIS_DB = config('REDIS_DB', default=0, cast=int)
REDIS_PASSWORD = config('REDIS_PASSWORD', default=None, cast=Secret)

# DB
DATABASE_URL = config('DATABASE_URL')

# Testing
TEST_DATABASE_URL = config('TEST_DATABASE_URL')
