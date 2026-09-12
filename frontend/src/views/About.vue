<script setup>
const stack = [
  { group: 'Frontend', items: ['Vue 3', 'Vite', 'Tailwind CSS', 'Vue Router', 'Axios', 'Lucide Vue Next'] },
  { group: 'Backend', items: ['Python', 'FastAPI', 'Uvicorn', 'Pydantic'] },
  { group: 'Machine Learning', items: ['TensorFlow / Keras', 'NumPy', 'Pandas', 'NLTK', 'scikit-learn'] },
  { group: 'Deployment', items: ['Docker', 'Docker Compose', 'Nginx'] }
]

const components = [
  'User interface (Vue 3 + Tailwind, "Liquid Glass" design system)',
  'Text preprocessing (cleaning, stopword removal, stemming)',
  'Tokenization (per-model Keras tokenizers)',
  'Model management (lazy loading and in-memory caching)',
  'Sentiment prediction (single-model inference)',
  'Model comparison (RNN, LSTM and GRU on the same input)',
  'Result visualization',
  'System information (model availability reporting)'
]
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <header class="mb-12 text-center">
      <h1 class="section-heading">DeepSentiment</h1>
      <p class="section-sub mx-auto text-center">
        Text Sentiment Analysis System Based on RNN, LSTM and GRU
      </p>
    </header>

    <div class="glass-card p-6 sm:p-8 mb-8">
      <h2 class="text-lg font-bold text-white mb-2">Purpose</h2>
      <p class="text-sm text-slate-400 leading-relaxed">
        DeepSentiment is an integrated software system for binary sentiment classification of text.
        It packages three recurrent neural network architectures — RNN, LSTM and GRU — as components
        of a single application, rather than as separate, unrelated programs. The system covers the
        full path from raw user text to a classified sentiment: preprocessing, tokenization, model
        inference, and result presentation.
      </p>
    </div>

    <div class="glass-card p-6 sm:p-8 mb-8">
      <h2 class="text-lg font-bold text-white mb-2">Architecture</h2>
      <p class="text-sm text-slate-400 leading-relaxed">
        A Vue 3 single-page frontend communicates with a FastAPI backend over a JSON REST API.
        The backend loads trained Keras models and their associated tokenizers on demand and caches
        them in memory for subsequent requests. Inference runs entirely on the server — no user text
        is sent to any third-party AI service.
      </p>
    </div>

    <div class="glass-card p-6 sm:p-8 mb-8">
      <h2 class="text-lg font-bold text-white mb-2">Software components</h2>
      <ul class="grid sm:grid-cols-2 gap-2">
        <li v-for="c in components" :key="c" class="text-sm text-slate-400 flex items-start gap-2">
          <span class="text-accent-cyan mt-1">•</span>{{ c }}
        </li>
      </ul>
    </div>

    <div class="glass-card p-6 sm:p-8 mb-8">
      <h2 class="text-lg font-bold text-white mb-4">Technology stack</h2>
      <div class="grid sm:grid-cols-2 gap-6">
        <div v-for="s in stack" :key="s.group">
          <h3 class="text-sm font-semibold text-slate-300 mb-2">{{ s.group }}</h3>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="item in s.items"
              :key="item"
              class="text-xs px-2.5 py-1 rounded-lg border border-white/10 bg-white/[0.04] text-slate-400"
            >
              {{ item }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="glass-card p-6 sm:p-8">
      <h2 class="text-lg font-bold text-white mb-2">Research foundation</h2>
      <p class="text-sm text-slate-400 leading-relaxed">
        The underlying models originate from research/development notebooks (RNN_Level1.ipynb,
        LSTM_Level2.ipynb, GRU_Level3.ipynb) that document the training methodology on the
        Sentiment140 dataset with GloVe 300-dimensional embeddings. These notebooks are preserved
        in the <code class="text-slate-300">notebooks/</code> directory as development evidence.
      </p>
    </div>
  </div>
</template>
