<template>
  <main class="app-page">
    <section class="dashboard-shell container">
      <div class="dashboard-card">
        <header class="dashboard-header">
          <div>
            <span class="eyebrow">Admin Dashboard</span>
            <h1>Welcome, {{ currentUser.name }}</h1>
            <p>Track platform activity, bookings, treks, and team capacity.</p>
          </div>

          <button type="button" class="btn ghost-button" @click="logout">
            Logout
          </button>
        </header>

        <div v-if="message.text" class="alert alert-danger" role="alert">
          {{ message.text }}
        </div>

        <p v-if="isLoading" class="loading-copy">Loading dashboard...</p>

        <div class="stats-grid">
          <div v-for="stat in stats" :key="stat.label" class="stat-card">
            <span>{{ stat.label }}</span>
            <strong>{{ stat.value }}</strong>
            <small>{{ stat.caption }}</small>
          </div>
        </div>

        <div class="dashboard-grid">
          <section class="management-panel">
            <div class="section-heading">
              <span>Manage</span>
              <h2>Operations</h2>
            </div>

            <div class="action-list">
              <button v-for="action in actions" :key="action.title" type="button" class="action-item">
                <span>{{ action.kicker }}</span>
                <strong>{{ action.title }}</strong>
                <small>{{ action.text }}</small>
              </button>
            </div>
          </section>

          <section class="management-panel">
            <div class="section-heading">
              <span>Profile</span>
              <h2>Quick View</h2>
            </div>

            <div class="quick-stack">
              <div class="quick-row">
                <span>Email</span>
                <strong>{{ currentUser.email }}</strong>
              </div>
              <div class="quick-row">
                <span>Role</span>
                <strong>{{ currentUser.role }}</strong>
              </div>
              <div class="quick-row">
                <span>Status</span>
                <strong>{{ currentUser.is_active ? "Active" : "Inactive" }}</strong>
              </div>
            </div>
          </section>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import { getAdminDashboard } from "../services/adminApi";
import { clearStoredSession, getStoredSession } from "../services/session";

export default {
  name: "AdminDashboard",
  data() {
    const session = getStoredSession();

    return {
      token: session.token,
      currentUser: session.user || {},
      dashboard: null,
      isLoading: false,
      message: {
        text: "",
      },
      actions: [
        {
          kicker: "Treks",
          title: "Manage treks",
          text: "Create, update, and review trek inventory.",
        },
        {
          kicker: "Staff",
          title: "Assign teams",
          text: "Coordinate trek staff and ownership.",
        },
        {
          kicker: "Bookings",
          title: "Review bookings",
          text: "Monitor demand and booking volume.",
        },
      ],
    };
  },
  computed: {
    stats() {
      const data = this.dashboard || {};

      return [
        {
          label: "Treks",
          value: data.total_treks ?? "0",
          caption: "Listed experiences",
        },
        {
          label: "Trekkers",
          value: data.total_users ?? "0",
          caption: "Registered users",
        },
        {
          label: "Staff",
          value: data.total_staff ?? "0",
          caption: "Team members",
        },
        {
          label: "Bookings",
          value: data.total_bookings ?? "0",
          caption: "Total reservations",
        },
      ];
    },
  },
  mounted() {
    this.loadDashboard();
  },
  methods: {
    async loadDashboard() {
      this.isLoading = true;
      this.message = { text: "" };

      try {
        this.dashboard = await getAdminDashboard(this.token);
      } catch (error) {
        this.message = { text: error.message };
      } finally {
        this.isLoading = false;
      }
    },
    logout() {
      clearStoredSession();
      this.$router.push("/login");
    },
  },
};
</script>
