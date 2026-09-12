<script setup>
import { CheckCircle, AlertCircle, XCircle } from 'lucide-vue-next'

const props = defineProps({
  result: { type: Object, required: true }
})
</script>

<template>
  <div class="glass-card p-6">
    <p class="text-xs font-semibold tracking-wide uppercase text-slate-400 mb-4">{{ result.model }}</p>

    <div v-if="result.available">
      <div class="flex items-center gap-2 mb-4">
        <CheckCircle v-if="result.sentiment === 'Positive'" :size="18" class="text-emerald-400" />
        <AlertCircle v-else :size="18" class="text-rose-400" />
        <span
          class="text-lg font-bold"
          :class="result.sentiment === 'Positive' ? 'text-emerald-300' : 'text-rose-300'"
        >
          {{ result.sentiment }}
        </span>
      </div>
      <p class="text-3xl font-bold text-white mb-1">{{ (result.confidence * 100).toFixed(1) }}%</p>
      <p class="text-xs text-slate-500">confidence · probability {{ result.probability.toFixed(3) }}</p>
    </div>

    <div v-else class="flex items-start gap-2">
      <XCircle :size="18" class="text-slate-500 flex-shrink-0 mt-0.5" />
      <div>
        <p class="text-sm font-semibold text-slate-400">Model unavailable</p>
        <p class="text-xs text-slate-600 mt-1">{{ result.error }}</p>
      </div>
    </div>
  </div>
</template>
