<template>
  <div class="flex flex-col gap-6">
    <div class="flex justify-end">
      <Button label="Новая цель" icon="pi pi-plus" @click="showDialog = true" />
    </div>

    <div v-if="store.loading" class="flex justify-center py-12">
      <ProgressSpinner />
    </div>

    <div v-else-if="!store.goals.length" class="text-center py-12 text-gray-400">
      <i class="pi pi-flag text-4xl mb-3 block" />
      <p>Целей пока нет. Добавьте первую!</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="goal in store.goals"
        :key="goal.id"
        class="bg-white rounded-xl border border-gray-200 p-5 flex flex-col gap-3"
        :class="{ 'opacity-60': !goal.is_active }"
      >
        <div class="flex items-start justify-between gap-2">
          <div>
            <div class="font-semibold text-gray-800">{{ goal.type.name }}</div>
            <div class="text-sm text-gray-500 mt-0.5">
              Цель: {{ goal.target_value }} {{ goal.type.unit }}
            </div>
          </div>
          <div class="flex gap-1 shrink-0">
            <Button
              v-if="goal.is_active"
              icon="pi pi-pause"
              v-tooltip="'Архивировать'"
              severity="secondary"
              text
              size="small"
              @click="store.archiveGoal(goal.id)"
            />
            <Button
              icon="pi pi-trash"
              severity="danger"
              text
              size="small"
              @click="store.removeGoal(goal.id)"
            />
          </div>
        </div>

        <div v-if="goal.progress !== null" class="flex flex-col gap-1">
          <div class="flex justify-between text-xs text-gray-500">
            <span>Прогресс</span>
            <span>{{ Math.min(Math.max(goal.progress, 0), 100).toFixed(1) }}%</span>
          </div>
          <ProgressBar
            :value="Math.min(Math.max(goal.progress, 0), 100)"
            :show-value="false"
            class="h-2"
          />
        </div>

        <div class="flex justify-between text-xs text-gray-400">
          <span>{{ formatDate(goal.start_date) }}</span>
          <span>{{ formatDate(goal.end_date) }}</span>
        </div>

        <Tag v-if="!goal.is_active" value="Архив" severity="secondary" class="self-start" />
      </div>
    </div>

    <Dialog v-model:visible="showDialog" modal header="Новая цель" class="w-full max-w-md">
      <form @submit.prevent="handleAdd" class="flex flex-col gap-4 pt-2">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">Тип измерения</label>
          <Select
            v-model="form.type_id"
            :options="types"
            option-label="name"
            option-value="id"
            placeholder="Выберите тип"
            class="w-full"
          />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">Начальное значение</label>
          <InputNumber v-model="form.start_value" :min-fraction-digits="0" :max-fraction-digits="2" class="w-full" />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">Целевое значение</label>
          <InputNumber v-model="form.target_value" :min-fraction-digits="0" :max-fraction-digits="2" class="w-full" />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div class="flex flex-col gap-1">
            <label class="text-sm font-medium text-gray-700">Дата начала</label>
            <DatePicker v-model="form.start_date" class="w-full" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-sm font-medium text-gray-700">Дата окончания</label>
            <DatePicker v-model="form.end_date" class="w-full" />
          </div>
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">Заметка</label>
          <Textarea v-model="form.notes" rows="2" class="w-full" />
        </div>

        <div class="flex gap-3 justify-end pt-2">
          <Button label="Отмена" severity="secondary" text @click="closeDialog" />
          <Button type="submit" label="Сохранить" :loading="saving" />
        </div>
      </form>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useGoalsStore } from '@/stores/goals'
import { measurementsApi } from '@/api/measurements'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import Select from 'primevue/select'
import InputNumber from 'primevue/inputnumber'
import DatePicker from 'primevue/datepicker'
import Textarea from 'primevue/textarea'
import ProgressBar from 'primevue/progressbar'
import ProgressSpinner from 'primevue/progressspinner'
import Tag from 'primevue/tag'

const store = useGoalsStore()
const types = ref([])
const showDialog = ref(false)
const saving = ref(false)

const defaultForm = () => ({
  type_id: null,
  start_value: null,
  target_value: null,
  start_date: new Date(),
  end_date: null,
  notes: '',
})
const form = ref(defaultForm())

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

async function handleAdd() {
  if (!form.value.type_id || !form.value.target_value || !form.value.end_date) return
  saving.value = true
  try {
    await store.addGoal({
      ...form.value,
      start_date: form.value.start_date.toISOString().slice(0, 10),
      end_date: form.value.end_date.toISOString().slice(0, 10),
      notes: form.value.notes || null,
    })
    closeDialog()
  } finally {
    saving.value = false
  }
}

function closeDialog() {
  showDialog.value = false
  form.value = defaultForm()
}

onMounted(async () => {
  await store.fetchGoals()
  const { data } = await measurementsApi.getTypes()
  types.value = data
})
</script>
