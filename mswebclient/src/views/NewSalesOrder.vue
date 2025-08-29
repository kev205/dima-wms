<template>
  <AppLayout page-title="New Sales Order" page-description="Create a new sales order for your customer">
    <div class="max-w-4xl mx-auto">
      <form @submit.prevent="handleSubmit">
        <!-- Customer Selection -->
        <div class="card mb-6">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Customer Information</h3>
          </div>
          <div class="p-6">
            <div class="mb-4">
              <label class="label">Select Customer *</label>
              <CustomerSelector v-model="selectedCustomer" :initial-customer-id="initialCustomerId"
                @update:modelValue="handleCustomerChange" />
              <p v-if="errors.customer_id" class="mt-1 text-sm text-red-600">{{ errors.customer_id }}</p>
            </div>

            <div v-if="selectedCustomer" class="bg-gray-50 rounded-lg p-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 class="text-sm font-medium text-gray-700">Contact Info</h4>
                  <p class="text-sm text-gray-600">{{ selectedCustomer.email }}</p>
                  <p class="text-sm text-gray-600">{{ selectedCustomer.phone }}</p>
                </div>
                <div>
                  <h4 class="text-sm font-medium text-gray-700">Billing Address</h4>
                  <p class="text-sm text-gray-600">{{ selectedCustomer.billing_address || 'No billing address' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Lines -->
        <div class="card mb-6">
          <div class="px-6 py-4 border-b border-gray-200">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-medium text-gray-900">Order Items</h3>
              <button type="button" @click="addOrderLine" class="btn-secondary text-sm">
                <PlusIcon class="w-4 h-4 mr-2" />
                Add Item
              </button>
            </div>
          </div>
          <div class="p-6">
            <div v-if="orderLines.length === 0" class="text-center py-8 text-gray-500">
              <ShoppingCartIcon class="mx-auto h-12 w-12 text-gray-400" />
              <p class="mt-2">No items added yet. Click "Add Item" to get started.</p>
            </div>

            <div v-else class="space-y-4">
              <div v-for="(line, index) in orderLines" :key="index" class="border border-gray-200 rounded-lg p-4">
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 items-start">
                  <div class="lg:col-span-4">
                    <label class="label text-xs">Product *</label>
                    <ProductSelector v-model="line.product"
                      @update:modelValue="(product) => handleProductChange(index, product)" />
                    <p v-if="errors[`lines.${index}.product_id`]" class="mt-1 text-sm text-red-600">
                      {{ errors[`lines.${index}.product_id`] }}
                    </p>
                  </div>

                  <div class="lg:col-span-2">
                    <label class="label text-xs">Quantity *</label>
                    <input v-model.number="line.qty" @input="calculateLineTotal(index)" type="number" min="1" required
                      class="input-field text-sm" />
                    <p v-if="line.product && line.qty > line.product.quantity_on_hand"
                      class="mt-1 text-xs text-yellow-600">
                      Only {{ line.product.quantity_on_hand }} available
                    </p>
                  </div>

                  <div class="lg:col-span-2">
                    <label class="label text-xs">Unit Price</label>
                    <div class="relative">
                      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <span class="text-gray-500 text-sm">$</span>
                      </div>
                      <input v-model.number="line.unit_price" @input="calculateLineTotal(index)" type="number" disabled
                        step="0.01" min="0" class="input-field pl-7 text-sm" />
                    </div>
                  </div>

                  <div class="lg:col-span-2">
                    <label class="label text-xs">Discount %</label>
                    <input v-model.number="line.discount_pct" @input="calculateLineTotal(index)" type="number"
                      step="0.01" min="0" max="100" class="input-field text-sm" />
                  </div>

                  <div class="lg:col-span-1">
                    <label class="label text-xs">Total</label>
                    <div class="text-sm font-medium text-gray-900 py-2">
                      ${{ line.sub_total?.toFixed(2) || '0.00' }}
                    </div>
                  </div>

                  <div class="lg:col-span-1 flex items-end">
                    <button type="button" @click="removeOrderLine(index)" class="text-red-600 hover:text-red-800 p-2">
                      <TrashIcon class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="card mb-6">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Order Summary</h3>
          </div>
          <div class="p-6">
            <div class="max-w-sm ml-auto space-y-2">
              <div class="flex justify-between text-sm">
                <span>Subtotal:</span>
                <span>${{ orderTotal.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span>VAT ({{ vatRate }}%):</span>
                <span>${{ vatAmount.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-lg font-medium border-t pt-2">
                <span>Total:</span>
                <span>${{ grandTotal.toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Notes -->
        <div class="card mb-6">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-medium text-gray-900">Notes</h3>
          </div>
          <div class="p-6">
            <textarea v-model="notes" rows="3" class="input-field"
              placeholder="Add any notes for this order..."></textarea>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-end space-x-4">
          <router-link to="/sales-orders" class="btn-secondary">
            Cancel
          </router-link>
          <button type="submit" :disabled="loading || !canSubmit" class="btn-primary">
            <LoadingSpinner v-if="loading" size="sm" class="mr-2" />
            Create Order
          </button>
        </div>
      </form>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { salesOrderApi } from '@/services/api'
import { useNotificationStore } from '@/stores/notifications'
import AppLayout from '@/components/AppLayout.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import CustomerSelector from '@/components/CustomerSelector.vue'
import ProductSelector from '@/components/ProductSelector.vue'
import {
  PlusIcon,
  ShoppingCartIcon,
  TrashIcon
} from '@heroicons/vue/24/outline'
import type { Customer, Product } from '@/types'

interface OrderLine {
  product: Product | null
  qty: number
  unit_price: number
  discount_pct: number
  sub_total: number
}

const router = useRouter()
const route = useRoute()
const notificationStore = useNotificationStore()

const loading = ref(false)
const errors = ref<Record<string, string>>({})

const selectedCustomer = ref<Customer | null>(null)
const orderLines = ref<OrderLine[]>([])
const notes = ref('')
const vatRate = ref(20)

const initialCustomerId = computed(() => route.query.customer_id as string)

const orderTotal = computed(() => {
  return orderLines.value.reduce((sum, line) => sum + (line.sub_total || 0), 0)
})

const vatAmount = computed(() => {
  return orderTotal.value * (vatRate.value / 100)
})

const grandTotal = computed(() => {
  return orderTotal.value + vatAmount.value
})

const canSubmit = computed(() => {
  return selectedCustomer.value &&
    orderLines.value.length > 0 &&
    orderLines.value.every(line => line.product && line.qty > 0 && line.unit_price >= 0)
})

const handleCustomerChange = (customer: Customer | null) => {
  selectedCustomer.value = customer
  errors.value.customer_id = ''
}

const addOrderLine = () => {
  orderLines.value.push({
    product: null,
    qty: 1,
    unit_price: 0,
    discount_pct: 0,
    sub_total: 0
  })
}

const removeOrderLine = (index: number) => {
  orderLines.value.splice(index, 1)
}

const handleProductChange = (index: number, product: Product | null) => {
  if (product && orderLines.value[index]) {
    orderLines.value[index].product = product
    orderLines.value[index].unit_price = Number(product.sales_price)
    calculateLineTotal(index)
  }

  delete errors.value[`lines.${index}.product_id`]
}

const calculateLineTotal = (index: number) => {
  const line = orderLines.value[index]
  if (line) {
    line.sub_total = line.qty * line.unit_price * (1 - line.discount_pct / 100)
  }
}

const validateForm = () => {
  errors.value = {}
  let isValid = true

  if (!selectedCustomer.value) {
    errors.value.customer_id = 'Please select a customer'
    isValid = false
  }

  if (orderLines.value.length === 0) {
    notificationStore.error('Order Error', 'Please add at least one item to the order')
    isValid = false
  }

  orderLines.value.forEach((line, index) => {
    if (!line.product) {
      errors.value[`lines.${index}.product_id`] = 'Please select a product'
      isValid = false
    }

    if (line.product && line.qty > line.product.quantity_on_hand) {
      notificationStore.warning(
        'Insufficient Stock',
        `${line.product.name} has only ${line.product.quantity_on_hand} units available`
      )
      isValid = false
    }
  })

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    loading.value = true

    const orderData = {
      customer_id: selectedCustomer.value!.id,
      notes: notes.value || undefined,
      lines: orderLines.value.map(line => ({
        product_id: line.product!.id,
        qty: line.qty,
        discount_pct: line.discount_pct || 0
      }))
    }

    const response = await salesOrderApi.create(orderData)

    notificationStore.success(
      'Order Created',
      `Sales order ${response.data.data.number} has been created successfully`
    )

    router.push(`/sales-orders/${response.data.data.id}`)
  } catch (error: any) {
    const errorMessage = error.response?.data?.message || 'An unexpected error occurred'

    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    }

    notificationStore.error('Failed to Create Order', errorMessage)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  addOrderLine()
})
</script>