import { describe, expect, it, vi } from 'vitest'

const post = vi.fn().mockResolvedValue({ data: { item: '纸箱', price: 1.2, currency: 'CNY' } })

vi.mock('axios', () => ({
  default: {
    create: () => ({
      post,
      get: vi.fn(),
      patch: vi.fn(),
      interceptors: { request: { use: vi.fn() } }
    })
  }
}))

describe('api client', () => {
  it('posts multipart form to /api/recognize', async () => {
    const { recognizeImage } = await import('../src/api/client')
    const file = new File(['x'], 't.jpg', { type: 'image/jpeg' })
    const res = await recognizeImage(file)
    expect(res.item).toBe('纸箱')
    expect(post).toHaveBeenCalled()
    const args = post.mock.calls[0]
    expect(args[0]).toBe('/api/recognize')
    expect(args[1]).toBeInstanceOf(FormData)
    expect(args[2]?.headers?.['Content-Type']).toBe('multipart/form-data')
  })
})
