<template>
  <main class="app-page">
    <section class="dashboard-shell container">
      <div class="dashboard-card">
        <header class="dashboard-header">
          <div>
            <span class="eyebrow">Admin Dashboard</span>
            <h1>Welcome, {{ currentUser.name }}</h1>
            <p>Review and manage treks, staff, bookings, and users.</p>
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
              <h2>Administration</h2>
            </div>

            <div class="action-list">
              <button
                type="button"
                class="action-item"
                :class="{ active: activePanel === 'treks' }"
                @click="activePanel = 'treks'"
              >
                <span>Treks</span>
                <strong>Manage routes</strong>
                <small>Create treks, assign staff, and delete routes.</small>
              </button>
              <button
                type="button"
                class="action-item"
                :class="{ active: activePanel === 'staff' }"
                @click="activePanel = 'staff'"
              >
                <span>Staff</span>
                <strong>Add staff</strong>
                <small>Create staff members and view team assignments.</small>
              </button>
              <button
                type="button"
                class="action-item"
                :class="{ active: activePanel === 'bookings' }"
                @click="activePanel = 'bookings'"
              >
                <span>Bookings</span>
                <strong>Review bookings</strong>
                <small>View all reservations across treks.</small>
              </button>
              <button
                type="button"
                class="action-item"
                :class="{ active: activePanel === 'users' }"
                @click="activePanel = 'users'"
              >
                <span>Users</span>
                <strong>Manage accounts</strong>
                <small>Search and activate/deactivate users.</small>
              </button>
              <button
                type="button"
                class="action-item"
                :class="{ active: activePanel === 'analytics' }"
                @click="activePanel = 'analytics'"
              >
                <span>Analytics</span>
                <strong>View insights</strong>
                <small>See popular treks and user participation.</small>
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

        <section class="management-panel admin-panel">
          <div class="section-heading">
            <span>Admin tools</span>
            <h2>{{ panelTitle }}</h2>
          </div>

          <div v-if="activePanel === 'treks'">
            <div class="panel-grid">
              <div class="panel-card">
                <h3>Create Trek Route</h3>
                <form @submit.prevent="createTrek">
                  <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input v-model="newTrek.name" class="form-control glass-input" minlength="3" maxlength="100" required />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Location</label>
                    <input v-model="newTrek.location" class="form-control glass-input" minlength="3" maxlength="100" required />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Difficulty</label>
                    <select v-model="newTrek.difficulty" class="form-control glass-input">
                      <option value="Easy">Easy</option>
                      <option value="Moderate">Moderate</option>
                      <option value="Hard">Hard</option>
                    </select>
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Duration (days)</label>
                    <input type="number" v-model.number="newTrek.duration_days" class="form-control glass-input" min="1" required />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Slots</label>
                    <input type="number" v-model.number="newTrek.available_slots" class="form-control glass-input" min="1" required />
                  </div>

                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Start Date</label>
                      <input type="date" v-model="newTrek.start_date" class="form-control glass-input" required />
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">End Date</label>
                      <input type="date" v-model="newTrek.end_date" class="form-control glass-input" required />
                    </div>
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea v-model="newTrek.description" class="form-control glass-input" rows="3" required></textarea>
                  </div>

                  <button type="submit" class="btn primary-button mt-2">Create trek</button>
                </form>
              </div>

              <div class="panel-card">
                <h3>Existing Treks</h3>
                <div class="mb-3">
                  <input v-model="trekSearchQuery" @input="searchTreks" type="text" class="form-control glass-input" placeholder="Search treks by name or location..." />
                </div>
                <div v-if="treks.length" class="trek-list">
                  <article v-for="trek in paginatedTreks" :key="trek.id" class="trek-row">
                    <div>
                      <span>{{ trek.location || 'Location pending' }}</span>
                      <strong>{{ trek.name }}</strong>
                      <small>{{ trek.status }} · {{ trek.available_slots }} slots</small>
                    </div>
                    <button type="button" class="btn ghost-button" @click="deleteTrek(trek.id)">Delete</button>
                  </article>
                  <div v-if="treks.length > pageSize" class="d-flex justify-content-between align-items-center mt-3">
                    <button type="button" class="btn ghost-button" :disabled="treksPage === 1" @click="treksPage--">Previous</button>
                    <small>Page {{ treksPage }} of {{ totalTreksPages }}</small>
                    <button type="button" class="btn ghost-button" :disabled="treksPage === totalTreksPages" @click="treksPage++">Next</button>
                  </div>
                </div>
                <div v-else class="empty-panel">No treks found.</div>
              </div>
            </div>
          </div>

          <div v-if="activePanel === 'staff'">
            <div class="panel-grid">
              <div class="panel-card">
                <h3>Add Trek Staff</h3>
                <form @submit.prevent="createStaff">
                  <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input v-model="newStaff.name" class="form-control glass-input" minlength="3" maxlength="50" required />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input v-model="newStaff.email" type="email" class="form-control glass-input" required />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Phone</label>
                    <input v-model="newStaff.phone" type="tel" class="form-control glass-input" pattern="^\+?[0-9\s\-\(\)]+$" title="Enter a valid phone number" />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Password</label>
                    <input v-model="newStaff.password" type="password" class="form-control glass-input" minlength="6" required />
                  </div>

                  <button type="submit" class="btn primary-button mt-2">Create staff</button>
                </form>
              </div>

              <div class="panel-card">
                <h3>Assign Staff to Trek</h3>
                <div class="mb-3">
                  <label class="form-label">Trek</label>
                  <select v-model.number="assignForm.trekId" class="form-control glass-input" required>
                    <option disabled value="">Select trek</option>
                    <option v-for="trek in treks" :key="trek.id" :value="trek.id">{{ trek.name }}</option>
                  </select>
                </div>

                <div class="mb-3">
                  <label class="form-label">Staff</label>
                  <select v-model.number="assignForm.staffId" class="form-control glass-input" required>
                    <option disabled value="">Select staff</option>
                    <option v-for="member in staffMembers" :key="member.id" :value="member.id">{{ member.name }}</option>
                  </select>
                </div>

                <button type="button" class="btn primary-button mt-2" @click="assignStaff">Assign staff</button>
              </div>
            </div>
          </div>

          <div v-if="activePanel === 'bookings'">
            <div class="panel-card">
              <h3>Recent Bookings</h3>
              <div v-if="bookings.length" class="trek-list">
                <article v-for="booking in paginatedBookings" :key="booking.id" class="trek-row">
                  <div>
                    <span>{{ booking.trek?.name || 'Unknown trek' }}</span>
                    <strong>{{ booking.user?.name || 'Unknown user' }}</strong>
                    <small>{{ booking.status }} · {{ booking.payment_status }}</small>
                  </div>
                  <b>{{ booking.booking_date }}</b>
                </article>
                <div v-if="bookings.length > pageSize" class="d-flex justify-content-between align-items-center mt-3">
                  <button type="button" class="btn ghost-button" :disabled="bookingsPage === 1" @click="bookingsPage--">Previous</button>
                  <small>Page {{ bookingsPage }} of {{ totalBookingsPages }}</small>
                  <button type="button" class="btn ghost-button" :disabled="bookingsPage === totalBookingsPages" @click="bookingsPage++">Next</button>
                </div>
              </div>
              <div v-else class="empty-panel">No bookings available.</div>
            </div>
          </div>

          <div v-if="activePanel === 'users'">
            <div class="panel-grid">
              <div class="panel-card">
                <h3>Users</h3>
                <div class="mb-3">
                  <input v-model="userSearchQuery" @input="searchUsers" type="text" class="form-control glass-input" placeholder="Search users by name or email..." />
                </div>
                <div v-if="users.length" class="trek-list">
                  <article v-for="user in paginatedUsers" :key="user.id" class="trek-row">
                    <div>
                      <span>{{ user.email }}</span>
                      <strong>{{ user.name }}</strong>
                      <small>{{ user.role }}</small>
                    </div>
                    <div class="d-flex align-items-center gap-2">
                      <b>{{ user.is_active ? 'Active' : 'Inactive' }}</b>
                      <button v-if="user.is_active" type="button" class="btn ghost-button" style="padding: 0.2rem 0.5rem; min-height: 2rem;" @click="toggleUserStatus(user)">Deactivate</button>
                      <button v-else type="button" class="btn primary-button" style="padding: 0.2rem 0.5rem; min-height: 2rem;" @click="toggleUserStatus(user)">Activate</button>
                    </div>
                  </article>
                  <div v-if="users.length > pageSize" class="d-flex justify-content-between align-items-center mt-3">
                    <button type="button" class="btn ghost-button" :disabled="usersPage === 1" @click="usersPage--">Previous</button>
                    <small>Page {{ usersPage }} of {{ totalUsersPages }}</small>
                    <button type="button" class="btn ghost-button" :disabled="usersPage === totalUsersPages" @click="usersPage++">Next</button>
                  </div>
                </div>
                <div v-else class="empty-panel">No users found.</div>
              </div>
              <div class="panel-card">
                <h3>Staff</h3>
                <div class="mb-3">
                  <input v-model="staffSearchQuery" @input="searchStaff" type="text" class="form-control glass-input" placeholder="Search staff by name or email..." />
                </div>
                <div v-if="staffMembers.length" class="trek-list">
                  <article v-for="staff in paginatedStaff" :key="staff.id" class="trek-row">
                    <div>
                      <span>{{ staff.email }}</span>
                      <strong>{{ staff.name }}</strong>
                      <small>{{ staff.phone || 'No phone' }}</small>
                    </div>
                    <div class="d-flex align-items-center gap-2">
                      <b>{{ staff.is_active ? 'Active' : 'Inactive' }}</b>
                      <button v-if="staff.is_active" type="button" class="btn ghost-button" style="padding: 0.2rem 0.5rem; min-height: 2rem;" @click="toggleUserStatus(staff)">Deactivate</button>
                      <button v-else type="button" class="btn primary-button" style="padding: 0.2rem 0.5rem; min-height: 2rem;" @click="toggleUserStatus(staff)">Activate</button>
                    </div>
                  </article>
                  <div v-if="staffMembers.length > pageSize" class="d-flex justify-content-between align-items-center mt-3">
                    <button type="button" class="btn ghost-button" :disabled="staffPage === 1" @click="staffPage--">Previous</button>
                    <small>Page {{ staffPage }} of {{ totalStaffPages }}</small>
                    <button type="button" class="btn ghost-button" :disabled="staffPage === totalStaffPages" @click="staffPage++">Next</button>
                  </div>
                </div>
                <div v-else class="empty-panel">No staff found.</div>
              </div>
            </div>
          </div>
          
          <div v-show="activePanel === 'analytics'">
            <div class="panel-grid">
              <div class="panel-card">
                <h3>Popular Treks</h3>
                <canvas id="popularTreksChart"></canvas>
              </div>
              <div class="panel-card">
                <h3>User Participation</h3>
                <canvas id="participationChart"></canvas>
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
  getAdminDashboard,
  getAdminTreks,
  createAdminTrek,
  deleteAdminTrek,
  getAdminUsers,
  createAdminStaff,
  assignStaffToTrek,
  getAdminBookings,
  searchAdminUsers,
  searchAdminStaff,
  searchAdminTreks,
  deactivateAdminUser,
  activateAdminUser,
  getAdminAnalytics,
} from "../services/adminApi";
import { clearStoredSession, getStoredSession } from "../services/session";
import Chart from "chart.js/auto";

