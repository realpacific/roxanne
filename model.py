import dataclasses
from typing import Optional


@dataclasses.dataclass
class Stats:
    author: str
    count: int
    author_id: int
    role: str
    full_message: str


@dataclasses.dataclass
class Query:
    channel_link: str
    by_user: Optional[str] = None
    search: Optional[str] = None
    filter: Optional[str] = None
    limit: Optional[int] = None
