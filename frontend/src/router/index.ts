import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import MarketView from '../views/MarketView.vue'
import SellView from '../views/SellView.vue'
import HistoryView from '../views/HistoryView.vue'
import MeView from '../views/MeView.vue'
import ListingView from '../views/ListingView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView },
    { path: '/register', name: 'register', component: RegisterView },
    { path: '/market', name: 'market', component: MarketView },
    { path: '/market/:id', name: 'listing', component: ListingView },
    { path: '/sell', name: 'sell', component: SellView },
    { path: '/history', name: 'history', component: HistoryView },
    { path: '/me', name: 'me', component: MeView }
  ]
})

router.beforeEach((to) => {
  if (to.path === '/login' || to.path === '/register') return true
  const token = localStorage.getItem('recycle_ai_token')
  if (token) return true
  return { path: '/login' }
})

export default router
