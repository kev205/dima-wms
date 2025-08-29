<template>
  <TransitionRoot as="template" :show="show">
    <Dialog as="div" class="relative z-50" @close="$emit('close')">
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
      </TransitionChild>

      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel class="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-2xl sm:p-6">
              <form @submit.prevent="handleSubmit">
                <div class="mb-6">
                  <DialogTitle as="h3" class="text-lg font-semibold leading-6 text-gray-900">
                    {{ isEditing ? 'Edit Customer' : 'Add New Customer' }}
                  </DialogTitle>
                </div>

                <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
                  <div class="sm:col-span-2">
                    <label for="name" class="label">Customer Name *</label>
                    <input
                      id="name"
                      v-model="form.name"
                      type="text"
                      required
                      class="input-field"
                      :class="{ 'border-red-300': errors.name }"
                    />
                    <p v-if="errors.name" class="mt-1 text-sm text-red-600">{{ errors.name }}</p>
                  </div>

                  <div>
                    <label for="email" class="label">Email Address *</label>
                    <input
                      id="email"
                      v-model="form.email"
                      type="email"
                      required
                      class="input-field"
                      :class="{ 'border-red-300': errors.email }"
                    />
                    <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
                  </div>

                  <div>
                    <label for="phone" class="label">Phone Number *</label>
                    <input
                      id="phone"
                      v-model="form.phone"
                      type="tel"
                      required
                      class="input-field"
                      :class="{ 'border-red-300': errors.phone }"
                    />
                    <p v-if="errors.phone" class="mt-1 text-sm text-red-600">{{ errors.phone }}</p>
                  </div>

                  <div class="sm:col-span-2">
                    <label for="billing_address" class="label">Billing Address</label>
                    <textarea
                      id="billing_address"
                      v-model="form.billing_address"
                      rows="3"
                      class="input-field"
                      :class="{ 'border-red-300': errors.billing_address }"
                      placeholder="Street address, city, state, postal code, country"
                    ></textarea>
                    <p v-if="errors.billing_address" class="mt-1 text-sm text-red-600">{{ errors.billing_address }}</p>
                  </div>

                  <div class="sm:col-span-2">
                    <div class="flex items-center">
                      <input
                        id="same_as_billing"
                        v-model="sameAsBilling"
                        type="checkbox"
                        class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                      />
                      <label for="same_as_billing" class="ml-2 block text-sm text-gray-900">
                        Shipping address is the same as billing address
                      </label>
                    </div>
                  </div>

                  <div v-if="!sameAsBilling" class="sm:col-span-2">
                    <label for="shipping_address" class="label">Shipping Address</label>
                    <textarea
                      id="shipping_address"
                      v-model="form.shipping_address"
                      rows="3"
                      class="input-field"
                      :class="{ 'border-red-300': errors.shipping_address }"
                      placeholder="Street address, city, state, postal code, country"
                    ></textarea>
                    <p v-if="errors.shipping_address" class="mt-1 text-sm text-red-600">{{ errors.shipping_address }}</p>
                  </div>
                </div>

                <div class="mt-6 flex items-center justify-end space-x-4">
                  <button
                    type="button"
                    @click="$emit('close')"
                    class="btn-secondary"
                    :disabled="loading"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    class="btn-primary"
                    :disabled="loading"
                  >
                    <LoadingSpinner v-if="loading" size="sm" class="mr-2" />
                    {{ isEditing ? 'Update Customer' : 'Create Customer' }}
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
import { customerApi } from '@/services/api'
import { useNotificationStore } from '@/stores/notifications'
import LoadingSpinner from './LoadingSpinner.vue'
import type { Customer } from '@/types'

interface Props {
  show: boolean
  customer?: Customer | null
}

const props = withDefaults(defineProps<Props>(), {
  customer: null
})

const emit = defineEmits<{
  close: []
  save: []
}>()

const notificationStore = useNotificationStore()

const loading = ref(false)
const errors = ref<Record<string, string>>({})
const sameAsBilling = ref(true)

const form = ref({
  name: '',
  email: '',
  phone: '',
  billing_address: '',
  shipping_address: ''
})

const isEditing = computed(() => !!props.customer)

const resetForm = () => {
  form.value = {
    name: '',
    email: '',
    phone: '',
    billing_address: '',
    shipping_address: ''
  }
  sameAsBilling.value = true
  errors.value = {}
}

const populateForm = (customer: Customer) => {
  form.value = {
    name: customer.name,
    email: customer.email,
    phone: customer.phone,
    billing_address: customer.billing_address || '',
    shipping_address: customer.shipping_address || ''
  }
  sameAsBilling.value = !customer.shipping_address || customer.shipping_address === customer.billing_address
}

const validateForm = () => {
  errors.value = {}
  let isValid = true

  if (!form.value.name.trim()) {
    errors.value.name = 'Customer name is required'
    isValid = false
  }

  if (!form.value.email.trim()) {
    errors.value.email = 'Email address is required'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    errors.value.email = 'Please enter a valid email address'
    isValid = false
  }

  if (!form.value.phone.trim()) {
    errors.value.phone = 'Phone number is required'
    isValid = false
  }

  return isValid
}

const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    loading.value = true

    const customerData = {
      ...form.value,
      shipping_address: sameAsBilling.value ? form.value.billing_address : form.value.shipping_address
    }

    if (isEditing.value && props.customer) {
      await customerApi.update(props.customer.id, customerData)
      notificationStore.success('Customer updated successfully')
    } else {
      await customerApi.create(customerData)
      notificationStore.success('Customer created successfully')
    }

    emit('save')
    resetForm()
  } catch (error: any) {
    const errorMessage = error.response?.data?.message || 'An unexpected error occurred'
    
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else {
      notificationStore.error(
        isEditing.value ? 'Failed to update customer' : 'Failed to create customer',
        errorMessage
      )
    }
  } finally {
    loading.value = false
  }
}

watch(() => props.show, (newValue) => {
  if (newValue) {
    if (props.customer) {
      populateForm(props.customer)
    } else {
      resetForm()
    }
  }
})

watch(sameAsBilling, (newValue) => {
  if (newValue) {
    form.value.shipping_address = form.value.billing_address
  }
})

watch(() => form.value.billing_address, (newValue) => {
  if (sameAsBilling.value) {
    form.value.shipping_address = newValue
  }
})
</script>