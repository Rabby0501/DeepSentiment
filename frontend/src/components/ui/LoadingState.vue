<script setup>
defineProps({
  label: { type: String, default: 'Running inference…' }
})
</script>

<template>
  <div class="flex flex-col items-center justify-center gap-3 py-10" role="status" aria-live="polite">
    <div class="h-8 w-8 rounded-full border-2 border-accent-cyan/30 border-t-accent-cyan animate-spin"></div>
    <p class="text-sm text-slate-400">{{ label }}</p>
  </div>
</template>
