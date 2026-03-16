<template>
  <div class="container">
    <NavBar />
    <div class="header">
      <div class="title">Recycle-AI 演示</div>
      <div class="subtitle">支持注册/登录、识别记录、旧物上架、浏览与购买（SQLite 本地存储）。</div>
    </div>
    <RouterView v-slot="{ Component }">
      <Transition name="page" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import NavBar from './components/NavBar.vue'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()

onMounted(() => {
  auth.refreshMe()
})
</script>
