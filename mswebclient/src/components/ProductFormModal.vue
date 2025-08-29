<template>
  <TransitionRoot as="template" :show="show">
    <Dialog as="div" class="relative z-50" @close="$emit('close')">
      <TransitionChild as="template" enter="ease-out duration-300" enter-from="opacity-0" enter-to="opacity-100"
        leave="ease-in duration-200" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <TransitionChild as="template" enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100" leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
            <DialogPanel
              class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-2xl sm:p-6">
              <form @submit.prevent="handleSubmit">
                <div class="mb-6">
                  <DialogTitle as="h3" class="text-lg font-semibold leading-6 text-gray-900">
                    {{ isEditing ? 'Edit Product' : 'Add New Product' }}
                  </DialogTitle>
                </div>

                <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
                  <div class="sm:col-span-2">
                    <label for="name" class="label">Product Name *</label>
                    <input id="name" v-model="form.name" type="text" required class="input-field"
                      :class="{ 'border-red-300': errors.name }" />
                    <p v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</p>
                  </div>

                  <div>
                    <label for="product_category" class="label">Category *</label>
                    <input id="product_category" v-model="form.product_category" type="text" required class="input-field"
                      :class="{ 'border-red-300': errors.product_category }" />
                    <p v-if="errors.product_category" class="mt-1 text-sm text-red-600">{{ errors.product_category }}</p>
                  </div>

                  <div>
                    <label for="sales_price" class="label">Price *</label>
                    <div class="relative">
                      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <span class="text-gray-500 sm:text-sm">$</span>
                      </div>
                      <input id="sales_price" v-model.number="form.sales_price" type="number" step="0.01" min="0" required
                        class="input-field pl-7" :class="{ 'border-red-300': errors.sales_price }" />
                    </div>
                    <p v-if="errors.sales_price" class="mt-1 text-sm text-red-600">{{ errors.sales_price }}</p>
                  </div>

                  <div>
                    <label for="internal_reference" class="label">Internal Reference *</label>
                    <input id="internal_reference" v-model="form.internal_reference" type="text" required class="input-field"
                      :class="{ 'border-red-300': errors.internal_reference }" />
                    <p v-if="errors.internal_reference" class="mt-1 text-sm text-red-600">{{ errors.internal_reference }}</p>
                  </div>

                  <div>
                    <label for="product_type" class="label">Product Type *</label>
                    <input id="product_type" v-model="form.product_type" type="text" required class="input-field"
                      :class="{ 'border-red-300': errors.product_type }" />
                    <p v-if="errors.product_type" class="mt-1 text-sm text-red-600">{{ errors.product_type }}</p>
                  </div>

                  <div>
                    <label for="cost" class="label">Cost *</label>
                    <div class="relative">
                      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <span class="text-gray-500 sm:text-sm">$</span>
                      </div>
                      <input id="cost" v-model.number="form.cost" type="number" step="0.01" min="0" required
                        class="input-field pl-7" :class="{ 'border-red-300': errors.cost }" />
                    </div>
                    <p v-if="errors.cost" class="mt-1 text-sm text-red-600">{{ errors.cost }}</p>
                  </div>

                  <div>
                    <label for="quantity_on_hand" class="label">Stock on Hand *</label>
                    <input id="quantity_on_hand" v-model.number="form.quantity_on_hand" type="number" min="0" required class="input-field"
                      :class="{ 'border-red-300': errors.quantity_on_hand }" />
                    <p v-if="errors.quantity_on_hand" class="mt-1 text-sm text-red-600">{{ errors.quantity_on_hand }}</p>
                  </div>

                  <div class="sm:col-span-2">
                    <label for="description" class="label">Description</label>
                    <textarea id="description" v-model="form.description" rows="3" class="input-field"
                      :class="{ 'border-red-300': errors.description }"></textarea>
                    <p v-if="errors.description" class="mt-1 text-sm text-red-600">{{ errors.description }}</p>
                  </div>
                </div>

                <div class="mt-6 flex items-center justify-end space-x-4">
                  <button type="button" @click="$emit('close')" class="btn-secondary" :disabled="loading">
                    Cancel
                  </button>
                  <button type="submit" class="btn-primary" :disabled="loading">
                    <LoadingSpinner v-if="loading" size="sm" class="mr-2" />
                    {{ isEditing ? 'Update Product' : 'Create Product' }}
                  </button>
                </div>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  TransitionChild,
  TransitionRoot
} from '@headlessui/vue'
import { productApi } from '@/services/api'
import { useNotificationStore } from '@/stores/notifications'
import LoadingSpinner from './LoadingSpinner.vue'
import type { Product } from '@/types'

interface Props {
  show: boolean
  product?: Product | null
}

const props = withDefaults(defineProps<Props>(), {
  product: null
})

const emit = defineEmits<{
  close: []
  save: []
}>()

const notificationStore = useNotificationStore()

const loading = ref(false)
const errors = ref<Record<string, string>>({})

const form = ref({
  name: '',
  product_category: '',
  internal_reference: '',
  product_type: '',
  sales_price: 0,
  cost: 0,
  quantity_on_hand: 0,
  description: ''
})

const isEditing = computed(() => !!props.product)

const resetForm = () => {
  form.value = {
    name: '',
    product_category: '',
    internal_reference: '',
    product_type: '',
    sales_price: 0,
    cost: 0,
    quantity_on_hand: 0,
    description: ''
  }
  errors.value = {}
}

const populateForm = (product: Product) => {
  form.value = {
    name: product.name,
    product_category: product.product_category,
    internal_reference: product.internal_reference,
    product_type: product.product_type,
    sales_price: Number(product.sales_price),
    cost: product.cost,
    quantity_on_hand: product.quantity_on_hand,
    description: product.description || ''
  }
}

const validateForm = () => {
  errors.value = {}
  let isValid = true

  if (!form.value.name.trim()) {
    errors.value.name = 'Product name is required'
    isValid = false
  }

  if (!form.value.product_category.trim()) {
    errors.value.product_category = 'Category is required'
    isValid = false
  }

  if (form.value.sales_price <= 0) {
    errors.value.sales_price = 'Price must be greater than 0'
    isValid = false
  }

  if (form.value.cost < 0) {
    errors.value.cost = 'Cost cannot be negative'
    isValid = false
  }

  if (form.value.quantity_on_hand < 0) {
    errors.value.quantity_on_hand = 'Stock cannot be negative'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    loading.value = true

    if (isEditing.value && props.product) {
      await productApi.update(props.product.id, form.value)
      notificationStore.success('Product updated successfully')
    } else {
      await productApi.create(form.value)
      notificationStore.success('Product created successfully')
    }

    emit('save')
    resetForm()
  } catch (error: any) {
    const errorMessage = error.response?.data?.message || 'An unexpected error occurred'

    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else {
      notificationStore.error(
        isEditing.value ? 'Failed to update product' : 'Failed to create product',
        errorMessage
      )
    }
  } finally {
    loading.value = false
  }
}

watch(() => props.show, (newValue) => {
  if (newValue) {
    if (props.product) {
      populateForm(props.product)
    } else {
      resetForm()
    }
  }
})
</script>