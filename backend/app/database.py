from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL. Use PostgreSQL.
# In a real-world application, this should be set via environment variables.
# Example using Docker:
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/sweetshop_db"

# Create the SQLAlchemy engine to connect to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class to manage database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

def get_db():
    """
    Dependency to get a database session. It handles opening and closing the session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
