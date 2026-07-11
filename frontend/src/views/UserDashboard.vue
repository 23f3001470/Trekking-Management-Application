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
              <span>Explore & Manage</span>
              <h2>My Activities</h2>
            </div>

            <div class="action-list">
              <button
                type="button"
                class="action-item"
                :class="{ active: activePanel === 'treks' }"
                @click="activePanel = 'treks'"
              >
                <span>Treks</span>
                <strong>Find Treks</strong>
                <small>Search and book upcoming treks.</small>
              </button>
              <button
                type="button"
                class="action-item"
                :class="{ active: activePanel === 'bookings' }"
                @click="activePanel = 'bookings'"
              >
                <span>Bookings</span>
                <strong>My Bookings</strong>
                <small>View status of your upcoming treks.</small>
              </button>
              <button
                type="button"
                class="action-item"
                :class="{ active: activePanel === 'history' }"
                @click="activePanel = 'history'"
              >
                <span>History</span>
                <strong>Past Treks</strong>
                <small>View your completed treks.</small>
              </button>
              <button
                type="button"
                class="action-item"
                :class="{ active: activePanel === 'profile' }"
                @click="activePanel = 'profile'"
              >
                <span>Profile</span>
                <strong>Edit Profile</strong>
                <small>Update your account details.</small>
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

        <section class="management-panel admin-panel mt-4">
          <div class="section-heading">
            <span>User Space</span>
            <h2>{{ panelTitle }}</h2>
          </div>

          <div v-if="activePanel === 'treks'">
            <div class="panel-card">
              <h3>Available Treks</h3>
              <div class="mb-3">
                <input v-model="trekSearchQuery" @input="searchTreks" type="text" class="form-control glass-input" placeholder="Search treks by name or location..." />
              </div>
              <div v-if="availableTreks.length" class="trek-list">
                <article v-for="trek in availableTreks" :key="trek.id" class="trek-row">
                  <div>
                    <span>{{ trek.location }}</span>
                    <strong>{{ trek.name }}</strong>
                    <small>Slots remaining: {{ trek.slots_remaining ?? trek.available_slots }} · Duration: {{ trek.duration_days }} days</small>
                  </div>
                  <div class="d-flex gap-2">
                    <b>{{ trek.status }}</b>
                    <button type="button" class="btn primary-button" style="padding: 0.2rem 0.5rem; min-height: 2rem;" @click="bookTrek(trek.id)">Book</button>
                  </div>
                </article>
              </div>
              <div v-else class="empty-panel">No treks available right now.</div>
            </div>
          </div>

          <div v-if="activePanel === 'bookings'">
            <div class="panel-card">
              <h3>My Bookings</h3>
              <div v-if="myBookingsList.length" class="trek-list">
                <article v-for="booking in myBookingsList" :key="booking.id || booking.booking_id" class="trek-row">
                  <div>
                    <span>{{ booking.trek?.location || booking.location || "Location pending" }}</span>
                    <strong>{{ booking.trek?.name || booking.name || "Trek booking" }}</strong>
                    <small>{{ booking.booking_date || "Date pending" }} · Payment: {{ booking.payment_status || "Pending" }}</small>
                  </div>
                  <b>{{ booking.status || "Pending" }}</b>
                </article>
              </div>
              <div v-else class="empty-panel">No active bookings yet.</div>
            </div>
          </div>

          <div v-if="activePanel === 'history'">
            <div class="panel-card">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h3 class="mb-0">Trekking History</h3>
                <button type="button" class="btn ghost-button" @click="exportHistory">Export to CSV</button>
              </div>
              <div v-if="history.length" class="trek-list">
                <article v-for="booking in history" :key="booking.id || booking.booking_id" class="trek-row">
                  <div>
                    <span>{{ booking.trek?.location || booking.location || "Location pending" }}</span>
                    <strong>{{ booking.trek?.name || booking.name || "Trek booking" }}</strong>
                    <small>Completed on: {{ booking.trek?.end_date || "Unknown" }}</small>
                  </div>
                  <b>{{ booking.status }}</b>
                </article>
              </div>
              <div v-else class="empty-panel">No completed treks yet.</div>
            </div>
          </div>

          <div v-if="activePanel === 'profile'">
            <div class="panel-grid">
              <div class="panel-card">
                <h3>Edit Profile</h3>
                <form @submit.prevent="saveProfile">
                  <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input v-model="profileForm.name" class="form-control glass-input" minlength="3" maxlength="50" required />
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Phone</label>
                    <input v-model="profileForm.phone" type="tel" class="form-control glass-input" pattern="^\+?[0-9\s\-\(\)]+$" title="Enter a valid phone number" />
                  </div>
                  <div class="mb-3">
                    <label class="form-label">New Password (leave blank to keep current)</label>
                    <input type="password" v-model="profileForm.password" class="form-control glass-input" minlength="6" />
                  </div>
                  <button type="submit" class="btn primary-button mt-2">Save Profile</button>
                </form>
              </div>
            </div>
          </div>
        </section>
      </div>
    </section>
  </main>
