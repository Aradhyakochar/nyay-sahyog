export interface User {
  id: number
  username: string
  email: string
  role: 'client' | 'advocate' | 'mediator' | 'arbitrator' | 'notary' | 'document_writer' | 'admin'
  full_name: string
  phone?: string
  address?: string
  city?: string
  state?: string
  pincode?: string
  is_verified: boolean
  is_active: boolean
  created_at: string
  provider_profile?: Provider
}

export interface Provider {
  id: number
  user_id: number
  user?: User
  specialization?: string
  experience_years: number
  bar_council_number?: string
  qualification?: string
  bio?: string
  consultation_fee: number
  hourly_rate: number
  rating: number
  total_reviews: number
  is_verified: boolean
  is_active: boolean
  created_at: string
  reviews?: Review[]
}

export interface Booking {
  id: number
  client_id: number
  client?: User
  provider_id: number
  provider?: User
  provider_profile_id: number
  service_type: string
  booking_date: string
  duration_minutes: number
  fee: number
  status: 'pending' | 'confirmed' | 'completed' | 'cancelled'
  description?: string
  meeting_link?: string
  location?: string
  created_at: string
  updated_at: string
}

export interface Message {
  id: number
  booking_id?: number
  sender_id: number
  sender?: User
  receiver_id: number
  receiver?: User
  subject?: string
  content: string
  is_read: boolean
  created_at: string
}

export interface Review {
  id: number
  booking_id: number
  provider_id: number
  client_id: number
  client?: User
  rating: number
  comment?: string
  created_at: string
}

export interface Pagination {
  page: number
  per_page: number
  total: number
  pages: number
  has_next: boolean
  has_prev: boolean
}

export interface ApiResponse<T> {
  data?: T
  message?: string
  error?: string
}

