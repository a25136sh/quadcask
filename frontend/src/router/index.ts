import { createRouter, createWebHistory } from 'vue-router'
import Storage from '../views/Storage.vue'
import Wishlist from '../views/Wishlist.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'storage',
      component: Storage,
    },
    {
      path: '/wishlist',
      name: 'wishlist',
      component: Wishlist,
    },
  ],
})

export default router