</template>

<script>
import { 
  getUserDashboard, 
  getUserTreks, 
  bookTrek, 
  getUserBookings, 
  getUserHistory, 
  updateProfile, 
  searchUserTreks,
  exportUserHistory
} from "../services/userApi";
import { clearStoredSession, getStoredSession, setStoredSession } from "../services/session";

export default {
  name: "UserDashboard",
  data() {
    const session = getStoredSession();

    return {
      token: session.token,
      currentUser: session.user || {},
      dashboard: null,
      activePanel: "treks",
      availableTreks: [],
      myBookingsList: [],
      history: [],
      trekSearchQuery: "",
      profileForm: {
        name: session.user?.name || "",
        phone: session.user?.phone || "",
        password: "",
      },
      isLoading: false,
      message: {
        text: "",
      },
    };
  },
  computed: {
    panelTitle() {
      switch (this.activePanel) {
        case "treks":
          return "Find Treks";
        case "bookings":
          return "My Bookings";
        case "history":
          return "Trekking History";
        case "profile":
          return "Edit Profile";
        default:
          return "User Space";
      }
    },
    bookings() {
      return (
        this.dashboard?.bookings ||
        this.dashboard?.my_bookings ||
        this.dashboard?.upcoming_bookings ||
        this.dashboard?.upcoming ||
        this.myBookingsList ||
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
        this.history.length;
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
    this.loadAllData();
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
    async loadAllData() {
      try {
        const [treksRes, bookingsRes, historyRes] = await Promise.all([
          getUserTreks(this.token),
          getUserBookings(this.token),
          getUserHistory(this.token)
        ]);
        this.availableTreks = treksRes.treks || treksRes.available_treks || [];
        this.myBookingsList = bookingsRes.bookings || bookingsRes.my_bookings || [];
        this.history = historyRes.history || historyRes.past_bookings || [];
      } catch (error) {
        console.error(error);
      }
    },
    async searchTreks() {
      try {
        if (!this.trekSearchQuery.trim()) {
          const res = await getUserTreks(this.token);
          this.availableTreks = res.treks || res.available_treks || [];
          return;
        }
        const res = await searchUserTreks(this.token, this.trekSearchQuery);
        this.availableTreks = res.treks || res.results || [];
      } catch (error) {
        console.error(error);
      }
    },
    async bookTrek(trekId) {
      try {
        await bookTrek(this.token, trekId);
        this.message = { text: "Trek booked successfully!" };
        await this.loadAllData();
        await this.loadDashboard();
        this.activePanel = 'bookings';
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    async saveProfile() {
      try {
        const payload = {
          name: this.profileForm.name,
          phone: this.profileForm.phone,
        };
        if (this.profileForm.password) {
          payload.password = this.profileForm.password;
        }
        const result = await updateProfile(this.token, payload);
        
        // Update current user data locally
        if (result.user) {
          this.currentUser = { ...this.currentUser, ...result.user };
          setStoredSession(this.token, this.currentUser);
        }
        
        this.message = { text: "Profile updated successfully." };
        this.profileForm.password = "";
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    async exportHistory() {
      try {
        const res = await exportUserHistory(this.token);
        this.message = { text: res.message || "Export started." };
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    logout() {
      clearStoredSession();
      this.$router.push("/login");
    },
  },
};
</script>
