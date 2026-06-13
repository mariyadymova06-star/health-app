<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="w-full max-w-md px-4">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800">Мониторинг здоровья</h1>
        <p class="text-gray-500 mt-2">Войдите в свой аккаунт</p>
      </div>

      <Card>
        <template #content>
          <form @submit.prevent="handleLogin" class="flex flex-col gap-5">
            <div class="flex flex-col gap-1">
              <label class="text-sm font-medium text-gray-700">Email</label>
              <InputText
                v-model="email"
                type="email"
                placeholder="example@mail.com"
                class="w-full"
                :invalid="!!error"
              />
            </div>

            <div class="flex flex-col gap-1">
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
              <RouterLink to="/register" class="text-primary-600 font-medium hover:underline">
                Зарегистрироваться
              </RouterLink>
            </p>
          </form>
        </template>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Card from 'primevue/card'
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
