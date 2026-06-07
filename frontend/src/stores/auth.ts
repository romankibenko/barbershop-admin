import { defineStore } from 'pinia'
import { computed, shallowRef } from 'vue'

import http from '@/api/http'

export const useAuthStore = defineStore('auth', () => {
  const token = shallowRef<string | null>(localStorage.getItem('token'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(username: string, password: string) {
    const form = new URLSearchParams({ username, password })
    const { data } = await http.post<{ access_token: string }>('/auth/login', form)
    token.value = data.access_token
    localStorage.setItem('token', data.access_token)
  }

  function logout() {
    token.value = null
    localStorage.removeItem('token')
  }

  return { token, isAuthenticated, login, logout }
})
