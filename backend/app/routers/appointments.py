from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import get_current_admin
from app.db.pool import get_pool
from app.schemas import (
    AppointmentCreate,
    AppointmentOut,
    AppointmentStatus,
    AppointmentStatusUpdate,
    Page,
)

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
    dependencies=[Depends(get_current_admin)],
)

# SELECT с join'ами справочников — общий для list/create/patch.
_SELECT = """
    SELECT a.id, a.start_at, a.status, a.price,
           a.client_id, c.name  AS client_name,
           a.barber_id, b.name  AS barber_name,
           a.service_id, s.title AS service_title
    FROM appointments a
    JOIN clients  c ON c.id = a.client_id
    JOIN barbers  b ON b.id = a.barber_id
    JOIN services s ON s.id = a.service_id
"""


@router.get("", response_model=Page[AppointmentOut])
async def list_appointments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    barber_id: int | None = Query(None),
    status_: AppointmentStatus | None = Query(None, alias="status"),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
):
    pool = get_pool()
    conds: list[str] = []
    params: list = []
    if barber_id is not None:
        params.append(barber_id)
        conds.append(f"a.barber_id = ${len(params)}")
    if status_ is not None:
        params.append(status_)
        conds.append(f"a.status = ${len(params)}")
    if date_from is not None:
        params.append(date_from)
        conds.append(f"a.start_at >= ${len(params)}")
    if date_to is not None:
        params.append(date_to)
        conds.append(f"a.start_at <= ${len(params)}")
    where = ("WHERE " + " AND ".join(conds)) if conds else ""

    total = await pool.fetchval(
        f"SELECT count(*) FROM appointments a {where}", *params
    )
    rows = await pool.fetch(
        f"{_SELECT} {where} ORDER BY a.start_at DESC LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}",
        *params,
        page_size,
        (page - 1) * page_size,
    )
    return Page(items=[dict(r) for r in rows], total=total)


@router.post("", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
async def create_appointment(data: AppointmentCreate):
    pool = get_pool()
    price = await pool.fetchval("SELECT price FROM services WHERE id = $1", data.service_id)
    if price is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Услуга не найдена")

    new_id = await pool.fetchval(
        """
        INSERT INTO appointments (client_id, barber_id, service_id, start_at, price)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING id
        """,
        data.client_id,
        data.barber_id,
        data.service_id,
        data.start_at,
        price,
    )
    row = await pool.fetchrow(f"{_SELECT} WHERE a.id = $1", new_id)
    return dict(row)


@router.patch("/{appointment_id}", response_model=AppointmentOut)
async def update_status(appointment_id: int, data: AppointmentStatusUpdate):
    pool = get_pool()
    updated = await pool.fetchval(
        "UPDATE appointments SET status = $2 WHERE id = $1 RETURNING id",
        appointment_id,
        data.status,
    )
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запись не найдена")
    row = await pool.fetchrow(f"{_SELECT} WHERE a.id = $1", appointment_id)
    return dict(row)
