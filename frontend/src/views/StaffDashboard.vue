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
              <article v-for="trek in assignedTreks" :key="trek.id" class="trek-row" style="cursor: pointer;" @click="selectTrek(trek)">
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

        <section v-if="selectedTrek" class="management-panel admin-panel mt-4">
          <div class="section-heading">
            <span>Manage Trek</span>
            <h2>{{ selectedTrek.name }}</h2>
          </div>

          <div class="panel-grid">
            <div class="panel-card">
              <h3>Update Trek</h3>
              <form @submit.prevent="updateTrek">
                <div class="mb-3">
                  <label class="form-label">Available Slots</label>
                  <input type="number" v-model.number="editTrek.available_slots" class="form-control glass-input" min="0" required />
                </div>
                <div class="mb-3">
                  <label class="form-label">Status</label>
                  <select v-model="editTrek.status" class="form-control glass-input">
                    <option value="Approved">Approved</option>
                    <option value="Open">Open</option>
                    <option value="Closed">Closed</option>
                    <option value="Completed">Completed</option>
                  </select>
                </div>
                <button type="submit" class="btn primary-button mt-2">Update Trek</button>
              </form>
              
              <div class="mt-4 pt-3 border-top">
                <h3 class="mb-3">Quick Actions</h3>
                <div class="d-flex gap-2">
                  <button type="button" class="btn primary-button flex-fill" @click="startTrek" :disabled="selectedTrek.status === 'Open'">Start Trek</button>
                  <button type="button" class="btn primary-button flex-fill" @click="completeTrek" :disabled="selectedTrek.status === 'Completed'">Complete</button>
                </div>
              </div>
            </div>

            <div class="panel-card">
              <h3>Participants</h3>
              <div v-if="participants.length" class="trek-list">
                <article v-for="participant in participants" :key="participant.booking_id" class="trek-row">
                  <div>
                    <span>{{ participant.user?.email || 'Unknown email' }}</span>
                    <strong>{{ participant.user?.name || 'Unknown user' }}</strong>
                    <small>Payment: {{ participant.payment_status }}</small>
                  </div>
                  <div>
                    <select class="form-control glass-input" style="min-height: 2rem; padding: 0.2rem 0.5rem;" :value="participant.status" @change="updatePStatus(participant.booking_id, $event.target.value)">
                      <option value="Booked">Booked</option>
                      <option value="Completed">Completed</option>
                      <option value="Cancelled">Cancelled</option>
                    </select>
                  </div>
                </article>
              </div>
              <div v-else class="empty-panel">No participants yet.</div>
            </div>
          </div>
        </section>
      </div>
    </section>
  </main>
</template>

<script>
import { 
  getStaffDashboard, 
  updateStaffTrek, 
  getTrekParticipants, 
  updateParticipantStatus, 
  startStaffTrek, 
  completeStaffTrek 
} from "../services/staffApi";
import { clearStoredSession, getStoredSession } from "../services/session";

export default {
  name: "StaffDashboard",
  data() {
    const session = getStoredSession();

    return {
      token: session.token,
      currentUser: session.user || {},
      dashboard: null,
      selectedTrek: null,
      participants: [],
      editTrek: {
        available_slots: 0,
        status: "",
      },
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
        if (this.selectedTrek) {
          const updatedTrek = this.dashboard.assigned_treks.find(t => t.id === this.selectedTrek.id);
          if (updatedTrek) {
            this.selectedTrek = updatedTrek;
          } else {
            this.selectedTrek = null;
          }
        }
      } catch (error) {
        this.message = { text: error.message };
      } finally {
        this.isLoading = false;
      }
    },
    async selectTrek(trek) {
      this.selectedTrek = trek;
      this.editTrek = {
        available_slots: trek.available_slots,
        status: trek.status,
      };
      await this.loadParticipants();
    },
    async loadParticipants() {
      if (!this.selectedTrek) return;
      try {
        const result = await getTrekParticipants(this.token, this.selectedTrek.id);
        this.participants = result.participants || [];
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    async updateTrek() {
      try {
        await updateStaffTrek(this.token, this.selectedTrek.id, this.editTrek);
        this.message = { text: "Trek updated successfully." };
        await this.loadDashboard();
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    async updatePStatus(bookingId, status) {
      try {
        await updateParticipantStatus(this.token, this.selectedTrek.id, bookingId, status);
        await this.loadParticipants();
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    async startTrek() {
      try {
        await startStaffTrek(this.token, this.selectedTrek.id);
        this.message = { text: "Trek started." };
        await this.loadDashboard();
        if (this.selectedTrek) {
          this.editTrek.status = "Open";
        }
      } catch (error) {
        this.message = { text: error.message };
      }
    },
    async completeTrek() {
      try {
        await completeStaffTrek(this.token, this.selectedTrek.id);
        this.message = { text: "Trek completed." };
        await this.loadDashboard();
        if (this.selectedTrek) {
          this.editTrek.status = "Completed";
        }
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
