import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'dashboard', component: () => import('../views/Dashboard.vue') },
  { path: '/analysis', name: 'analysis', component: () => import('../views/SentimentAnalysis.vue') },
  { path: '/comparison', name: 'comparison', component: () => import('../views/ModelComparison.vue') },
  { path: '/methodology', name: 'methodology', component: () => import('../views/Methodology.vue') },
  { path: '/about', name: 'about', component: () => import('../views/About.vue') }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
