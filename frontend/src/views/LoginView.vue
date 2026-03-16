<template>
  <div class="auth-wrap">
    <div class="card auth-card">
      <div class="auth-top">
        <div>
          <div class="auth-title">欢迎回来</div>
          <div class="auth-subtitle">登录后可使用识别、上架、购买、历史记录等完整功能。</div>
        </div>
        <div class="pill">演示模式</div>
      </div>

      <div class="auth-tabs">
        <RouterLink class="auth-tab" to="/login">登录</RouterLink>
        <RouterLink class="auth-tab" to="/register">注册</RouterLink>
      </div>

      <div style="display: grid; gap: 10px">
        <label class="field">
          <span class="field-label">用户名</span>
          <input v-model="username" class="input" autocomplete="username" />
        </label>
        <label class="field">
          <span class="field-label">密码</span>
          <input v-model="password" class="input" type="password" autocomplete="current-password" />
          <div class="help">演示账号：demo3 / demo123</div>
        </label>

        <div class="row" style="justify-content: space-between; margin-top: 6px">
          <button class="btn" type="button" @click="fillDemo" :disabled="auth.status === 'loading'">填入演示账号</button>
          <button class="btn" type="button" @click="submit" :disabled="auth.status === 'loading'">
            {{ auth.status === 'loading' ? '登录中…' : '登录' }}
          </button>
        </div>

        <div v-if="error" class="pill danger" style="border-color: rgba(255, 91, 91, 0.35)">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const username = ref('demo3')
const password = ref('demo123')

const error = computed(() => auth.errorMessage)

function fillDemo() {
  username.value = 'demo3'
  password.value = 'demo123'
}

async function submit() {
  try {
    await auth.login(username.value.trim(), password.value)
    await router.push('/')
  } catch (e) {
    auth.errorMessage = e instanceof Error ? e.message : '登录失败'
  }
}
</script>
