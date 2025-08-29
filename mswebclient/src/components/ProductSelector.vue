<template>
  <div class="relative">
    <Combobox v-model="selectedProduct" @update:model-value="$emit('update:modelValue', $event)">
      <div class="relative">
        <ComboboxInput
          class="input-field pr-10"
          :display-value="(product) => (product as Product)?.name || ''"
          @change="handleSearch($event.target.value)"
          placeholder="Search products..."
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
          
          <div v-else-if="filteredProducts.length === 0 && query !== ''" class="px-4 py-2 text-gray-500">
            No products found.
          </div>
          
          <ComboboxOption
            v-for="product in filteredProducts"
            :key="product.id"
            :value="product"
            v-slot="{ selected, active }"
          >
            <li
              :class="[
                'relative cursor-pointer select-none py-2 pl-3 pr-9',
                active ? 'bg-primary-600 text-white' : 'text-gray-900'
              ]"
            >
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <span :class="['block truncate', selected ? 'font-semibold' : 'font-normal']">
                    {{ product.name }}
                  </span>
                  <div class="flex items-center space-x-2 text-sm">
                    <span :class="active ? 'text-primary-200' : 'text-gray-500'">
                      ${{ product.sales_price }}
                    </span>
                  </div>
                </div>
                <div class="flex flex-col items-end text-xs">
                  <span
                    :class="[
                      'px-2 py-1 rounded-full text-xs font-medium',
                      product.availables > 0
                        ? (active ? 'bg-green-200 text-green-800' : 'bg-green-100 text-green-800')
                        : (active ? 'bg-red-200 text-red-800' : 'bg-red-100 text-red-800')
                    ]"
                  >
                    {{ product.availables }} available
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
import { productApi } from '@/services/api'
import LoadingSpinner from './LoadingSpinner.vue'
import { debounce } from 'lodash-es'
import type { Product } from '@/types'

interface Props {
  modelValue?: Product | null
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null
})

const emit = defineEmits<{
  'update:modelValue': [product: Product | null]
}>()

const products = ref<Product[]>([])
const loading = ref(false)
const query = ref('')
const selectedProduct = ref<Product | null>(props.modelValue)

const filteredProducts = computed(() => {
  if (query.value === '') {
    return products.value.slice(0, 10) // Show first 10 when no search
  }
  
  return products.value.filter((product) =>
    product.name.toLowerCase().includes(query.value.toLowerCase()) ||
    product.product_category.toLowerCase().includes(query.value.toLowerCase()) ||
    product.product_type?.toLowerCase().includes(query.value.toLowerCase()) ||
    product.internal_reference?.toLowerCase().includes(query.value.toLowerCase())
  )
})

const loadProducts = async (search?: string) => {
  try {
    loading.value = true
    const response = await productApi.getAll({ search })
    products.value = response.data.results
  } catch (error) {
    console.error('Failed to load products:', error)
  } finally {
    loading.value = false
  }
}

const debouncedLoad = debounce(loadProducts, 300)

const handleSearch = (searchQuery: string) => {
  query.value = searchQuery
  if (searchQuery.length > 0) {
    debouncedLoad(searchQuery)
  }
}

watch(() => props.modelValue, (newValue) => {
  selectedProduct.value = newValue
})

onMounted(() => {
  loadProducts()
})
</script>