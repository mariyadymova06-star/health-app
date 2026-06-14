<template>
  <RouterView />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(() => {
  if (localStorage.getItem('access_token') && !authStore.user) {
    authStore.fetchMe()
  }
})
</script>
