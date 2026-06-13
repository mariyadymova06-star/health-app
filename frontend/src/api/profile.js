import client from './client'

export const profileApi = {
  get: () => client.get('/profile'),
  update: (data) => client.patch('/profile', data),
}
