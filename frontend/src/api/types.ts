// TS-зеркало схем бэкенда (app/schemas.py).

export interface Page<T> {
  items: T[]
  total: number
}

export interface Client {
  id: number
  name: string
  phone: string
  notes: string | null
  created_at: string
}

export interface Barber {
  id: number
  slug: string
  name: string
  role: string
  active: boolean
}

export interface Service {
  id: number
  slug: string
  title: string
  price: number
  duration_min: number
}

export type AppointmentStatus = 'pending' | 'confirmed' | 'done' | 'cancelled'

export interface Appointment {
  id: number
  start_at: string
  status: AppointmentStatus
  price: number
  client_id: number
  client_name: string
  barber_id: number
  barber_name: string
  service_id: number
  service_title: string
}

export interface StatsKpi {
  appointments_today: number
  revenue_month: number
  new_clients_month: number
  total_clients: number
}

export interface DayCount {
  day: string
  count: number
}

export interface ServiceRevenue {
  service: string
  revenue: number
}

export interface Stats {
  kpi: StatsKpi
  by_day: DayCount[]
  by_service: ServiceRevenue[]
}
