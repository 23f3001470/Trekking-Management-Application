<template>
  <main class="app-page">
    <section class="auth-shell container">
      <div class="row align-items-center g-4 g-lg-5">
        <div class="col-lg-6">
          <div class="brand-panel">
            <span class="eyebrow">Trekking Management Application</span>
            <h1>Plan cleanly. Trek freely.</h1>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="auth-card">
            <div class="mode-toggle" role="tablist" aria-label="Authentication mode">
              <button
                type="button"
                class="mode-button"
                :class="{ active: mode === 'login' }"
                @click="goToMode('login')"
              >
                Login
              </button>
              <button
                type="button"
                class="mode-button"
                :class="{ active: mode === 'register' }"
                @click="goToMode('register')"
              >
                Register
              </button>
            </div>

            <div class="card-heading">
              <span>{{ mode === "login" ? "Welcome back" : "Create account" }}</span>
              <h2>{{ mode === "login" ? "Sign in" : "Join the trail" }}</h2>
            </div>

            <form @submit.prevent="submitForm">
              <div v-if="mode === 'register'" class="mb-3">
                <label for="name" class="form-label">Full name</label>
                <input
                  id="name"
                  v-model.trim="form.name"
                  type="text"
                  class="form-control glass-input"
                  placeholder="Aarav Sharma"
                  autocomplete="name"
                  minlength="3"
                  maxlength="50"
                  required
                >
              </div>

              <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input
                  id="email"
                  v-model.trim="form.email"
                  type="email"
                  class="form-control glass-input"
                  placeholder="you@example.com"
                  autocomplete="email"
                  required
                >
              </div>

              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  id="password"
                  v-model="form.password"
                  type="password"
                  class="form-control glass-input"
                  placeholder="Enter your password"
                  :autocomplete="mode === 'login' ? 'current-password' : 'new-password'"
                  minlength="6"
                  required
                >
              </div>

              <div v-if="mode === 'register'" class="mb-4">
                <label for="phone" class="form-label">Phone number</label>
                <input
                  id="phone"
                  v-model.trim="form.phone"
                  type="tel"
                  class="form-control glass-input"
                  placeholder="+91 98765 43210"
                  autocomplete="tel"
                  pattern="^\+?[0-9\s\-\(\)]+$"
                  title="Enter a valid phone number"
                >
              </div>

              <div v-if="message.text" class="alert" :class="messageClass" role="alert">
                {{ message.text }}
              </div>

              <button type="submit" class="btn primary-button w-100" :disabled="isSubmitting">
                <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
                {{ submitLabel }}
              </button>
            </form>

            <p class="helper-copy">
              {{ mode === "login" ? "New here?" : "Already registered?" }}
              <button type="button" class="link-button" @click="toggleMode">
                {{ mode === "login" ? "Create an account" : "Login instead" }}
              </button>
            </p>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import { loginUser, registerUser } from "../services/authApi";
import { setStoredSession } from "../services/session";

const emptyForm = () => ({
  name: "",
  email: "",
  password: "",
  phone: "",
});

const roleRoute = {
  admin: "/admin/dashboard",
  staff: "/staff/dashboard",
  user: "/user/dashboard",
};

export default {
  name: "AuthView",
  data() {
    return {
      form: emptyForm(),
      isSubmitting: false,
      message: {
        type: "",
        text: "",
      },
    };
  },
  computed: {
    mode() {
      return this.$route.meta.mode || "login";
    },
    submitLabel() {
      if (this.isSubmitting) {
        return this.mode === "login" ? "Signing in..." : "Creating account...";
      }

      return this.mode === "login" ? "Login" : "Register";
    },
    messageClass() {
      return this.message.type === "success" ? "alert-success" : "alert-danger";
    },
  },
  watch: {
    mode() {
      this.form = emptyForm();
      this.message = { type: "", text: "" };
    },
  },
  methods: {
    goToMode(mode) {
      this.$router.push(mode === "login" ? "/login" : "/register");
    },
    toggleMode() {
      this.goToMode(this.mode === "login" ? "register" : "login");
    },
    validateForm() {
      if (!this.form.email || !this.form.password) {
        return "Email and password are required.";
      }

      if (this.mode === "register" && !this.form.name) {
        return "Full name is required.";
      }

      return "";
    },
    async submitForm() {
      const validationError = this.validateForm();

      if (validationError) {
        this.message = { type: "error", text: validationError };
        return;
      }

      this.isSubmitting = true;
      this.message = { type: "", text: "" };

      try {
        const payload =
          this.mode === "login"
            ? {
                email: this.form.email,
                password: this.form.password,
              }
            : {
                name: this.form.name,
                email: this.form.email,
                password: this.form.password,
                phone: this.form.phone,
              };

        const result = this.mode === "login" ? await loginUser(payload) : await registerUser(payload);
        setStoredSession(result.token, result.user);
        this.$router.push(roleRoute[result.user.role] || "/login");
      } catch (error) {
        this.message = {
          type: "error",
          text: error.message,
        };
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
