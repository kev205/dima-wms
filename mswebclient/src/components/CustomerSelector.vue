<template>
  <div class="relative">
    <Combobox v-model="selectedCustomer" @update:model-value="$emit('update:modelValue', $event)">
      <div class="relative">
        <ComboboxInput
          class="input-field pr-10"
          :display-value="(customer) => (customer as Customer)?.name || ''"
          @change="handleSearch($event.target.value)"
          placeholder="Search customers..."
        />
        <ComboboxButton class="absolute inset-y-0 right-0 flex items-center pr-3">
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" />
        </ComboboxButton>
      </div>

      <TransitionRoot
        leave="transition ease-in duration-100"
        leave-from="opacity-100"
        leave-to="opacity-0"
        @after-leave="query = ''"
      >
        <ComboboxOptions class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
          <div v-if="loading" class="px-4 py-2 text-gray-500">
            <LoadingSpinner size="sm" text="Searching..." />
          </div>
          
          <div v-else-if="filteredCustomers.length === 0 && query !== ''" class="px-4 py-2 text-gray-500">
            No customers found.
          </div>
          
          <ComboboxOption
            v-for="customer in filteredCustomers"
            :key="customer.id"
            :value="customer"
            v-slot="{ selected, active }"
          >
            <li
              :class="[
                'relative cursor-pointer select-none py-2 pl-3 pr-9',
                active ? 'bg-primary-600 text-white' : 'text-gray-900'
              ]"
            >
              <div class="flex items-center">
                <div class="flex-1">
                  <span :class="['block truncate', selected ? 'font-semibold' : 'font-normal']">
                    {{ customer.name }}
                  </span>
                  <span :class="['block text-sm truncate', active ? 'text-primary-200' : 'text-gray-500']">
                    {{ customer.email }}
                  </span>
                </div>
              </div>
              
              <span
                v-if="selected"
                :class="[
                  'absolute inset-y-0 right-0 flex items-center pr-4',
                  active ? 'text-white' : 'text-primary-600'
                ]"
              >
                <CheckIcon class="h-5 w-5" />
              </span>
            </li>
          </ComboboxOption>
        </ComboboxOptions>
      </TransitionRoot>
    </Combobox>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import {
  Combobox,
  ComboboxInput,
  ComboboxOptions,
  ComboboxOption,
  ComboboxButton,
  TransitionRoot
} from '@headlessui/vue'
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid'
import { customerApi } from '@/services/api'
import LoadingSpinner from './LoadingSpinner.vue'
import { debounce } from 'lodash-es'
import type { Customer } from '@/types'

interface Props {
  modelValue?: Customer | null
  initialCustomerId?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  initialCustomerId: undefined
})

const emit = defineEmits<{
  'update:modelValue': [customer: Customer | null]
}>()

const customers = ref<Customer[]>([])
const loading = ref(false)
const query = ref('')
const selectedCustomer = ref<Customer | null>(props.modelValue)

const filteredCustomers = computed(() => {
  if (query.value === '') {
    return customers.value.slice(0, 10) // Show first 10 when no search
  }
  
  return customers.value.filter((customer) =>
    customer.name.toLowerCase().includes(query.value.toLowerCase()) ||
    customer.email.toLowerCase().includes(query.value.toLowerCase())
  )
})

const loadCustomers = async (search?: string) => {
  try {
    loading.value = true
    const response = await customerApi.getAll({ search })
    customers.value = response.data.results
  } catch (error) {
    console.error('Failed to load customers:', error)
  } finally {
    loading.value = false
  }
}

const debouncedLoad = debounce(loadCustomers, 300)

const handleSearch = (searchQuery: string) => {
  query.value = searchQuery
  if (searchQuery.length > 0) {
    debouncedLoad(searchQuery)
  }
}

const loadInitialCustomer = async () => {
  if (props.initialCustomerId) {
    try {
      const response = await customerApi.getById(props.initialCustomerId)
      selectedCustomer.value = response.data.data
      emit('update:modelValue', response.data.data)
    } catch (error) {
      console.error('Failed to load initial customer:', error)
    }
  }
}

watch(() => props.modelValue, (newValue) => {
  selectedCustomer.value = newValue
})

onMounted(() => {
  loadCustomers()
  loadInitialCustomer()
})
</script>