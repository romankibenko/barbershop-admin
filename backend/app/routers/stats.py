from fastapi import APIRouter, Depends

from app.auth import get_current_admin
from app.db.pool import get_pool
from app.schemas import StatsKpi, StatsOut

router = APIRouter(prefix="/stats", tags=["stats"], dependencies=[Depends(get_current_admin)])


@router.get("", response_model=StatsOut)
async def get_stats():
    pool = get_pool()

    kpi_row = await pool.fetchrow(
        """
        SELECT
          (SELECT count(*) FROM appointments
             WHERE start_at::date = current_date) AS appointments_today,
          (SELECT COALESCE(SUM(price), 0) FROM appointments
             WHERE status = 'done'
               AND start_at >= date_trunc('month', current_date)) AS revenue_month,
          (SELECT count(*) FROM clients
             WHERE created_at >= date_trunc('month', current_date)) AS new_clients_month,
          (SELECT count(*) FROM clients) AS total_clients
        """
    )

    by_day = await pool.fetch(
        """
        SELECT d::date AS day, count(a.id) AS count
        FROM generate_series(current_date - interval '13 days', current_date, interval '1 day') d
        LEFT JOIN appointments a ON a.start_at::date = d::date
        GROUP BY d
        ORDER BY d
        """
    )

    by_service = await pool.fetch(
        """
        SELECT s.title AS service, COALESCE(SUM(a.price), 0) AS revenue
        FROM services s
        LEFT JOIN appointments a ON a.service_id = s.id AND a.status = 'done'
        GROUP BY s.id, s.title
        ORDER BY revenue DESC
        """
    )

    return StatsOut(
        kpi=StatsKpi(**dict(kpi_row)),
        by_day=[dict(r) for r in by_day],
        by_service=[dict(r) for r in by_service],
    )
