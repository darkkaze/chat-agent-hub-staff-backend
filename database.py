from sqlmodel import Session, create_engine
from settings import DATABASE_URL, logger

# Create engine with appropriate settings for the database type
if DATABASE_URL.startswith("sqlite"):
    # SQLite settings
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
    )
    logger.info(f"Database engine created: SQLite")
elif DATABASE_URL.startswith("postgresql"):
    # PostgreSQL settings
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
    logger.info(f"Database engine created: PostgreSQL")
else:
    raise ValueError(f"Unsupported database URL: {DATABASE_URL}")


def get_session():
    """Dependency for getting database sessions in FastAPI endpoints."""
    with Session(engine) as session:
        yield session
