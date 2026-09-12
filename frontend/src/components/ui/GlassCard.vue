<script setup>
defineProps({
  hoverable: { type: Boolean, default: false },
  padded: { type: Boolean, default: true }
})
</script>

<template>
  <div
    class="glass-card"
    :class="[hoverable ? 'glass-card-hover' : '', padded ? 'p-6' : '']"
  >
    <slot />
  </div>
</template>
