<template>
  <router-view />
</template>

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

.app-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding: 3rem 0;
  overflow: hidden;
  position: relative;
}

.app-page::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(145deg, rgba(22, 63, 52, 0.22), transparent 42%),
    url("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1800&q=80") center/cover;
  opacity: 0.2;
  z-index: 0;
}

.auth-shell,
.dashboard-shell {
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

.auth-card,
.dashboard-card {
  border: 1px solid var(--glass-border);
  border-radius: 0.75rem;
  background: var(--mist);
  box-shadow: 0 1.4rem 4rem rgba(25, 56, 49, 0.18);
  backdrop-filter: blur(24px);
}

.auth-card {
  width: min(100%, 30rem);
  margin-left: auto;
  padding: 1.25rem;
}

.dashboard-card {
  padding: 1.25rem;
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

.card-heading,
.section-heading {
  margin-bottom: 1.35rem;
}

.card-heading {
  margin-top: 1.6rem;
}

.card-heading span,
.section-heading span,
.stat-card span,
.action-item span,
.quick-row span,
.trek-row span {
  color: var(--accent-strong);
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
}

.card-heading h2,
.section-heading h2 {
  margin: 0.35rem 0 0;
  color: var(--pine);
  font-weight: 800;
}

.card-heading h2 {
  font-size: 1.85rem;
}

.section-heading h2 {
  font-size: 1.45rem;
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

.primary-button {
  min-height: 3.15rem;
  border: 0;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, var(--forest), var(--accent));
  color: #fff;
  font-weight: 800;
  box-shadow: 0 1rem 1.8rem rgba(22, 63, 52, 0.24);
}

.primary-button:hover,
.primary-button:focus {
  color: #fff;
  background: linear-gradient(135deg, #0e332b, #236e5b);
}

.primary-button:disabled {
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

.loading-copy {
  margin: 0 0 1rem;
  color: var(--muted);
  font-weight: 700;
}

.dashboard-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 1.35rem;
}

.dashboard-header h1 {
  margin: 0;
  color: var(--pine);
  font-size: 3.25rem;
  line-height: 1;
  font-weight: 800;
}

.dashboard-header p {
  max-width: 40rem;
  margin: 0.8rem 0 0;
  color: #314d45;
  line-height: 1.7;
}

.ghost-button {
  min-height: 2.75rem;
  padding: 0 1.1rem;
  border: 1px solid rgba(31, 95, 80, 0.18);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.54);
  color: var(--accent-strong);
  font-weight: 800;
}

.ghost-button:hover,
.ghost-button:focus {
  border-color: rgba(31, 95, 80, 0.32);
  background: rgba(255, 255, 255, 0.78);
  color: var(--pine);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.85rem;
}

.stat-card,
.management-panel,
.action-item {
  border: 1px solid rgba(255, 255, 255, 0.52);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.42);
  box-shadow: 0 1rem 2.2rem rgba(21, 55, 48, 0.1);
  backdrop-filter: blur(16px);
}

.stat-card {
  min-height: 8.5rem;
  padding: 1.15rem;
}

.stat-card strong {
  display: block;
  margin-top: 0.45rem;
  color: var(--pine);
  font-size: 2.5rem;
  line-height: 1;
}

.stat-card small,
.action-item small,
.trek-row small {
  display: block;
  margin-top: 0.75rem;
  color: var(--muted);
  line-height: 1.5;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 0.85rem;
  margin-top: 0.85rem;
}

.management-panel {
  padding: 1.15rem;
}

.action-list,
.trek-list,
.quick-stack {
  display: grid;
  gap: 0.85rem;
}

.action-list {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.panel-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
}

.panel-card {
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.52);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.42);
  box-shadow: 0 1rem 2.2rem rgba(21, 55, 48, 0.1);
  backdrop-filter: blur(16px);
}

.panel-card h3 {
  margin: 0 0 1.25rem 0;
  color: var(--pine);
  font-size: 1.25rem;
  font-weight: 800;
}

.admin-panel {
  margin-top: 1.25rem;
}

.action-item {
  min-height: 9rem;
  padding: 1rem;
  text-align: left;
  color: var(--pine);
  transition: 160ms ease;
}

.action-item strong {
  display: block;
  margin-top: 0.5rem;
  font-size: 1.05rem;
}

.action-item:hover,
.action-item:focus {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.62);
}

.quick-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem 0;
  border-bottom: 1px solid rgba(31, 95, 80, 0.14);
}

.quick-row:last-child {
  border-bottom: 0;
}

.quick-row strong {
  color: var(--pine);
  text-align: right;
  word-break: break-word;
}

.trek-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid rgba(31, 95, 80, 0.14);
  border-radius: 0.5rem;
  background: rgba(255, 255, 255, 0.44);
}

.trek-row strong {
  display: block;
  margin-top: 0.25rem;
  color: var(--pine);
  font-size: 1.08rem;
}

.trek-row b {
  flex: 0 0 auto;
  padding: 0.4rem 0.65rem;
  border-radius: 999px;
  background: rgba(47, 127, 104, 0.12);
  color: var(--accent-strong);
  font-size: 0.78rem;
  text-transform: uppercase;
}

.empty-panel {
  padding: 1rem;
  border: 1px dashed rgba(31, 95, 80, 0.26);
  border-radius: 0.5rem;
  color: var(--muted);
  font-weight: 700;
}

@media (max-width: 991.98px) {
  .app-page {
    align-items: flex-start;
    padding: 2rem 0;
  }

  .auth-card {
    margin: 0;
  }

  .brand-panel h1 {
    font-size: 3.4rem;
  }

  .dashboard-header {
    flex-direction: column;
  }

  .dashboard-header h1 {
    font-size: 2.6rem;
  }

  .stats-grid,
  .dashboard-grid,
  .action-list,
  .panel-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 575.98px) {
  .brand-panel h1 {
    font-size: 2.65rem;
  }

  .dashboard-card {
    padding: 1rem;
  }

  .dashboard-header h1 {
    font-size: 2rem;
  }

  .quick-row,
  .trek-row {
    align-items: flex-start;
    flex-direction: column;
    gap: 0.25rem;
  }

  .quick-row strong {
    text-align: left;
  }
}
</style>
