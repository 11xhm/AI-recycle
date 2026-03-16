<template>
  <div class="pill" style="border-color: rgba(85, 214, 190, 0.35); color: rgba(255, 255, 255, 0.92)">
    <span style="font-weight: 800; color: var(--accent)">¥</span>
    <span style="font-weight: 800">{{ formatted }}</span>
    <span class="muted">{{ currency }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  price: number
  currency: string
}>()

const formatted = computed(() => {
  const n = Number.isFinite(props.price) ? props.price : 0
  return n.toFixed(2)
})
</script>
