import { defineStore } from 'pinia'
import { ref } from 'vue'
import { dashboardApi } from '@/api/dashboard'

export const useDashboardStore = defineStore('dashboard', () => {
  const summary = ref(null)
  const chart = ref(null)
  const loading = ref(false)

  async function fetchSummary() {
    loading.value = true
    try {
      const { data } = await dashboardApi.getSummary()
      summary.value = data
    } finally {
      loading.value = false
    }
  }

  async function fetchChart(typeKey, days = 30) {
    const { data } = await dashboardApi.getChart(typeKey, days)
    chart.value = data
  }

  return { summary, chart, loading, fetchSummary, fetchChart }
})
