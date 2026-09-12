<script setup>
import { ref, computed } from 'vue'
import ModelSelector from '../components/sentiment/ModelSelector.vue'
import PredictionResult from '../components/sentiment/PredictionResult.vue'
import LoadingState from '../components/ui/LoadingState.vue'
import ErrorMessage from '../components/ui/ErrorMessage.vue'
import { predictSentiment } from '../services/api'

const text = ref('')
const model = ref('lstm')
const loading = ref(false)
const error = ref('')
const result = ref(null)

const MAX_LENGTH = 5000

const charCount = computed(() => text.value.length)
const isOverLimit = computed(() => charCount.value > MAX_LENGTH)
const canSubmit = computed(() => text.value.trim().length > 0 && !isOverLimit.value && !loading.value)

async function analyze() {
  if (!canSubmit.value) return
  loading.value = true
  error.value = ''
  result.value = null
  try {
    result.value = await predictSentiment(text.value, model.value)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <header class="mb-10 text-center">
      <h1 class="section-heading">Sentiment Analysis</h1>
      <p class="section-sub mx-auto text-center">
        Enter text, choose a model, and run inference against the trained RNN, LSTM or GRU network.
      </p>
    </header>

    <div class="glass-card p-6 sm:p-8">
      <label for="analysis-text" class="block text-sm font-medium text-slate-300 mb-2">
        Text to analyze
      </label>
      <textarea
        id="analysis-text"
        v-model="text"
        rows="6"
        maxlength="5000"
        placeholder="Type or paste text here…"
        class="glass-input resize-none"
        aria-describedby="char-count"
      ></textarea>
      <div id="char-count" class="mt-2 flex justify-between text-xs">
        <span :class="isOverLimit ? 'text-rose-400' : 'text-slate-500'">
          {{ charCount }} / {{ MAX_LENGTH }} characters
        </span>
      </div>

      <div class="mt-6">
        <ModelSelector v-model="model" />
      </div>

      <button
        type="button"
        class="glass-button-primary w-full mt-6"
        :disabled="!canSubmit"
        @click="analyze"
      >
        {{ loading ? 'Analyzing…' : 'Analyze text' }}
      </button>
    </div>

    <div class="mt-8">
      <LoadingState v-if="loading" label="Running inference…" />
      <ErrorMessage v-else-if="error" :message="error" />
      <PredictionResult v-else-if="result" :result="result" />
    </div>
  </div>
</template>
