<template>
  <AppLayout 
    page-title="Products" 
    page-description="Manage your product inventory"
  >
    <template #header-actions>
      <button
        @click="showCreateDialog = true"
        class="btn-primary"
      >
        <PlusIcon class="w-4 h-4 mr-2" />
        Add Product
      </button>
    </template>

    <!-- Modern Search Bar -->
    <div class="mb-8">
      <div class="max-w-md">
        <label for="search" class="label">
          <span class="flex items-center">
            <CubeIcon class="w-4 h-4 mr-2" />
            Search Products
          </span>
        </label>
        <div class="relative">
          <input
            id="search"
            v-model="searchQuery"
            @input="debouncedSearch"
            type="text"
            placeholder="Search by name, or category..."
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

    <!-- Modern Products Grid -->
    <div class="card">
      <div class="p-8">
        <LoadingSpinner v-if="loading" text="Loading products..." />
        
        <div v-else-if="products.length === 0" class="text-center py-16">
          <div class="w-20 h-20 bg-gradient-to-r from-purple-100 to-purple-200 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <CubeIcon class="h-10 w-10 text-purple-600" />
          </div>
          <h3 class="text-xl font-bold text-gray-900 mb-2">No products found</h3>
          <p class="text-gray-500 mb-8 max-w-md mx-auto">
            {{ searchQuery ? 'No products match your search criteria. Try adjusting your search terms.' : 'Get started by adding your first product to the catalog.' }}
          </p>
          <button
            @click="showCreateDialog = true"
            class="btn-primary"
          >
            <PlusIcon class="w-4 h-4 mr-2" />
            Add First Product
          </button>
        </div>

        <div v-else>
          <!-- Modern Table -->
          <table class="table-modern">
            <thead class="table-header">
              <tr>
                <th class="px-8 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">
                  Product
                </th>
                <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">
                  Price
                </th>
                <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">
                  Stock
                </th>
                <th class="px-6 py-4 text-left text-xs font-bold text-gray-600 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-4 text-right text-xs font-bold text-gray-600 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="product in products" :key="product.id" class="table-row group">
                <td class="px-8 py-6 whitespace-nowrap">
                  <div class="flex items-center space-x-4">
                    <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                      <span class="text-white font-bold text-lg">{{ product.name.charAt(0) }}</span>
                    </div>
                    <div>
                      <div class="text-sm font-bold text-gray-900 group-hover:text-purple-600 transition-colors duration-200">{{ product.name }}</div>
                      <div class="inline-flex items-center px-2 py-1 rounded-lg text-xs font-medium text-gray-700 mt-1">
                        {{ product.internal_reference }}
                      </div>
                      <div class="inline-flex items-center px-2 py-1 rounded-lg text-xs font-medium bg-gray-100 text-gray-700 mt-1">
                        {{ product.product_category }}
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-6 whitespace-nowrap">
                  <div class="text-lg font-bold text-gray-900">${{ product.sales_price }}</div>
                  <div class="text-sm text-gray-500">Cost: ${{ product.cost }}</div>
                </td>
                <td class="px-6 py-6 whitespace-nowrap">
                  <div class="flex items-center space-x-2">
                    <div>
                      <div class="text-sm font-semibold text-gray-900">Available</div>
                      <div class="text-xs text-gray-500">{{ product.quantity_on_hand }} on hand, {{ product.reserved }} reserved</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-6 whitespace-nowrap">
                  <span :class="[
                    'badge',
                    product.quantity_on_hand > 10 
                      ? 'badge-success' 
                      : product.quantity_on_hand > 0 
                        ? 'badge-warning'
                        : 'badge-error'
                  ]">
                    {{ product.quantity_on_hand > 10 ? 'In Stock' : product.available  ? 'Low Stock' : 'Out of Stock' }}
                  </span>
                </td>
                <td class="px-6 py-6 whitespace-nowrap text-right">
                  <div class="flex items-center justify-end space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                    <button
                      @click="editProduct(product)"
                      class="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-200"
                      title="Edit product"
                    >
                      <PencilIcon class="w-4 h-4" />
                    </button>
                    <button
                      @click="confirmDelete(product)"
                      class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all duration-200"
                      title="Delete product"
                    >
                      <TrashIcon class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Product Form Modal -->
    <ProductFormModal
      :show="showCreateDialog || showEditDialog"
      :product="editingProduct"
      @close="closeDialog"
      @save="handleSave"
    />

    <!-- Delete Confirmation -->
    <ConfirmDialog
      :show="showDeleteDialog"
      title="Delete Product"
      :message="`Are you sure you want to delete '${deletingProduct?.name}'? This action cannot be undone.`"
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
import { productApi } from '@/services/api'
import { useNotificationStore } from '@/stores/notifications'
import AppLayout from '@/components/AppLayout.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import ProductFormModal from '@/components/ProductFormModal.vue'
import { debounce } from 'lodash-es'
import {
  PlusIcon,
  CubeIcon,
  TrashIcon,
  PencilIcon
} from '@heroicons/vue/24/outline'
import type { Product } from '@/types'

const notificationStore = useNotificationStore()

const products = ref<Product[]>([])
const loading = ref(false)
const searchQuery = ref('')

const showCreateDialog = ref(false)
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)

const editingProduct = ref<Product | null>(null)
const deletingProduct = ref<Product | null>(null)

const deleteDialog = ref()

const loadProducts = async () => {
  try {
    loading.value = true
    const response = await productApi.getAll({
      search: searchQuery.value || undefined
    })
    products.value = response.data.results
  } catch (error: any) {
    notificationStore.error(
      'Failed to load products',
      error.response?.data?.message || 'An unexpected error occurred'
    )
  } finally {
    loading.value = false
  }
}

const debouncedSearch = debounce(loadProducts, 300)

const clearSearch = () => {
  searchQuery.value = ''
  loadProducts()
}

const editProduct = (product: Product) => {
  editingProduct.value = product
  showEditDialog.value = true
}

const confirmDelete = (product: Product) => {
  deletingProduct.value = product
  showDeleteDialog.value = true
}

const handleDelete = async () => {
  if (!deletingProduct.value) return

  try {
    await productApi.delete(deletingProduct.value.id)
    notificationStore.success('Product deleted successfully')
    showDeleteDialog.value = false
    await loadProducts()
  } catch (error: any) {
    notificationStore.error(
      'Failed to delete product',
      error.response?.data?.message || 'An unexpected error occurred'
    )
  } finally {
    deleteDialog.value?.setLoading(false)
  }
}

const handleSave = async () => {
  showCreateDialog.value = false
  showEditDialog.value = false
  editingProduct.value = null
  await loadProducts()
}

const closeDialog = () => {
  showCreateDialog.value = false
  showEditDialog.value = false
  editingProduct.value = null
}

onMounted(() => {
  loadProducts()
})
</script>