import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { apiLogin, apiMe, apiRegister } from '../api/client'

const TOKEN_KEY = 'recycle_ai_token'

type User = {
  id: number
  username: string
  display_name: string
  created_at: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem(TOKEN_KEY))
  const user = ref<User | null>(null)
  const status = ref<'idle' | 'loading' | 'authed' | 'error'>('idle')
  const errorMessage = ref<string | null>(null)

  const isAuthed = computed(() => !!token.value)

  function setToken(next: string | null) {
    token.value = next
    if (next) localStorage.setItem(TOKEN_KEY, next)
    else localStorage.removeItem(TOKEN_KEY)
  }

  async function refreshMe() {
    if (!token.value) {
      user.value = null
      status.value = 'idle'
      return
    }
    status.value = 'loading'
    errorMessage.value = null
    try {
      const me = await apiMe()
      user.value = me
      status.value = 'authed'
    } catch (e) {
      setToken(null)
      user.value = null
      status.value = 'error'
      errorMessage.value = e instanceof Error ? e.message : '获取用户信息失败'
    }
  }

  async function login(username: string, password: string) {
    status.value = 'loading'
    errorMessage.value = null
    const res = await apiLogin({ username, password })
    setToken(res.access_token)
    await refreshMe()
  }

  async function register(username: string, password: string, display_name?: string) {
    status.value = 'loading'
    errorMessage.value = null
    const res = await apiRegister({ username, password, display_name })
    setToken(res.access_token)
    await refreshMe()
  }

  function logout() {
    setToken(null)
    user.value = null
    status.value = 'idle'
    errorMessage.value = null
  }

  return { token, user, status, errorMessage, isAuthed, setToken, refreshMe, login, register, logout }
})
