import { shallowRef } from 'vue'

import http from '@/api/http'
import type { Stats } from '@/api/types'

export function useStats() {
  const stats = shallowRef<Stats | null>(null)
  const loading = shallowRef(false)

  async function load() {
    loading.value = true
    try {
      const { data } = await http.get<Stats>('/stats')
      stats.value = data
    }
    finally {
      loading.value = false
    }
  }

  return { stats, loading, load }
}
