import { describe, expect, it } from 'vitest'
import router from '../src/router'

describe('router', () => {
  it('navigates to home', async () => {
    localStorage.setItem('recycle_ai_token', 't')
    await router.push('/')
    await router.isReady()
    expect(router.currentRoute.value.path).toBe('/')
  })

  it('navigates to market', async () => {
    localStorage.setItem('recycle_ai_token', 't')
    await router.push('/market')
    await router.isReady()
    expect(router.currentRoute.value.path).toBe('/market')
  })

  it('redirects to login for protected routes', async () => {
    localStorage.removeItem('recycle_ai_token')
    await router.push('/me')
    await router.isReady()
    expect(router.currentRoute.value.path).toBe('/login')
  })
})
