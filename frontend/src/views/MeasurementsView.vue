<template>
  <div class="flex flex-col gap-6">
    <div class="flex items-center justify-between">
      <Select
        v-model="selectedType"
        :options="typeOptions"
        option-label="label"
        option-value="value"
        placeholder="Все типы"
        class="w-56"
        @change="onTypeChange"
      />
      <Button label="Добавить" icon="pi pi-plus" @click="showDialog = true" />
    </div>

    <div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <DataTable
        :value="store.measurements"
        :loading="store.loading"
        striped-rows
        size="small"
      >
        <template #empty>
          <div class="text-center py-8 text-gray-400">Нет измерений</div>
        </template>

        <Column field="measured_at" header="Дата">
          <template #body="{ data }">
            {{ formatDate(data.measured_at) }}
          </template>
        </Column>

        <Column field="type.name" header="Тип" />

        <Column header="Значение">
          <template #body="{ data }">
            {{ formatValue(data.value, data.type.key) }}
            <template v-if="data.secondary_value"> / {{ data.secondary_value }}</template>
            {{ data.type.unit }}
          </template>
        </Column>

        <Column field="notes" header="Заметка">
          <template #body="{ data }">
            <span class="text-gray-500 text-sm">{{ data.notes ?? '—' }}</span>
          </template>
        </Column>

        <Column header="" style="width: 48px">
          <template #body="{ data }">
            <Button
              icon="pi pi-trash"
              severity="danger"
              text
              size="small"
              @click="handleDelete(data.id)"
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <Dialog v-model:visible="showDialog" modal header="Новое измерение" class="w-full max-w-md">
      <form @submit.prevent="handleAdd" class="flex flex-col gap-4 pt-2">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">Тип измерения</label>
          <Select
            v-model="form.type_id"
            :options="store.types"
            option-label="name"
            option-value="id"
            placeholder="Выберите тип"
            class="w-full"
          />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">Значение</label>
          <InputNumber v-model="form.value" :min-fraction-digits="0" :max-fraction-digits="2" class="w-full" />
        </div>

        <div v-if="selectedTypeObj?.has_secondary" class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">
            Второе значение ({{ selectedTypeObj.secondary_unit }})
          </label>
          <InputNumber v-model="form.secondary_value" :min-fraction-digits="0" :max-fraction-digits="2" class="w-full" />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-gray-700">Дата и время</label>
          <DatePicker v-model="form.measured_at" show-time hour-format="24" class="w-full" />
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
import { ref, computed, onMounted } from 'vue'
import { useMeasurementsStore } from '@/stores/measurements'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Select from 'primevue/select'
import InputNumber from 'primevue/inputnumber'
import Textarea from 'primevue/textarea'
import DatePicker from 'primevue/datepicker'
import Dialog from 'primevue/dialog'

const store = useMeasurementsStore()

const showDialog = ref(false)
const saving = ref(false)
const selectedType = ref(null)

const defaultForm = () => ({
  type_id: null,
  value: null,
  secondary_value: null,
  measured_at: new Date(),
  notes: '',
})
const form = ref(defaultForm())

const typeOptions = computed(() => [
  { label: 'Все типы', value: null },
  ...store.types.map((t) => ({ label: t.name, value: t.key })),
])

const selectedTypeObj = computed(() =>
  store.types.find((t) => t.id === form.value.type_id) ?? null
)

function formatDate(iso) {
  return new Date(iso).toLocaleString('ru-RU', {
    day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit',
  })
}

function formatValue(value, typeKey) {
  if (typeKey === 'steps') return Math.round(value).toLocaleString('ru-RU')
  if (typeKey === 'temperature') return Number(value).toFixed(1)
  return value
}

async function onTypeChange() {
  await store.fetchMeasurements(selectedType.value ? { type_key: selectedType.value } : {})
}

async function handleAdd() {
  if (!form.value.type_id || form.value.value === null) return
  saving.value = true
  try {
    await store.addMeasurement({
      ...form.value,
      measured_at: form.value.measured_at.toISOString(),
      notes: form.value.notes || null,
      secondary_value: form.value.secondary_value ?? null,
    })
    closeDialog()
  } finally {
    saving.value = false
  }
}

async function handleDelete(id) {
  await store.removeMeasurement(id)
}

function closeDialog() {
  showDialog.value = false
  form.value = defaultForm()
}

onMounted(async () => {
  await store.fetchTypes()
  await store.fetchMeasurements()
})
</script>
