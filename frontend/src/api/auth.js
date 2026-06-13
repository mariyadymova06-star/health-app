import client from './client'

export const authApi = {
  login: (email, password) => client.post('/auth/login', { email, password }),
  register: (email, password) => client.post('/auth/register', { email, password }),
  me: () => client.get('/auth/me'),
  refresh: (refresh_token) => client.post('/auth/refresh', { refresh_token }),
}
