<template>
  <div class="auth-wrap">
    <div class="card auth-card">
      <div class="auth-top">
        <div>
          <div class="auth-title">创建账号</div>
          <div class="auth-subtitle">注册后即可发布旧物、购买商品，并查看历史记录与个人信息。</div>
        </div>
        <div class="pill">SQLite</div>
      </div>

      <div class="auth-tabs">
        <RouterLink class="auth-tab" to="/login">登录</RouterLink>
        <RouterLink class="auth-tab" to="/register">注册</RouterLink>
      </div>

      <div style="display: grid; gap: 10px">
        <label class="field">
          <span class="field-label">用户名</span>
          <input v-model="username" class="input" autocomplete="username" />
          <div class="help">至少 3 位</div>
        </label>
        <label class="field">
          <span class="field-label">显示昵称（可选）</span>
          <input v-model="displayName" class="input" autocomplete="nickname" />
        </label>
        <label class="field">
          <span class="field-label">密码</span>
          <input v-model="password" class="input" type="password" autocomplete="new-password" />
          <div class="help">至少 6 位；服务端只保存哈希，不保存明文</div>
        </label>

        <div class="row" style="justify-content: flex-end; margin-top: 6px">
          <button class="btn" type="button" @click="submit" :disabled="auth.status === 'loading'">
            {{ auth.status === 'loading' ? '注册中…' : '注册并进入' }}
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

const username = ref('')
const displayName = ref('')
const password = ref('')
const error = computed(() => auth.errorMessage)

async function submit() {
  try {
    await auth.register(username.value.trim(), password.value, displayName.value.trim() || undefined)
    await router.push('/')
  } catch (e) {
    auth.errorMessage = e instanceof Error ? e.message : '注册失败'
  }
}
</script>
