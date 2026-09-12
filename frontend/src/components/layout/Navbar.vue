<script setup>
import { ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { BrainCircuit, Menu, X } from 'lucide-vue-next'

const open = ref(false)
const route = useRoute()

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/analysis', label: 'Analysis' },
  { to: '/comparison', label: 'Comparison' },
  { to: '/methodology', label: 'Methodology' },
  { to: '/about', label: 'About' }
]

function isActive(path) {
  return route.path === path
}
</script>

<template>
  <header class="sticky top-0 z-50 border-b border-white/10 bg-base-950/70 backdrop-blur-xl">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between" aria-label="Main navigation">
      <RouterLink to="/" class="flex items-center gap-2 font-bold text-lg text-white">
        <span class="glass-icon text-accent-cyan">
          <BrainCircuit :size="20" />
        </span>
        DeepSentiment
      </RouterLink>

      <ul class="hidden md:flex items-center gap-1">
        <li v-for="link in links" :key="link.to">
          <RouterLink
            :to="link.to"
            class="px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
            :class="isActive(link.to) ? 'text-white bg-white/10' : 'text-slate-400 hover:text-white hover:bg-white/5'"
          >
            {{ link.label }}
          </RouterLink>
        </li>
      </ul>

      <button
        class="md:hidden glass-icon text-slate-300"
        :aria-expanded="open"
        aria-controls="mobile-menu"
        aria-label="Toggle navigation menu"
        @click="open = !open"
      >
        <Menu v-if="!open" :size="20" />
        <X v-else :size="20" />
      </button>
    </nav>

    <div v-if="open" id="mobile-menu" class="md:hidden border-t border-white/10 bg-base-950/95 backdrop-blur-xl">
      <ul class="px-4 py-3 flex flex-col gap-1">
        <li v-for="link in links" :key="link.to">
          <RouterLink
            :to="link.to"
            class="block px-3 py-2 rounded-lg text-sm font-medium"
            :class="isActive(link.to) ? 'text-white bg-white/10' : 'text-slate-400 hover:text-white hover:bg-white/5'"
            @click="open = false"
          >
            {{ link.label }}
          </RouterLink>
        </li>
      </ul>
    </div>
  </header>
</template>
