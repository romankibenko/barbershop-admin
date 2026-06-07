"""Создаёт базу barbershop (если нет) и применяет schema.sql.

Запуск из каталога backend:
    .venv\\Scripts\\python.exe -m scripts.init_db
"""
import asyncio
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import asyncpg

from app.config import settings

SCHEMA = Path(__file__).resolve().parent.parent / "app" / "db" / "schema.sql"


async def ensure_database() -> None:
    parsed = urlparse(settings.database_url)
    db_name = parsed.path.lstrip("/")
    # Подключаемся к служебной базе postgres теми же кредами, чтобы создать целевую.
    admin_dsn = urlunparse(parsed._replace(path="/postgres"))

    conn = await asyncpg.connect(admin_dsn)
    try:
        exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", db_name)
        if not exists:
            await conn.execute(f'CREATE DATABASE "{db_name}"')
            print(f"[ok] База {db_name} создана")
        else:
            print(f"[--] База {db_name} уже существует")
    finally:
        await conn.close()


async def apply_schema() -> None:
    conn = await asyncpg.connect(settings.database_url)
    try:
        await conn.execute(SCHEMA.read_text(encoding="utf-8"))
        print("[ok] Схема применена")
    finally:
        await conn.close()


async def main() -> None:
    await ensure_database()
    await apply_schema()


if __name__ == "__main__":
    asyncio.run(main())
