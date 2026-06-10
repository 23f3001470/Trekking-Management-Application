# Trekking Management Application

A simple web app for managing trekking activities. The project is being built with a Flask API, Vue.js frontend, Bootstrap styling, and SQLite.

The app supports three roles:

- Admin
- Trek Staff
- User or Trekker

Right now, the backend APIs are present and the frontend has the login/register page.

## Project Structure

```text
trekking-23f3001470/
  backend/
    app.py
    API.md
    requirements.txt
    models/
    routes/
    seeders/
  frontend/
    package.json
    vue.config.js
    src/
```

## Run The Backend

Open a terminal in the project root.

```bash
cd trekking-23f3001470/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The backend runs at:

```text
http://127.0.0.1:5000
```

The database is created automatically when the Flask app starts.

Default seeded admin:

```text
Email: admin@trekapp.com
Password: Admin@123
```

## Run The Frontend

Open another terminal in the project root.

```bash
cd trekking-23f3001470/frontend
npm install
npm run serve
```

The Vue app will show the local URL in the terminal, usually:

```text
http://localhost:8080
```

The frontend proxies `/auth` requests to the Flask backend, so keep the backend running while using login or register.
