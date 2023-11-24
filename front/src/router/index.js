import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from '@/stores/auth.js';

import Sobre from '../views/Sobre.vue'
import Bordado from '../views/Bordado.vue'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'

const routes = [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/login",
      name: "login",
      component: Login,
    },
    {
      path: "/sobre",
      name: "sobre",
      component: Sobre,
    },
    {
      path: "/bordado",
      name: "bordado",
      component: Bordado,
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
  });

router.beforeEach(async (to, from) => {
  const auth = useAuthStore();
  let autenticado = false;
  if ( auth && auth.user && auth.user.name ) {
    autenticado = true;
  }
  if (
    !autenticado &&
    ['home', 'login', 'sobre'].indexOf(to.name) < 0
  ) {
    return { name: 'home' }
  }
})

export default router;
