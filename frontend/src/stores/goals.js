import { defineStore } from 'pinia'
import { ref } from 'vue'
import { goalsApi } from '@/api/goals'

export const useGoalsStore = defineStore('goals', () => {
  const goals = ref([])
  const loading = ref(false)

  async function fetchGoals() {
    loading.value = true
    try {
      const { data } = await goalsApi.getAll()
      goals.value = data
    } finally {
      loading.value = false
    }
  }

  async function addGoal(payload) {
    await goalsApi.create(payload)
    await fetchGoals()
  }

  async function archiveGoal(id) {
    await goalsApi.update(id, { is_active: false })
    await fetchGoals()
  }

  async function removeGoal(id) {
    await goalsApi.remove(id)
    goals.value = goals.value.filter((g) => g.id !== id)
  }

  return { goals, loading, fetchGoals, addGoal, archiveGoal, removeGoal }
})
