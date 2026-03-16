<template>
  <div class="card" style="max-width: 680px; margin: 0 auto">
    <div class="row" style="justify-content: space-between; margin-bottom: 10px">
      <div class="pill">个人信息</div>
      <button class="btn" type="button" @click="refresh" :disabled="auth.status === 'loading'">
        {{ auth.status === 'loading' ? '刷新中…' : '刷新' }}
      </button>
    </div>

    <div v-if="!auth.isAuthed" class="pill danger" style="border-color: rgba(255, 91, 91, 0.35)">
      需要登录后才能查看
      <RouterLink to="/login" style="margin-left: 8px; text-decoration: underline">去登录</RouterLink>
    </div>

    <div v-if="auth.user" style="display: grid; gap: 10px">
      <div class="row">
        <div class="pill">ID：{{ auth.user.id }}</div>
        <div class="pill">用户名：{{ auth.user.username }}</div>
        <div class="pill">创建时间：{{ auth.user.created_at }}</div>
      </div>

      <label style="display: grid; gap: 6px">
        <span class="muted" style="font-size: 13px">显示昵称</span>
        <input v-model="displayName" class="input" :disabled="saving" />
      </label>

      <div class="row" style="justify-content: flex-end">
        <button class="btn" type="button" @click="save" :disabled="saving">
          {{ saving ? '保存中…' : '保存' }}
        </button>
      </div>

      <div v-if="msg" class="pill" style="border-color: rgba(85, 214, 190, 0.35)">{{ msg }}</div>
      <div v-if="error" class="pill danger" style="border-color: rgba(255, 91, 91, 0.35)">{{ error }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { apiUpdateMe } from '../api/client'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const displayName = ref('')
const saving = ref(false)
const msg = ref<string | null>(null)
const error = ref<string | null>(null)

watch(
  () => auth.user,
  (u) => {
    displayName.value = u?.display_name ?? ''
  },
  { immediate: true }
)

const isAuthed = computed(() => auth.isAuthed)

async function refresh() {
  await auth.refreshMe()
}

async function save() {
  if (!isAuthed.value) {
    await router.push('/login')
    return
  }
  saving.value = true
  msg.value = null
  error.value = null
  try {
    await apiUpdateMe({ display_name: displayName.value })
    await auth.refreshMe()
    msg.value = '已保存'
  } catch (e) {
    error.value = e instanceof Error ? e.message : '保存失败'
  } finally {
    saving.value = false
  }
}
</script>
