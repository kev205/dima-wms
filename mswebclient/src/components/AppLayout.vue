<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
    <!-- Navigation -->
    <nav class="glass border-b border-white/20 backdrop-blur-xl sticky top-0 z-40">
      <div class="container-modern">
        <div class="flex justify-between h-16">
          <div class="flex">
            <!-- Logo -->
            <div class="flex-shrink-0 flex items-center">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                  <CubeIcon class="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 class="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">DIMA WMS</h1>
                  <span class="text-xs text-gray-500 -mt-1 block">Telesales Console - v1.0.0</span>
                </div>
              </div>
            </div>
            
            <!-- Main Navigation -->
            <div class="hidden md:ml-10 md:flex md:space-x-1">
              <router-link
                v-for="item in navigation"
                :key="item.name"
                :to="item.href"
                :class="[
                  $route.name === item.name
                    ? 'bg-blue-50 text-blue-700 border-blue-500'
                    : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50/50 border-transparent',
                  'inline-flex items-center px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 border'
                ]"
              >
                <component :is="item.icon" class="w-4 h-4 mr-2" />
                {{ item.label }}
              </router-link>
            </div>
          </div>

          <!-- Right side -->
          <div class="flex items-center space-x-4">
            <!-- Mobile menu button -->
            <button
              @click="showMobileMenu = !showMobileMenu"
              class="md:hidden p-2 rounded-lg text-gray-600 hover:text-blue-600 hover:bg-blue-50 transition-colors duration-200"
            >
              <Bars3Icon v-if="!showMobileMenu" class="w-6 h-6" />
              <XMarkIcon v-else class="w-6 h-6" />
            </button>

            <!-- User menu -->
            <div class="relative" data-user-menu>
              <button
                @click="showUserMenu = !showUserMenu"
                class="flex items-center space-x-3 p-2 rounded-xl text-sm hover:bg-blue-50 transition-all duration-200 focus-ring"
              >
                <div class="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                  <span class="text-white text-sm font-semibold">
                    {{ userInitials }}
                  </span>
                </div>
                <div class="hidden sm:block text-left">
                  <p class="text-gray-900 font-semibold">{{ authStore.user?.name || 'User' }}</p>
                  <p class="text-xs text-gray-500">Administrator</p>
                </div>
                <ChevronDownIcon class="w-4 h-4 text-gray-400 transition-transform duration-200" :class="{ 'rotate-180': showUserMenu }" />
              </button>

              <!-- User menu dropdown -->
              <transition
                enter-active-class="transition ease-out duration-200"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-150"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <div
                  v-if="showUserMenu"
                  class="origin-top-right absolute right-0 mt-2 w-56 rounded-2xl shadow-xl bg-white border border-gray-100 focus:outline-none z-50"
                >
                  <div class="p-2">
                    <div class="px-4 py-3 border-b border-gray-100">
                      <p class="text-sm font-semibold text-gray-900">{{ authStore.user?.name || 'User' }}</p>
                      <p class="text-xs text-gray-500">{{ authStore.user?.email || 'user@example.com' }}</p>
                    </div>
                    <button
                      @click="handleLogout"
                      class="w-full text-left px-4 py-3 text-sm text-red-600 hover:bg-red-50 rounded-xl transition-colors duration-200 flex items-center mt-2"
                    >
                      <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                      </svg>
                      Sign Out
                    </button>
                  </div>
                </div>
              </transition>
            </div>
          </div>
        </div>
      </div>

      <!-- Mobile menu -->
      <transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <div v-if="showMobileMenu" class="md:hidden border-t border-white/20">
          <div class="container-modern py-4">
            <div class="space-y-2">
              <router-link
                v-for="item in navigation"
                :key="item.name"
                :to="item.href"
                :class="[
                  $route.name === item.name
                    ? 'bg-blue-50 text-blue-700 border-blue-500'
                    : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50/50 border-transparent',
                  'flex items-center px-4 py-3 rounded-xl text-sm font-semibold transition-all duration-200 border'
                ]"
                @click="showMobileMenu = false"
              >
                <component :is="item.icon" class="w-5 h-5 mr-3" />
                {{ item.label }}
              </router-link>
            </div>
          </div>
        </div>
      </transition>
    </nav>

    <!-- Page header -->
    <header v-if="pageTitle" class="border-b border-white/20 glass">
      <div class="container-modern">
        <div class="py-8">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between space-y-4 sm:space-y-0">
            <div>
              <h1 class="text-3xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">{{ pageTitle }}</h1>
              <p v-if="pageDescription" class="mt-2 text-gray-600">
                {{ pageDescription }}
              </p>
            </div>
            <div class="flex-shrink-0">
              <slot name="header-actions" />
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="container-modern py-8">
      <slot />
    </main>

    <!-- Notifications -->
    <NotificationList />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import {
  HomeIcon,
  CubeIcon,
  UsersIcon,
  ShoppingCartIcon,
  ChevronDownIcon,
  Bars3Icon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import NotificationList from './NotificationList.vue'

interface Props {
  pageTitle?: string
  pageDescription?: string
}

const props = withDefaults(defineProps<Props>(), {
  pageTitle: '',
  pageDescription: ''
})

const router = useRouter()
const authStore = useAuthStore()

const showUserMenu = ref(false)
const showMobileMenu = ref(false)

const navigation = [
  { name: 'Dashboard', label: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Products', label: 'Products', href: '/products', icon: CubeIcon },
  { name: 'Customers', label: 'Customers', href: '/customers', icon: UsersIcon },
  { name: 'SalesOrders', label: 'Sales Orders', href: '/sales-orders', icon: ShoppingCartIcon }
]

const userInitials = computed(() => {
  const name = authStore.user?.name || 'User'
  return name.split(' ').map((n: string) => n[0]).join('').toUpperCase()
})

const handleLogout = async () => {
  await authStore.logout()
  showUserMenu.value = false
  router.push('/login')
}

const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  if (!target.closest('[data-user-menu]')) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>