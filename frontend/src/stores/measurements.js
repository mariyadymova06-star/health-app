import { defineStore } from 'pinia'
import { ref } from 'vue'
import { measurementsApi } from '@/api/measurements'

export const useMeasurementsStore = defineStore('measurements', () => {
  const measurements = ref([])
  const types = ref([])
  const loading = ref(false)

  async function fetchTypes() {
    const { data } = await measurementsApi.getTypes()
    types.value = data
  }

  async function fetchMeasurements(params = {}) {
    loading.value = true
    try {
      const { data } = await measurementsApi.getAll(params)
      measurements.value = data
    } finally {
      loading.value = false
    }
  }

  async function addMeasurement(payload) {
    await measurementsApi.create(payload)
    await fetchMeasurements()
  }

  async function removeMeasurement(id) {
    await measurementsApi.remove(id)
    measurements.value = measurements.value.filter((m) => m.id !== id)
  }

  return { measurements, types, loading, fetchTypes, fetchMeasurements, addMeasurement, removeMeasurement }
})
