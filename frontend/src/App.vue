<template>
  <main class="auth-page">
    <section class="auth-shell container">
      <div class="row align-items-center g-4 g-lg-5">
        <div class="col-lg-6">
          <div class="brand-panel">
            <span class="eyebrow">Trekking Management Application</span>
            <h1>Plan cleanly. Trek freely.</h1>
            <p>
              A focused entry point for trekkers, staff, and admins to access
              the platform. Start with login or create a trekker account.
            </p>

            <div class="feature-grid">
              <div class="feature-pill">
                <span>01</span>
                Role based access
              </div>
              <div class="feature-pill">
                <span>02</span>
                Booking readiness
              </div>
              <div class="feature-pill">
                <span>03</span>
                Trek staff workflow
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="auth-card">
            <div class="mode-toggle" role="tablist" aria-label="Authentication mode">
              <button
                type="button"
                class="mode-button"
                :class="{ active: mode === 'login' }"
                @click="setMode('login')"
              >
                Login
              </button>
              <button
                type="button"
                class="mode-button"
                :class="{ active: mode === 'register' }"
                @click="setMode('register')"
              >
                Register
              </button>
            </div>

            <div class="card-heading">
              <span>{{ mode === "login" ? "Welcome back" : "Create trekker account" }}</span>
              <h2>{{ mode === "login" ? "Sign in to continue" : "Join the trail" }}</h2>
            </div>

            <form @submit.prevent="submitForm" novalidate>
              <div v-if="mode === 'register'" class="mb-3">
                <label for="name" class="form-label">Full name</label>
                <input
                  id="name"
                  v-model.trim="form.name"
                  type="text"
                  class="form-control glass-input"
                  placeholder="Aarav Sharma"
                  autocomplete="name"
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
                >
              </div>

              <div v-if="message.text" class="alert" :class="messageClass" role="alert">
                {{ message.text }}
              </div>

              <button type="submit" class="btn submit-button w-100" :disabled="isSubmitting">
                <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>
                {{ submitLabel }}
              </button>
            </form>

            <p class="helper-copy">
              {{ mode === "login" ? "New trekker?" : "Already registered?" }}
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
import { loginUser, registerUser } from "./services/authApi";

const emptyForm = () => ({
  name: "",
  email: "",
  password: "",
  phone: "",
});

