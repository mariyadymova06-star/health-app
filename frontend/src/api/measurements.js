import client from './client'

export const measurementsApi = {
  getTypes: () => client.get('/measurement-types'),
  getAll: (params = {}) => client.get('/measurements', { params }),
  create: (data) => client.post('/measurements', data),
  remove: (id) => client.delete(`/measurements/${id}`),
}
