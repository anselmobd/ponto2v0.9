import { createRouter, createWebHistory } from "vue-router";
import Sobre from '../views/Sobre.vue'
import Bordado from '../views/Bordado.vue'
import Home from '../views/Home.vue'

const routes = [
    {
      path: "/",
      name: "Home",
      component: Home,
    },
    {
      path: "/sobre",
      name: "Sobre",
      component: Sobre,
    },
    {
      path: "/bordado",
      name: "Bordado",
      component: Bordado,
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
  });
  
export default router;
