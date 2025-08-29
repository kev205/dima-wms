<template>
  <div id="app">
    <template v-if="authStore.isAuthenticated">
      <router-view />
    </template>
    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  if (authStore.token) {
    await authStore.verifyToken()
  }
})
</script>