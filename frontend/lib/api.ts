import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Product API
export const productApi = {
  getAll: async (params?: { category_id?: number; search?: string }) => {
    const { data } = await api.get('/shop/products', { params })
    return data
  },
  getBySlug: async (slug: string) => {
    const { data } = await api.get(`/shop/products/${slug}`)
    return data
  },
}

export default api
