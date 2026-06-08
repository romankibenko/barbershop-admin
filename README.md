# Brick & Razor — админ-панель

Mini-CRM барбершопа: клиенты, записи и дашборд с аналитикой. Часть портфолио-кейса «полный диджитал для бизнеса» — вместе с [лендингом и Telegram-ботом](https://github.com/romankibenko/barbershop-landing).

## Демо

- **Приложение:** https://barbershop-admin-six.vercel.app
- **Демо-доступ:** `admin` / `admin123`

> Бэкенд живёт на бесплатном тарифе Render — после простоя первый запрос будит сервис (~30–50 с), дальше работает быстро.

## Стек

**Backend** — FastAPI + asyncpg (PostgreSQL, чистый SQL) + JWT-авторизация
**Frontend** — Vue 3 + Vuetify + Pinia + Vue Router + TypeScript + Chart.js

## Структура

```
barbershop-admin/
├── backend/          ← FastAPI (Render)
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── db/        ← пул соединений, схема, seed
│       └── routers/   ← auth, clients, appointments, stats
└── frontend/         ← Vue 3 + Vuetify (Vercel)
    └── src/
```

## Запуск локально

### Backend

```bash
cd backend
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
copy .env.example .env                            # прописать DATABASE_URL, JWT_SECRET
python -m scripts.init_db                         # накатить схему
python -m scripts.seed                            # засеять демо-данные (50 клиентов / 200 записей)
uvicorn app.main:app --reload
```

API на `http://localhost:8000`, Swagger — `/docs`.

### Frontend

```bash
cd frontend
npm install
copy .env.example .env                            # прописать VITE_API_URL
npm run dev
```

## Деплой

- **PostgreSQL** — [Neon](https://neon.tech) (serverless, EU/Frankfurt)
- **Backend** — [Render](https://render.com) (Blueprint `render.yaml`, бесплатный тариф)
- **Frontend** — [Vercel](https://vercel.com) (SPA-fallback в `frontend/vercel.json`)

Бэкенд и БД настраиваются через переменные окружения (см. `backend/.env.example`); фронт — через `VITE_API_URL`.
