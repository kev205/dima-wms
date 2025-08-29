<template>
  <AppLayout 
    page-title="Dashboard" 
    page-description="Welcome back! Here's what's happening with your business today."
  >
    <!-- Modern Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Total Orders -->
      <div class="card p-6 hover-lift">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600 mb-1">Total Orders</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.totalOrders }}</p>
            <div class="flex items-center mt-2">
              <svg class="w-4 h-4 text-green-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              <span class="text-sm text-green-600 font-medium">+12.5%</span>
              <span class="text-sm text-gray-500 ml-1">from last month</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center">
            <ShoppingCartIcon class="h-6 w-6 text-white" />
          </div>
        </div>
      </div>

      <!-- Total Customers -->
      <div class="card p-6 hover-lift">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600 mb-1">Customers</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.totalCustomers }}</p>
            <div class="flex items-center mt-2">
              <svg class="w-4 h-4 text-green-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              <span class="text-sm text-green-600 font-medium">+8.3%</span>
              <span class="text-sm text-gray-500 ml-1">this month</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-green-600 rounded-xl flex items-center justify-center">
            <UsersIcon class="h-6 w-6 text-white" />
          </div>
        </div>
      </div>

      <!-- Total Products -->
      <div class="card p-6 hover-lift">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600 mb-1">Products</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.totalProducts }}</p>
            <div class="flex items-center mt-2">
              <svg class="w-4 h-4 text-blue-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
              </svg>
              <span class="text-sm text-gray-600 font-medium">No change</span>
              <span class="text-sm text-gray-500 ml-1">from last month</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl flex items-center justify-center">
            <CubeIcon class="h-6 w-6 text-white" />
          </div>
        </div>
      </div>

      <!-- Revenue -->
      <div class="card p-6 hover-lift">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600 mb-1">Revenue</p>
            <p class="text-3xl font-bold text-gray-900">${{ formatNumber(stats.totalRevenue) }}</p>
            <div class="flex items-center mt-2">
              <svg class="w-4 h-4 text-green-500 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              <span class="text-sm text-green-600 font-medium">+15.2%</span>
              <span class="text-sm text-gray-500 ml-1">from last month</span>
            </div>
          </div>
          <div class="w-12 h-12 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-xl flex items-center justify-center">
            <CurrencyDollarIcon class="h-6 w-6 text-white" />
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Recent Orders -->
      <div class="card">
        <div class="px-8 py-6 border-b border-gray-100">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center">
                <ShoppingCartIcon class="h-5 w-5 text-white" />
              </div>
              <div>
                <h3 class="text-lg font-bold text-gray-900">Recent Orders</h3>
                <p class="text-sm text-gray-500">Latest customer orders</p>
              </div>
            </div>
            <router-link
              to="/sales-orders"
              class="btn-secondary text-sm py-2 px-4"
            >
              View All
            </router-link>
          </div>
        </div>
        <div class="p-8">
          <div v-if="loadingOrders" class="text-center py-8">
            <LoadingSpinner size="sm" />
            <p class="text-sm text-gray-500 mt-2">Loading orders...</p>
          </div>
          <div v-else-if="recentOrders.length === 0" class="text-center py-12">
            <div class="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <ShoppingCartIcon class="h-8 w-8 text-gray-400" />
            </div>
            <h4 class="text-lg font-semibold text-gray-900 mb-2">No recent orders</h4>
            <p class="text-sm text-gray-500">Orders will appear here once customers start placing them.</p>
          </div>
          <div v-else class="space-y-4">
            <div
              v-for="order in recentOrders"
              :key="order.id"
              class="card-compact p-4 hover:shadow-lg transition-all duration-200 cursor-pointer hover:border-blue-200"
              @click="$router.push(`/sales-orders/${order.id}`)"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <div class="w-10 h-10 bg-gradient-to-r from-gray-100 to-gray-200 rounded-xl flex items-center justify-center">
                    <span class="text-sm font-bold text-gray-600">#{{ order.number.slice(-3) }}</span>
                  </div>
                  <div>
                    <p class="font-semibold text-gray-900">Order {{ order.number }}</p>
                    <p class="text-sm text-gray-500">{{ order.customer.name }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="font-bold text-gray-900">${{ order.order_total }}</p>
                  <span :class="getModernStatusClasses(order.status)">
                    {{ getStatusLabel(order.status) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card">
        <div class="px-8 py-6 border-b border-gray-100">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">Quick Actions</h3>
              <p class="text-sm text-gray-500">Common tasks and shortcuts</p>
            </div>
          </div>
        </div>
        <div class="p-8">
          <div class="grid grid-cols-1 gap-4">
            <router-link
              to="/sales-orders/new"
              class="card-compact p-4 hover:shadow-lg transition-all duration-200 group border-l-4 border-l-blue-500 hover:border-l-blue-600"
            >
              <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                  <PlusIcon class="h-6 w-6 text-white" />
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-gray-900 group-hover:text-blue-600">Create Sales Order</h4>
                  <p class="text-sm text-gray-500">Start a new order for a customer</p>
                </div>
                <svg class="w-5 h-5 text-gray-400 group-hover:text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </router-link>

            <router-link
              to="/customers"
              class="card-compact p-4 hover:shadow-lg transition-all duration-200 group border-l-4 border-l-green-500 hover:border-l-green-600"
            >
              <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-green-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                  <UsersIcon class="h-6 w-6 text-white" />
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-gray-900 group-hover:text-green-600">Manage Customers</h4>
                  <p class="text-sm text-gray-500">View and edit customer information</p>
                </div>
                <svg class="w-5 h-5 text-gray-400 group-hover:text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </router-link>

            <router-link
              to="/products"
              class="card-compact p-4 hover:shadow-lg transition-all duration-200 group border-l-4 border-l-purple-500 hover:border-l-purple-600"
            >
              <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                  <CubeIcon class="h-6 w-6 text-white" />
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-gray-900 group-hover:text-purple-600">Product Catalog</h4>
                  <p class="text-sm text-gray-500">Browse and manage products</p>
                </div>
                <svg class="w-5 h-5 text-gray-400 group-hover:text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </router-link>

            <router-link
              to="/sales-orders"
              class="card-compact p-4 hover:shadow-lg transition-all duration-200 group border-l-4 border-l-orange-500 hover:border-l-orange-600"
            >
              <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-gradient-to-r from-orange-500 to-orange-600 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                  <ShoppingCartIcon class="h-6 w-6 text-white" />
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-gray-900 group-hover:text-orange-600">View All Orders</h4>
                  <p class="text-sm text-gray-500">Track and manage sales orders</p>
                </div>
                <svg class="w-5 h-5 text-gray-400 group-hover:text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Low Stock Alert -->
    <div v-if="lowStockProducts.length > 0" class="mt-8">
      <div class="card border-l-4 border-l-amber-500">
        <div class="px-8 py-6 border-b border-gray-100">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-r from-amber-500 to-amber-600 rounded-xl flex items-center justify-center">
              <ExclamationTriangleIcon class="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 class="text-lg font-bold text-gray-900">Low Stock Alert</h3>
              <p class="text-sm text-gray-500">{{ lowStockProducts.length }} products running low</p>
            </div>
          </div>
        </div>
        <div class="p-8">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="product in lowStockProducts"
              :key="product.id"
              class="card-compact p-4 border-l-4 border-l-amber-500 hover:shadow-lg transition-all duration-200"
            >
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <p class="font-semibold text-gray-900">{{ product.name }}</p>
                </div>
                <div class="text-right">
                  <div class="flex items-center space-x-2">
                    <div class="w-8 h-8 bg-gradient-to-r from-amber-100 to-amber-200 rounded-lg flex items-center justify-center">
                      <span class="text-sm font-bold text-amber-800">{{ product.quantity_on_hand }}</span>
                    </div>
                  </div>
                  <p class="text-xs text-amber-600 font-medium mt-1">Low Stock</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { salesOrderApi, productApi, customerApi } from '@/services/api'
import AppLayout from '@/components/AppLayout.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import {
  ShoppingCartIcon,
  UsersIcon,
  CubeIcon,
  CurrencyDollarIcon,
  PlusIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import type { SalesOrder, Product } from '@/types'

const stats = ref({
  totalOrders: 0,
  totalCustomers: 0,
  totalProducts: 0,
  totalRevenue: 0
})

const recentOrders = ref<SalesOrder[]>([])
const lowStockProducts = ref<Product[]>([])
const loadingOrders = ref(false)

const loadDashboardData = async () => {
  try {
    // Load recent orders
    loadingOrders.value = true
    const ordersResponse = await salesOrderApi.getAll({ page: 1 })
    recentOrders.value = ordersResponse.data.results.slice(0, 5)
    stats.value.totalOrders = ordersResponse.data.count

    // Calculate revenue from confirmed orders
    stats.value.totalRevenue = recentOrders.value
      .filter(order => order.status === 'CONFIRMED')
      .reduce((sum, order) => sum + order.order_total, 0)

    // Load products for low stock check
    const productsResponse = await productApi.getAll()
    const products = productsResponse.data.results
    stats.value.totalProducts = productsResponse.data.count
    
    // Find low stock products (less than 10 available)
    lowStockProducts.value = products.filter(product => product.quantity_on_hand < 10 && product.available)

    // Load customer count
    const customersResponse = await customerApi.getAll()
    stats.value.totalCustomers = customersResponse.data.count

  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    loadingOrders.value = false
  }
}

const getModernStatusClasses = (status: string) => {
  const baseClasses = 'badge'
  
  switch (status) {
    case 'DRAFT':
      return `${baseClasses} badge-info`
    case 'CONFIRMED':
      return `${baseClasses} badge-success`
    case 'CANCELLED':
      return `${baseClasses} badge-error`
    default:
      return `${baseClasses} badge-info`
  }
}

const formatNumber = (num: number) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(num)
}

const getStatusLabel = (status: string) => {
  switch (status) {
    case 'DRAFT':
      return 'Draft'
    case 'CONFIRMED':
      return 'Confirmed'
    case 'CANCELLED':
      return 'Cancelled'
    default:
      return status
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>