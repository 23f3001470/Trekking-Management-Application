<template>
  <main class="app-page">
    <section class="dashboard-shell container">
      <div class="dashboard-card">
        <header class="dashboard-header">
          <div>
            <span class="eyebrow">User Dashboard</span>
            <h1>Your trek space</h1>
            <p>Review bookings, upcoming plans, and account details.</p>
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
              <span>Bookings</span>
              <h2>My Treks</h2>
            </div>

            <div v-if="bookings.length" class="trek-list">
              <article v-for="booking in bookings" :key="booking.id || booking.booking_id" class="trek-row">
                <div>
                  <span>{{ booking.trek?.location || booking.location || "Location pending" }}</span>
                  <strong>{{ booking.trek?.name || booking.name || "Trek booking" }}</strong>
                  <small>{{ booking.booking_date || "Date pending" }} · {{ booking.payment_status || "Payment pending" }}</small>
                </div>
                <b>{{ booking.status || "Pending" }}</b>
              </article>
            </div>

            <div v-else class="empty-panel">
              No bookings yet.
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
                <span>Phone</span>
                <strong>{{ currentUser.phone || "Not added" }}</strong>
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
import { getUserDashboard } from "../services/userApi";
import { clearStoredSession, getStoredSession } from "../services/session";

export default {
  name: "UserDashboard",
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
    bookings() {
      return (
        this.dashboard?.bookings ||
        this.dashboard?.my_bookings ||
        this.dashboard?.upcoming_bookings ||
        this.dashboard?.upcoming ||
        []
      );
    },
    stats() {
      const bookings = this.bookings;
      const upcomingCount =
        this.dashboard?.upcoming_count ??
        this.dashboard?.upcoming_bookings?.length ??
        bookings.filter((booking) => booking.status !== "Completed" && booking.status !== "Cancelled").length;
      const completedCount =
        this.dashboard?.completed_count ??
        this.dashboard?.past_bookings?.length ??
        bookings.filter((booking) => booking.status === "Completed").length;
      const paidCount = bookings.filter((booking) => booking.payment_status === "Paid").length;

      return [
        {
          label: "Bookings",
          value: bookings.length,
          caption: "Total reservations",
        },
        {
          label: "Upcoming",
          value: upcomingCount,
          caption: "Treks ahead",
        },
        {
          label: "Completed",
          value: completedCount,
          caption: "Finished treks",
        },
        {
          label: "Paid",
          value: paidCount,
          caption: "Confirmed payments",
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
        this.dashboard = await getUserDashboard(this.token);
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
