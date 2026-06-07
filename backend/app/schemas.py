from datetime import date, datetime
from typing import Generic, Literal, TypeVar

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


# ── Справочники ──────────────────────────────────────────

class BarberOut(BaseModel):
    id: int
    slug: str
    name: str
    role: str
    active: bool


class ServiceOut(BaseModel):
    id: int
    slug: str
    title: str
    price: int
    duration_min: int


# ── Appointments ─────────────────────────────────────────

AppointmentStatus = Literal["pending", "confirmed", "done", "cancelled"]


class AppointmentCreate(BaseModel):
    client_id: int
    barber_id: int
    service_id: int
    start_at: datetime


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus


class AppointmentOut(BaseModel):
    id: int
    start_at: datetime
    status: AppointmentStatus
    price: int
    client_id: int
    client_name: str
    barber_id: int
    barber_name: str
    service_id: int
    service_title: str


# ── Stats ────────────────────────────────────────────────

class StatsKpi(BaseModel):
    appointments_today: int
    revenue_month: int
    new_clients_month: int
    total_clients: int


class DayCount(BaseModel):
    day: date
    count: int


class ServiceRevenue(BaseModel):
    service: str
    revenue: int


class StatsOut(BaseModel):
    kpi: StatsKpi
    by_day: list[DayCount]
    by_service: list[ServiceRevenue]
