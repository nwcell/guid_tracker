"""Basic utility module."""
from datetime import datetime, timedelta
from starlette.exceptions import HTTPException


def validate_guid(guid: str) -> bool:
    """Validates that a guid is formatted properly"""
    valid_chars = set('0123456789abcdef')
    count = 0
    for char in guid:
        count += 1
        if char not in valid_chars or count > 32:
            raise ValueError('Invalid GUID format.')
    if count != 32:
        raise ValueError('Invalid GUID format.')
    return guid

