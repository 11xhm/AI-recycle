import { describe, expect, it } from 'vitest'
import { mount } from '@vue/test-utils'
import PriceBadge from '../src/components/PriceBadge.vue'

describe('PriceBadge', () => {
  it('formats price to 2 decimals', () => {
    const wrapper = mount(PriceBadge, { props: { price: 1.239, currency: 'CNY' } })
    expect(wrapper.text()).toContain('1.24')
  })

  it('handles non-finite price', () => {
    const wrapper = mount(PriceBadge, { props: { price: Number.NaN, currency: 'CNY' } })
    expect(wrapper.text()).toContain('0.00')
  })
})
