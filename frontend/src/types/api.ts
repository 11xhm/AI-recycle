export type RecognizeSuccess = {
  item: string
  price: number
  currency: 'CNY'
}

export type Me = {
  id: number
  username: string
  display_name: string
  created_at: string
}

export type ListingsItem = {
  id: number
  item: string
  description: string
  price: number
  currency: string
  image_url: string
  is_sold: boolean
  created_at: string
  seller?: { id: number; username: string; display_name: string } | null
}

export type Listing = ListingsItem

export type ApiError = {
  error: {
    code: string
    message: string
    details?: unknown
  }
}

export type RecognizeResponse = RecognizeSuccess | ApiError
