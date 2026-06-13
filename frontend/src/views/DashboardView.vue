<template>
  <div class="flex flex-col gap-6">
    <div v-if="store.loading" class="flex justify-center py-12">
      <ProgressSpinner />
    </div>

    <template v-else-if="store.summary">
      <div v-if="store.summary.bmi" class="bg-blue-50 border border-blue-200 rounded-xl px-6 py-4 flex items-center gap-4">
        <div class="text-3xl font-bold text-blue-700">{{ store.summary.bmi }}</div>
        <div>
          <div class="font-medium text-blue-800">Индекс массы тела (ИМТ)</div>
          <div class="text-sm text-blue-600">{{ bmiLabel(store.summary.bmi) }}</div>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div
          v-for="metric in store.summary.metrics"
          :key="metric.type_key"
          class="bg-white rounded-xl border border-gray-200 p-5 flex flex-col gap-2"
        >
          <div class="text-xs font-medium text-gray-500 uppercase tracking-wide">{{ metric.name }}</div>
          <div class="flex items-end gap-1">
            <span class="text-2xl font-bold text-gray-800">
              {{ metric.value }}
              <template v-if="metric.secondary_value"> / {{ metric.secondary_value }}</template>
            </span>
            <span class="text-sm text-gray-400 mb-0.5">{{ metric.unit }}</span>
          </div>
          <div class="text-xs text-gray-400">{{ formatDate(metric.measured_at) }}</div>
        </div>
      </div>

      <div v-if="chart" class="bg-white rounded-xl border border-gray-200 p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-semibold text-gray-800">{{ chart.name }}, {{ chart.unit }}</h3>
          <div class="flex gap-2">
            <button
              v-for="d in dayOptions"
              :key="d"
              @click="loadChart(d)"
              class="px-3 py-1 text-sm rounded-lg transition-colors"
              :class="activeDays === d ? 'bg-primary-100 text-primary-700 font-medium' : 'text-gray-500 hover:bg-gray-100'"
            >
              {{ d }} дн.
            </button>
          </div>
        </div>
        <apexchart
          type="bar"
          height="260"
          :options="chartOptions"
          :series="chartSeries"
        />
      </div>

      <div v-if="!store.summary.metrics.length" class="text-center py-12 text-gray-400">
        <i class="pi pi-heart text-4xl mb-3 block" />
        <p>Нет данных. Добавьте первое измерение.</p>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import ProgressSpinner from 'primevue/progressspinner'

const store = useDashboardStore()
const activeDays = ref(30)
const dayOptions = [7, 30, 90]

const chart = computed(() => store.chart)

const chartOptions = computed(() => ({
  chart: { toolbar: { show: false }, fontFamily: 'inherit' },
  xaxis: {
    categories: chart.value?.points.map(p => formatDate(p.measured_at)) ?? [],
    labels: { style: { fontSize: '11px' } },
  },
  yaxis: { labels: { style: { fontSize: '11px' } } },
  colors: ['#6366f1'],
  plotOptions: { bar: { borderRadius: 4 } },
  dataLabels: { enabled: false },
  grid: { borderColor: '#f1f5f9' },
}))

const chartSeries = computed(() => [
  { name: chart.value?.name ?? '', data: chart.value?.points.map(p => p.value) ?? [] },
])

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' })
}

function bmiLabel(bmi) {
  if (bmi < 18.5) return 'Недостаточный вес'
  if (bmi < 25) return 'Норма'
  if (bmi < 30) return 'Избыточный вес'
  return 'Ожирение'
}

async function loadChart(days) {
  activeDays.value = days
  await store.fetchChart('weight', days)
}

onMounted(async () => {
  await store.fetchSummary()
  if (store.summary?.metrics.some(m => m.type_key === 'weight')) {
    await loadChart(30)
  }
})
</script>
