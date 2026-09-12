<script setup>
import { ref, computed } from 'vue'
import ComparisonCard from '../components/comparison/ComparisonCard.vue'
import LoadingState from '../components/ui/LoadingState.vue'
import ErrorMessage from '../components/ui/ErrorMessage.vue'
import { compareSentiment } from '../services/api'

const text = ref('')
const loading = ref(false)
const error = ref('')
const results = ref(null)

const MAX_LENGTH = 5000
const charCount = computed(() => text.value.length)
const isOverLimit = computed(() => charCount.value > MAX_LENGTH)
const canSubmit = computed(() => text.value.trim().length > 0 && !isOverLimit.value && !loading.value)

async function runComparison() {
  if (!canSubmit.value) return
  loading.value = true
  error.value = ''
  results.value = null
  try {
    const data = await compareSentiment(text.value)
    results.value = data.results
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <header class="mb-10 text-center">
      <h1 class="section-heading">Model Comparison</h1>
      <p class="section-sub mx-auto text-center">
        Run the same input through RNN, LSTM and GRU side by side.
      </p>
    </header>

    <div class="glass-card p-6 sm:p-8">
      <label for="compare-text" class="block text-sm font-medium text-slate-300 mb-2">
        Text to compare
      </label>
      <textarea
        id="compare-text"
        v-model="text"
        rows="5"
        maxlength="5000"
        placeholder="Type or paste text here…"
        class="glass-input resize-none"
      ></textarea>
      <div class="mt-2 flex justify-between text-xs">
        <span :class="isOverLimit ? 'text-rose-400' : 'text-slate-500'">
          {{ charCount }} / {{ MAX_LENGTH }} characters
        </span>
      </div>

      <button
        type="button"
        class="glass-button-primary w-full mt-6"
        :disabled="!canSubmit"
        @click="runComparison"
      >
        {{ loading ? 'Comparing…' : 'Compare models' }}
      </button>
    </div>

    <div class="mt-8">
      <LoadingState v-if="loading" label="Running RNN, LSTM and GRU…" />
      <ErrorMessage v-else-if="error" :message="error" />
      <div v-else-if="results" class="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <ComparisonCard v-for="r in results" :key="r.model" :result="r" />
      </div>
    </div>
  </div>
</template>
