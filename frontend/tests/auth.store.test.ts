import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from '../src/stores/auth'

vi.mock('../src/api/client', () => ({
  apiLogin: vi.fn(),
  apiRegister: vi.fn(),
  apiMe: vi.fn()
}))

const { apiLogin, apiRegister, apiMe } = await import('../src/api/client')

describe('auth store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    vi.resetAllMocks()
  })

  it('registers then loads me', async () => {
    ;(apiRegister as unknown as ReturnType<typeof vi.fn>).mockResolvedValue({ access_token: 't', token_type: 'bearer' })
    ;(apiMe as unknown as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: 1,
      username: 'u',
      display_name: 'n',
      created_at: 'now'
    })

    const store = useAuthStore()
    await store.register('u', 'secret1', 'n')
    expect(store.isAuthed).toBe(true)
    expect(store.user?.username).toBe('u')
    expect(localStorage.getItem('recycle_ai_token')).toBe('t')
  })

  it('logs in then logs out', async () => {
    ;(apiLogin as unknown as ReturnType<typeof vi.fn>).mockResolvedValue({ access_token: 't2', token_type: 'bearer' })
    ;(apiMe as unknown as ReturnType<typeof vi.fn>).mockResolvedValue({
      id: 2,
      username: 'u2',
      display_name: '',
      created_at: 'now'
    })

    const store = useAuthStore()
    await store.login('u2', 'secret1')
    expect(store.user?.id).toBe(2)

    store.logout()
    expect(store.isAuthed).toBe(false)
    expect(store.user).toBe(null)
  })
})
