import axios from 'axios'
import type { Listing, ListingsItem, Me, RecognizeSuccess } from '../types/api'

const baseURL = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

export const api = axios.create({
  baseURL,
  timeout: 30_000
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('recycle_ai_token')
  if (token) {
    config.headers = config.headers ?? {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export async function recognizeImage(file: File): Promise<RecognizeSuccess> {
  const form = new FormData()
  form.append('file', file)

  const res = await api.post<RecognizeSuccess>('/api/recognize', form, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
  return res.data
}

export async function apiRegister(payload: {
  username: string
  password: string
  display_name?: string
}): Promise<{ access_token: string; token_type: string }> {
  const res = await api.post('/api/auth/register', payload)
  return res.data
}

export async function apiLogin(payload: {
  username: string
  password: string
}): Promise<{ access_token: string; token_type: string }> {
  const res = await api.post('/api/auth/login', payload)
  return res.data
}

export async function apiMe(): Promise<Me> {
  const res = await api.get('/api/me')
  return res.data
}

export async function apiUpdateMe(payload: { display_name: string }): Promise<{ ok: true }> {
  const res = await api.patch('/api/me', payload)
  return res.data
}

export async function apiHistory(): Promise<{
  recognitions: Array<{ id: number; item: string; price: number; currency: string; created_at: string }>
  purchases: Array<{ id: number; listing_id: number; price: number; currency: string; created_at: string }>
  sales: Array<{ id: number; listing_id: number; price: number; currency: string; created_at: string }>
  my_listings: ListingsItem[]
}> {
  const res = await api.get('/api/history')
  return res.data
}

export async function apiListListings(includeSold = false): Promise<ListingsItem[]> {
  const res = await api.get('/api/listings', { params: { include_sold: includeSold } })
  return res.data
}

export async function apiGetListing(id: number): Promise<Listing> {
  const res = await api.get(`/api/listings/${id}`)
  return res.data
}

export async function apiCreateListing(payload: {
  file: File
  description: string
  price?: number | null
}): Promise<ListingsItem> {
  const form = new FormData()
  form.append('file', payload.file)
  form.append('description', payload.description ?? '')
  if (payload.price !== undefined && payload.price !== null) form.append('price', String(payload.price))
  const res = await api.post('/api/listings', form, { headers: { 'Content-Type': 'multipart/form-data' } })
  return res.data
}

export async function apiPurchase(listingId: number): Promise<{ order_id: number }> {
  const res = await api.post(`/api/listings/${listingId}/purchase`)
  return res.data
}
