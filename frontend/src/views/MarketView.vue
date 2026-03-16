<template>
  <div class="card">
    <div class="row" style="justify-content: space-between; margin-bottom: 10px">
      <div class="pill">在售商品</div>
      <button class="btn" type="button" @click="load" :disabled="loading">{{ loading ? '刷新中…' : '刷新' }}</button>
    </div>

    <div v-if="error" class="pill danger" style="border-color: rgba(255, 91, 91, 0.35)">{{ error }}</div>

    <div v-if="items.length === 0 && !loading" class="muted" style="font-size: 14px; line-height: 1.7">
      暂无商品。你可以去“上架”发布旧物。
    </div>

    <div class="market-grid" v-if="items.length">
      <div v-for="it in items" :key="it.id" class="market-item">
        <RouterLink :to="`/market/${it.id}`">
          <img v-if="it.image_url" class="market-img" :src="imgUrl(it.image_url)" alt="img" />
        </RouterLink>
        <div style="display: grid; gap: 6px">
          <RouterLink :to="`/market/${it.id}`" style="font-weight: 900; letter-spacing: 0.2px">
            {{ it.item }}
          </RouterLink>
          <div class="muted" style="font-size: 13px; line-height: 1.5">{{ it.description || '—' }}</div>
          <div class="row" style="justify-content: space-between; margin-top: 6px">
            <div class="pill">
              <span style="font-weight: 800; color: var(--accent)">¥</span>
              <span style="font-weight: 900">{{ Number(it.price).toFixed(2) }}</span>
              <span class="muted">{{ it.currency }}</span>
            </div>
            <button class="btn" type="button" @click="buy(it.id)" :disabled="buyingId === it.id">
              {{ buyingId === it.id ? '购买中…' : '购买' }}
            </button>
          </div>
          <div class="muted" style="font-size: 12px">
            卖家：{{ it.seller?.display_name || it.seller?.username || '—' }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiListListings, apiPurchase } from '../api/client'
import type { ListingsItem } from '../types/api'
import { useAuthStore } from '../stores/auth'

const items = ref<ListingsItem[]>([])
const loading = ref(false)
const error = ref<string | null>(null)
const buyingId = ref<number | null>(null)

const router = useRouter()
const auth = useAuthStore()

function imgUrl(path: string) {
  const base = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'
  if (path.startsWith('http')) return path
  return `${base}${path}`
}

async function load() {
  loading.value = true
  error.value = null
  try {
    items.value = await apiListListings(false)
  } catch (e) {
    error.value = e instanceof Error ? e.message : '加载失败'
  } finally {
    loading.value = false
  }
}

async function buy(id: number) {
  if (!auth.isAuthed) {
    await router.push('/login')
    return
  }
  buyingId.value = id
  error.value = null
  try {
    await apiPurchase(id)
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '购买失败'
  } finally {
    buyingId.value = null
  }
}

onMounted(load)
</script>
