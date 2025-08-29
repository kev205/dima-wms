<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <!-- Background decoration -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-32 w-80 h-80 bg-gradient-to-br from-blue-400/20 to-purple-400/20 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-32 w-80 h-80 bg-gradient-to-tr from-purple-400/20 to-pink-400/20 rounded-full blur-3xl"></div>
    </div>
    
    <div class="max-w-md w-full space-y-8 relative">
      <!-- Header -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 flex items-center justify-center bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl shadow-xl transform rotate-3 hover:rotate-0 transition-transform duration-300">
          <CubeIcon class="h-10 w-10 text-white" />
        </div>
        <h2 class="mt-8 text-center text-4xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
          Welcome Back
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Sign in to <span class="font-semibold text-blue-600">DIMA WMS</span>
        </p>
        <p class="text-xs text-gray-400 mt-1">Telesales Console</p>
      </div>
      
      <!-- Login Form -->
      <div class="card p-8 backdrop-blur-lg bg-white/80 border border-white/20">
        <form class="space-y-6" @submit.prevent="handleSubmit">
          <div class="space-y-4">
            <div>
              <label for="email-address" class="label">
                <span class="flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                  Email Address
                </span>
              </label>
              <input
                id="email-address"
                v-model="form.email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="input-field"
                placeholder="Enter your email"
              />
            </div>
            
            <div>
              <label for="password" class="label">
                <span class="flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                  Password
                </span>
              </label>
              <input
                id="password"
                v-model="form.password"
                name="password"
                type="password"
                autocomplete="current-password"
                required
                class="input-field"
                placeholder="Enter your password"
              />
            </div>
          </div>

          <!-- Error Alert -->
          <div v-if="error" class="rounded-xl bg-red-50 border border-red-100 p-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <ExclamationTriangleIcon class="h-5 w-5 text-red-400" />
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-semibold text-red-800">
                  Authentication Error
                </h3>
                <div class="mt-1 text-sm text-red-700">
                  <p>{{ error }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <div>
            <button
              type="submit"
              :disabled="loading"
              class="btn-primary w-full text-base"
            >
              <LoadingSpinner v-if="loading" size="sm" class="mr-2" />
              <svg v-else class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
              </svg>
              Sign In
            </button>
          </div>
        </form>
      </div>

      <!-- Demo Credentials -->
      <div class="card-compact p-6 bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
        <div class="text-center">
          <h4 class="text-sm font-semibold text-blue-800 mb-3 flex items-center justify-center">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Demo Credentials
          </h4>
          <div class="text-sm text-blue-700 space-y-1 mb-4">
            <p><span class="font-medium">Email:</span> admin@example.com</p>
            <p><span class="font-medium">Password:</span> adminpass</p>
          </div>
          <button
            type="button"
            @click="fillDemoCredentials"
            class="btn-secondary text-sm py-2 px-4"
          >
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
            Quick Fill
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notifications'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import {
  CubeIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const loading = ref(false)
const error = ref('')

const form = ref({
  email: '',
  password: ''
})

const fillDemoCredentials = () => {
  form.value.email = 'admin@example.com'
  form.value.password = 'adminpass'
}

const handleSubmit = async () => {
  error.value = ''
  
  if (!form.value.email || !form.value.password) {
    error.value = 'Please enter both email and password'
    return
  }

  try {
    loading.value = true
    const result = await authStore.login(form.value.email, form.value.password)
    
    if (result.success) {
      notificationStore.success('Welcome back!', 'You have successfully signed in')
      router.push('/')
    } else {
      error.value = result.message || 'Invalid credentials'
    }
  } catch (err: any) {
    error.value = err.message || 'An unexpected error occurred'
  } finally {
    loading.value = false
  }
}
</script>