#!/bin/bash
set -e

case "$1" in
  "fastapi")
    exec fastapi run main.py --host 0.0.0.0 --port 8002
    ;;
  "manage_init_db")
    exec python manage.py init_db
    ;;
  "manage")
    shift
    exec python manage.py "$@"
    ;;
  *)
    exec "$@"
    ;;
esac
