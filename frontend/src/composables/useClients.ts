import { shallowRef } from 'vue'

import http from '@/api/http'
import type { Client, Page } from '@/api/types'

export interface ClientPayload {
  name: string
  phone: string
  notes: string | null
}

export interface LoadParams {
  page: number
  itemsPerPage: number
  search: string
}

export function useClients() {
  const items = shallowRef<Client[]>([])
  const total = shallowRef(0)
  const loading = shallowRef(false)

  async function load({ page, itemsPerPage, search }: LoadParams) {
    loading.value = true
    try {
      const { data } = await http.get<Page<Client>>('/clients', {
        params: { page, page_size: itemsPerPage, search: search || undefined },
      })
      items.value = data.items
      total.value = data.total
    }
    finally {
      loading.value = false
    }
  }

  function create(payload: ClientPayload) {
    return http.post('/clients', payload)
  }

  function update(id: number, payload: ClientPayload) {
    return http.patch(`/clients/${id}`, payload)
  }

  function remove(id: number) {
    return http.delete(`/clients/${id}`)
  }

  return { items, total, loading, load, create, update, remove }
}
