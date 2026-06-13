import client from './client'

export const goalsApi = {
  getAll: () => client.get('/goals'),
  create: (data) => client.post('/goals', data),
  update: (id, data) => client.patch(`/goals/${id}`, data),
  remove: (id) => client.delete(`/goals/${id}`),
}
