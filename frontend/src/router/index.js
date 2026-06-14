import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { public: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { public: true },
  },
  {
    path: '/',
    component: () => import('@/components/AppLayout.vue'),
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/DashboardView.vue'),
      },
      {
        path: 'measurements',
        name: 'Measurements',
        component: () => import('@/views/MeasurementsView.vue'),
      },
      {
        path: 'measurements/:typeKey',
        name: 'MeasurementDetail',
        component: () => import('@/views/MeasurementDetailView.vue'),
      },
      {
        path: 'goals',
        name: 'Goals',
        component: () => import('@/views/GoalsView.vue'),
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/ProfileView.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const isAuthenticated = !!localStorage.getItem('access_token')
  if (!to.meta.public && !isAuthenticated) return { name: 'Login' }
  if (to.meta.public && isAuthenticated) return { name: 'Dashboard' }
})

export default router
