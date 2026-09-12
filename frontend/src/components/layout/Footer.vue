<script setup>
import { BrainCircuit } from 'lucide-vue-next'
</script>

<template>
  <footer class="border-t border-white/10 mt-24">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 flex flex-col sm:flex-row items-center justify-between gap-4">
      <div class="flex items-center gap-2 text-slate-300 font-semibold">
        <BrainCircuit :size="18" class="text-accent-cyan" />
        DeepSentiment
      </div>
      <p class="text-sm text-slate-500 text-center">
        @2026 DeepSentiment. All rights reserved.
      </p>
      <p class="text-xs text-slate-600">
        Developed by <a href="https://github.com/Rabby0501" target="_blank" class="text-accent-cyan hover:underline">Md Golam Rabby</a>
      </p>
    </div>
  </footer>
</template>
