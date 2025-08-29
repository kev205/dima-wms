<template>
  <AppLayout page-title="Sales Orders" page-description="Manage sales orders and track order status">
    <template #header-actions>
      <router-link to="/sales-orders/new" class="btn-primary">
        <PlusIcon class="w-4 h-4 mr-2" />
        New Order
      </router-link>
    </template>

    <!-- Filters -->
    <div class="mb-6 flex flex-col sm:flex-row gap-4">
      <div class="flex-1 max-w-lg">
        <label for="search" class="sr-only">Search orders</label>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
          </div>
          <input id="search" v-model="searchQuery" @input="debouncedSearch" type="text"
            placeholder="Search by order number or customer..."
            class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm" />
        </div>
      </div>

      <div>
        <select v-model="statusFilter" @change="loadOrders"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md bg-white text-sm focus:outline-none focus:ring-1 focus:ring-primary-500 focus:border-primary-500">
          <option value="">All Status</option>
          <option value="DRAFT">Draft</option>
          <option value="CONFIRMED">Confirmed</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
      </div>
    </div>

    <!-- Orders list -->
    <div class="card">
      <div class="px-4 py-5 sm:p-6">
        <LoadingSpinner v-if="loading" text="Loading orders..." />

        <div v-else-if="orders.length === 0" class="text-center py-8">
          <ShoppingCartIcon class="mx-auto h-12 w-12 text-gray-400" />
          <h3 class="mt-2 text-sm font-medium text-gray-900">No orders</h3>
          <p class="mt-1 text-sm text-gray-500">
            {{
            searchQuery || statusFilter
            ? 'No orders match your filters.'
            : 'Get started by creating a new sales order.'
            }}
          </p>
          <div class="mt-6">
            <router-link to="/sales-orders/new" class="btn-primary">
              <PlusIcon class="w-4 h-4 mr-2" />
              New Order
            </router-link>
          </div>
        </div>

        <div v-else class="overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Order
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Customer
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th scope="col" class="relative px-6 py-3">
                  <span class="sr-only">Actions</span>
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ order.number }}</div>
                    <div class="text-xs text-gray-500">{{ order.lines.length }} item(s)</div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ order.customer.name }}</div>
                    <div class="text-xs text-gray-500">{{ order.customer.email }}</div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span :class="getStatusClasses(order.status)">
                    {{ getStatusLabel(order.status) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">${{ order.order_total }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(order.created_at) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div class="flex items-center justify-end space-x-2">
                    <router-link :to="`/sales-orders/${order.id}`" class="text-primary-600 hover:text-primary-900">
                      View
                    </router-link>

                    <button v-if="order.status === 'DRAFT'" @click="confirmOrder(order)"
                      class="text-green-600 hover:text-green-900">
                      Confirm
                    </button>

                    <button v-if="order.status === 'CONFIRMED'" @click="cancelOrder(order)"
                      class="text-yellow-600 hover:text-yellow-900">
                      Cancel
                    </button>

                    <button v-if="order.status === 'DRAFT'" @click="deleteOrder(order)"
                      class="text-red-600 hover:text-red-900">
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Confirmation Dialogs -->
    <ConfirmDialog :show="showConfirmDialog" title="Confirm Order"
      :message="`Are you sure you want to confirm order '${confirmingOrder?.number}'? This will reserve inventory and cannot be undone.`"
      confirm-text="Confirm Order" @confirm="handleConfirmOrder" @cancel="showConfirmDialog = false"
      ref="confirmDialog" />

    <ConfirmDialog :show="showCancelDialog" title="Cancel Order"
      :message="`Are you sure you want to cancel order '${cancellingOrder?.number}'? This will release any reserved inventory.`"
      confirm-text="Cancel Order" variant="warning" @confirm="handleCancelOrder" @cancel="showCancelDialog = false"
      ref="cancelDialog" />

    <ConfirmDialog :show="showDeleteDialog" title="Delete Order"
      :message="`Are you sure you want to delete order '${deletingOrder?.number}'? This action cannot be undone.`"
      confirm-text="Delete" variant="danger" @confirm="handleDeleteOrder" @cancel="showDeleteDialog = false"
      ref="deleteDialog" />
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { salesOrderApi } from '@/services/api'
import { useNotificationStore } from '@/stores/notifications'
import AppLayout from '@/components/AppLayout.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import { debounce } from 'lodash-es'
import { format } from 'date-fns'
import { PlusIcon, MagnifyingGlassIcon, ShoppingCartIcon } from '@heroicons/vue/24/outline'
import type { SalesOrder } from '@/types'

const notificationStore = useNotificationStore()

const orders = ref<SalesOrder[]>([])
const loading = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')

const showConfirmDialog = ref(false)
const showCancelDialog = ref(false)
const showDeleteDialog = ref(false)

const confirmingOrder = ref<SalesOrder | null>(null)
const cancellingOrder = ref<SalesOrder | null>(null)
const deletingOrder = ref<SalesOrder | null>(null)

const confirmDialog = ref()
const cancelDialog = ref()
const deleteDialog = ref()

const loadOrders = async () => {
  try {
    loading.value = true
    const response = await salesOrderApi.getAll({
      status: statusFilter.value || undefined
    })
    orders.value = response.data.results
  } catch (error: any) {
    notificationStore.error(
      'Failed to load orders',
      error.response?.data?.message || 'An unexpected error occurred'
    )
  } finally {
    loading.value = false
  }
}

const debouncedSearch = debounce(loadOrders, 300)

const getStatusClasses = (status: string) => {
  const classes = 'inline-flex px-2 py-1 text-xs font-semibold rounded-full'

  switch (status) {
    case 'DRAFT':
      return `${classes} bg-gray-100 text-gray-800`
    case 'CONFIRMED':
      return `${classes} bg-green-100 text-green-800`
    case 'CANCELLED':
      return `${classes} bg-red-100 text-red-800`
    default:
      return `${classes} bg-gray-100 text-gray-800`
  }
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

const formatDate = (dateString: string) => {
  return format(new Date(dateString), 'MMM dd, yyyy h:mm:ss a')
}

const confirmOrder = (order: SalesOrder) => {
  confirmingOrder.value = order
  showConfirmDialog.value = true
}

const cancelOrder = (order: SalesOrder) => {
  cancellingOrder.value = order
  showCancelDialog.value = true
}

const deleteOrder = (order: SalesOrder) => {
  deletingOrder.value = order
  showDeleteDialog.value = true
}

const handleConfirmOrder = async () => {
  if (!confirmingOrder.value) return

  try {
    await salesOrderApi.confirm(confirmingOrder.value.id)
    notificationStore.success('Order confirmed successfully', 'Inventory has been reserved')
    showConfirmDialog.value = false
    await loadOrders()
  } catch (error: any) {
    notificationStore.error(
      'Failed to confirm order',
      error.response?.data?.message || 'An unexpected error occurred'
    )
  } finally {
    confirmDialog.value?.setLoading(false)
  }
}

const handleCancelOrder = async () => {
  if (!cancellingOrder.value) return

  try {
    await salesOrderApi.cancel(cancellingOrder.value.id)
    notificationStore.success(
      'Order cancelled successfully',
      'Reserved inventory has been released'
    )
    showCancelDialog.value = false
    await loadOrders()
  } catch (error: any) {
    notificationStore.error(
      'Failed to cancel order',
      error.response?.data?.message || 'An unexpected error occurred'
    )
  } finally {
    cancelDialog.value?.setLoading(false)
  }
}

const handleDeleteOrder = async () => {
  if (!deletingOrder.value) return

  try {
    await salesOrderApi.delete(deletingOrder.value.id)
    notificationStore.success('Order deleted successfully')
    showDeleteDialog.value = false
    await loadOrders()
  } catch (error: any) {
    notificationStore.error(
      'Failed to delete order',
      error.response?.data?.message || 'An unexpected error occurred'
    )
  } finally {
    deleteDialog.value?.setLoading(false)
  }
}

onMounted(() => {
  loadOrders()
})
</script>
