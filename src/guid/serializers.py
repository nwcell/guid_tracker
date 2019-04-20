from datetime import datetime, timedelta, time, timezone
from typing import Optional, Type, Union
from pydantic import BaseModel, validator

from guid.util import default_expire, validate_guid


class GuidIn(BaseModel):
    expire: datetime = None
    name: str

    @validator('expire', pre=True, always=True)
    def set_expire(cls, v):
        if v is None:
            return datetime.now() + timedelta(days=30)
        return v


class GuidUpdate(BaseModel):
    expire: datetime = None
    name: str = None


class GuidOut(BaseModel):
    id: str
    expire: datetime
    name: str

    @validator('expire')
    def check_expire(cls, v: Union[datetime, str]) -> str:
        if type(v) == str:
            v = datetime.fromisoformat(v)
        return str(int(v.replace(tzinfo=timezone.utc).timestamp()))
