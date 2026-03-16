<template>
  <div class="card">
    <div class="row" style="justify-content: space-between; margin-bottom: 10px">
      <div class="pill">商品详情</div>
      <div class="row">
        <RouterLink class="btn" to="/market">返回商城</RouterLink>
        <button class="btn" type="button" @click="load" :disabled="loading">{{ loading ? '刷新中…' : '刷新' }}</button>
      </div>
    </div>

    <div v-if="error" class="pill danger" style="border-color: rgba(255, 91, 91, 0.35)">{{ error }}</div>

    <div v-if="item" class="grid" style="grid-template-columns: 1fr; gap: 14px">
      <div>
        <img v-if="item.image_url" class="market-img" :src="imgUrl(item.image_url)" alt="img" style="height: 320px" />
      </div>
      <div style="display: grid; gap: 10px">
        <div style="font-weight: 900; font-size: 20px">{{ item.item }}</div>
        <div class="row">
          <div class="pill">
            <span style="font-weight: 800; color: var(--accent)">¥</span>
            <span style="font-weight: 900">{{ Number(item.price).toFixed(2) }}</span>
            <span class="muted">{{ item.currency }}</span>
          </div>
          <div class="pill" :class="item.is_sold ? 'danger' : ''">{{ item.is_sold ? '已售' : '在售' }}</div>
        </div>
        <div class="muted" style="font-size: 13px; line-height: 1.7">{{ item.description || '—' }}</div>
        <div class="muted" style="font-size: 12px">
          卖家：{{ item.seller?.display_name || item.seller?.username || '—' }} · {{ item.created_at }}
        </div>

        <div class="row" style="justify-content: flex-end">
          <button class="btn" type="button" @click="buy" :disabled="buying || item.is_sold">
            {{ item.is_sold ? '已售出' : buying ? '购买中…' : '购买' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="!item && !loading && !error" class="muted" style="font-size: 14px">未找到商品</div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiGetListing, apiPurchase } from '../api/client'
import type { Listing } from '../types/api'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const loading = ref(false)
const buying = ref(false)
const error = ref<string | null>(null)
const item = ref<Listing | null>(null)

function imgUrl(path: string) {
  const base = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'
  if (path.startsWith('http')) return path
  return `${base}${path}`
}

async function load() {
  const id = Number(route.params.id)
  if (!Number.isFinite(id)) {
    item.value = null
    return
  }
  loading.value = true
  error.value = null
  try {
    item.value = await apiGetListing(id)
  } catch (e) {
    item.value = null
    error.value = e instanceof Error ? e.message : '加载失败'
  } finally {
    loading.value = false
  }
}

async function buy() {
  if (!auth.isAuthed) {
    await router.push('/login')
    return
  }
  if (!item.value) return
  buying.value = true
  error.value = null
  try {
    await apiPurchase(item.value.id)
    await load()
  } catch (e) {
    error.value = e instanceof Error ? e.message : '购买失败'
  } finally {
    buying.value = false
  }
}

onMounted(load)
</script>
