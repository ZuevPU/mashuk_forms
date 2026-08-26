#!/bin/sh
set -e
PORT="${PORT:-8000}"
exec gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b "0.0.0.0:${PORT}" app:app
