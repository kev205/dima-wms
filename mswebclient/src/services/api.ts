import axios from 'axios'
import type {
  Product,
  Customer,
  SalesOrder,
  CreateSalesOrderRequest,
  ApiResponse,
  PaginatedResponse
} from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const productApi = {
  getAll: (params?: { page?: number; search?: string }) =>
    api.get<PaginatedResponse<Product>>('/products/', { params }),

  getById: (id: string) => api.get<ApiResponse<Product>>(`/products/${id}/`),

  create: (data: Omit<Product, 'id' | 'created_at' | 'updated_at' | 'available' | 'reserved'>) =>
    api.post<ApiResponse<Product>>('/products/', data),

  update: (id: string, data: Partial<Product>) =>
    api.put<ApiResponse<Product>>(`/products/${id}/`, data),

  delete: (id: string) => api.delete(`/products/${id}/`)
}

export const customerApi = {
  getAll: (params?: { page?: number; search?: string }) =>
    api.get<PaginatedResponse<Customer>>('/sales/customers/', { params }),

  getById: (id: string) => api.get<ApiResponse<Customer>>(`/sales/customers/${id}/`),

  create: (data: Omit<Customer, 'id' | 'created_at' | 'updated_at'>) =>
    api.post<ApiResponse<Customer>>('/sales/customers/', data),

  update: (id: string, data: Partial<Customer>) =>
    api.put<ApiResponse<Customer>>(`/sales/customers/${id}/`, data),

  delete: (id: string) => api.delete(`/sales/customers/${id}/`)
}

export const salesOrderApi = {
  getAll: (params?: { page?: number; status?: string }) =>
    api.get<PaginatedResponse<SalesOrder>>('/sales/orders/', { params }),

  getById: (id: string) => api.get<ApiResponse<SalesOrder>>(`/sales/orders/${id}/`),

  create: (data: CreateSalesOrderRequest) =>
    api.post<ApiResponse<SalesOrder>>('/sales/orders/', data),

  update: (id: string, data: Partial<SalesOrder>) =>
    api.put<ApiResponse<SalesOrder>>(`/sales/orders/${id}/`, data),

  confirm: (id: string) => api.post<ApiResponse<SalesOrder>>(`/sales/orders/${id}/confirm/`),

  cancel: (id: string) => api.post<ApiResponse<SalesOrder>>(`/sales/orders/${id}/cancel/`),

  delete: (id: string) => api.delete(`/sales/orders/${id}/`)
}

export const authApi = {
  login: (email: string, password: string) =>
    api.post<{ access: string; refresh: string; user: any }>('/token/', {
      username: email,
      password
    }),

  logout: () => api.post('/logout/'),

  verify: () => api.get('/token/refresh/')
}

export default api
