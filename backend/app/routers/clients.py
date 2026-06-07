from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.auth import get_current_admin
from app.db.pool import get_pool
from app.schemas import ClientCreate, ClientOut, ClientUpdate, Page

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    dependencies=[Depends(get_current_admin)],
)


@router.get("", response_model=Page[ClientOut])
async def list_clients(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
):
    pool = get_pool()
    where = ""
    params: list = []
    if search:
        params.append(f"%{search}%")
        where = "WHERE name ILIKE $1 OR phone ILIKE $1"

    total = await pool.fetchval(f"SELECT count(*) FROM clients {where}", *params)

    limit_pos = len(params) + 1
    offset_pos = len(params) + 2
    rows = await pool.fetch(
        f"""
        SELECT id, name, phone, notes, created_at
        FROM clients {where}
        ORDER BY created_at DESC
        LIMIT ${limit_pos} OFFSET ${offset_pos}
        """,
        *params,
        page_size,
        (page - 1) * page_size,
    )
    return Page(items=[dict(r) for r in rows], total=total)


@router.post("", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
async def create_client(data: ClientCreate):
    pool = get_pool()
    row = await pool.fetchrow(
        """
        INSERT INTO clients (name, phone, notes)
        VALUES ($1, $2, $3)
        RETURNING id, name, phone, notes, created_at
        """,
        data.name,
        data.phone,
        data.notes,
    )
    return dict(row)


@router.patch("/{client_id}", response_model=ClientOut)
async def update_client(client_id: int, data: ClientUpdate):
    pool = get_pool()
    row = await pool.fetchrow(
        """
        UPDATE clients SET name = $2, phone = $3, notes = $4
        WHERE id = $1
        RETURNING id, name, phone, notes, created_at
        """,
        client_id,
        data.name,
        data.phone,
        data.notes,
    )
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найден")
    return dict(row)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: int):
    pool = get_pool()
    result = await pool.execute("DELETE FROM clients WHERE id = $1", client_id)
    if result == "DELETE 0":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Клиент не найден")
