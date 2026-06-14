<template>
  <div class="min-h-screen flex">
    <div class="hidden lg:flex lg:w-5/12 bg-gradient-to-br from-green-600 to-emerald-800 flex-col justify-between p-12 text-white">
      <div class="flex items-center gap-3">
        <img src="@/assets/health-icon.png" alt="logo" class="w-10 h-10 rounded-xl" />
        <span class="text-lg font-bold tracking-tight">HealthTrack</span>
      </div>

      <div>
        <h2 class="text-3xl font-bold leading-snug mb-3">
          Следите за здоровьем<br>каждый день
        </h2>
        <p class="text-green-100 leading-relaxed">
          Измерения, цели, статистика — всё в одном месте.
        </p>
      </div>

      <div class="flex flex-col gap-3">
        <div class="flex items-center gap-3 text-sm text-green-100">
          <i class="pi pi-chart-line w-4 text-center shrink-0" />
          Отслеживайте 8 видов показателей
        </div>
        <div class="flex items-center gap-3 text-sm text-green-100">
          <i class="pi pi-flag w-4 text-center shrink-0" />
          Ставьте цели и контролируйте прогресс
        </div>
        <div class="flex items-center gap-3 text-sm text-green-100">
          <i class="pi pi-history w-4 text-center shrink-0" />
          История с графиками за любой период
        </div>
      </div>
    </div>

    <div class="flex-1 flex items-center justify-center bg-white px-8 py-12">
      <div class="w-full max-w-sm">
        <div class="flex lg:hidden items-center gap-2 mb-10">
          <img src="@/assets/health-icon.png" alt="logo" class="w-8 h-8 rounded-lg" />
          <span class="font-bold text-gray-800">HealthTrack</span>
        </div>

        <h1 class="text-2xl font-bold text-gray-900 mb-1">Добро пожаловать</h1>
        <p class="text-gray-500 text-sm mb-8">Войдите в свой аккаунт</p>

        <form @submit.prevent="handleLogin" class="flex flex-col gap-5">
          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-gray-700">Email</label>
            <InputText
              v-model="email"
              type="email"
              placeholder="example@mail.com"
              class="w-full"
              :invalid="!!error"
            />
          </div>

          <div class="flex flex-col gap-1.5">
            <label class="text-sm font-medium text-gray-700">Пароль</label>
            <Password
              v-model="password"
              placeholder="Введите пароль"
              :feedback="false"
              toggleMask
              class="w-full"
              inputClass="w-full"
              :invalid="!!error"
            />
          </div>

          <Message v-if="error" severity="error" :closable="false">{{ error }}</Message>

          <Button
            type="submit"
            label="Войти"
            :loading="loading"
            class="w-full"
          />

          <p class="text-center text-sm text-gray-500">
            Нет аккаунта?
            <RouterLink to="/register" class="text-green-600 font-medium hover:underline">
              Зарегистрироваться
            </RouterLink>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Message from 'primevue/message'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await authStore.login(email.value, password.value)
    router.push('/')
  } catch {
    error.value = 'Неверный email или пароль'
  } finally {
    loading.value = false
  }
}
</script>