export default {
  name: "App",
  data() {
    return {
      mode: "login",
      form: emptyForm(),
      isSubmitting: false,
      message: {
        type: "",
        text: "",
      },
    };
  },
  computed: {
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
  methods: {
    setMode(mode) {
      this.mode = mode;
      this.form = emptyForm();
      this.message = { type: "", text: "" };
    },
    toggleMode() {
      this.setMode(this.mode === "login" ? "register" : "login");
    },
    validateForm() {
      if (!this.form.email || !this.form.password) {
        return "Email and password are required.";
      }

      if (this.mode === "register" && !this.form.name) {
        return "Full name is required for registration.";
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

        localStorage.setItem("tma_token", result.token);
        localStorage.setItem("tma_user", JSON.stringify(result.user));

        this.message = {
          type: "success",
          text: `${result.message}. Logged in as ${result.user.name}.`,
        };
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

<style>
:root {
  --forest: #163f34;
  --pine: #0d2b27;
  --mist: rgba(255, 255, 255, 0.72);
  --glass-border: rgba(255, 255, 255, 0.48);
  --ink: #13231f;
  --muted: #5f716b;
  --accent: #2f7f68;
  --accent-strong: #1f5f50;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  color: var(--ink);
  background:
    radial-gradient(circle at top left, rgba(236, 248, 235, 0.95), transparent 32rem),
    linear-gradient(135deg, #eff7f1 0%, #cddfd8 45%, #9bb8ad 100%);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 3rem 0;
  overflow: hidden;
  position: relative;
}

.auth-page::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(145deg, rgba(22, 63, 52, 0.22), transparent 42%),
    url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1800&q=80") center/cover;
  opacity: 0.2;
  z-index: 0;
}

.auth-shell {
  position: relative;
  z-index: 1;
}

.brand-panel {
  color: var(--pine);
  max-width: 36rem;
}

.eyebrow {
  display: inline-flex;
  margin-bottom: 1.25rem;
  padding: 0.45rem 0.8rem;
  border: 1px solid rgba(22, 63, 52, 0.16);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.42);
  backdrop-filter: blur(14px);
  color: var(--accent-strong);
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
}

.brand-panel h1 {
  margin: 0;
  font-size: 5.4rem;
  line-height: 0.95;
  font-weight: 800;
}

.brand-panel p {
  max-width: 33rem;
  margin: 1.35rem 0 0;
  color: #314d45;
  font-size: 1.05rem;
  line-height: 1.8;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.85rem;
  margin-top: 2rem;
}

.feature-pill {
  min-height: 6rem;
  padding: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.52);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.42);
  box-shadow: 0 1rem 2.2rem rgba(21, 55, 48, 0.1);
  backdrop-filter: blur(16px);
  color: var(--pine);
  font-weight: 700;
}

.feature-pill span {
  display: block;
  margin-bottom: 0.55rem;
  color: var(--accent);
  font-size: 0.8rem;
}

.auth-card {
  width: min(100%, 30rem);
  margin-left: auto;
  padding: 1.25rem;
  border: 1px solid var(--glass-border);
  border-radius: 0.75rem;
  background: var(--mist);
  box-shadow: 0 1.4rem 4rem rgba(25, 56, 49, 0.18);
  backdrop-filter: blur(24px);
}

.mode-toggle {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.4rem;
  padding: 0.35rem;
  border: 1px solid rgba(31, 95, 80, 0.14);
  border-radius: 0.55rem;
  background: rgba(255, 255, 255, 0.5);
}

.mode-button {
  min-height: 2.75rem;
  border: 0;
  border-radius: 0.4rem;
  background: transparent;
  color: var(--muted);
  font-weight: 700;
  transition: 160ms ease;
}

.mode-button.active {
  background: var(--pine);
  color: #fff;
  box-shadow: 0 0.75rem 1.4rem rgba(13, 43, 39, 0.22);
}

.card-heading {
  margin: 1.6rem 0 1.35rem;
}

.card-heading span {
  color: var(--accent-strong);
  font-size: 0.86rem;
  font-weight: 800;
  text-transform: uppercase;
}

.card-heading h2 {
  margin: 0.35rem 0 0;
  color: var(--pine);
  font-size: 1.85rem;
  font-weight: 800;
}

.form-label {
  color: #28443d;
  font-size: 0.92rem;
  font-weight: 700;
}

.glass-input {
  min-height: 3rem;
  border: 1px solid rgba(31, 95, 80, 0.18);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.68);
  color: var(--ink);
  box-shadow: none;
}

.glass-input:focus {
  border-color: rgba(47, 127, 104, 0.65);
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 0 0 0.22rem rgba(47, 127, 104, 0.16);
}

.submit-button {
  min-height: 3.15rem;
  border: 0;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, var(--forest), var(--accent));
  color: #fff;
  font-weight: 800;
  box-shadow: 0 1rem 1.8rem rgba(22, 63, 52, 0.24);
}

.submit-button:hover,
.submit-button:focus {
  color: #fff;
  background: linear-gradient(135deg, #0e332b, #236e5b);
}

.submit-button:disabled {
  opacity: 0.72;
}

.helper-copy {
  margin: 1.2rem 0 0;
  color: var(--muted);
  text-align: center;
}

.link-button {
  border: 0;
  background: transparent;
  color: var(--accent-strong);
  font-weight: 800;
}

.alert {
  border: 0;
  border-radius: 0.5rem;
  font-weight: 600;
}

@media (max-width: 991.98px) {
  .auth-page {
    align-items: flex-start;
    padding: 2rem 0;
  }

  .auth-card {
    margin: 0;
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }

  .brand-panel h1 {
    font-size: 3.4rem;
  }
}

@media (max-width: 575.98px) {
  .brand-panel h1 {
    font-size: 2.65rem;
  }
}
</style>
