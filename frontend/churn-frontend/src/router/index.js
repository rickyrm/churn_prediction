import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../store/auth";

import Login from "../pages/Login-Page.vue";
import Dashboard from "../pages/Dashboard-Page.vue";
import Predictions from "../components/PredictForm.vue";
import Stats from "../pages/Stats-Page.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true } },
  { path: "/predictions", component: Predictions, meta: { requiresAuth: true } },
  { path: "/stats", component: Stats, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Protección de rutas
router.beforeEach((to) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.token) {
    return "/login"; // redirige si no hay token
  }
});

export default router;


