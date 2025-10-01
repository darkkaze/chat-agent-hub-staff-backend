#!/usr/bin/env python3
"""
Management commands for Agent Hub Staff Timetable.

Usage:
    python manage.py init_db
    python manage.py update_db
    python manage.py check_db
"""

import sys
from sqlmodel import text
from database import engine, get_session
from settings import logger
from models.staff_models import Staff


def init_db():
    """Initialize Staff table only (auth tables already exist)."""
    logger.info("Creating Staff table if it doesn't exist...")

    # Only create Staff table
    Staff.__table__.create(engine, checkfirst=True)
    logger.info(f"✓ Created/verified table: {Staff.__tablename__}")

    logger.info("Staff table created successfully")


def check_db():
    """Check database connection and tables."""
    try:
        with next(get_session()) as session:
            # Check for PostgreSQL
            result = session.exec(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
            tables = result.fetchall()
            logger.info(f"Database connected. Found {len(tables)} tables: {[t[0] for t in tables]}")
    except Exception as e:
        # Try SQLite format
        try:
            with next(get_session()) as session:
                result = session.exec(text("SELECT name FROM sqlite_master WHERE type='table'"))
                tables = result.fetchall()
                logger.info(f"Database connected. Found {len(tables)} tables: {[t[0] for t in tables]}")
        except Exception as e2:
            logger.error(f"Database connection failed: {e}, {e2}")
            sys.exit(1)


def update_db():
    """Intelligently update database - only create Staff table if missing."""
    try:
        with next(get_session()) as session:
            # Get existing tables
            try:
                # Try PostgreSQL
                result = session.exec(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
                existing_tables = {row[0] for row in result.fetchall()}
            except:
                # Try SQLite
                result = session.exec(text("SELECT name FROM sqlite_master WHERE type='table'"))
                existing_tables = {row[0] for row in result.fetchall()}

            logger.info(f"Existing tables: {sorted(existing_tables)}")

            # Check if Staff table exists
            if 'staff' not in existing_tables:
                logger.info("Creating missing Staff table...")
                Staff.__table__.create(engine, checkfirst=True)
                logger.info(f"✓ Created table: staff")
                logger.info("Database update completed successfully")
            else:
                logger.info("✓ Database is up to date - Staff table exists")

    except Exception as e:
        logger.error(f"Failed to update database: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py <command>")
        print("Commands:")
        print("  init_db    - Initialize Staff table")
        print("  update_db  - Create Staff table if missing")
        print("  check_db   - Check database connection")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init_db":
        init_db()
    elif command == "update_db":
        update_db()
    elif command == "check_db":
        check_db()
    else:
        print(f"Unknown command: {command}")
        print("Run 'python manage.py' to see available commands")
        sys.exit(1)


if __name__ == "__main__":
    main()
