import { createRouter, createWebHistory } from 'vue-router'
import Chat from '@/components/Chat.vue'
import UserAuth from '@/components/UserAuth.vue'

const routes = [
  {
    path: '/chats/:uri?',
    name: 'Chat',
    component: Chat
},
  { path: '/auth', name: 'UserAuth', component: UserAuth },
  { path: '/', redirect: '/auth' }
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('app_auth_token')
  if (token || to.path === '/auth') next()
  else next('/auth')
})

export default router
