from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int


# ── Clients ──────────────────────────────────────────────

class ClientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=5, max_length=32)
    notes: str | None = Field(default=None, max_length=1000)


class ClientUpdate(ClientCreate):
    pass


class ClientOut(BaseModel):
    id: int
    name: str
    phone: str
    notes: str | None
    created_at: datetime
