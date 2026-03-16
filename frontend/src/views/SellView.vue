<template>
  <div class="grid">
    <div class="card">
      <div class="row" style="justify-content: space-between; margin-bottom: 10px">
        <div class="pill">发布旧物</div>
        <button class="btn" type="button" @click="reset" :disabled="submitting">重置</button>
      </div>

      <div v-if="!auth.isAuthed" class="pill danger" style="border-color: rgba(255, 91, 91, 0.35)">
        需要登录后才能发布
        <RouterLink to="/login" style="margin-left: 8px; text-decoration: underline">去登录</RouterLink>
      </div>

      <label style="display: grid; gap: 6px; margin-top: 12px">
        <span class="muted" style="font-size: 13px">图片</span>
        <input class="input" type="file" accept="image/*" @change="onPick" :disabled="!auth.isAuthed || submitting" />
      </label>

      <div v-if="previewUrl" style="margin-top: 12px">
        <img :src="previewUrl" class="market-img" alt="preview" style="height: 220px" />
      </div>

      <label style="display: grid; gap: 6px; margin-top: 12px">
        <span class="muted" style="font-size: 13px">描述</span>
        <textarea v-model="description" class="input" rows="4" :disabled="!auth.isAuthed || submitting"></textarea>
      </label>

      <label style="display: grid; gap: 6px; margin-top: 12px">
        <span class="muted" style="font-size: 13px">价格（可不填，默认用 AI+价格库）</span>
        <input v-model="priceText" class="input" inputmode="decimal" :disabled="!auth.isAuthed || submitting" />
      </label>

      <div class="row" style="justify-content: flex-end; margin-top: 12px">
        <button class="btn" type="button" @click="submit" :disabled="!canSubmit">
          {{ submitting ? '发布中…' : '发布' }}
        </button>
      </div>

      <div v-if="error" class="pill danger" style="border-color: rgba(255, 91, 91, 0.35)">{{ error }}</div>
    </div>

    <div class="card">
      <div class="pill" style="margin-bottom: 10px">发布结果</div>
      <div v-if="created" style="display: grid; gap: 10px">
        <div style="font-size: 18px; font-weight: 900">{{ created.item }}</div>
        <div class="row">
          <div class="pill">
            <span style="font-weight: 800; color: var(--accent)">¥</span>
            <span style="font-weight: 900">{{ Number(created.price).toFixed(2) }}</span>
            <span class="muted">{{ created.currency }}</span>
          </div>
          <div class="pill">ID：{{ created.id }}</div>
        </div>
        <img v-if="created.image_url" :src="imgUrl(created.image_url)" class="market-img" alt="img" />
        <div class="muted" style="font-size: 13px; line-height: 1.6">{{ created.description || '—' }}</div>
        <RouterLink class="btn" to="/market">去商城查看</RouterLink>
      </div>
      <div v-else class="muted" style="font-size: 14px; line-height: 1.7">
        选择图片并点击发布。服务端会识别物品名称，并用价格库匹配参考价作为默认上架价。
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { apiCreateListing } from '../api/client'
import type { ListingsItem } from '../types/api'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

const file = ref<File | null>(null)
const previewUrl = ref<string | null>(null)
const description = ref('')
const priceText = ref('')
const submitting = ref(false)
const error = ref<string | null>(null)
const created = ref<ListingsItem | null>(null)

function imgUrl(path: string) {
  const base = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'
  if (path.startsWith('http')) return path
  return `${base}${path}`
}

function onPick(e: Event) {
  const input = e.target as HTMLInputElement
  const f = input.files?.item(0) ?? null
  if (!f) return
  if (!f.type.startsWith('image/')) return
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  previewUrl.value = URL.createObjectURL(f)
  file.value = f
}

function reset() {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  previewUrl.value = null
  file.value = null
  description.value = ''
  priceText.value = ''
  error.value = null
  created.value = null
}

const canSubmit = computed(() => auth.isAuthed && !submitting.value && file.value !== null)

async function submit() {
  if (!file.value) return
  submitting.value = true
  error.value = null
  created.value = null
  const price = priceText.value.trim() ? Number(priceText.value.trim()) : null
  try {
    created.value = await apiCreateListing({ file: file.value, description: description.value, price })
  } catch (e) {
    error.value = e instanceof Error ? e.message : '发布失败'
  } finally {
    submitting.value = false
  }
}
</script>
