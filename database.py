from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL — file will be created automatically
DATABASE_URL = "sqlite:///./employees.db"

# For PostgreSQL, replace with:
# DATABASE_URL = "postgresql://user:password@localhost:5432/employee_db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite only
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency — used in route functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
