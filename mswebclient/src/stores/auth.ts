import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authApi } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const user = ref<any>(null)
  const isAuthenticated = ref(!!token.value)

  const login = async (email: string, password: string) => {
    try {
      const response = await authApi.login(email, password)
      token.value = response.data.access
      user.value = response.data.user
      isAuthenticated.value = true
      localStorage.setItem('auth_token', response.data.access)
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
      user.value = null
      isAuthenticated.value = false
      localStorage.removeItem('auth_token')
    }
  }

  const verifyToken = async () => {
    if (!token.value) return false

    try {
      const response = await authApi.verify()
      user.value = response.data
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
