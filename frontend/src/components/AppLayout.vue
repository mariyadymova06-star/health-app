<template>
  <div class="flex min-h-screen bg-gray-50">
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col fixed h-full">
      <div class="px-6 py-5 border-b border-gray-200">
        <h1 class="text-lg font-bold text-gray-800">Мониторинг здоровья</h1>
        <p v-if="authStore.user" class="text-xs text-gray-500 mt-1 truncate">
          {{ authStore.user.email }}
        </p>
      </div>

      <nav class="flex-1 px-3 py-4 flex flex-col gap-1">
        <RouterLink
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="isActive(item.to)
            ? 'bg-primary-50 text-primary-700'
            : 'text-gray-600 hover:bg-gray-100 hover:text-gray-900'"
        >
          <i :class="item.icon" class="text-base w-5 text-center" />
          {{ item.label }}
        </RouterLink>
      </nav>

      <div class="px-3 py-4 border-t border-gray-200">
        <button
          @click="handleLogout"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-gray-600 hover:bg-red-50 hover:text-red-600 transition-colors w-full"
        >
          <i class="pi pi-sign-out text-base w-5 text-center" />
          Выйти
        </button>
      </div>
    </aside>

    <main class="ml-64 flex-1 flex flex-col">
      <header class="bg-white border-b border-gray-200 px-8 py-4 sticky top-0 z-10">
        <h2 class="text-lg font-semibold text-gray-800">{{ currentTitle }}</h2>
      </header>

      <div class="flex-1 p-8">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const navItems = [
  { to: '/', label: 'Дашборд', icon: 'pi pi-chart-bar' },
  { to: '/measurements', label: 'Измерения', icon: 'pi pi-list' },
  { to: '/goals', label: 'Цели', icon: 'pi pi-flag' },
  { to: '/profile', label: 'Профиль', icon: 'pi pi-user' },
]

const titles = {
  '/': 'Дашборд',
  '/measurements': 'Измерения',
  '/goals': 'Цели',
  '/profile': 'Профиль',
}

const currentTitle = computed(() => titles[route.path] ?? '')

function isActive(to) {
  return to === '/' ? route.path === '/' : route.path.startsWith(to)
}

async function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
