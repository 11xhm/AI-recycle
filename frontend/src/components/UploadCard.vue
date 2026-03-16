<template>
  <div class="card">
    <div class="row" style="justify-content: space-between; margin-bottom: 10px">
      <div class="pill">
        <span>图片上传</span>
        <span v-if="store.file" class="muted">{{ store.file.name }}</span>
      </div>
      <div class="row">
        <button class="btn" type="button" @click="pickFile" :disabled="store.status === 'uploading'">选择图片</button>
        <button class="btn" type="button" @click="store.clear" :disabled="!store.file || store.status === 'uploading'">
          清除
        </button>
        <input ref="inputEl" type="file" accept="image/*" @change="onInputChange" style="display: none" />
      </div>
    </div>

    <div
      :style="dropStyle"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
      @click="pickFile"
      role="button"
      tabindex="0"
    >
      <template v-if="store.previewUrl">
        <img :src="store.previewUrl" alt="preview" :style="imgStyle" />
      </template>
      <template v-else>
        <div style="display: grid; gap: 6px; padding: 14px">
          <div style="font-weight: 700">点击或拖拽上传</div>
          <div class="muted" style="font-size: 13px">支持常见图片格式（JPG/PNG/WebP）</div>
        </div>
      </template>
    </div>

    <div class="row" style="margin-top: 12px; justify-content: space-between">
      <div class="muted" style="font-size: 13px">后端接口：POST /api/recognize</div>
      <button class="btn" type="button" @click="store.submit" :disabled="!store.canSubmit">
        {{ store.status === 'uploading' ? '识别中…' : '开始识别' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRecognizeStore } from '../stores/recognize'

const store = useRecognizeStore()
const inputEl = ref<HTMLInputElement | null>(null)
const dragging = ref(false)

function pickFile() {
  inputEl.value?.click()
}

function setFromFileList(list: FileList | null) {
  const f = list?.item(0) ?? null
  if (!f) return
  if (!f.type.startsWith('image/')) return
  store.setFile(f)
}

function onInputChange(e: Event) {
  const target = e.target as HTMLInputElement
  setFromFileList(target.files)
  if (target.value) target.value = ''
}

function onDragOver() {
  dragging.value = true
}

function onDragLeave() {
  dragging.value = false
}

function onDrop(e: DragEvent) {
  dragging.value = false
  setFromFileList(e.dataTransfer?.files ?? null)
}

const dropStyle = computed(() => ({
  border: `1px dashed ${dragging.value ? 'rgba(85, 214, 190, 0.9)' : 'rgba(255,255,255,0.18)'}`,
  background: dragging.value ? 'rgba(85, 214, 190, 0.08)' : 'rgba(255,255,255,0.04)',
  borderRadius: '14px',
  minHeight: '220px',
  display: 'grid',
  placeItems: 'center',
  cursor: 'pointer',
  overflow: 'hidden'
}))

const imgStyle = computed(() => ({
  width: '100%',
  height: '100%',
  objectFit: 'cover',
  minHeight: '220px'
}))
</script>
