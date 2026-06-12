import { createRouter, createWebHistory } from "vue-router";
import AuthView from "../views/AuthView.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import StaffDashboard from "../views/StaffDashboard.vue";
import UserDashboard from "../views/UserDashboard.vue";
import { getStoredSession } from "../services/session";

const roleDashboard = {
  admin: "/admin/dashboard",
  staff: "/staff/dashboard",
  user: "/user/dashboard",
};

const routes = [
  {
    path: "/",
    redirect: () => {
      const session = getStoredSession();
      return session.user ? roleDashboard[session.user.role] || "/login" : "/login";
    },
  },
  {
    path: "/login",
    name: "login",
    component: AuthView,
    meta: { guestOnly: true, mode: "login" },
  },
  {
    path: "/register",
    name: "register",
    component: AuthView,
    meta: { guestOnly: true, mode: "register" },
  },
  {
    path: "/admin/dashboard",
    name: "admin-dashboard",
    component: AdminDashboard,
    meta: { role: "admin" },
  },
  {
    path: "/staff/dashboard",
    name: "staff-dashboard",
    component: StaffDashboard,
    meta: { role: "staff" },
  },
  {
    path: "/user/dashboard",
    name: "user-dashboard",
    component: UserDashboard,
    meta: { role: "user" },
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const session = getStoredSession();

  if (to.meta.guestOnly && session.user) {
    return roleDashboard[session.user.role] || "/login";
  }

  if (to.meta.role && (!session.token || !session.user)) {
    return "/login";
  }

  if (to.meta.role && session.user.role !== to.meta.role) {
    return roleDashboard[session.user.role] || "/login";
  }

  return true;
});

export default router;
