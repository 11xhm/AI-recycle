<template>
  <div class="card">
    <div class="row" style="justify-content: space-between; margin-bottom: 10px">
      <div class="pill">历史记录</div>
      <button class="btn" type="button" @click="load" :disabled="loading">{{ loading ? '刷新中…' : '刷新' }}</button>
    </div>

    <div v-if="!auth.isAuthed" class="pill danger" style="border-color: rgba(255, 91, 91, 0.35)">
      需要登录后才能查看
      <RouterLink to="/login" style="margin-left: 8px; text-decoration: underline">去登录</RouterLink>
    </div>

    <div v-if="error" class="pill danger" style="border-color: rgba(255, 91, 91, 0.35)">{{ error }}</div>

    <div v-if="auth.isAuthed" style="display: grid; gap: 14px; margin-top: 12px">
      <div class="card" style="padding: 12px">
        <div class="pill" style="margin-bottom: 10px">识别记录（最多 50 条）</div>
        <div v-if="data?.recognitions?.length" style="display: grid; gap: 8px">
          <div v-for="r in data!.recognitions" :key="r.id" class="row" style="justify-content: space-between">
            <div>
              <div style="font-weight: 900">{{ r.item }}</div>
              <div class="muted" style="font-size: 12px">{{ r.created_at }}</div>
            </div>
            <div class="pill">
              <span style="font-weight: 800; color: var(--accent)">¥</span>
              <span style="font-weight: 900">{{ Number(r.price).toFixed(2) }}</span>
              <span class="muted">{{ r.currency }}</span>
            </div>
          </div>
        </div>
        <div v-else class="muted" style="font-size: 13px">暂无识别记录</div>
      </div>

      <div class="card" style="padding: 12px">
        <div class="pill" style="margin-bottom: 10px">购买记录</div>
        <div v-if="data?.purchases?.length" style="display: grid; gap: 8px">
          <div v-for="o in data!.purchases" :key="o.id" class="row" style="justify-content: space-between">
            <div>
              <div style="font-weight: 900">订单 #{{ o.id }}</div>
              <div class="muted" style="font-size: 12px">商品ID：{{ o.listing_id }} · {{ o.created_at }}</div>
            </div>
            <div class="pill">
              <span style="font-weight: 800; color: var(--accent)">¥</span>
              <span style="font-weight: 900">{{ Number(o.price).toFixed(2) }}</span>
              <span class="muted">{{ o.currency }}</span>
            </div>
          </div>
        </div>
        <div v-else class="muted" style="font-size: 13px">暂无购买记录</div>
      </div>

      <div class="card" style="padding: 12px">
        <div class="pill" style="margin-bottom: 10px">我的上架</div>
        <div v-if="data?.my_listings?.length" class="market-grid">
          <div v-for="it in data!.my_listings" :key="it.id" class="market-item">
            <img v-if="it.image_url" class="market-img" :src="imgUrl(it.image_url)" alt="img" />
            <div style="display: grid; gap: 6px">
              <div style="font-weight: 900">{{ it.item }}</div>
              <div class="row" style="justify-content: space-between">
                <div class="pill">
                  <span style="font-weight: 800; color: var(--accent)">¥</span>
                  <span style="font-weight: 900">{{ Number(it.price).toFixed(2) }}</span>
                  <span class="muted">{{ it.currency }}</span>
                </div>
                <div class="pill" :class="it.is_sold ? 'danger' : ''">{{ it.is_sold ? '已售' : '在售' }}</div>
              </div>
              <div class="muted" style="font-size: 12px">{{ it.created_at }}</div>
            </div>
          </div>
        </div>
        <div v-else class="muted" style="font-size: 13px">暂无上架记录</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiHistory } from '../api/client'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const loading = ref(false)
const error = ref<string | null>(null)
const data = ref<Awaited<ReturnType<typeof apiHistory>> | null>(null)

function imgUrl(path: string) {
  const base = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'
  if (path.startsWith('http')) return path
  return `${base}${path}`
}

async function load() {
  if (!auth.isAuthed) {
    data.value = null
    return
  }
  loading.value = true
  error.value = null
  try {
    data.value = await apiHistory()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '加载失败'
    if (String(error.value).includes('未登录')) {
      auth.logout()
      await router.push('/login')
    }
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
