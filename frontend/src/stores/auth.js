import { defineStore } from 'pinia'
import { ref } from 'vue'
import client from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = ref(!!localStorage.getItem('access_token'))

  async function login(email, password) {
    const { data } = await client.post('/auth/login', { email, password })
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    isAuthenticated.value = true
    await fetchMe()
  }

  async function register(email, password) {
    const { data } = await client.post('/auth/register', { email, password })
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
    isAuthenticated.value = true
    await fetchMe()
  }

  async function fetchMe() {
    const { data } = await client.get('/auth/me')
    user.value = data
  }

  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
    isAuthenticated.value = false
  }

  return { user, isAuthenticated, login, register, fetchMe, logout }
})
