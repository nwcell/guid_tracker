"""Pydantic serializers for managing (de)serializationand doc generation."""
from datetime import datetime, timedelta, time, timezone
from typing import Optional, Type, Union
from pydantic import BaseModel, validator


class GuidIn(BaseModel):
    """
    Serializer for creating a record.

    Formats data, so that it'll play nicely  w/ the DB.

    Also, sets defaults for `expire`.
    """

    expire: datetime = None
    name: str

    @validator('expire', pre=True, always=True)
    def set_expire(cls, v):
        """Set expire time as 30 days from now, if not specified."""
        if v is None:
            return datetime.now(timezone.utc) + timedelta(days=30)
        return v

    @validator('expire', always=True)
    def set_tz(cls, v):
        """After initial validation logic, add utc as the timezone."""
        return v.replace(tzinfo=timezone.utc)


class GuidUpdate(BaseModel):
    """
    Serializer for updating a record.

    Formats data, so that it'll play nicely  w/ the DB.
    """

    expire: datetime = None
    name: str = None


class GuidOut(BaseModel):
    """Serialize output, that'll be sent to the end user properly."""
    id: str
    expire: datetime
    name: str

    @validator('expire')
    def check_expire(cls, v: Union[datetime, str]) -> str:
        """Coerce expire into being Unix Time."""
        if type(v) == str:
            v = datetime.fromisoformat(v)
        return str(int(v.replace(tzinfo=timezone.utc).timestamp()))
