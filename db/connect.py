"""
Database connection module for Finance Tracker API.

This module provides database connectivity and session management for the
Finance Tracker application using SQLAlchemy ORM. It handles database
configuration, engine creation, session factory setup, and provides
dependency injection for database sessions in FastAPI endpoints.

The module configures a PostgreSQL database connection using environment
variables and provides a generator function for database session management
with proper cleanup.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings


env_variables = get_settings()

DB_URL = f"postgresql://{env_variables.db_username}:{env_variables.db_password}@{env_variables.db_host}/{env_variables.db_name}"

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Database session dependency for FastAPI endpoints.

    This function provides a database session that is automatically
    managed by FastAPI's dependency injection system. It creates a new
    database session for each request and ensures proper cleanup when
    the request is complete.

    Yields:
        Session: SQLAlchemy database session for database operations

    Example:
        ```python
        @app.get("/users/")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
        ```

    Database Session Lifecycle:
    1. Creates a new database session using SessionLocal
    2. Yields the session to the endpoint function
    3. Automatically closes the session when the request completes
    4. Handles cleanup even if exceptions occur during processing

    Note:
        This function should be used as a FastAPI dependency in endpoint
        functions. FastAPI will automatically handle the session lifecycle
        and ensure proper cleanup.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
