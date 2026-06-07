"""Наполняет базу демо-данными барбершопа.

Запуск из каталога backend:
    .venv\\Scripts\\python.exe -m scripts.seed

Идемпотентно: barbers/services — upsert по slug, clients/appointments — пересоздаются.
"""
import asyncio
import random
from datetime import datetime, timedelta, timezone

import asyncpg

from app.config import settings

random.seed(42)  # воспроизводимый набор данных

# Барберы и услуги синхронизированы с barbershop-landing/bot/data.ts
BARBERS = [
    ("volkov", "Андрей Волков", "старший барбер"),
    ("sazonov", "Михаил Сазонов", "мастер бороды"),
    ("kareev", "Денис Кареев", "fade-специалист"),
]

SERVICES = [
    ("haircut", "Мужская стрижка", 2200, 60),
    ("combo", "Стрижка + борода", 3500, 90),
    ("camo", "Камуфляж бороды", 2000, 40),
    ("shave", "Бритьё опасной бритвой", 1800, 50),
    ("kids", "Детская стрижка", 1500, 40),
    ("fatherson", "Отец и сын", 3300, 90),
]

FIRST_NAMES = [
    "Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Артём",
    "Илья", "Кирилл", "Михаил", "Никита", "Иван", "Роман", "Егор", "Павел",
    "Антон", "Владимир", "Денис", "Евгений", "Глеб",
]
LAST_NAMES = [
    "Иванов", "Смирнов", "Кузнецов", "Попов", "Соколов", "Лебедев", "Козлов",
    "Новиков", "Морозов", "Петров", "Волков", "Соловьёв", "Васильев", "Зайцев",
    "Павлов", "Семёнов", "Голубев", "Виноградов", "Богданов", "Воробьёв",
]

SLOT_HOURS = list(range(10, 22))  # 10:00–21:00


def random_phone() -> str:
    return f"+7 9{random.randint(0, 99):02d} {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"


async def main() -> None:
    conn = await asyncpg.connect(settings.database_url)
    try:
        # Справочники — upsert по slug
        for bid, (slug, name, role) in enumerate(BARBERS, start=1):
            await conn.execute(
                """
                INSERT INTO barbers (slug, name, role, active) VALUES ($1, $2, $3, TRUE)
                ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name, role = EXCLUDED.role
                """,
                slug, name, role,
            )
        for slug, title, price, dur in SERVICES:
            await conn.execute(
                """
                INSERT INTO services (slug, title, price, duration_min) VALUES ($1, $2, $3, $4)
                ON CONFLICT (slug) DO UPDATE
                  SET title = EXCLUDED.title, price = EXCLUDED.price, duration_min = EXCLUDED.duration_min
                """,
                slug, title, price, dur,
            )

        barber_ids = [r["id"] for r in await conn.fetch("SELECT id FROM barbers ORDER BY id")]
        services = await conn.fetch("SELECT id, price FROM services ORDER BY id")

        # Клиенты и записи — с чистого листа
        await conn.execute("TRUNCATE appointments, clients RESTART IDENTITY CASCADE")

        client_ids = []
        for _ in range(50):
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
            created = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 60))
            cid = await conn.fetchval(
                "INSERT INTO clients (name, phone, created_at) VALUES ($1, $2, $3) RETURNING id",
                name, random_phone(), created,
            )
            client_ids.append(cid)

        now = datetime.now(timezone.utc)
        for _ in range(200):
            svc = random.choice(services)
            # день в диапазоне [-18; +5] от сегодня
            day_offset = random.randint(-18, 5)
            day = (now + timedelta(days=day_offset)).date()
            start_at = datetime(day.year, day.month, day.day,
                                random.choice(SLOT_HOURS), 0, tzinfo=timezone.utc)
            # статус зависит от того, прошла ли дата
            if day_offset < 0:
                status = "cancelled" if random.random() < 0.12 else "done"
            elif day_offset == 0:
                status = random.choice(["confirmed", "done"])
            else:
                status = random.choice(["pending", "confirmed"])

            await conn.execute(
                """
                INSERT INTO appointments (client_id, barber_id, service_id, start_at, status, price)
                VALUES ($1, $2, $3, $4, $5, $6)
                """,
                random.choice(client_ids), random.choice(barber_ids),
                svc["id"], start_at, status, svc["price"],
            )

        print(f"[ok] barbers={len(BARBERS)} services={len(SERVICES)} clients=50 appointments=200")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
