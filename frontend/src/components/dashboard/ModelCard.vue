<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, required: true },
  detail: { type: String, required: true }
})
</script>

<template>
  <div class="glass-card glass-card-hover p-6">
    <h3 class="text-xl font-bold text-white mb-2">{{ title }}</h3>
    <p class="text-sm text-slate-400 mb-4">{{ description }}</p>
    <p class="text-xs font-mono text-accent-cyan/80 bg-accent-cyan/5 border border-accent-cyan/10 rounded-lg px-3 py-2">
      {{ detail }}
    </p>
  </div>
</template>
