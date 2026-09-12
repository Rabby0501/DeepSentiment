<script setup>
const pipeline = [
  'User Text',
  'Text Preprocessing',
  'Tokenization',
  'Sequence Padding',
  'GloVe 300D',
  'RNN / LSTM / GRU',
  'Sigmoid Probability',
  'Positive / Negative'
]

const sections = [
  {
    title: 'Dataset',
    body: 'The models were trained on Sentiment140, a dataset of tweets labeled for binary sentiment. The relevant columns used are the sentiment label and the raw text. Labels are mapped to a binary target: 0 for negative and 1 for positive.'
  },
  {
    title: 'Preprocessing',
    body: 'Raw text is lowercased, then mentions, URLs and non-alphanumeric characters are stripped. The remaining tokens are split on whitespace, English stopwords are removed, and each token is reduced to its stem using the Snowball (Porter2) English stemmer before being reconstructed into a single cleaned string.'
  },
  {
    title: 'Tokenization',
    body: 'Each model (RNN, LSTM, GRU) has its own Keras Tokenizer, fit during training on the cleaned corpus. Cleaned text is converted to integer sequences using that same tokenizer at inference time — tokenizers are not interchangeable between models.'
  },
  {
    title: 'GloVe Embeddings',
    body: 'The original pipeline initializes the embedding layer with pretrained 300-dimensional GloVe word vectors (glove.6B.300d). Once a model is trained and saved, its embedding weights are stored inside the model file itself, so inference does not need to reload the raw GloVe file unless required.'
  },
  {
    title: 'RNN',
    body: 'Embedding → SimpleRNN(128) → Dropout(0.3) → Dense(1, sigmoid). The simplest recurrent architecture in the system, serving as a baseline.'
  },
  {
    title: 'LSTM',
    body: 'Embedding → LSTM(128) → Dropout(0.3) → Dense(1, sigmoid). Long Short-Term Memory cells use input, forget and output gates to retain longer-range dependencies.'
  },
  {
    title: 'GRU',
    body: 'Embedding → GRU(128) → Dropout(0.3) → Dense(1, sigmoid). Gated Recurrent Units simplify the LSTM gating mechanism into update and reset gates, typically with fewer parameters.'
  },
  {
    title: 'Prediction',
    body: 'Sequences are padded to a maximum length of 30 tokens and passed through the selected model, which outputs a single sigmoid probability. A probability of 0.5 or above is classified as Positive; below 0.5 is classified as Negative. Confidence is reported as the probability of the predicted class.'
  }
]
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
    <header class="mb-12 text-center">
      <h1 class="section-heading">Methodology</h1>
      <p class="section-sub mx-auto text-center">
        The end-to-end pipeline used to go from raw text to a sentiment prediction.
      </p>
    </header>

    <!-- Visual pipeline -->
    <div class="glass-card p-6 sm:p-8 mb-12">
      <div class="flex flex-col items-center gap-2">
        <template v-for="(step, idx) in pipeline" :key="step">
          <div class="w-full max-w-sm text-center rounded-xl border border-white/10 bg-white/[0.04] px-4 py-2.5 text-sm font-medium text-slate-200">
            {{ step }}
          </div>
          <span v-if="idx < pipeline.length - 1" class="text-slate-600 text-lg leading-none">↓</span>
        </template>
      </div>
    </div>

    <!-- Sections -->
    <div class="space-y-6">
      <div v-for="s in sections" :key="s.title" class="glass-card p-6">
        <h2 class="text-lg font-bold text-white mb-2">{{ s.title }}</h2>
        <p class="text-sm text-slate-400 leading-relaxed">{{ s.body }}</p>
      </div>
    </div>
  </div>
</template>
