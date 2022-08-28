import { createRouter, createWebHistory } from "vue-router";

import { useAuthStore } from "@/stores";
import { HomeView, LoginView, SignupView, ProfileView, PlanMealView, RecommendationView, PastDaysView, ServerErrorView } from "@/views";

export const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
    },
    {
      path: "/signup",
      name: "signup",
      component: SignupView,
    },
    {
      path: "/profile",
      name: "profile",
      component: ProfileView,
    },
    {
      path: "/plan",
      name: "plan",
      component: PlanMealView,
    },
    {
      path: "/recommendation/:mealType",
      name: "recommendation",
      component: RecommendationView,
      props: true
    },
    {
      path: "/past",
      name: "past",
      component: PastDaysView
    },
    {
      path: "/error",
      name: "server-error",
      component: ServerErrorView
    },
  ],
});

router.beforeEach(async (to) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ["/login", "/signup"];
  const authRequired = !publicPages.includes(to.path);
  const auth = useAuthStore();

  if (authRequired && !auth.user) {
    auth.returnUrl = to.fullPath;
    return "/login";
  }
});
