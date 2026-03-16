<template>
  <div class="card">
    <div class="row" style="justify-content: space-between; margin-bottom: 10px">
      <div class="pill">识别结果</div>
      <div class="pill" v-if="store.status === 'uploading'">识别中…</div>
      <div class="pill" v-else-if="store.status === 'success'">成功</div>
      <div class="pill danger" v-else-if="store.status === 'error'">失败</div>
      <div class="pill" v-else>待上传</div>
    </div>

    <div v-if="store.errorMessage" class="pill danger" style="border-color: rgba(255, 91, 91, 0.35)">
      {{ store.errorMessage }}
    </div>

    <div v-if="store.result" style="display: grid; gap: 12px; margin-top: 12px">
      <div style="display: grid; gap: 6px">
        <div class="muted" style="font-size: 13px">物品名称</div>
        <div style="font-size: 20px; font-weight: 800; letter-spacing: 0.2px">{{ store.result.item }}</div>
      </div>
      <div style="display: grid; gap: 6px">
        <div class="muted" style="font-size: 13px">参考回收价</div>
        <PriceBadge :price="store.result.price" :currency="store.result.currency" />
      </div>
      <div class="muted" style="font-size: 13px; line-height: 1.6">
        价格来自本地价格库（关键词包含匹配，命中多个取最高价）。仅供参考。
      </div>
    </div>

    <div v-else style="display: grid; gap: 10px; margin-top: 12px">
      <div class="muted" style="font-size: 14px; line-height: 1.7">
        上传图片后点击“开始识别”，后端会调用百度通用图像识别（可配置降级 mock）并返回物品名称与价格。
      </div>
      <div class="row">
        <div class="pill">CORS：仅允许 http://localhost:5173</div>
        <div class="pill">后端：http://localhost:8000</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRecognizeStore } from '../stores/recognize'
import PriceBadge from './PriceBadge.vue'

const store = useRecognizeStore()
</script>
