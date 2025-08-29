import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const user = ref<any>(null)
  const isAuthenticated = ref(!!token.value)

  const login = async (email: string, password: string) => {
    try {
      const response = await authApi.login(email, password)
      token.value = response.data.access
      refreshToken.value = response.data.refresh
      user.value = response.data.user
      isAuthenticated.value = true
      localStorage.setItem('auth_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
      return { success: true }
    } catch (error: any) {
      return {
        success: false,
        message: error.response?.data?.message || 'Login failed'
      }
    }
  }

  const logout = async () => {
    try {
      await authApi.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      refreshToken.value = null
      user.value = null
      isAuthenticated.value = false
      localStorage.removeItem('auth_token')
      localStorage.removeItem('refresh_token')
    }
  }

  const verifyToken = async () => {
    if (!refreshToken.value) return false

    try {
      const response = await authApi.verify(refreshToken.value)
      token.value = response.data.access
      localStorage.setItem('auth_token', response.data.access)
      isAuthenticated.value = true
      return true
    } catch (error) {
      logout()
      return false
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    verifyToken
  }
})
