import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { recognizeImage } from '../api/client'
import type { RecognizeSuccess } from '../types/api'
import axios from 'axios'

type Status = 'idle' | 'ready' | 'uploading' | 'success' | 'error'

export const useRecognizeStore = defineStore('recognize', () => {
  const file = ref<File | null>(null)
  const previewUrl = ref<string | null>(null)
  const status = ref<Status>('idle')
  const result = ref<RecognizeSuccess | null>(null)
  const errorMessage = ref<string | null>(null)

  const canSubmit = computed(() => status.value !== 'uploading' && file.value !== null)

  function setFile(next: File | null) {
    if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = next ? URL.createObjectURL(next) : null
    file.value = next
    result.value = null
    errorMessage.value = null
    status.value = next ? 'ready' : 'idle'
  }

  function clear() {
    setFile(null)
  }

  async function submit() {
    if (!file.value || status.value === 'uploading') return
    status.value = 'uploading'
    errorMessage.value = null
    result.value = null
    try {
      const data = await recognizeImage(file.value)
      result.value = data
      status.value = 'success'
    } catch (e) {
      const message =
        axios.isAxiosError(e) && e.response?.data?.error?.message
          ? String(e.response.data.error.message)
          : e instanceof Error
            ? e.message
            : '识别失败'
      errorMessage.value = message
      status.value = 'error'
    }
  }

  return { file, previewUrl, status, result, errorMessage, canSubmit, setFile, clear, submit }
})
