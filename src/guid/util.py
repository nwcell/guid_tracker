from datetime import datetime, timedelta
from starlette.exceptions import HTTPException


def default_expire():
    return datetime.now() + timedelta(days=30)


def validate_guid(string: str) -> bool:
    valid_chars = set('0123456789abcdef')
    count = 0
    for char in string:
        count += 1
        if char not in valid_chars or count > 32:
            raise ValueError('Invalid GUID format.')
    if count != 32:
        raise ValueError('Invalid GUID format.')
    return string

