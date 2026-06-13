import { defineStore } from 'pinia'
import { ref } from 'vue'
import { profileApi } from '@/api/profile'

export const useProfileStore = defineStore('profile', () => {
  const profile = ref(null)
  const loading = ref(false)

  async function fetchProfile() {
    loading.value = true
    try {
      const { data } = await profileApi.get()
      profile.value = data
    } finally {
      loading.value = false
    }
  }

  async function updateProfile(payload) {
    const { data } = await profileApi.update(payload)
    profile.value = data
  }

  return { profile, loading, fetchProfile, updateProfile }
})
