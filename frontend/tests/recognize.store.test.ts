import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useRecognizeStore } from '../src/stores/recognize'

vi.mock('../src/api/client', () => ({
  recognizeImage: vi.fn()
}))

const { recognizeImage } = await import('../src/api/client')

describe('recognize store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.resetAllMocks()
    if (!globalThis.URL.createObjectURL) {
      globalThis.URL.createObjectURL = () => 'blob:mock'
    }
    if (!globalThis.URL.revokeObjectURL) {
      globalThis.URL.revokeObjectURL = () => undefined
    }
  })

  it('submits and stores result', async () => {
    ;(recognizeImage as unknown as ReturnType<typeof vi.fn>).mockResolvedValue({
      item: '纸箱',
      price: 1.2,
      currency: 'CNY'
    })

    const store = useRecognizeStore()
    store.setFile(new File(['x'], 't.jpg', { type: 'image/jpeg' }))
    expect(store.status).toBe('ready')

    await store.submit()
    expect(store.status).toBe('success')
    expect(store.result?.item).toBe('纸箱')
  })

  it('handles error', async () => {
    ;(recognizeImage as unknown as ReturnType<typeof vi.fn>).mockRejectedValue(new Error('boom'))
    const store = useRecognizeStore()
    store.setFile(new File(['x'], 't.jpg', { type: 'image/jpeg' }))
    await store.submit()
    expect(store.status).toBe('error')
    expect(store.errorMessage).toBeTruthy()
  })
})
