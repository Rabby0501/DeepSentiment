<script setup>
const props = defineProps({
  modelValue: { type: String, required: true }
})
const emit = defineEmits(['update:modelValue'])

const models = [
  { id: 'rnn', label: 'RNN', desc: 'SimpleRNN(128)' },
  { id: 'lstm', label: 'LSTM', desc: 'LSTM(128)' },
  { id: 'gru', label: 'GRU', desc: 'GRU(128)' }
]
</script>

<template>
  <fieldset>
    <legend class="text-sm font-medium text-slate-300 mb-2">Model</legend>
    <div class="grid grid-cols-3 gap-2">
      <button
        v-for="m in models"
        :key="m.id"
        type="button"
        class="rounded-xl border px-3 py-3 text-center transition-all duration-200"
        :class="modelValue === m.id
          ? 'border-accent-cyan/60 bg-accent-cyan/10 text-white'
          : 'border-white/10 bg-white/[0.03] text-slate-400 hover:border-white/20 hover:text-slate-200'"
        :aria-pressed="modelValue === m.id"
        @click="emit('update:modelValue', m.id)"
      >
        <span class="block font-semibold text-sm">{{ m.label }}</span>
        <span class="block text-[11px] mt-0.5 opacity-70">{{ m.desc }}</span>
      </button>
    </div>
  </fieldset>
</template>
