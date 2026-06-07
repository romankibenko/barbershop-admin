# Brick & Razor — админ-панель

Админ-панель барбершопа: клиенты, записи, аналитика. Часть портфолио-кейса «полный диджитал для бизнеса» — вместе с [лендингом и Telegram-ботом](https://github.com/romankibenko/barbershop-landing).

## Стек

**Backend** — FastAPI + asyncpg (PostgreSQL) + JWT-авторизация
**Frontend** — Vue 3 + Vuetify + Pinia + Vue Router + TypeScript + Chart.js

## Структура

```
barbershop-admin/
├── backend/          ← FastAPI (Railway)
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

- **Backend + PostgreSQL** — Railway
- **Frontend** — Vercel

Подробности — в `backend/README` и при настройке деплоя.
