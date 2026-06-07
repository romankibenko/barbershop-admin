from fastapi import APIRouter, Depends

from app.auth import get_current_admin
from app.db.pool import get_pool
from app.schemas import BarberOut, ServiceOut

router = APIRouter(tags=["refs"], dependencies=[Depends(get_current_admin)])


@router.get("/barbers", response_model=list[BarberOut])
async def list_barbers():
    pool = get_pool()
    rows = await pool.fetch("SELECT id, slug, name, role, active FROM barbers ORDER BY id")
    return [dict(r) for r in rows]


@router.get("/services", response_model=list[ServiceOut])
async def list_services():
    pool = get_pool()
    rows = await pool.fetch(
        "SELECT id, slug, title, price, duration_min FROM services ORDER BY id"
    )
    return [dict(r) for r in rows]
