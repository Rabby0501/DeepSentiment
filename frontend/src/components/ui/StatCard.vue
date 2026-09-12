<script setup>
defineProps({
  icon: { type: [Object, Function], required: true },
  label: { type: String, required: true }
})
</script>

<template>
  <div class="glass-card glass-card-hover p-5 flex items-center gap-4">
    <span class="glass-icon text-accent-cyan flex-shrink-0">
      <component :is="icon" :size="18" />
    </span>
    <span class="text-sm font-medium text-slate-300">{{ label }}</span>
  </div>
</template>
