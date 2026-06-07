-- Схема админ-панели барбершопа Brick & Razor.
-- Идемпотентна: безопасно применять повторно (CREATE ... IF NOT EXISTS).

CREATE TABLE IF NOT EXISTS barbers (
    id    SERIAL PRIMARY KEY,
    slug  TEXT NOT NULL UNIQUE,
    name  TEXT NOT NULL,
    role  TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS services (
    id           SERIAL PRIMARY KEY,
    slug         TEXT NOT NULL UNIQUE,
    title        TEXT NOT NULL,
    price        INTEGER NOT NULL,          -- рубли, целое
    duration_min INTEGER NOT NULL DEFAULT 60
);

CREATE TABLE IF NOT EXISTS clients (
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    phone      TEXT NOT NULL,
    notes      TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_clients_created_at ON clients (created_at DESC);

CREATE TABLE IF NOT EXISTS appointments (
    id         SERIAL PRIMARY KEY,
    client_id  INTEGER NOT NULL REFERENCES clients (id) ON DELETE CASCADE,
    barber_id  INTEGER NOT NULL REFERENCES barbers (id) ON DELETE RESTRICT,
    service_id INTEGER NOT NULL REFERENCES services (id) ON DELETE RESTRICT,
    start_at   TIMESTAMPTZ NOT NULL,
    status     TEXT NOT NULL DEFAULT 'pending'
               CHECK (status IN ('pending', 'confirmed', 'done', 'cancelled')),
    price      INTEGER NOT NULL,            -- цена на момент записи
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_appointments_start_at ON appointments (start_at DESC);
CREATE INDEX IF NOT EXISTS idx_appointments_barber   ON appointments (barber_id);
CREATE INDEX IF NOT EXISTS idx_appointments_status   ON appointments (status);
