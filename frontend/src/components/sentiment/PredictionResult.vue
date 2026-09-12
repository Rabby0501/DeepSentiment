<script setup>
import { CheckCircle, AlertCircle } from 'lucide-vue-next'

const props = defineProps({
  result: { type: Object, required: true }
})

const isPositive = () => props.result.sentiment === 'Positive'
</script>

<template>
  <div
    class="glass-card p-6 border-l-4"
    :class="isPositive() ? 'border-l-emerald-400/70' : 'border-l-rose-400/70'"
  >
    <div class="flex items-center justify-between mb-4">
      <span class="text-xs font-semibold tracking-wide uppercase text-slate-400">
        {{ result.model }}
      </span>
      <span
        class="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-sm font-semibold"
        :class="isPositive() ? 'bg-emerald-400/10 text-emerald-300' : 'bg-rose-400/10 text-rose-300'"
      >
        <CheckCircle v-if="isPositive()" :size="14" />
        <AlertCircle v-else :size="14" />
        {{ result.sentiment }}
      </span>
    </div>

    <div class="grid grid-cols-2 gap-4 mb-4">
      <div>
        <p class="text-xs text-slate-500 mb-1">Confidence</p>
        <p class="text-2xl font-bold text-white">{{ (result.confidence * 100).toFixed(1) }}%</p>
      </div>
      <div>
        <p class="text-xs text-slate-500 mb-1">Raw probability</p>
        <p class="text-2xl font-bold text-slate-300">{{ result.probability.toFixed(3) }}</p>
      </div>
    </div>

    <div>
      <p class="text-xs text-slate-500 mb-1">Processed text</p>
      <p class="text-sm font-mono text-slate-300 bg-black/20 rounded-lg px-3 py-2 border border-white/5 break-words">
        {{ result.processed_text || '—' }}
      </p>
    </div>
  </div>
</template>
