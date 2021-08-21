from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class MessageMeta(BaseModel):
    author_id: Optional[int]
    full_message: Optional[str]
    time: datetime


class Query(BaseModel):
    channel_link: str
    by_user: Optional[str] = None
    search: Optional[str] = None
    filter: Optional[str] = None
    limit: Optional[int] = None
