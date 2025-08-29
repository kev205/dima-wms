export interface Product {
  id: string
  name: string
  product_category: string
  internal_reference: string
  product_type: string
  sales_price: number
  cost: number
  quantity_on_hand: number
  availables: number
  reserved: number
  available: boolean
  description?: string
  created_at: string
  updated_at: string
}

export interface Customer {
  id: string
  name: string
  email: string
  phone: string
  billing_address?: string
  shipping_address?: string
  created_at: string
  updated_at: string
}

export interface SalesOrder {
  id: string
  number: string
  customer: Customer
  status: 'DRAFT' | 'CONFIRMED' | 'CANCELLED'
  notes?: string
  vat_rate:  number
  sub_total:  number
  order_total:  number
  created_at: string
  updated_at: string
  lines: SalesOrderLine[]
}

export interface SalesOrderLine {
  id: string
  order_id: string
  product: Product
  qty: number
  unit_price: number
  discount_pct: number
  sub_total: number
}

export interface CreateSalesOrderRequest {
  customer_id: string
  notes?: string
  lines: {
    product_id: string
    qty: number
    discount_pct?: number
  }[]
}

export interface Reservation {
  id: string
  order_id: string
  product_id: string
  qty: number
  created_at: string
}

export interface ApiResponse<T> {
  data: T
  message?: string
  status: 'success' | 'error'
}

export interface PaginatedResponse<T> {
  data: T[]
  results: T[]
  total: number
  count: number
  page: number
  page_size: number
  total_pages: number
}