import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('@/views/Dashboard.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/products',
      name: 'Products',
      component: () => import('@/views/Products.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/customers',
      name: 'Customers',
      component: () => import('@/views/Customers.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/sales-orders',
      name: 'SalesOrders',
      component: () => import('@/views/SalesOrders.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/sales-orders/new',
      name: 'NewSalesOrder',
      component: () => import('@/views/NewSalesOrder.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/sales-orders/:id',
      name: 'SalesOrderDetail',
      component: () => import('@/views/SalesOrderDetail.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresGuest: true }
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/')
    return
  }
  
  next()
})

export default router