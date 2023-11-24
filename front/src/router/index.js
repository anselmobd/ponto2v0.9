import { createRouter, createWebHistory } from "vue-router";
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
  
export default router;
