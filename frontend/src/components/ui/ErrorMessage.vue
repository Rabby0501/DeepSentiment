<script setup>
import { AlertCircle } from 'lucide-vue-next'
defineProps({
  message: { type: String, required: true }
})
</script>

<template>
  <div
    class="flex items-start gap-3 rounded-xl border border-red-500/20 bg-red-500/[0.06] p-4"
    role="alert"
  >
    <AlertCircle :size="18" class="text-red-400 flex-shrink-0 mt-0.5" />
    <p class="text-sm text-red-300">{{ message }}</p>
  </div>
</template>
