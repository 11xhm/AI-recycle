import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import ResultPanel from '../src/components/ResultPanel.vue'
import { useRecognizeStore } from '../src/stores/recognize'

describe('ResultPanel', () => {
  it('renders result', async () => {
    const pinia = createPinia()
    setActivePinia(pinia)

    const store = useRecognizeStore()
    store.status = 'success'
    store.result = { item: '旧手机', price: 50, currency: 'CNY' }
    store.errorMessage = null

    const wrapper = mount(ResultPanel, { global: { plugins: [pinia] } })
    expect(wrapper.text()).toContain('旧手机')
    expect(wrapper.text()).toContain('50.00')
  })
})
