<template>
  <main class="app-page">
    <section class="dashboard-shell container">
      <div class="dashboard-card">
        <header class="dashboard-header">
          <div>
            <span class="eyebrow">Staff Dashboard</span>
            <h1>Trail workbench</h1>
            <p>Review assigned treks, participant counts, and available capacity.</p>
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
              <span>Assigned</span>
              <h2>My Treks</h2>
            </div>

            <div v-if="assignedTreks.length" class="trek-list">
              <article v-for="trek in assignedTreks" :key="trek.id" class="trek-row">
                <div>
                  <span>{{ trek.location || "Location pending" }}</span>
                  <strong>{{ trek.name }}</strong>
                  <small>{{ trek.registered_count }} registered · {{ trek.available_slots }} slots</small>
                </div>
                <b>{{ trek.status || "Pending" }}</b>
              </article>
            </div>

            <div v-else class="empty-panel">
              No treks assigned yet.
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
import { getStaffDashboard } from "../services/staffApi";
import { clearStoredSession, getStoredSession } from "../services/session";

export default {
  name: "StaffDashboard",
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
    };
  },
  computed: {
    assignedTreks() {
      return this.dashboard?.assigned_treks || [];
    },
    stats() {
      const assignedTreks = this.assignedTreks;
      const registeredCount = assignedTreks.reduce((total, trek) => total + (trek.registered_count || 0), 0);
      const availableSlots = assignedTreks.reduce((total, trek) => total + (trek.available_slots || 0), 0);
      const activeTreks = assignedTreks.filter((trek) => trek.status === "Open").length;

      return [
        {
          label: "Assigned",
          value: assignedTreks.length,
          caption: "Treks under you",
        },
        {
          label: "Registered",
          value: registeredCount,
          caption: "Booked participants",
        },
        {
          label: "Open",
          value: activeTreks,
          caption: "Currently active",
        },
        {
          label: "Slots",
          value: availableSlots,
          caption: "Available capacity",
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
        this.dashboard = await getStaffDashboard(this.token);
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
