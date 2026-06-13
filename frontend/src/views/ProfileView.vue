<template>
  <div class="max-w-lg">
    <div v-if="store.loading" class="flex justify-center py-12">
      <ProgressSpinner />
    </div>

    <form v-else @submit.prevent="handleSave" class="bg-white rounded-xl border border-gray-200 p-6 flex flex-col gap-5">
      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700">Email</label>
        <InputText :value="authStore.user?.email" disabled class="w-full" />
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700">Имя</label>
        <InputText v-model="form.name" placeholder="Ваше имя" class="w-full" />
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700">Пол</label>
        <Select
          v-model="form.gender"
          :options="genderOptions"
          option-label="label"
          option-value="value"
          placeholder="Не указан"
          class="w-full"
        />
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700">Дата рождения</label>
        <DatePicker v-model="form.birth_date" class="w-full" date-format="dd.mm.yy" />
      </div>

      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium text-gray-700">Рост (см)</label>
        <InputNumber
          v-model="form.height_cm"
          :min="50"
          :max="250"
          :min-fraction-digits="0"
          :max-fraction-digits="1"
          placeholder="175"
          class="w-full"
        />
      </div>

      <div class="flex items-center gap-3 pt-2">
        <Button type="submit" label="Сохранить" :loading="saving" />
        <span v-if="saved" class="text-sm text-green-600 flex items-center gap-1">
          <i class="pi pi-check" /> Сохранено
        </span>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useProfileStore } from '@/stores/profile'
import { useAuthStore } from '@/stores/auth'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Select from 'primevue/select'
import DatePicker from 'primevue/datepicker'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'

const store = useProfileStore()
const authStore = useAuthStore()

const saving = ref(false)
const saved = ref(false)

const genderOptions = [
  { label: 'Мужской', value: 'male' },
  { label: 'Женский', value: 'female' },
  { label: 'Другой', value: 'other' },
]

const form = ref({ name: '', gender: null, birth_date: null, height_cm: null })

async function handleSave() {
  saving.value = true
  saved.value = false
  try {
    await store.updateProfile({
      name: form.value.name || null,
      gender: form.value.gender || null,
      birth_date: form.value.birth_date
        ? new Date(form.value.birth_date).toISOString().slice(0, 10)
        : null,
      height_cm: form.value.height_cm || null,
    })
    saved.value = true
    setTimeout(() => (saved.value = false), 3000)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  await store.fetchProfile()
  if (store.profile) {
    form.value = {
      name: store.profile.name ?? '',
      gender: store.profile.gender ?? null,
      birth_date: store.profile.birth_date ? new Date(store.profile.birth_date) : null,
      height_cm: store.profile.height_cm ?? null,
    }
  }
})
</script>
