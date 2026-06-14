<template>
  <div class="flex flex-col gap-6">
    <div class="flex items-center gap-4">
      <button
        @click="router.push('/')"
        class="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-800 transition-colors"
      >
        <i class="pi pi-arrow-left text-xs" />
        На дашборд
      </button>
      <span class="text-gray-300">|</span>
      <span class="text-sm font-medium text-gray-700">{{ typeName }}</span>
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
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMeasurementsStore } from '@/stores/measurements'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

const route = useRoute()
const router = useRouter()
const store = useMeasurementsStore()

const typeName = computed(() => {
  const t = store.types.find(t => t.key === route.params.typeKey)
  return t?.name ?? route.params.typeKey
})

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

onMounted(async () => {
  if (!store.types.length) await store.fetchTypes()
  await store.fetchMeasurements({ type_key: route.params.typeKey })
})
</script>
