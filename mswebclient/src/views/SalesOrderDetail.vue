<template>
  <AppLayout>
    <LoadingSpinner v-if="loading" text="Loading order details..." />

    <div v-else-if="order" class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Order {{ order.number }}</h1>
          <p class="mt-1 text-sm text-gray-600">
            Created {{ formatDate(order.created_at) }}
          </p>
        </div>
        <div class="flex items-center space-x-4">
          <span :class="getStatusClasses(order.status)">
            {{ getStatusLabel(order.status) }}
          </span>

          <div class="flex space-x-2">
            <button v-if="order.status === 'DRAFT'" @click="confirmOrder" class="btn-primary">
              Confirm Order
            </button>

            <button v-if="order.status === 'CONFIRMED'" @click="cancelOrder" class="btn-secondary">
              Cancel Order
            </button>

            <router-link to="/sales-orders" class="btn-secondary">
              Back to Orders
            </router-link>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Order Details -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Customer Information -->
          <div class="card">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Customer Information</h3>
            </div>
            <div class="p-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 class="text-sm font-medium text-gray-700">Contact Details</h4>
                  <div class="mt-2 space-y-1">
                    <p class="text-sm text-gray-900">{{ order.customer.name }}</p>
                    <p class="text-sm text-gray-600">{{ order.customer.email }}</p>
                    <p class="text-sm text-gray-600">{{ order.customer.phone }}</p>
                  </div>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-gray-700">Addresses</h4>
                  <div class="mt-2 space-y-2">
                    <div v-if="order.customer.billing_address">
                      <p class="text-xs font-medium text-gray-500 uppercase">Billing</p>
                      <p class="text-sm text-gray-900">{{ order.customer.billing_address }}</p>
                    </div>
                    <div v-if="order.customer.shipping_address">
                      <p class="text-xs font-medium text-gray-500 uppercase">Shipping</p>
                      <p class="text-sm text-gray-900">{{ order.customer.shipping_address }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Order Items -->
          <div class="card">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Order Items</h3>
            </div>
            <div class="overflow-hidden">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Product
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Quantity
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Price
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Discount
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Total
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="line in order.lines" :key="line.id">
                    <td class="px-6 py-4">
                      <div>
                        <div class="text-sm font-medium text-gray-900">{{ line.product.name }}</div>
                      </div>
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-900">
                      {{ line.qty }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-900">
                      ${{ line.unit_price }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-900">
                      {{ line.discount_pct > 0 ? `${line.discount_pct}%` : '-' }}
                    </td>
                    <td class="px-6 py-4 text-sm font-medium text-gray-900">
                      ${{ line.sub_total }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Notes -->
          <div v-if="order.notes" class="card">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Notes</h3>
            </div>
            <div class="p-6">
              <p class="text-sm text-gray-700">{{ order.notes }}</p>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="lg:col-span-1">
          <div class="card sticky top-6">
            <div class="px-6 py-4 border-b border-gray-200">
              <h3 class="text-lg font-medium text-gray-900">Order Summary</h3>
            </div>
            <div class="p-6 space-y-4">
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span>Subtotal:</span>
                  <span>${{ order.order_total }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span>VAT ({{ order.vat_rate }}%):</span>
                  <span>${{ (order.order_total -= (order.order_total * (order.vat_rate / 100))) }}</span>
                </div>
                <div class="flex justify-between text-lg font-medium border-t pt-2">
                  <span>Total:</span>
                  <span>${{ order.order_total }}</span>
                </div>
              </div>

              <div class="pt-4 border-t">
                <div class="text-xs text-gray-500 uppercase tracking-wider font-medium mb-2">
                  Order Status
                </div>
                <div class="space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-sm">Created</span>
                    <span class="text-sm text-gray-500">{{ formatDate(order.created_at) }}</span>
                  </div>
                  <div v-if="order.status === 'CONFIRMED'" class="flex items-center justify-between">
                    <span class="text-sm">Confirmed</span>
                    <span v-if="order.updated_at" class="text-sm text-gray-500">{{ formatDate(order.updated_at)
                      }}</span>
                  </div>
                  <div v-if="order.status === 'CANCELLED'" class="flex items-center justify-between">
                    <span class="text-sm">Cancelled</span>
                    <span v-if="order.updated_at" class="text-sm text-gray-500">{{ formatDate(order.updated_at)
                      }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-8">
      <h3 class="text-lg font-medium text-gray-900">Order not found</h3>
      <p class="mt-2 text-sm text-gray-500">The requested order could not be found.</p>
      <div class="mt-6">
        <router-link to="/sales-orders" class="btn-primary">
          Back to Orders
        </router-link>
      </div>
    </div>

    <!-- Confirmation Dialogs -->
    <ConfirmDialog :show="showConfirmDialog" title="Confirm Order"
      :message="`Are you sure you want to confirm order '${order?.number}'? This will reserve inventory and cannot be undone.`"
      confirm-text="Confirm Order" @confirm="handleConfirmOrder" @cancel="showConfirmDialog = false"
      ref="confirmDialog" />

    <ConfirmDialog :show="showCancelDialog" title="Cancel Order"
      :message="`Are you sure you want to cancel order '${order?.number}'? This will release any reserved inventory.`"
      confirm-text="Cancel Order" variant="warning" @confirm="handleCancelOrder" @cancel="showCancelDialog = false"
      ref="cancelDialog" />
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { salesOrderApi } from '@/services/api'
import { useNotificationStore } from '@/stores/notifications'
import AppLayout from '@/components/AppLayout.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import { format } from 'date-fns'
import type { SalesOrder } from '@/types'

const route = useRoute()
const notificationStore = useNotificationStore()

const order = ref<SalesOrder | null>(null)
const loading = ref(false)

const showConfirmDialog = ref(false)
const showCancelDialog = ref(false)

const confirmDialog = ref()
const cancelDialog = ref()

const loadOrder = async () => {
  try {
    loading.value = true
    const orderId = route.params.id as string
    const response = await salesOrderApi.getById(orderId)
    order.value = response.data.data
  } catch (error: any) {
    notificationStore.error(
      'Failed to load order',
      error.response?.data?.message || 'An unexpected error occurred'
    )
  } finally {
    loading.value = false
  }
}

const getStatusClasses = (status: string) => {
  const classes = 'inline-flex px-3 py-1 text-sm font-semibold rounded-full'
  
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
  return format(new Date(dateString), 'MMM dd, h:mm:ss a')
}

const confirmOrder = () => {
  showConfirmDialog.value = true
}

const cancelOrder = () => {
  showCancelDialog.value = true
}

const handleConfirmOrder = async () => {
  if (!order.value) return

  try {
    const response = await salesOrderApi.confirm(order.value.id)
    order.value = response.data.data
    notificationStore.success('Order confirmed successfully', 'Inventory has been reserved')
    showConfirmDialog.value = false
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
  if (!order.value) return

  try {
    const response = await salesOrderApi.cancel(order.value.id)
    order.value = response.data.data
    notificationStore.success('Order cancelled successfully', 'Reserved inventory has been released')
    showCancelDialog.value = false
  } catch (error: any) {
    notificationStore.error(
      'Failed to cancel order',
      error.response?.data?.message || 'An unexpected error occurred'
    )
  } finally {
    cancelDialog.value?.setLoading(false)
  }
}

onMounted(() => {
  loadOrder()
})
</script>