import client from './client'

export const dashboardApi = {
  getSummary: () => client.get('/dashboard/summary'),
  getChart: (typeKey, days = 30) => client.get(`/dashboard/chart/${typeKey}`, { params: { days } }),
}
