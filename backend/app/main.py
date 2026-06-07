from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import pool
from app.routers import appointments, auth, clients, refs, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    await pool.connect()
    yield
    await pool.disconnect()


app = FastAPI(title="Brick & Razor Admin API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(refs.router)
app.include_router(appointments.router)
app.include_router(stats.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
