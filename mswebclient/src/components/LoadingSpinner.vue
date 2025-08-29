<template>
  <div v-if="show" class="flex items-center justify-center" :class="containerClass">
    <div
      class="animate-spin rounded-full border-2 border-gray-300"
      :class="[
        sizeClasses[size],
        `border-t-${color}-600`
      ]"
    ></div>
    <span v-if="text" class="ml-3 text-gray-600" :class="textSizeClasses[size]">
      {{ text }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  show?: boolean
  size?: 'sm' | 'md' | 'lg'
  color?: string
  text?: string
  containerClass?: string
}

const props = withDefaults(defineProps<Props>(), {
  show: true,
  size: 'md',
  color: 'primary',
  text: '',
  containerClass: 'py-8'
})

const sizeClasses = {
  sm: 'h-4 w-4',
  md: 'h-8 w-8',
  lg: 'h-12 w-12'
}

const textSizeClasses = {
  sm: 'text-sm',
  md: 'text-base',
  lg: 'text-lg'
}
</script>