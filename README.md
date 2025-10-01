# Backend Staff Timetable

Backend FastAPI para gestión de horarios semanales del personal.

## Features

- CRUD completo de personal
- Gestión de horarios semanales (múltiples turnos por día)
- Autenticación compartida con sistema principal
- Tabla `staff` compartida con sistema POS

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DB_BACKEND=postgres
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=agent_hub
export POSTGRES_USER=your_user
export POSTGRES_PASSWORD=your_password

# Initialize database
python manage.py init_db

# Run server
fastapi dev main.py --port 8002
```

## API Docs

http://localhost:8002/staff-timetable/api/docs

## Deploy

See `../STAFF_TIMETABLE_DEPLOY.md`
