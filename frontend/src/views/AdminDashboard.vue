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
                    <input v-model="newTrek.name" class="form-control glass-input" required />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Location</label>
                    <input v-model="newTrek.location" class="form-control glass-input" />
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
                    <input type="number" v-model.number="newTrek.duration_days" class="form-control glass-input" min="1" />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Slots</label>
                    <input type="number" v-model.number="newTrek.available_slots" class="form-control glass-input" min="0" />
                  </div>

                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Start Date</label>
                      <input type="date" v-model="newTrek.start_date" class="form-control glass-input" />
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">End Date</label>
                      <input type="date" v-model="newTrek.end_date" class="form-control glass-input" />
                    </div>
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea v-model="newTrek.description" class="form-control glass-input" rows="3"></textarea>
                  </div>

                  <button type="submit" class="btn primary-button mt-2">Create trek</button>
                </form>
              </div>

              <div class="panel-card">
                <h3>Existing Treks</h3>
                <div v-if="treks.length" class="trek-list">
                  <article v-for="trek in treks" :key="trek.id" class="trek-row">
                    <div>
                      <span>{{ trek.location || 'Location pending' }}</span>
                      <strong>{{ trek.name }}</strong>
                      <small>{{ trek.status }} · {{ trek.available_slots }} slots</small>
                    </div>
                    <button type="button" class="btn ghost-button" @click="deleteTrek(trek.id)">Delete</button>
                  </article>
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
                    <input v-model="newStaff.name" class="form-control glass-input" required />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input v-model="newStaff.email" type="email" class="form-control glass-input" required />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Phone</label>
                    <input v-model="newStaff.phone" class="form-control glass-input" />
                  </div>

                  <div class="mb-3">
                    <label class="form-label">Password</label>
                    <input v-model="newStaff.password" type="password" class="form-control glass-input" required />
                  </div>

                  <button type="submit" class="btn primary-button mt-2">Create staff</button>
                </form>
              </div>

              <div class="panel-card">
                <h3>Assign Staff to Trek</h3>
                <div class="mb-3">
                  <label class="form-label">Trek</label>
                  <select v-model.number="assignForm.trekId" class="form-control glass-input">
                    <option disabled value="">Select trek</option>
                    <option v-for="trek in treks" :key="trek.id" :value="trek.id">{{ trek.name }}</option>
                  </select>
                </div>

                <div class="mb-3">
                  <label class="form-label">Staff</label>
                  <select v-model.number="assignForm.staffId" class="form-control glass-input">
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
                <article v-for="booking in bookings" :key="booking.id" class="trek-row">
                  <div>
                    <span>{{ booking.trek?.name || 'Unknown trek' }}</span>
                    <strong>{{ booking.user?.name || 'Unknown user' }}</strong>
                    <small>{{ booking.status }} · {{ booking.payment_status }}</small>
                  </div>
                  <b>{{ booking.booking_date }}</b>
                </article>
              </div>
              <div v-else class="empty-panel">No bookings available.</div>
            </div>
          </div>

          <div v-if="activePanel === 'users'">
            <div class="panel-grid">
              <div class="panel-card">
                <h3>Users</h3>
                <div v-if="users.length" class="trek-list">
                  <article v-for="user in users" :key="user.id" class="trek-row">
                    <div>
                      <span>{{ user.email }}</span>
                      <strong>{{ user.name }}</strong>
                      <small>{{ user.role }}</small>
                    </div>
                    <b>{{ user.is_active ? 'Active' : 'Inactive' }}</b>
                  </article>
                </div>
                <div v-else class="empty-panel">No users found.</div>
              </div>
              <div class="panel-card">
                <h3>Staff</h3>
                <div v-if="staffMembers.length" class="trek-list">
                  <article v-for="staff in staffMembers" :key="staff.id" class="trek-row">
                    <div>
                      <span>{{ staff.email }}</span>
                      <strong>{{ staff.name }}</strong>
                      <small>{{ staff.phone || 'No phone' }}</small>
                    </div>
                    <b>{{ staff.is_active ? 'Active' : 'Inactive' }}</b>
                  </article>
                </div>
                <div v-else class="empty-panel">No staff found.</div>
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
} from "../services/adminApi";
import { clearStoredSession, getStoredSession } from "../services/session";

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
      activePanel: "treks",
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
          return "Trek management";
        case "staff":
          return "Staff management";
        case "bookings":
          return "Booking overview";
        case "users":
          return "User and staff lists";
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
    logout() {
      clearStoredSession();
      this.$router.push("/login");
    },
  },
};
</script>
