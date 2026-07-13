# Trekking Management Application

A complete, production-ready web application designed to manage trekking activities seamlessly. It is built with a powerful Flask backend, a modern Vue.js frontend, and a highly responsive design.

The application serves three distinct roles with their own dedicated dashboards:
- **Admin**: Create treks, assign staff, oversee all bookings, and manage all user accounts.
- **Trek Staff**: View assigned treks, manage trek statuses (Open, Closed, Completed), and update participant statuses.
- **User/Trekker**: Search available treks, book slots, view trekking history, and export booking history as a CSV.

## Key Features

- **Robust State Management**: Strict backend validations prevent illogical booking states (e.g., booking a closed trek or refunding a completed trek).
- **Automated Tasks**: Integrated with Celery & Redis to handle daily automated reminders, monthly admin reports, and asynchronous CSV exports.
- **Pagination**: Clean frontend UI with built-in pagination for long lists of users, staff, and treks.
- **Secure Authentication**: Token-based authentication with role-based access control and active session invalidation for deactivated users.

## Project Structure

```text
/
  start.sh              # Single entry point script to run everything
  backend/              # Flask API, Celery Workers, SQLite DB, Pytest Suite
  frontend/             # Vue.js PWA with Bootstrap styling
```

## Quick Start

You don't need to manually start the frontend, backend, or task queues separately. We've included a handy bash script that runs the entire stack concurrently.

1. Ensure you have `redis-server` running in the background (required for Celery and Caching).
2. Open a terminal in the project root.
3. Run the startup script:

```bash
./start.sh
```

This will automatically:
- Start the Flask backend on `http://127.0.0.1:5000`
- Start the Vue.js frontend on `http://localhost:8080`
- Boot up the Celery Worker and Beat Scheduler for background tasks.

### Default Accounts

On the very first startup, the application automatically seeds the following Admin account so you can log in immediately:

- **Email**: `23f3001470@ds.study.iitm.ac.in`
- **Password**: `password`

### Generating Fake Data
If you want to populate the database with a massive list of fake treks, users, and bookings for testing purposes, you can manually run the seeder script from the root directory while the virtual environment is active:

```bash
python3 backend/seeders/seeder.py
```
*(Warning: This will drop the existing database and generate a fresh dataset!)*

## Testing

The backend includes a comprehensive `pytest` suite ensuring all validations, state transitions, and background tasks work correctly. To run the test suite:

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```
