<template>
  <div class="nav">
    <div class="nav-left">
      <RouterLink class="nav-brand" to="/">Recycle-AI</RouterLink>
      <template v-if="auth.isAuthed">
        <RouterLink class="nav-link" to="/">识别</RouterLink>
        <RouterLink class="nav-link" to="/market">商城</RouterLink>
        <RouterLink class="nav-link" to="/sell">上架</RouterLink>
        <RouterLink class="nav-link" to="/history">记录</RouterLink>
        <RouterLink class="nav-link" to="/me">我</RouterLink>
      </template>
    </div>
    <div class="nav-right">
      <div v-if="auth.user" class="pill">
        <span style="font-weight: 800">{{ auth.user.display_name || auth.user.username }}</span>
      </div>
      <RouterLink v-if="!auth.isAuthed" class="btn" to="/login">登录</RouterLink>
      <RouterLink v-if="!auth.isAuthed" class="btn" to="/register">注册</RouterLink>
      <button v-if="auth.isAuthed" class="btn" type="button" @click="logout">退出</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

async function logout() {
  auth.logout()
  await router.push('/login')
}
</script>
