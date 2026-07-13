#!/bin/bash
cd "$(dirname "$0")"

sudo systemctl start redis-server 2>/dev/null || true

cd backend
source venv/bin/activate

celery -A make_celery:celery worker -l error &
CELERY_WORKER_PID=$!

celery -A make_celery:celery beat -l error &
CELERY_BEAT_PID=$!

flask run &
FLASK_PID=$!

cd ../frontend
npm run serve &
FRONTEND_PID=$!

cleanup() {
    kill $CELERY_WORKER_PID 2>/dev/null
    kill $CELERY_BEAT_PID 2>/dev/null
    kill $FLASK_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

wait
