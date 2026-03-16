import { beforeEach, describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import UploadCard from '../src/components/UploadCard.vue'
import { useRecognizeStore } from '../src/stores/recognize'

function createFileList(files: File[]): FileList {
  const list: any = { length: files.length, item: (i: number) => files[i] ?? null }
  files.forEach((f, i) => {
    list[i] = f
  })
  return list as FileList
}

function setInputFiles(input: HTMLInputElement, files: File[]) {
  Object.defineProperty(input, 'files', { value: createFileList(files), configurable: true })
}

describe('UploadCard', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    if (!globalThis.URL.createObjectURL) {
      globalThis.URL.createObjectURL = () => 'blob:mock'
    }
    if (!globalThis.URL.revokeObjectURL) {
      globalThis.URL.revokeObjectURL = () => undefined
    }
  })

  it('accepts image file from input and shows preview', async () => {
    const wrapper = mount(UploadCard, { global: { plugins: [createPinia()] } })
    expect(wrapper.text()).toContain('点击或拖拽上传')

    const input = wrapper.find('input[type="file"]').element as HTMLInputElement
    setInputFiles(input, [new File(['x'], 't.jpg', { type: 'image/jpeg' })])
    await wrapper.find('input[type="file"]').trigger('change')

    const store = useRecognizeStore()
    expect(store.file?.name).toBe('t.jpg')
    expect(wrapper.find('img').exists()).toBe(true)

    await wrapper.findAll('button').find((b) => b.text().includes('清除'))!.trigger('click')
    expect(store.file).toBe(null)
  })

  it('ignores non-image file', async () => {
    const wrapper = mount(UploadCard, { global: { plugins: [createPinia()] } })
    const input = wrapper.find('input[type="file"]').element as HTMLInputElement
    setInputFiles(input, [new File(['x'], 't.txt', { type: 'text/plain' })])
    await wrapper.find('input[type="file"]').trigger('change')

    const store = useRecognizeStore()
    expect(store.file).toBe(null)
  })
})
