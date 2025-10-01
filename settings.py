import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Create logger instance for the application
logger = logging.getLogger("agent_hub_staff_timetable")

# Set third-party loggers to WARNING to reduce noise
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

# Database configuration
DB_BACKEND = os.getenv("DB_BACKEND", "sqlite").lower()

if DB_BACKEND == "sqlite":
    SQLITE_PATH = os.getenv("SQLITE_PATH", "./agent_hub_staff_timetable.db")
    DATABASE_URL = f"sqlite:///{SQLITE_PATH}"
elif DB_BACKEND == "postgres":
    # Required PostgreSQL environment variables
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    if not all([POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD]):
        raise ValueError(
            "PostgreSQL backend requires POSTGRES_HOST, POSTGRES_DB, "
            "POSTGRES_USER, and POSTGRES_PASSWORD environment variables"
        )

    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
else:
    raise ValueError(f"Unsupported DB_BACKEND: {DB_BACKEND}. Use 'sqlite' or 'postgres'")