export default {
  name: "AdminDashboard",
  data() {
    const session = getStoredSession();

    return {
      token: session.token,
      currentUser: session.user || {},
      dashboard: null,
      treks: [],
      staffMembers: [],
      users: [],
      bookings: [],
      analyticsData: null,
      activePanel: "treks",
      pageSize: 5,
      treksPage: 1,
      staffPage: 1,
      usersPage: 1,
      bookingsPage: 1,
      newTrek: {
        name: "",
        location: "",
        difficulty: "Moderate",
        duration_days: 1,
        available_slots: 0,
        status: "Pending",
        start_date: "",
        end_date: "",
        description: "",
      },
      newStaff: {
        name: "",
        email: "",
        phone: "",
        password: "",
      },
      assignForm: {
        trekId: null,
        staffId: null,
      },
      userSearchQuery: "",
      staffSearchQuery: "",
      trekSearchQuery: "",
      isLoading: false,
      message: {
        text: "",
      },
    };
  },
  computed: {
    paginatedTreks() {
      const start = (this.treksPage - 1) * this.pageSize;
      return this.treks.slice(start, start + this.pageSize);
    },
    totalTreksPages() {
      return Math.ceil(this.treks.length / this.pageSize) || 1;
    },
    paginatedStaff() {
      const start = (this.staffPage - 1) * this.pageSize;
      return this.staffMembers.slice(start, start + this.pageSize);
    },
    totalStaffPages() {
      return Math.ceil(this.staffMembers.length / this.pageSize) || 1;
    },
    paginatedUsers() {
      const start = (this.usersPage - 1) * this.pageSize;
      return this.users.slice(start, start + this.pageSize);
    },
    totalUsersPages() {
      return Math.ceil(this.users.length / this.pageSize) || 1;
    },
    paginatedBookings() {
      const start = (this.bookingsPage - 1) * this.pageSize;
      return this.bookings.slice(start, start + this.pageSize);
    },
    totalBookingsPages() {
      return Math.ceil(this.bookings.length / this.pageSize) || 1;
    },
    panelTitle() {
      switch (this.activePanel) {
        case "treks":
          return "Trek management";
        case "staff":
          return "Staff management";
        case "bookings":
          return "Booking overview";
        case "users":
          return "User and staff lists";
        case "analytics":
          return "System analytics";
        default:
          return "Admin tools";
      }
    },
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
    this.loadAllData();
    this.loadAnalytics();
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
    async loadAllData() {
      try {
        const [treksResult, staffResult, usersResult, bookingsResult] = await Promise.all([
          getAdminTreks(this.token),
          getAdminUsers(this.token, "staff"),
          getAdminUsers(this.token, "user"),
          getAdminBookings(this.token),
        ]);

        this.treks = treksResult.treks || [];
        this.staffMembers = staffResult.users || [];
        this.users = usersResult.users || [];
        this.bookings = bookingsResult.bookings || [];
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    async loadAnalytics() {
      try {
        this.analyticsData = await getAdminAnalytics(this.token);
        this.renderCharts();
      } catch (error) {
        console.error("Failed to load analytics", error);
      }
    },
    renderCharts() {
      if (!this.analyticsData) return;
      
      const popularTreksCtx = document.getElementById('popularTreksChart');
      if (popularTreksCtx) {
        new Chart(popularTreksCtx, {
          type: 'bar',
          data: {
            labels: this.analyticsData.popular_treks.map(t => t.name),
            datasets: [{
              label: 'Bookings',
              data: this.analyticsData.popular_treks.map(t => t.count),
              backgroundColor: '#2ecc71',
              borderRadius: 4
            }]
          },
          options: {
            responsive: true,
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
          }
        });
      }

      const participationCtx = document.getElementById('participationChart');
      if (participationCtx) {
        new Chart(participationCtx, {
          type: 'line',
          data: {
            labels: this.analyticsData.user_participation.map(p => p.month),
            datasets: [{
              label: 'Bookings per Month',
              data: this.analyticsData.user_participation.map(p => p.count),
              borderColor: '#3498db',
              backgroundColor: 'rgba(52, 152, 219, 0.2)',
              fill: true,
              tension: 0.3
            }]
          },
          options: {
            responsive: true,
            scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
          }
        });
      }
    },
    async createTrek() {
      try {
        await createAdminTrek(this.token, this.newTrek);
        this.message = { text: "Trek created successfully." };
        this.newTrek = {
          name: "",
          location: "",
          difficulty: "Moderate",
          duration_days: 1,
          available_slots: 0,
          status: "Pending",
          start_date: "",
          end_date: "",
          description: "",
        };
        await this.loadAllData();
        await this.loadDashboard();
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    async createStaff() {
      try {
        await createAdminStaff(this.token, this.newStaff);
        this.message = { text: "Staff created successfully." };
        this.newStaff = { name: "", email: "", phone: "", password: "" };
        await this.loadAllData();
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    async assignStaff() {
      if (!this.assignForm.trekId || !this.assignForm.staffId) {
        this.message = { text: "Please select a trek and a staff member." };
        return;
      }

      try {
        await assignStaffToTrek(this.token, this.assignForm.trekId, this.assignForm.staffId);
        this.message = { text: "Staff assigned successfully." };
        this.assignForm = { trekId: null, staffId: null };
        await this.loadAllData();
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    async deleteTrek(trekId) {
      if (!confirm("Delete this trek route? This action cannot be undone.")) {
        return;
      }

      try {
        await deleteAdminTrek(this.token, trekId);
        this.message = { text: "Trek deleted successfully." };
        await this.loadAllData();
        await this.loadDashboard();
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    async searchUsers() {
      this.usersPage = 1;
      try {
        if (!this.userSearchQuery.trim()) {
          const res = await getAdminUsers(this.token, "user");
          this.users = res.users || [];
          return;
        }
        const res = await searchAdminUsers(this.token, this.userSearchQuery);
        this.users = res.users || [];
      } catch (error) {
        console.error(error);
      }
    },
    async searchStaff() {
      this.staffPage = 1;
      try {
        if (!this.staffSearchQuery.trim()) {
          const res = await getAdminUsers(this.token, "staff");
          this.staffMembers = res.users || [];
          return;
        }
        const res = await searchAdminStaff(this.token, this.staffSearchQuery);
        this.staffMembers = res.users || [];
      } catch (error) {
        console.error(error);
      }
    },
    async searchTreks() {
      this.treksPage = 1;
      try {
        if (!this.trekSearchQuery.trim()) {
          const res = await getAdminTreks(this.token);
          this.treks = res.treks || [];
          return;
        }
        const res = await searchAdminTreks(this.token, this.trekSearchQuery);
        this.treks = res.treks || [];
      } catch (error) {
        console.error(error);
      }
    },
    async toggleUserStatus(user) {
      try {
        if (user.is_active) {
          await deactivateAdminUser(this.token, user.id);
        } else {
          await activateAdminUser(this.token, user.id);
        }
        await this.loadAllData();
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
