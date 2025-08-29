<template>
  <AppLayout 
    page-title="Customers" 
    page-description="Manage your customer database"
  >
    <template #header-actions>
      <button
        @click="showCreateDialog = true"
        class="btn-primary"
      >
        <PlusIcon class="w-4 h-4 mr-2" />
        Add Customer
      </button>
    </template>

    <!-- Modern Search Bar -->
    <div class="mb-8">
      <div class="max-w-md">
        <label for="search" class="label">
          <span class="flex items-center">
            <MagnifyingGlassIcon class="w-4 h-4 mr-2" />
            Search Customers
          </span>
        </label>
        <div class="relative">
          <input
            id="search"
            v-model="searchQuery"
            @input="debouncedSearch"
            type="text"
            placeholder="Search by name, email, or phone..."
            class="input-field pl-4"
          />
          <div v-if="searchQuery" class="absolute inset-y-0 right-0 pr-3 flex items-center">
            <button
              @click="clearSearch"
              class="text-gray-400 hover:text-gray-600 transition-colors duration-200"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modern Customers Grid -->
    <div class="card">
      <div class="p-8">
        <LoadingSpinner v-if="loading" text="Loading customers..." />
        
        <div v-else-if="customers.length === 0" class="text-center py-16">
          <div class="w-20 h-20 bg-gradient-to-r from-blue-100 to-blue-200 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <UsersIcon class="h-10 w-10 text-blue-600" />
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-2">No customers found</h3>
          <p class="text-gray-500 mb-8 max-w-md mx-auto">
            {{ searchQuery ? 'No customers match your search criteria. Try adjusting your search terms.' : 'Get started by adding your first customer to the system.' }}
          </p>
          <button
            @click="showCreateDialog = true"
            class="btn-primary"
          >
            <PlusIcon class="w-4 h-4 mr-2" />
            Add First Customer
          </button>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="customer in customers"
            :key="customer.id"
            class="card hover-lift group"
          >
            <div class="p-6">
              <!-- Header with Avatar -->
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-3">
                  <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center">
                    <span class="text-white font-bold text-lg">{{ customer.name.charAt(0) }}</span>
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-900 group-hover:text-blue-600 transition-colors duration-200">{{ customer.name }}</h3>
                    <p class="text-sm text-gray-500">Customer</p>
                  </div>
                </div>
                
                <div class="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                  <button
                    @click="editCustomer(customer)"
                    class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200"
                    title="Edit customer"
                  >
                    <PencilIcon class="w-4 h-4" />
                  </button>
                  <button
                    @click="confirmDelete(customer)"
                    class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all duration-200"
                    title="Delete customer"
                  >
                    <TrashIcon class="w-4 h-4" />
                  </button>
                </div>
              </div>

              <!-- Contact Info -->
              <div class="space-y-3">
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center">
                    <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                    </svg>
                  </div>
                  <span class="text-sm text-gray-600 font-medium">{{ customer.email }}</span>
                </div>
                
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center">
                    <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <span class="text-sm text-gray-600 font-medium">{{ customer.phone }}</span>
                </div>
              </div>

              <!-- Addresses -->
              <div class="mt-6 pt-4 border-t border-gray-100 space-y-4">
                <div v-if="customer.billing_address">
                  <div class="flex items-center space-x-2 mb-2">
                    <div class="w-6 h-6 bg-green-100 rounded-lg flex items-center justify-center">
                      <svg class="w-3 h-3 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    </div>
                    <span class="text-xs font-semibold text-green-700">Billing Address</span>
                  </div>
                  <p class="text-sm text-gray-600 ml-8">{{ customer.billing_address }}</p>
                </div>
                
                <div v-if="customer.shipping_address">
                  <div class="flex items-center space-x-2 mb-2">
                    <div class="w-6 h-6 bg-blue-100 rounded-lg flex items-center justify-center">
                      <svg class="w-3 h-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10" />
                      </svg>
                    </div>
                    <span class="text-xs font-semibold text-blue-700">Shipping Address</span>
                  </div>
                  <p class="text-sm text-gray-600 ml-8">{{ customer.shipping_address }}</p>
                </div>
              </div>

              <div class="mt-4 pt-4 border-t border-gray-100">
                <button
                  @click="createOrderForCustomer(customer)"
                  class="w-full btn-primary text-sm"
                >
                  <ShoppingCartIcon class="w-4 h-4 mr-2" />
                  Create Order
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Customer Form Modal -->
    <CustomerFormModal
      :show="showCreateDialog || showEditDialog"
      :customer="editingCustomer"
      @close="closeDialog"
      @save="handleSave"
    />

    <!-- Delete Confirmation -->
    <ConfirmDialog
      :show="showDeleteDialog"
      title="Delete Customer"
      :message="`Are you sure you want to delete '${deletingCustomer?.name}'? This action cannot be undone.`"
      confirm-text="Delete"
      variant="danger"
      @confirm="handleDelete"
      @cancel="showDeleteDialog = false"
      ref="deleteDialog"
    />
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { customerApi } from '@/services/api'
import { useNotificationStore } from '@/stores/notifications'
import AppLayout from '@/components/AppLayout.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import CustomerFormModal from '@/components/CustomerFormModal.vue'
import { debounce } from 'lodash-es'
import {
  PlusIcon,
  MagnifyingGlassIcon,
  UsersIcon,
  PencilIcon,
  TrashIcon,
  ShoppingCartIcon
} from '@heroicons/vue/24/outline'
import type { Customer } from '@/types'

const router = useRouter()
const notificationStore = useNotificationStore()

const customers = ref<Customer[]>([])
const loading = ref(false)
const searchQuery = ref('')

const showCreateDialog = ref(false)
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)

const editingCustomer = ref<Customer | null>(null)
const deletingCustomer = ref<Customer | null>(null)

const deleteDialog = ref()

const loadCustomers = async () => {
  try {
    loading.value = true
    const response = await customerApi.getAll({
      search: searchQuery.value || undefined
    })
    customers.value = response.data.results
  } catch (error: any) {
    notificationStore.error(
      'Failed to load customers',
      error.response?.data?.message || 'An unexpected error occurred'
    )
  } finally {
    loading.value = false
  }
}

const debouncedSearch = debounce(loadCustomers, 300)

const clearSearch = () => {
  searchQuery.value = ''
  loadCustomers()
}

const editCustomer = (customer: Customer) => {
  editingCustomer.value = customer
  showEditDialog.value = true
}

const confirmDelete = (customer: Customer) => {
  deletingCustomer.value = customer
  showDeleteDialog.value = true
}

const handleDelete = async () => {
  if (!deletingCustomer.value) return

  try {
    await customerApi.delete(deletingCustomer.value.id)
    notificationStore.success('Customer deleted successfully')
    showDeleteDialog.value = false
    await loadCustomers()
  } catch (error: any) {
    notificationStore.error(
      'Failed to delete customer',
      error.response?.data?.message || 'An unexpected error occurred'
    )
  } finally {
    deleteDialog.value?.setLoading(false)
  }
}

const handleSave = async () => {
  showCreateDialog.value = false
  showEditDialog.value = false
  editingCustomer.value = null
  await loadCustomers()
}

const closeDialog = () => {
  showCreateDialog.value = false
  showEditDialog.value = false
  editingCustomer.value = null
}

const createOrderForCustomer = (customer: Customer) => {
  router.push({
    name: 'NewSalesOrder',
    query: { customer_id: customer.id }
  })
}

onMounted(() => {
  loadCustomers()
})
</script>