<script setup>
import { RouterLink } from 'vue-router'
import { ArrowRight, BarChart3, Cpu, Database, Activity, Sparkles } from 'lucide-vue-next'
import ModelCard from '../components/dashboard/ModelCard.vue'
import StatCard from '../components/ui/StatCard.vue'

const stats = [
  { icon: Cpu, label: '3 Deep Learning Models' },
  { icon: Activity, label: 'Binary Sentiment Classification' },
  { icon: Database, label: 'GloVe 300D Embeddings' },
  { icon: BarChart3, label: 'FastAPI Backend' },
  { icon: Sparkles, label: 'Vue Frontend' }
]
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <!-- Hero -->
    <section class="py-20 sm:py-28 text-center">
      <p class="inline-flex items-center gap-2 text-xs font-semibold tracking-wide uppercase text-accent-cyan/80 bg-accent-cyan/5 border border-accent-cyan/10 rounded-full px-4 py-1.5 mb-6">
        Text Sentiment Analysis System Based on RNN, LSTM and GRU
      </p>
      <h1 class="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight">
        Understand the sentiment<br class="hidden sm:block" /> behind text.
      </h1>
      <p class="mt-6 text-lg text-slate-400 max-w-2xl mx-auto">
        Analyze text using recurrent neural network architectures including RNN, LSTM and GRU.
      </p>
      <div class="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
        <RouterLink to="/analysis" class="glass-button-primary">
          Analyze text
          <ArrowRight :size="16" />
        </RouterLink>
        <RouterLink to="/comparison" class="glass-button">
          Compare models
        </RouterLink>
      </div>
    </section>

    <!-- Model cards -->
    <section class="pb-20">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <ModelCard
          title="RNN"
          description="A SimpleRNN-based recurrent architecture — the foundational sequence model in this system."
          detail="Embedding → SimpleRNN(128) → Dropout(0.3) → Dense(1, sigmoid)"
        />
        <ModelCard
          title="LSTM"
          description="Long Short-Term Memory network, designed to capture longer-range dependencies in text."
          detail="Embedding → LSTM(128) → Dropout(0.3) → Dense(1, sigmoid)"
        />
        <ModelCard
          title="GRU"
          description="Gated Recurrent Unit, a lighter-weight gated alternative to LSTM."
          detail="Embedding → GRU(128) → Dropout(0.3) → Dense(1, sigmoid)"
        />
      </div>
    </section>

    <!-- System highlights -->
    <section class="pb-24">
      <h2 class="section-heading text-center">System highlights</h2>
      <div class="mt-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard v-for="s in stats" :key="s.label" :icon="s.icon" :label="s.label" />
      </div>
    </section>
  </div>
</template>
